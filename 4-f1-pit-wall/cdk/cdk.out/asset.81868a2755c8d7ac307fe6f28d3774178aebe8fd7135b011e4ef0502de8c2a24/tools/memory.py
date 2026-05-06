"""Memory tool — stores and retrieves user preferences via AgentCore Memory."""

import json
import os
import boto3
from strands import tool

REGION = os.environ.get("BEDROCK_REGION", "us-west-2")
MEMORY_ID = os.environ.get("MEMORY_ID", "f1_pit_wall_memory-6gnCDp5iJc")

client = boto3.client("bedrock-agentcore", region_name=REGION)


@tool
def remember_preference(user_id: str, preference_type: str, value: str) -> str:
    """Store a user preference in memory (favorite team, driver, etc).

    Args:
        user_id: The user identifier
        preference_type: Type of preference (e.g., "favorite_team", "favorite_driver")
        value: The preference value (e.g., "Ferrari", "Verstappen")
    """
    try:
        client.create_event(
            memoryId=MEMORY_ID,
            actorId=user_id,
            sessionId=f"{user_id}-session",
            eventTimestamp=__import__("datetime").datetime.now().isoformat(),
            payload={
                "contentBlocks": [
                    {"text": f"User preference: {preference_type} = {value}"}
                ]
            },
        )
        return json.dumps({"status": "saved", "preference": preference_type, "value": value})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
def recall_preferences(user_id: str) -> str:
    """Retrieve stored preferences for a user from memory.

    Args:
        user_id: The user identifier to look up preferences for
    """
    try:
        response = client.retrieve_memory_records(
            memoryId=MEMORY_ID,
            actorId=user_id,
            query="user preferences favorite team driver",
            maxResults=5,
        )
        records = response.get("memoryRecords", [])
        if not records:
            return json.dumps({"preferences": [], "message": "No preferences stored yet for this user."})

        prefs = [r.get("content", {}).get("text", "") for r in records]
        return json.dumps({"preferences": prefs})
    except Exception as e:
        return json.dumps({"preferences": [], "message": f"Could not retrieve: {str(e)}"})
