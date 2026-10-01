"""
05_setup_backend.py — DynamoDB job table + async backend chat Lambda.

Async pattern (orchestration takes minutes; API Gateway caps at 30s):
  - POST /chat {message}        -> create job (PENDING) in DDB, async self-invoke as worker, return {jobId}
  - worker (async self-invoke)  -> set RUNNING, invoke orchestrator (long), store result, set DONE/ERROR
  - GET  /chat/{jobId}          -> read job from DDB, return status (+ result when DONE)

One Lambda, three modes. The worker mode uses a long timeout (900s) to cover the full
research -> strategy -> document chain.
"""

import json
import time
import common as c

TABLE = c.JOB_TABLE
FN_NAME = f"{c.PROJECT}-chat-backend"


def ensure_table():
    ddb = c.boto3.client("dynamodb", region_name=c.REGION)
    try:
        ddb.create_table(
            TableName=TABLE,
            AttributeDefinitions=[{"AttributeName": "jobId", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "jobId", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"OK Creating table {TABLE}...")
        ddb.get_waiter("table_exists").wait(TableName=TABLE)
        # TTL so finished jobs auto-expire
        try:
            ddb.update_time_to_live(
                TableName=TABLE,
                TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
            )
        except Exception:
            pass
        print(f"OK Table {TABLE} ready")
    except ddb.exceptions.ResourceInUseException:
        print(f"OK Table {TABLE} already exists")


BACKEND_SRC = '''
import json, os, time, uuid
import boto3
from botocore.config import Config

REGION = os.environ["REGION"]
TABLE = os.environ["TABLE"]
ORCH_ARN = os.environ["ORCH_ARN"]
SELF_NAME = os.environ["SELF_NAME"]

ddb = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
lambda_client = boto3.client("lambda", region_name=REGION)
# Long read timeout for the worker's streaming orchestrator call.
agentcore = boto3.client("bedrock-agentcore", region_name=REGION,
                         config=Config(read_timeout=870, connect_timeout=20, retries={"max_attempts": 0}))

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
}

def _resp(code, body):
    return {"statusCode": code, "headers": {**CORS, "Content-Type": "application/json"},
            "body": json.dumps(body)}

def _run_orchestration(job_id, message):
    ddb.update_item(Key={"jobId": job_id},
                    UpdateExpression="SET #s=:s", ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={":s": "RUNNING"})
    try:
        session_id = str(uuid.uuid4())
        resp = agentcore.invoke_harness(
            harnessArn=ORCH_ARN, runtimeSessionId=session_id,
            messages=[{"role": "user", "content": [{"text": message}]}],
        )
        chunks = []
        for ev in resp["stream"]:
            if "contentBlockDelta" in ev:
                d = ev["contentBlockDelta"].get("delta", {})
                if d.get("text"):
                    chunks.append(d["text"])
            elif "runtimeClientError" in ev:
                raise Exception(ev["runtimeClientError"].get("message", "runtime error"))
        result = "".join(chunks).strip()
        ddb.update_item(Key={"jobId": job_id},
                        UpdateExpression="SET #s=:s, #r=:r",
                        ExpressionAttributeNames={"#s": "status", "#r": "result"},
                        ExpressionAttributeValues={":s": "DONE", ":r": result})
    except Exception as e:
        ddb.update_item(Key={"jobId": job_id},
                        UpdateExpression="SET #s=:s, #e=:e",
                        ExpressionAttributeNames={"#s": "status", "#e": "error"},
                        ExpressionAttributeValues={":s": "ERROR", ":e": str(e)})

def lambda_handler(event, context):
    # Mode 1: worker (async self-invoke)
    if event.get("worker"):
        _run_orchestration(event["jobId"], event["message"])
        return {"ok": True}

    # Mode 2/3: API Gateway (HTTP API v2 event)
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    raw_path = event.get("rawPath", "")

    if method == "OPTIONS":
        return _resp(200, {"ok": True})

    if method == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
        except Exception:
            return _resp(400, {"error": "invalid JSON body"})
        message = (body.get("message") or "").strip()
        if not message:
            return _resp(400, {"error": "message is required"})
        job_id = str(uuid.uuid4())
        ddb.put_item(Item={"jobId": job_id, "status": "PENDING", "message": message,
                           "ttl": int(time.time()) + 86400})
        # Fire the worker asynchronously (returns immediately).
        lambda_client.invoke(FunctionName=SELF_NAME, InvocationType="Event",
                             Payload=json.dumps({"worker": True, "jobId": job_id, "message": message}).encode())
        return _resp(202, {"jobId": job_id, "status": "PENDING"})

    if method == "GET":
        job_id = raw_path.rstrip("/").split("/")[-1]
        item = ddb.get_item(Key={"jobId": job_id}).get("Item")
        if not item:
            return _resp(404, {"error": "job not found"})
        out = {"jobId": job_id, "status": item.get("status")}
        if item.get("status") == "DONE":
            out["result"] = item.get("result", "")
        elif item.get("status") == "ERROR":
            out["error"] = item.get("error", "unknown error")
        return _resp(200, out)

    return _resp(405, {"error": "method not allowed"})
'''


def main():
    ensure_table()
    orch_arn = json.load(open(".orchestrator.json"))["harnessArn"]

    r, a = c.REGION, c.ACCOUNT_ID
    statements = [
        {"Effect": "Allow",
         "Action": ["bedrock-agentcore:InvokeHarness", "bedrock-agentcore:InvokeAgentRuntime"],
         "Resource": [orch_arn,
                      f"arn:aws:bedrock-agentcore:{r}:{a}:harness/*",
                      f"arn:aws:bedrock-agentcore:{r}:{a}:runtime/*"]},
        {"Effect": "Allow",
         "Action": ["dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:UpdateItem"],
         "Resource": f"arn:aws:dynamodb:{r}:{a}:table/{TABLE}"},
        {"Effect": "Allow",
         "Action": ["lambda:InvokeFunction"],
         "Resource": f"arn:aws:lambda:{r}:{a}:function:{FN_NAME}"},
    ]
    role = c.ensure_lambda_role(f"{FN_NAME}-role", statements)

    fn_arn = c.deploy_lambda(
        FN_NAME, BACKEND_SRC, role,
        timeout=900, memory=512,
        env={"REGION": c.REGION, "TABLE": TABLE, "ORCH_ARN": orch_arn, "SELF_NAME": FN_NAME},
    )

    with open(".backend.json", "w") as f:
        json.dump({"functionName": FN_NAME, "functionArn": fn_arn, "table": TABLE}, f, indent=2)

    print("\n" + "=" * 60)
    print("BACKEND READY")
    print("=" * 60)
    print(f"Lambda: {fn_arn}")
    print(f"Table : {TABLE}")
    print("=" * 60)
    return fn_arn


if __name__ == "__main__":
    main()
