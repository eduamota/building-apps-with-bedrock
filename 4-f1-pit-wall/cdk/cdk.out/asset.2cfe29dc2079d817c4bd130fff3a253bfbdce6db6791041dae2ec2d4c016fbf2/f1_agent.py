"""F1 Pit Wall — Main Agent Entry Point for AgentCore Runtime."""

from bedrock_agentcore import BedrockAgentCoreApp
from agents.supervisor import create_supervisor_agent

app = BedrockAgentCoreApp()
supervisor = create_supervisor_agent()


@app.entrypoint
def invoke(payload):
    """AgentCore invocation handler."""
    user_message = payload.get("prompt", "")
    session_id = payload.get("session_id", "default")

    result = supervisor(user_message)
    return {
        "response": result.message,
        "session_id": session_id,
    }


if __name__ == "__main__":
    app.run()
