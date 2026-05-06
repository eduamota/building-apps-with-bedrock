"""Lambda handler — API Gateway entry point for F1 Pit Wall agent."""

import json
import os
from agents.supervisor import create_supervisor_agent

agent = create_supervisor_agent()


def lambda_handler(event, context):
    """Handle API Gateway POST /chat requests."""
    body = json.loads(event.get("body", "{}"))
    user_message = body.get("message", "")
    session_id = body.get("session_id", "default")

    if not user_message:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "message field is required"}),
        }

    result = agent(user_message)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps({
            "response": result.message,
            "session_id": session_id,
        }),
    }
