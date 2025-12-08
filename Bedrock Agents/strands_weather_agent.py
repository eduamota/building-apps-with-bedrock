
from strands import Agent, tool
from strands_tools import calculator
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@tool
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    return {"city": city, "temp": 72, "condition": "sunny"}

@tool
def get_forecast(city: str, days: int = 3) -> dict:
    """Get weather forecast for a city."""
    return {"city": city, "forecast": ["sunny", "cloudy", "rainy"][:days]}

agent = Agent(
    system_prompt="You are a helpful weather and calculation assistant.",
    tools=[get_weather, get_forecast, calculator]
)

@app.entrypoint
def invoke(payload):
    prompt = payload.get("prompt", "Hello!")
    response = agent(prompt)
    return {"result": str(response)}

if __name__ == "__main__":
    app.run()
