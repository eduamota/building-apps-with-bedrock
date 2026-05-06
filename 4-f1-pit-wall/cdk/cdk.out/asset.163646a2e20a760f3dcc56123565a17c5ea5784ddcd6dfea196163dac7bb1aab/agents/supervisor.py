"""Supervisor Agent — Routes queries to specialist agents."""

from strands import Agent, tool
from strands.models import BedrockModel
from agents.strategist import create_strategist_agent
from agents.analyst import create_analyst_agent
from agents.historian import create_historian_agent
from agents.technical import create_technical_agent
from tools.memory import remember_preference, recall_preferences

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-pro-v1:0"

SYSTEM_PROMPT = """You are the F1 Pit Wall Supervisor — a Formula 1 AI command center.

You coordinate a team of specialist agents. Based on the user's question, delegate to the right specialist:

1. **Race Strategist** (use analyze_strategy tool) — tire strategy, pit stops, weather impact, race pace
2. **Data Analyst** (use analyze_data tool) — standings, statistics, lap times, predictions, points
3. **Historian** (use ask_historian tool) — past champions, records, famous moments, rivalries
4. **Technical Expert** (use ask_technical tool) — car regulations, rules, penalties, DRS, engine specs

You also manage user preferences:
- When a user mentions their favorite team or driver, use remember_preference to save it
- At the start of conversations or when relevant, use recall_preferences to personalize responses
- Incorporate known preferences naturally (e.g., "Since you're a Ferrari fan...")

Always delegate to a specialist. Combine their response with a brief introduction indicating which expert answered.
If a question spans multiple areas, consult multiple specialists and synthesize.
"""

# Create specialist agents (module-level singletons)
_strategist = None
_analyst = None
_historian = None
_technical = None


def _get_strategist():
    global _strategist
    if _strategist is None:
        _strategist = create_strategist_agent()
    return _strategist


def _get_analyst():
    global _analyst
    if _analyst is None:
        _analyst = create_analyst_agent()
    return _analyst


def _get_historian():
    global _historian
    if _historian is None:
        _historian = create_historian_agent()
    return _historian


def _get_technical():
    global _technical
    if _technical is None:
        _technical = create_technical_agent()
    return _technical


@tool
def analyze_strategy(question: str) -> str:
    """Ask the Race Strategist about tire strategy, pit stops, weather impact, race pace analysis.

    Args:
        question: The strategy question to analyze
    """
    result = _get_strategist()(question)
    return result.message


@tool
def analyze_data(question: str) -> str:
    """Ask the Data Analyst about standings, statistics, lap times, predictions, championship points.

    Args:
        question: The data/statistics question to analyze
    """
    result = _get_analyst()(question)
    return result.message


@tool
def ask_historian(question: str) -> str:
    """Ask the Historian about past champions, records, famous moments, legendary rivalries.

    Args:
        question: The history question to answer
    """
    result = _get_historian()(question)
    return result.message


@tool
def ask_technical(question: str) -> str:
    """Ask the Technical Expert about car regulations, rules, penalties, DRS, engine specs, safety.

    Args:
        question: The technical/regulations question to answer
    """
    result = _get_technical()(question)
    return result.message


def create_supervisor_agent() -> Agent:
    """Create the supervisor agent with specialist tools."""
    model = BedrockModel(model_id=MODEL_ID, region_name=REGION)

    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            analyze_strategy, analyze_data, ask_historian, ask_technical,
            remember_preference, recall_preferences,
        ],
    )
