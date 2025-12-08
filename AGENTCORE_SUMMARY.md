# AWS Bedrock AgentCore Summary

## Overview

Amazon Bedrock AgentCore is AWS's production-grade platform for deploying AI agents at scale. It's **framework-agnostic** and works with any Python agent framework (LangGraph, CrewAI, Strands Agents, custom code).

**Key Value Proposition:** Deploy your existing agent code to enterprise infrastructure with zero code changes.

## Platform Services

| Service | Purpose |
|---------|---------|
| **Runtime** | Serverless deployment and scaling - no infrastructure management |
| **Memory** | Persistent conversation history (short-term & long-term with fact extraction) |
| **Gateway** | Transform existing APIs into agent tools |
| **Browser** | Cloud-based browser automation for web interaction |
| **Code Interpreter** | Secure sandboxed Python code execution |
| **Identity** | Authentication and access management (OAuth support) |
| **Observability** | Real-time monitoring, tracing, and CloudWatch integration |
| **Policy** | Real-time security controls outside agent code |
| **Evaluation** | Continuous quality inspection based on agent behavior |

## Installation

```bash
# Install core packages
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit

# Verify installation
agentcore --help
```

## Prerequisites

- AWS Account with credentials configured
- Python 3.10+
- Boto3 installed
- Model access: Anthropic Claude Sonnet 4.0 enabled in Bedrock console
- Required IAM permissions for AgentCore operations

## Basic Agent Example

```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent()

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()  # Runs locally on port 8080
```

## Local Development Workflow

```bash
# 1. Create agent file (my_agent.py)
# 2. Test locally
python my_agent.py

# 3. Test with curl
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```

## Deployment Workflow

```bash
# 1. Configure agent (creates .bedrock_agentcore.yaml)
agentcore configure -e my_agent.py

# Optional: Specify region
agentcore configure -e my_agent.py -r us-east-1

# Optional: Disable memory
agentcore configure -e my_agent.py --disable-memory

# 2. Deploy to AWS (no Docker needed - uses CodeBuild)
agentcore deploy

# 3. Check status
agentcore status

# 4. Test deployed agent
agentcore invoke '{"prompt": "tell me a joke"}'

# 5. Clean up when done
agentcore destroy
```

## Deployment Modes

| Mode | Command | Use Case | Requirements |
|------|---------|----------|--------------|
| **Direct Code Deploy** (Default) | `agentcore deploy` | Most use cases | None - uses CodeBuild |
| **Local Development** | `agentcore deploy --local` | Rapid iteration, debugging | Docker/Finch/Podman |
| **Local Build + Cloud** | `agentcore deploy --local-build` | Custom build needs | Docker/Finch/Podman |

## Programmatic Invocation

```python
import json
import uuid
import boto3

# Initialize client
client = boto3.client('bedrock-agentcore')

# Prepare payload
payload = json.dumps({"prompt": "Tell me a joke"}).encode()

# Invoke agent
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-west-2:123456789012:agent-runtime/my-agent',
    runtimeSessionId=str(uuid.uuid4()),
    payload=payload,
    qualifier="DEFAULT"
)

# Process response
content = []
for chunk in response.get("response", []):
    content.append(chunk.decode('utf-8'))
    
result = json.loads(''.join(content))
print(result)
```

## Memory Configuration

During `agentcore configure`, you can choose:

- **Short-term memory (STM) only** - Available immediately
- **Short-term + Long-term memory (LTM)** - Automatic extraction of facts, preferences, summaries (takes 2-5 minutes to provision)
- **No memory** - Use `--disable-memory` flag

## Resource Locations (AWS Console)

| Resource | Location |
|----------|----------|
| **Agent Logs** | CloudWatch → Log groups → `/aws/bedrock-agentcore/runtimes/{agent-id}-DEFAULT` |
| **Memory Resources** | Bedrock AgentCore → Memory |
| **Container Images** | ECR → Repositories → `bedrock-agentcore-{agent-name}` |
| **S3 Deployment** | S3 → Buckets → `{agent-name}/deployment.zip` |
| **IAM Role** | IAM → Roles → Search "BedrockAgentCore" |

