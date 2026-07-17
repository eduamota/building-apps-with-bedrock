"""Race Strategist Agent — Tire strategy, pit stops, weather analysis. Uses RAG + tools."""

from strands import Agent
from strands.models import BedrockModel
from tools.predictions import predict_race
from tools.calendar import get_calendar
from tools.knowledge_base import search_f1_knowledge

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """You are an F1 Race Strategist on the pit wall. You specialize in:
- Tire strategy and compound selection
- Pit stop timing optimization
- Weather impact on race strategy
- Undercut and overcut analysis
- Safety car probability and strategy adjustments

Use search_f1_knowledge to look up tire compounds, regulations, and track data.
Use predict_race for race outcome predictions.
Use get_calendar for schedule information.
Be specific with lap numbers and tire compound recommendations.
Speak like a real race engineer — concise, data-driven, decisive.
"""


def create_strategist_agent() -> Agent:
    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[predict_race, get_calendar, search_f1_knowledge],
    )
