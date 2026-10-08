from collections import OrderedDict
from typing import Any

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client

LangchainInstrumentor().instrument()

app = BedrockAgentCoreApp()
log = app.logger

_llm = None

def get_or_create_model():
    global _llm
    if _llm is None:
        _llm = load_model()
    return _llm


DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant. Use tools when appropriate.

"""


# Define a simple function tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Return the sum of two numbers"""
    return a + b


# Define a collection of tools used by the model
tools = [add_numbers]

# Module-level checkpointer preserves conversation history across invocations.
# InMemorySaver keeps every thread_id (= session_id) checkpoint in memory
# forever, so we bound it to 128 active threads with LRU eviction (the
# least-recently-used thread is deleted and its history reset) to keep a
# long-running process from growing without limit. For durable history, swap in
# a persistent checkpointer (e.g. SqliteSaver/AsyncSqliteSaver with a file path).
_CHECKPOINT_LIMIT = 128
_checkpointer = InMemorySaver()
_thread_ids = OrderedDict()


def touch_thread(thread_id):
    if thread_id in _thread_ids:
        _thread_ids.move_to_end(thread_id)
        return
    while len(_thread_ids) >= _CHECKPOINT_LIMIT:
        evicted, _ = _thread_ids.popitem(last=False)
        _checkpointer.delete_thread(evicted)
    _thread_ids[thread_id] = True



@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

    # Get MCP Client
    mcp_client = get_streamable_http_mcp_client()

    # Load MCP Tools
    mcp_tools = []
    if mcp_client:
        mcp_tools = await mcp_client.get_tools()

    # Define the agent using create_react_agent (checkpointer is shared across invocations)
    graph = create_react_agent(
        get_or_create_model(),
        tools=mcp_tools + tools,
        prompt=DEFAULT_SYSTEM_PROMPT,
        checkpointer=_checkpointer,
    )

    # Process the user prompt
    prompt = payload.get("prompt", "What can you help me with?")
    if not isinstance(prompt, str):
        raise ValueError("prompt must be a string")
    session_id = getattr(context, "session_id", "default-session")
    touch_thread(session_id)
    log.info(f"Agent input: {prompt}")

    # Run the agent (checkpointer auto-loads/saves history per session)
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=prompt)]},
        config={"configurable": {"thread_id": session_id}},
    )

    # Return result
    output = result["messages"][-1].content
    log.info(f"Agent output: {output}")
    return {"result": output}


if __name__ == "__main__":
    app.run()
