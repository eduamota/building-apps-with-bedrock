"""
08_setup_apikey.py — Add API key authentication to the chat HTTP API.

HTTP APIs (API Gateway v2) do NOT support native API keys / usage plans (that's a REST API v1
feature). The standard pattern is a Lambda REQUEST authorizer that checks an 'x-api-key' header.

This script:
  1. Creates/【reuses】an API key stored in AWS Secrets Manager (not hardcoded).
  2. Deploys an authorizer Lambda that compares the request's x-api-key to the secret.
  3. Creates an HTTP API REQUEST authorizer (simple responses) with identity source x-api-key.
  4. Attaches the authorizer to POST /chat and GET /chat/{jobId}.
  5. Adds x-api-key to the API's CORS allow-headers.
  6. Writes the key to .apikey.json for the site deploy step.

Security note: if the key is embedded in the public static site it is visible to anyone who views
source. It gates casual use + enables throttling, but is not strong auth. See README.
"""

import json
import secrets
import time
import common as c

SECRET_NAME = f"{c.PROJECT}-chat-api-key"
AUTH_FN = f"{c.PROJECT}-chat-authorizer"


def ensure_api_key():
    """Create the secret with a random key if missing; return the key value."""
    sm = c.boto3.client("secretsmanager", region_name=c.REGION)
    try:
        val = sm.get_secret_value(SecretId=SECRET_NAME)["SecretString"]
        key = json.loads(val)["apiKey"]
        print(f"OK Reusing API key secret {SECRET_NAME}")
    except sm.exceptions.ResourceNotFoundException:
        key = "orgintel_" + secrets.token_urlsafe(32)
        sm.create_secret(Name=SECRET_NAME, SecretString=json.dumps({"apiKey": key}))
        print(f"OK Created API key secret {SECRET_NAME}")
    return key


AUTHORIZER_SRC = '''
import json, os
import boto3

SECRET_NAME = os.environ["SECRET_NAME"]
_sm = boto3.client("secretsmanager")
_cached = None

def _expected_key():
    global _cached
    if _cached is None:
        val = _sm.get_secret_value(SecretId=SECRET_NAME)["SecretString"]
        _cached = json.loads(val)["apiKey"]
    return _cached

def lambda_handler(event, context):
    # HTTP API REQUEST authorizer with simple responses.
    headers = event.get("headers") or {}
    # header names are lower-cased in HTTP API v2
    provided = headers.get("x-api-key", "")
    ok = bool(provided) and provided == _expected_key()
    return {"isAuthorized": ok}
'''


def main():
    apigw = c.boto3.client("apigatewayv2", region_name=c.REGION)
    api = json.load(open(".api.json"))
    api_id = api["apiId"]
    endpoint = api["endpoint"]

    api_key = ensure_api_key()

    # Authorizer Lambda (needs secretsmanager:GetSecretValue on the secret)
    r, a = c.REGION, c.ACCOUNT_ID
    auth_role = c.ensure_lambda_role(f"{AUTH_FN}-role", [
        {"Effect": "Allow", "Action": ["secretsmanager:GetSecretValue"],
         "Resource": f"arn:aws:secretsmanager:{r}:{a}:secret:{SECRET_NAME}-*"},
    ])
    auth_arn = c.deploy_lambda(AUTH_FN, AUTHORIZER_SRC, auth_role,
                               timeout=10, memory=128,
                               env={"SECRET_NAME": SECRET_NAME})

    # API Gateway must be allowed to invoke the authorizer Lambda
    try:
        c.lambda_client.add_permission(
            FunctionName=AUTH_FN, StatementId=f"apigw-authorizer-{api_id}",
            Action="lambda:InvokeFunction", Principal="apigateway.amazonaws.com",
            SourceArn=f"arn:aws:execute-api:{r}:{a}:{api_id}/authorizers/*",
        )
        print("OK Granted API Gateway invoke on authorizer")
    except c.lambda_client.exceptions.ResourceConflictException:
        print("OK Authorizer invoke permission already present")

    # Create (or reuse) the REQUEST authorizer with simple responses
    authorizer_uri = f"arn:aws:apigateway:{r}:lambda:path/2015-03-31/functions/{auth_arn}/invocations"
    existing = {z["Name"]: z["AuthorizerId"]
                for z in apigw.get_authorizers(ApiId=api_id).get("Items", [])}
    name = "apikey-authorizer"
    if name in existing:
        authorizer_id = existing[name]
        print(f"OK Reusing authorizer {authorizer_id}")
    else:
        authorizer_id = apigw.create_authorizer(
            ApiId=api_id, Name=name, AuthorizerType="REQUEST",
            AuthorizerUri=authorizer_uri,
            AuthorizerPayloadFormatVersion="2.0",
            EnableSimpleResponses=True,
            IdentitySource=["$request.header.x-api-key"],
            AuthorizerResultTtlInSeconds=0,  # no caching so revocation is immediate
        )["AuthorizerId"]
        print(f"OK Created authorizer {authorizer_id}")

    # Attach the authorizer to the two app routes (not the auto $default/OPTIONS)
    for route in apigw.get_routes(ApiId=api_id).get("Items", []):
        rk = route["RouteKey"]
        if rk in ("POST /chat", "GET /chat/{jobId}"):
            apigw.update_route(ApiId=api_id, RouteId=route["RouteId"],
                               AuthorizationType="CUSTOM", AuthorizerId=authorizer_id)
            print(f"OK Secured route {rk}")

    # Add x-api-key to CORS allow-headers (keep existing config)
    apigw.update_api(
        ApiId=api_id,
        CorsConfiguration={
            "AllowOrigins": ["*"],
            "AllowMethods": ["GET", "POST", "OPTIONS"],
            "AllowHeaders": ["content-type", "x-api-key"],
        },
    )
    print("OK Updated CORS allow-headers (+x-api-key)")

    with open(".apikey.json", "w") as f:
        json.dump({"apiKey": api_key, "secretName": SECRET_NAME}, f, indent=2)

    print("\n" + "=" * 60)
    print("API KEY AUTH ENABLED")
    print("=" * 60)
    print(f"API: {endpoint}")
    print(f"Secret: {SECRET_NAME}")
    print(f"Key (also in .apikey.json): {api_key}")
    print("Send header:  x-api-key: <key>")
    print("=" * 60)
    return api_key


if __name__ == "__main__":
    main()
