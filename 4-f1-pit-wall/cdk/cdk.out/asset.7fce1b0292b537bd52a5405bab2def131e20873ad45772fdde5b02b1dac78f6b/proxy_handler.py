"""Proxy Lambda — invokes AgentCore Runtime via boto3."""

import json
import os
import re
import uuid
import boto3

RUNTIME_ID = os.environ["AGENTCORE_RUNTIME_ID"]
REGION = os.environ.get("AWS_REGION", "us-west-2")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID", "")

client = boto3.client("bedrock-agentcore", region_name=REGION)

# Construct ARN from runtime ID
RUNTIME_ARN = f"arn:aws:bedrock-agentcore:{REGION}:{ACCOUNT_ID}:runtime/{RUNTIME_ID}"

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
    session_id = body.get("session_id", "")
    if len(session_id) < 33:
        session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, session_id or "default"))

    if not message:
        return {"statusCode": 400, "headers": CORS_HEADERS, "body": json.dumps({"error": "message required"})}

    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps({"prompt": message}),
        )
        # Response body may be a StreamingBody or direct dict
        resp_body = response.get("body")
        if hasattr(resp_body, "read"):
            result = json.loads(resp_body.read())
        else:
            result = response

        # Extract text from various response formats
        text = result.get("response", result.get("result", result.get("payload", "")))
        if isinstance(text, bytes):
            text = text.decode()
        if isinstance(text, dict):
            content = text.get("content", [])
            text = "".join(block.get("text", "") for block in content if isinstance(block, dict))

        text = re.sub(r"<thinking>.*?</thinking>\s*", "", str(text), flags=re.DOTALL).strip()
    except Exception as e:
        # Include response keys for debugging
        debug = ""
        try:
            debug = f" | response keys: {list(response.keys())}"
        except:
            pass
        text = f"Error invoking AgentCore Runtime: {str(e)}{debug}"

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({"response": text, "session_id": session_id}),
    }
