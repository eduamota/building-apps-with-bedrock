# Strands Agents Framework Summary

## Overview

Strands Agents is an **open-source, lightweight Python SDK** from AWS that takes a **model-driven approach** to building AI agents. It emphasizes letting the LLM handle planning and reasoning rather than hardcoding workflows.

**Key Philosophy**: Minimal scaffolding, trust modern LLMs to drive planning, reasoning, and tool execution autonomously.

**GitHub**: https://github.com/strands-agents/sdk-python  
**Documentation**: https://strandsagents.com  
**License**: Apache 2.0

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Strands and tools
pip install strands-agents strands-agents-tools
```

## Quick Start

```python
from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])
response = agent("What is the square root of 1764?")
print(response)
```

## Core Features

| Feature | Description |
|---------|-------------|
| **Lightweight** | Simple agent loop, fully customizable |
| **Model Agnostic** | Bedrock, Anthropic, OpenAI, Gemini, Ollama, LiteLLM, custom |
| **Multi-Agent** | Built-in support for agent collaboration patterns |
| **MCP Support** | Native Model Context Protocol integration |
| **Streaming** | Support for generators and async generators |
| **Hot Reloading** | Auto-load tools from `./tools/` directory |
| **Bidirectional Streaming** | Real-time voice/audio conversations (experimental) |

## Basic Agent Patterns

### 1. Simple Agent with Tools

```python
from strands import Agent, tool

@tool
def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())

agent = Agent(tools=[word_count])
response = agent("How many words are in this sentence?")
```

### 2. Agent with System Prompt

```python
agent = Agent(
    system_prompt="You are a helpful research assistant.",
    tools=[web_search, calculator]
)
response = agent("Research the latest AI trends")
```

### 3. Hot Reloading from Directory

```python
# Agent watches ./tools/ directory for changes
agent = Agent(load_tools_from_directory=True)
response = agent("Use any tools you find")
```

## Model Providers

### Amazon Bedrock (Default)

```python
from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.amazon.nova-pro-v1:0",
    temperature=0.3,
    streaming=True
)
agent = Agent(model=model)
```

### OpenAI

```python
from strands.models import OpenAIModel

model = OpenAIModel(
    client_args={"api_key": "your_key"},
    model_id="gpt-4",
    params={"temperature": 0.7}
)
agent = Agent(model=model)
```

### Anthropic

```python
from strands.models import AnthropicModel

model = AnthropicModel(
    client_args={"api_key": "your_key"},
    model_id="claude-3-5-sonnet-20241022",
    params={"temperature": 0.7}
)
agent = Agent(model=model)
```

### Ollama (Local)

```python
from strands.models import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3"
)
agent = Agent(model=model)
```

### Google Gemini

```python
from strands.models import GeminiModel

model = GeminiModel(
    client_args={"api_key": "your_key"},
    model_id="gemini-2.5-flash",
    params={"temperature": 0.7}
)
agent = Agent(model=model)
```

## Multi-Agent Collaboration Patterns

### 1. Agents as Tools Pattern

**Use Case**: Hierarchical delegation - orchestrator delegates to specialized agents

```python
from strands import Agent, tool

# Define specialist agents as tools
@tool
def research_assistant(query: str) -> str:
    """Provide research answers."""
    research_agent = Agent(
        system_prompt="You are a research specialist.",
        tools=[web_search, knowledge_base]
    )
    return str(research_agent(query))

@tool
def editor_assistant(content: str) -> str:
    """Edit and improve content."""
    editor_agent = Agent(
        system_prompt="You are an editor.",
        tools=[grammar_check, style_guide]
    )
    return str(editor_agent(content))

# Orchestrator uses specialist agents
orchestrator = Agent(
    system_prompt="You coordinate domain experts.",
    tools=[research_assistant, editor_assistant]
)

response = orchestrator("Research AI trends and write a summary")
```

**Pros**: Separation of concerns, modularity, hierarchical decision-making  
**Cons**: Orchestrator complexity, single point of failure

### 2. Swarm Pattern

**Use Case**: Decentralized collaboration with peer agents sharing information

```python
from strands import Agent
from strands.models import BedrockModel
from strands.multiagent import Swarm

# Create specialized agents
research_agent = Agent(
    name="researcher",
    system_prompt="Research and gather info, then hand off to analyst.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0"),
    tools=[web_search, knowledge_base]
)

analysis_agent = Agent(
    name="analyst",
    system_prompt="Analyze research data and hand off to writer.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0"),
    tools=[data_analysis, financial_metrics]
)

