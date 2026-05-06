"""Memory tool — stores and retrieves user preferences via AgentCore Memory."""

import json
import os
from datetime import datetime, timezone
import boto3
from strands import tool

REGION = os.environ.get("BEDROCK_REGION", "us-west-2")
MEMORY_ID = os.environ.get("MEMORY_ID", "f1_pit_wall_memory-6gnCDp5iJc")

client = boto3.client("bedrock-agentcore", region_name=REGION)


@tool
def remember_preference(preference_type: str, value: str) -> str:
    """Store a user preference in memory (favorite team, driver, etc).

    Args:
        preference_type: Type of preference (e.g., "favorite_team", "favorite_driver")
        value: The preference value (e.g., "Ferrari", "Verstappen")
    """
    try:
        client.create_event(
            memoryId=MEMORY_ID,
            actorId="default_user",
            sessionId="default_user-session-00000000000000",
            eventTimestamp=datetime.now(timezone.utc).isoformat(),
            payload=[
                {"conversational": {"role": "USER", "content": {"text": f"My {preference_type} is {value}"}}}
            ],
        )
        return json.dumps({"status": "saved", "preference": preference_type, "value": value})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
def recall_preferences() -> str:
    """Retrieve stored preferences for the user from memory."""
    try:
        response = client.retrieve_memory_records(
            memoryId=MEMORY_ID,
            actorId="default_user",
            query="user preferences favorite team driver",
            maxResults=5,
        )
        records = response.get("memoryRecords", [])
        if not records:
            return json.dumps({"preferences": [], "message": "No preferences stored yet."})

        prefs = [r.get("content", {}).get("text", str(r.get("content", ""))) for r in records]
        return json.dumps({"preferences": prefs})
    except Exception as e:
        return json.dumps({"preferences": [], "message": f"Could not retrieve: {str(e)}"})
