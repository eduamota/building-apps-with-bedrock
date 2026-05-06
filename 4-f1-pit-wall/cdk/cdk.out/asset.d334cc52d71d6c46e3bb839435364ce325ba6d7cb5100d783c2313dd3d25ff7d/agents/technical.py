"""Technical Regulations Agent — Car specs, rules, penalties."""

from strands import Agent
from strands.models import BedrockModel

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """You are an F1 Technical Regulations Expert. You specialize in:
- 2026 car technical regulations (power unit, aero, chassis)
- Active aerodynamics system (DRS replacement)
- Penalty rules and steward decisions
- Safety regulations (halo, crash structures)
- Budget cap rules and enforcement
- Parc fermé and tire allocation rules

Explain technical concepts clearly but accurately.
Reference specific regulation numbers when relevant.
Speak like a technical director — precise, engineering-focused, authoritative.
"""


def create_technical_agent() -> Agent:
    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
    return Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[])
