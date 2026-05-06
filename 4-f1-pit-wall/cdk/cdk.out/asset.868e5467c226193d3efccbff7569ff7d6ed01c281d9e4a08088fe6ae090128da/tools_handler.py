"""Tools Lambda handler — invoked by AgentCore Gateway for tool calls."""

import json
from tools.standings import get_standings
from tools.predictions import predict_race
from tools.lap_times import compare_lap_times
from tools.calendar import get_calendar

TOOLS = {
    "get_standings": lambda params: get_standings(category=params.get("category", "drivers")),
    "predict_race": lambda params: predict_race(track=params.get("track", "")),
    "compare_lap_times": lambda params: compare_lap_times(
        driver1=params.get("driver1", ""), driver2=params.get("driver2", ""), track=params.get("track", "")),
    "get_calendar": lambda params: get_calendar(next_n=int(params.get("next_n", 5))),
}


def handler(event, context):
    """Handle tool invocations from AgentCore Gateway."""
    # Gateway sends tool name with target prefix: "f1-tools__get_standings"
    tool_name = event.get("toolName", "").split("__")[-1]
    params = event.get("input", {})

    if tool_name in TOOLS:
        result = TOOLS[tool_name](params)
        return {"statusCode": 200, "body": result}

    return {"statusCode": 404, "body": json.dumps({"error": f"Unknown tool: {tool_name}"})}
