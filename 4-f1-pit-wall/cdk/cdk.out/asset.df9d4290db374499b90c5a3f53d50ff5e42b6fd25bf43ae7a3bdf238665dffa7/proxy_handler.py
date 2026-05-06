"""Proxy Lambda — forwards frontend requests to AgentCore Runtime."""

import json
import os
import re
import boto3

RUNTIME_ID = os.environ.get("AGENTCORE_RUNTIME_ID", "")
REGION = os.environ.get("AWS_REGION", "us-west-2")

client = boto3.client("bedrock-agentcore-runtime", region_name=REGION)

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    body = json.loads(event.get("body", "{}"))
    message = body.get("message", "")
    session_id = body.get("session_id", "default")

    if not message:
        return {"statusCode": 400, "headers": CORS_HEADERS, "body": json.dumps({"error": "message required"})}

    response = client.invoke_runtime(
        agentRuntimeId=RUNTIME_ID,
        sessionId=session_id,
        payload=json.dumps({"prompt": message}),
    )

    result = json.loads(response["body"].read())
    text = result.get("response", str(result))

    # Clean thinking tags
    text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL).strip()

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({"response": text, "session_id": session_id}),
    }
