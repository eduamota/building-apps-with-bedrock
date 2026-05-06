"""Lambda handler — API Gateway entry point for F1 Pit Wall agent."""

import json
import os
from agents.supervisor import create_supervisor_agent

agent = create_supervisor_agent()


CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def lambda_handler(event, context):
    """Handle API Gateway POST /chat requests."""
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    body = json.loads(event.get("body", "{}"))
    user_message = body.get("message", "")
    session_id = body.get("session_id", "default")

    if not user_message:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "message field is required"}),
        }

    import re
    result = agent(user_message)

    msg = result.message
    if isinstance(msg, dict):
        content = msg.get("content", [])
        text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
    elif isinstance(msg, str):
        text = msg
    else:
        text = str(msg)

    # Remove thinking tags
    text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL).strip()

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "response": text,
            "session_id": session_id,
        }),
    }
