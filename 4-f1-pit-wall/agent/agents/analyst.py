"""Data Analyst Agent — Standings, statistics, lap time comparisons."""

from strands import Agent
from strands.models import BedrockModel
from tools.standings import get_standings
from tools.lap_times import compare_lap_times

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """You are an F1 Data Analyst. You specialize in:
- Championship standings and points calculations
- Lap time analysis and driver comparisons
- Statistical trends and performance metrics
- Championship scenarios and mathematical possibilities

Use your tools to look up current standings and compare lap times.
Present data clearly with numbers and context.
Speak like a data scientist — precise, factual, analytical.
"""

def create_analyst_agent() -> Agent:
    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_standings, compare_lap_times, get_skills],
    )