writer_agent = Agent(
    name="writer",
    system_prompt="Create final report based on analysis.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0"),
    tools=[editor, formatter]
)

# Configure swarm with handoff controls
swarm = Swarm(
    agents=[research_agent, analysis_agent, writer_agent],
    max_handoffs=2,           # Allow up to 2 handoffs
    max_iterations=3,         # Up to 3 rounds of refinement
    execution_timeout=300.0,  # Total timeout (5 minutes)
    node_timeout=60.0         # Individual agent timeout (1 minute)
)

# Execute collaborative workflow
result = swarm("Analyze Q3 financial performance")
print(f"Final result: {result.final_response}")
print(f"Path: {[node.node_id for node in result.node_history]}")
```

**Pros**: Diversity of thought, emergent improvement, no single failure point  
**Cons**: Timeout sensitivity, iteration overhead, cost accumulation

### 3. Graph Pattern

**Use Case**: Structured network with directed connections and explicit control flow

```python
from strands import Agent
from strands_tools import agent_graph

builder = GraphBuilder()

# Add nodes (agents)
builder.add_node(coordinator_agent, "research")
builder.add_node(stock_agent, "stock_price_search")
builder.add_node(web_agent, "fin_web_searcher")
builder.add_node(report_agent, "report")
builder.add_node(image_agent, "create_display_img")

# Add edges (dependencies) - star topology
builder.add_edge("research", "stock_price_search")
builder.add_edge("research", "fin_web_searcher")
builder.add_edge("research", "report")
builder.add_edge("research", "create_display_img")

# Set entry point
builder.set_entry_point("research")

# Build and run
graph = builder.build()
result = graph("Analyze Q3 financial performance")
```

**Pros**: Predictable control flow, explicit dependencies, fine-grained data flow  
**Cons**: Design effort, less dynamic adaptability, latency in deep graphs

### 4. Workflow Pattern

**Use Case**: Predefined sequence with task ordering and dependency management

```python
from strands import Agent
from strands.models import BedrockModel

# Create specialized agents for each step
researcher = Agent(
    system_prompt="You are a research specialist.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0")
)

analyst = Agent(
    system_prompt="You analyze research data.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0")
)

writer = Agent(
    system_prompt="You create polished reports.",
    model=BedrockModel(model_id="us.amazon.nova-pro-v1:0")
)

# Define workflow function
def process_workflow(topic: str):
    # Step 1: Research
    research_results = researcher(f"Research {topic}")
    
    # Step 2: Analysis
    analysis = analyst(f"Analyze: {research_results}")
    
    # Step 3: Reporting
    final_report = writer(f"Write report: {analysis}")
    
    return final_report

# Execute workflow
result = process_workflow("AI in healthcare")
```

**Pros**: Clear structure, parallel efficiency, error handling per step  
**Cons**: Less flexibility, up-front design effort, orchestration overhead

## Model Context Protocol (MCP) Support

```python
from strands import Agent
from strands.tools.mcp import MCPClient

# Connect to MCP server
mcp_client = MCPClient("http://localhost:3000")

# Use MCP tools
agent = Agent(tools=mcp_client.get_tools())
response = agent("Use the MCP tools to help me")
```

## Bidirectional Streaming (Experimental)

Real-time voice/audio conversations with persistent streaming connections.

```python
import asyncio
from strands.experimental.bidi import BidiAgent
from strands.experimental.bidi.models import BidiNovaSonicModel
from strands.experimental.bidi.io import BidiAudioIO, BidiTextIO
from strands.experimental.bidi.tools import stop_conversation
from strands_tools import calculator

async def main():
    # Create bidirectional agent
    model = BidiNovaSonicModel()
    agent = BidiAgent(model=model, tools=[calculator, stop_conversation])
    
    # Setup I/O
    audio_io = BidiAudioIO()
    text_io = BidiTextIO()
    
    # Run with real-time streaming
    await agent.run(
        inputs=[audio_io.input()],
        outputs=[audio_io.output(), text_io.output()]
    )

asyncio.run(main())
```

**Supported Models**:
- Amazon Nova Sonic (`amazon.nova-sonic-v1:0`)
- Google Gemini Live (`gemini-2.5-flash-native-audio-preview-09-2025`)
- OpenAI Realtime API (`gpt-realtime`)

## Built-in Tools (strands-agents-tools)

```python
from strands import Agent
from strands_tools import (
    calculator,
    web_search,
    file_operations,
    http_request,
    system_execution
)

agent = Agent(tools=[calculator, web_search, file_operations])
```

## Custom Tool Creation

```python
from strands import tool

