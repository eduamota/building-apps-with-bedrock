# Bedrock Agents Examples

This folder contains examples for building AI agents using Amazon Bedrock Agents.

## Notebooks

### 1. Basic Agent Setup (`1-basic_agent_setup.ipynb`)
Create a simple agent with action groups that can execute custom functions.

**Features:**
- IAM role creation for agents
- Lambda function for action execution
- OpenAPI schema definition
- Agent preparation and testing

**Use Case:** Weather assistant that can get current weather and forecasts

### 2. Agent with Knowledge Base (`2-agent_with_knowledge_base.ipynb`)
Build an agent that uses RAG (Retrieval Augmented Generation) with a knowledge base.

**Features:**
- S3 bucket for document storage
- Knowledge base creation with vector embeddings
- Data source ingestion
- Agent-KB association

**Use Case:** Product assistant that answers questions from documentation

### 3. Multi-Agent Collaboration (`3-multi_agent_collaboration.ipynb`)
Create multiple specialized agents that work together on complex tasks.

**Features:**
- Multiple specialized agents (research, analysis, coordinator)
- Inter-agent communication via Lambda
- Task delegation and orchestration
- Workflow coordination

**Use Case:** Research and analysis system with coordinated agents

## Prerequisites

```bash
pip install boto3
```

## AWS Permissions Required

- `bedrock:*` - For agent operations
- `iam:CreateRole`, `iam:AttachRolePolicy` - For role creation
- `lambda:CreateFunction`, `lambda:InvokeFunction` - For action groups
- `s3:CreateBucket`, `s3:PutObject` - For knowledge bases
- `aoss:*` - For OpenSearch Serverless (knowledge bases)

## Architecture Patterns

### Basic Agent
```
User → Agent → Action Group (Lambda) → External API/Service
```

### Agent with Knowledge Base
```
User → Agent → Knowledge Base (Vector Search) → S3 Documents
```

### Multi-Agent System
```
User → Coordinator Agent → Research Agent
                        → Analysis Agent
                        → Synthesis
```

## Key Concepts

**Agent**: AI assistant powered by foundation models
**Action Group**: Set of APIs the agent can call
**Knowledge Base**: Vector database for RAG
**Alias**: Versioned deployment of an agent

## Cost Considerations

- Model invocations charged per token
- Knowledge base storage in OpenSearch Serverless
- Lambda execution time
- S3 storage for documents

## Next Steps

1. Start with basic agent to understand core concepts
2. Add knowledge base for domain-specific information
3. Build multi-agent systems for complex workflows
4. Integrate with your applications via API Gateway
