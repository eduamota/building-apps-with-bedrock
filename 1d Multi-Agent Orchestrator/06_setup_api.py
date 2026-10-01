"""
06_setup_api.py — HTTP API Gateway in front of the async backend Lambda.

Routes:
  POST /chat            -> start a job (returns 202 {jobId})
  GET  /chat/{jobId}    -> poll job status/result
CORS is enabled for the static site (allow any origin for the demo).
"""

import json
import time
import common as c

API_NAME = c.API_NAME


def find_api(name):
    apis = c.boto3.client("apigatewayv2", region_name=c.REGION).get_apis()
    for a in apis.get("Items", []):
        if a["Name"] == name:
            return a["ApiId"]
    return None


def main():
    apigw = c.boto3.client("apigatewayv2", region_name=c.REGION)
    backend = json.load(open(".backend.json"))
    fn_name = backend["functionName"]
    fn_arn = backend["functionArn"]

    api_id = find_api(API_NAME)
    if api_id:
        print(f"OK Reusing API {api_id}")
    else:
        api = apigw.create_api(
            Name=API_NAME,
            ProtocolType="HTTP",
            CorsConfiguration={
                "AllowOrigins": ["*"],
                "AllowMethods": ["GET", "POST", "OPTIONS"],
                "AllowHeaders": ["content-type"],
            },
        )
        api_id = api["ApiId"]
        print(f"OK Created API {api_id}")

    # Allow API Gateway to invoke the backend Lambda (unique statement id per api).
    try:
        c.lambda_client.add_permission(
            FunctionName=fn_name,
            StatementId=f"apigw-{api_id}",
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=f"arn:aws:execute-api:{c.REGION}:{c.ACCOUNT_ID}:{api_id}/*/*",
        )
        print("OK Granted API Gateway invoke on backend Lambda")
    except c.lambda_client.exceptions.ResourceConflictException:
        print("OK Lambda invoke permission already present")

    # Integration (AWS_PROXY to the backend Lambda)
    existing = {i.get("IntegrationUri"): i["IntegrationId"]
                for i in apigw.get_integrations(ApiId=api_id).get("Items", []) if i.get("IntegrationUri")}
    if fn_arn in existing:
        integ_id = existing[fn_arn]
    else:
        integ_id = apigw.create_integration(
            ApiId=api_id, IntegrationType="AWS_PROXY", IntegrationUri=fn_arn,
            PayloadFormatVersion="2.0",
        )["IntegrationId"]
    print(f"OK Integration {integ_id}")

    # Routes
    existing_routes = {r["RouteKey"] for r in apigw.get_routes(ApiId=api_id).get("Items", [])}
    for route_key in ["POST /chat", "GET /chat/{jobId}"]:
        if route_key not in existing_routes:
            apigw.create_route(ApiId=api_id, RouteKey=route_key, Target=f"integrations/{integ_id}")
            print(f"OK Route {route_key}")
        else:
            print(f"OK Route exists {route_key}")

    # Stage (auto-deploy)
    stages = {s["StageName"] for s in apigw.get_stages(ApiId=api_id).get("Items", [])}
    if "prod" not in stages:
        apigw.create_stage(ApiId=api_id, StageName="prod", AutoDeploy=True)
        print("OK Stage prod")

    endpoint = f"https://{api_id}.execute-api.{c.REGION}.amazonaws.com/prod"

    with open(".api.json", "w") as f:
        json.dump({"apiId": api_id, "endpoint": endpoint}, f, indent=2)

    print("\n" + "=" * 60)
    print("API READY")
    print("=" * 60)
    print(f"Endpoint: {endpoint}")
    print(f"  POST {endpoint}/chat")
    print(f"  GET  {endpoint}/chat/{{jobId}}")
    print("=" * 60)
    return endpoint


if __name__ == "__main__":
    main()