@tool
def get_weather(city: str) -> dict:
    """Get weather for a city. Docstring is used by LLM."""
    # Your implementation
    return {"temp": 72, "condition": "sunny", "city": city}

agent = Agent(tools=[get_weather])
```

## Observability & Monitoring

Strands integrates with OpenTelemetry for tracing and monitoring:

```python
from strands import Agent
from strands.observability import enable_tracing

# Enable tracing
enable_tracing()

agent = Agent(tools=[...])
response = agent("Your query")
```

## Deployment with AgentCore

Strands agents can be deployed to AWS Bedrock AgentCore:

```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent(tools=[...])

@app.entrypoint
def invoke(payload):
    return {"result": agent(payload.get("prompt"))}

if __name__ == "__main__":
    app.run()
```

Then deploy:
```bash
agentcore configure -e my_agent.py
agentcore deploy
```

## Pattern Selection Guide

| Pattern | Best For | Complexity | Control |
|---------|----------|------------|---------|
| **Agents as Tools** | Hierarchical delegation, specialized tasks | Low | High |
| **Swarm** | Brainstorming, diverse perspectives, iterative refinement | Medium | Low |
| **Graph** | Complex workflows, explicit dependencies | High | Very High |
| **Workflow** | Sequential pipelines, multi-stage processes | Medium | High |

## Why Strands + Amazon Nova?

**Amazon Nova Benefits**:
- **High throughput**: 200+ tokens/second
- **Low latency**: Sub-second first-token
- **Ultra-low cost**: Fractions of a cent per 1K tokens
- **Structured output**: Consistent tool calling

**Perfect for Multi-Agent**:
- Thousands of prompts per request affordable
- Fast iteration and refinement
- Redundancy and fail-over without cost concerns

## Common Use Cases

1. **Content Generation Pipeline**: Draft → Fact-check → Edit → Approve
2. **Research & Analysis**: Gather data → Analyze → Report
3. **Customer Service**: Route → Specialist → Resolution
4. **Document Processing**: Extract → Classify → Validate → Store
5. **Financial Analysis**: Data collection → Analysis → Reporting
6. **Multi-modal Tasks**: Text + Image + Audio processing

## Best Practices

1. **Start Simple**: Begin with single agent, add complexity as needed
2. **Let LLM Decide**: Trust model-driven approach for planning
3. **Use Appropriate Pattern**: Match pattern to problem structure
4. **Monitor Costs**: Track token usage in multi-agent systems
5. **Implement Timeouts**: Prevent runaway agent loops
6. **Test Locally**: Use hot reloading for rapid development
7. **Add Observability**: Enable tracing for production systems

## Comparison: Strands vs Other Frameworks

| Feature | Strands | LangGraph | CrewAI | AutoGen |
|---------|---------|-----------|--------|---------|
| **Philosophy** | Model-driven | Graph-based | Role-based | Conversation-based |
| **Complexity** | Low | Medium | Medium | High |
| **Flexibility** | High | Very High | Medium | High |
| **Learning Curve** | Easy | Moderate | Easy | Steep |
| **Multi-Agent** | Built-in | Built-in | Built-in | Built-in |
| **MCP Support** | Native | Plugin | No | No |
| **AWS Integration** | Excellent | Good | Good | Good |

## Resources

- **Documentation**: https://strandsagents.com
- **GitHub SDK**: https://github.com/strands-agents/sdk-python
- **GitHub Tools**: https://github.com/strands-agents/tools
- **Samples**: https://github.com/strands-agents/samples
- **PyPI**: https://pypi.org/project/strands-agents/
- **AWS Blog**: Multi-Agent Collaboration Patterns

## Key Advantages

✅ **Minimal code** - Build agents in just a few lines  
✅ **Model-agnostic** - Works with any LLM provider  
✅ **Production-ready** - Used in enterprise deployments  
✅ **Open source** - Apache 2.0 license, community-driven  
✅ **AWS optimized** - Seamless Bedrock integration  
✅ **MCP native** - Access thousands of pre-built tools  
✅ **Flexible** - From simple to complex multi-agent systems  

## Example Projects

1. **Multimodal Email Assistant** - Agents as Tools pattern
2. **Financial Assistant Swarm** - Swarm pattern with handoffs
3. **Document Processing Pipeline** - Workflow pattern
4. **Research & Analysis System** - Graph pattern
5. **Voice Assistant** - Bidirectional streaming

---

**Last Updated**: December 2025  
**Version**: 1.19.0  
**Status**: Production Ready  
**Stars**: 4.2k+ on GitHub