## Key Advantages

✅ **Zero infrastructure management** - No servers, containers, or scaling concerns
✅ **Keep your existing code** - Works with any Python agent framework
✅ **Production-ready** - Built-in auth, memory, observability, security
✅ **Framework agnostic** - LangGraph, CrewAI, Strands, custom logic
✅ **ARM64 optimized** - Runs on AWS Graviton for performance
✅ **Enterprise security** - Built-in identity, isolation, access controls
✅ **Streaming support** - Native support for generators and async generators

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Permission denied** | Verify AWS credentials: `aws sts get-caller-identity` |
| **Model access denied** | Enable Claude 4.0 in Bedrock console for your region |
| **Port 8080 in use** | Kill process: `lsof -ti:8080 \| xargs kill -9` (Mac/Linux) |
| **Region mismatch** | Use `-r` flag during configure to specify region |
| **Memory not ready** | Wait 2-5 minutes, check with `agentcore status` |
| **Docker not found** | Ignore - default mode uses CodeBuild (no Docker needed) |

## Advanced Configuration

### Custom Execution Role

```bash
agentcore configure -e my_agent.py \
  --execution-role arn:aws:iam::111122223333:role/MyRole
```

### Requirements File

Create `requirements.txt` for dependencies:

```
bedrock-agentcore
strands-agents
langchain
# Add other dependencies
```

## Architecture Pattern

```
User Request
    ↓
API Gateway / Direct Invoke
    ↓
AgentCore Runtime (Serverless)
    ↓
Your Agent Code (any framework)
    ↓
├─→ Memory (conversation history)
├─→ Gateway (external APIs as tools)
├─→ Browser (web automation)
├─→ Code Interpreter (code execution)
└─→ Foundation Models (Bedrock)
    ↓
Response
```

## Integration with Other Frameworks

### LangGraph Example

```python
from bedrock_agentcore import BedrockAgentCoreApp
from langgraph.graph import StateGraph

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    # Your LangGraph logic
    graph = StateGraph(...)
    result = graph.invoke(payload)
    return result
```

### Custom Framework Example

```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    # Your custom agent logic
    prompt = payload.get("prompt")
    
    # Process with your custom logic
    response = my_custom_agent_function(prompt)
    
    return {"result": response}
```

## Cost Considerations

- **Runtime**: Pay per invocation and compute time
- **Memory**: Storage costs for conversation history
- **Models**: Bedrock model invocation costs (per token)
- **CloudWatch**: Log storage and queries
- **S3/ECR**: Storage for deployment artifacts

## Official Resources

- **Documentation**: https://docs.aws.amazon.com/bedrock-agentcore/
- **SDK GitHub**: https://github.com/aws/bedrock-agentcore-sdk-python
- **Starter Toolkit**: https://github.com/aws/bedrock-agentcore-starter-toolkit
- **Samples**: https://github.com/awslabs/amazon-bedrock-agentcore-samples
- **Quickstart Guide**: https://aws.github.io/bedrock-agentcore-starter-toolkit/

## Next Steps

1. **Start Simple**: Deploy a basic agent using the quickstart
2. **Add Memory**: Enable conversation persistence
3. **Integrate Tools**: Use Gateway to connect external APIs
4. **Add Security**: Implement Policy for access controls
5. **Monitor**: Enable Observability for production insights
6. **Scale**: Let AgentCore handle scaling automatically

## Comparison: AgentCore vs Traditional Bedrock Agents

| Feature | AgentCore | Traditional Bedrock Agents |
|---------|-----------|---------------------------|
| **Framework** | Any Python framework | Bedrock-specific |
| **Deployment** | Serverless runtime | Managed service |
| **Code Control** | Full control | Limited to action groups |
| **Memory** | Built-in STM/LTM | Separate configuration |
| **Tools** | Browser, Code Interpreter | Action groups only |
| **Flexibility** | High - any logic | Medium - predefined patterns |
| **Use Case** | Complex, custom agents | Standard conversational agents |

---

**Last Updated**: December 2025
**Status**: Generally Available (GA)
**Default Region**: us-west-2
