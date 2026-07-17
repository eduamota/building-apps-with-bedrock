"""Memory tool — stores and retrieves user preferences. Uses AgentCore Memory with in-memory fallback."""

import json
import os
from datetime import datetime, timezone
import boto3
from strands import tool

REGION = os.environ.get("BEDROCK_REGION", "us-west-2")
MEMORY_ID = os.environ.get("MEMORY_ID", "f1_pit_wall_memory-6gnCDp5iJc")

# In-memory fallback for preferences
_local_prefs = {}

try:
    client = boto3.client("bedrock-agentcore", region_name=REGION)
except Exception:
    client = None


@tool
def remember_preference(preference_type: str, value: str) -> str:
    """Store a user preference in memory (favorite team, driver, etc).

    Args:
        preference_type: Type of preference (e.g., "favorite_team", "favorite_driver")
        value: The preference value (e.g., "Ferrari", "Verstappen")
    """
    # Always store locally
    _local_prefs[preference_type] = value

    # Try AgentCore Memory
    if client:
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
        except Exception:
            pass  # Fallback to local storage

    return json.dumps({"status": "saved", "preference": preference_type, "value": value})


@tool
def recall_preferences() -> str:
    """Retrieve stored preferences for the user from memory."""
    # Try AgentCore Memory first
    if client:
        try:
            response = client.retrieve_memory_records(
                memoryId=MEMORY_ID,
                actorId="default_user",
                query="user preferences favorite team driver",
                maxResults=5,
            )
            records = response.get("memoryRecords", [])
            if records:
                prefs = [r.get("content", {}).get("text", str(r.get("content", ""))) for r in records]
                return json.dumps({"preferences": prefs})
        except Exception:
            pass

    # Fallback to local preferences
    if _local_prefs:
        prefs = [f"{k}: {v}" for k, v in _local_prefs.items()]
        return json.dumps({"preferences": prefs})

    return json.dumps({"preferences": [], "message": "No preferences stored yet."})
