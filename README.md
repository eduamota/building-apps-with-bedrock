# Building Apps with Amazon Bedrock

A comprehensive guide to building production-ready AI applications using Amazon Bedrock, featuring hands-on notebooks, agent frameworks, and deployment patterns.

## 📚 Project Structure

```
building-apps-with-bedrock/
├── Basic Bedrock/              # Foundation concepts
│   ├── 1-bedrock_intro.ipynb
│   ├── 2-image_generation.ipynb
│   ├── 3-video_generation.ipynb
│   └── 4-inference_profiles.ipynb
│
├── Async Pipeline/             # Serverless async workflows
│   └── async_pipeline_setup.ipynb
│
├── Bedrock Agents/            # Agent development & deployment
│   ├── 1-basic_agent_setup.ipynb
│   ├── 2-agent_with_knowledge_base.ipynb
│   ├── 3-multi_agent_collaboration.ipynb
│   ├── 4-strands_with_agentcore.ipynb
│   ├── 5-knowledge_base_s3_vectors.ipynb
│   ├── 6-strands_agent_kb_agentcore.ipynb
│   ├── 7-bedrock_guardrails.ipynb
│   └── 8-strands_guardrails_kb_agentcore.ipynb
│
├── Bedrock RAG/               # RAG implementations & patterns
│   ├── Demo1-Basic-RAG/       # Fully managed RAG with Aurora
│   ├── Demo2-S3-Vectors/      # Cost-effective S3 native vectors
│   ├── Demo3-Hybrid-Search/   # Vector + keyword search fusion
│   ├── Demo4-Reranking-Pipeline/ # Two-stage retrieval with re-ranking
│   ├── Demo5-Multi-Collection/ # Enterprise multi-collection RAG
│   ├── Demo-Chunking-Strategies/ # Document chunking optimization
│   ├── Demo-RAGAS-Evaluation/ # RAG evaluation metrics
│   └── embedding_comparison_demo.ipynb # Embedding model comparison
│
├── S3VectorsApp/              # Complete RAG application
│   ├── lambda/                # Lambda function code
│   ├── s3vectors_app/         # CDK infrastructure
│   ├── streamlit_app.py       # Chat UI
│   ├── app.py                 # CDK app entry point
│   └── README.md              # Deployment guide
│
├── UI/                        # Interactive demo interface
│   ├── app.py                 # Streamlit application
│   ├── requirements.txt
│   └── README.md
│
├── Application/               # Sample data & resources
│   └── pre-requisites/documents/spec-sheets/
│
├── AGENTCORE_SUMMARY.md      # AgentCore platform guide
├── STRANDS_AGENTS_SUMMARY.md # Strands framework guide
└── BEDROCK_KB_S3_VECTORS_SUMMARY.md  # Knowledge Base guide
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install required packages
pip install boto3 strands-agents strands-agents-tools bedrock-agentcore bedrock-agentcore-starter-toolkit

# Configure AWS credentials
aws configure
```

### 🎨 Interactive Demo UI

Launch the Streamlit interface to explore all capabilities:

```bash
cd UI
pip install -r requirements.txt
streamlit run app.py
```

**Features:**
- 💬 Chat with Bedrock models (Nova, Claude)
- 📚 Knowledge Base RAG with equipment specs
- 🛡️ Test guardrails in real-time
- 🎨 Generate images with Nova Canvas
- 🎬 Create videos with Nova Reel

Open `http://localhost:8501` in your browser to start exploring!

### Learning Path

#### 1️⃣ **Foundations** (Basic Bedrock/)
Start here to understand core Bedrock capabilities:
- **Bedrock Intro** - Models, APIs, basic usage
- **Image Generation** - Nova Canvas for images
- **Video Generation** - Nova Reel for videos
- **Inference Profiles** - System vs Application profiles

#### 2️⃣ **Async Workflows** (Async Pipeline/)
Build serverless async pipelines:
- API Gateway + Step Functions + Lambda
- Image-to-video generation pipeline
- Status tracking and S3 artifact storage

#### 3️⃣ **Agent Development** (Bedrock Agents/)
Progress through agent complexity:

**Basic Agents:**
- Traditional Bedrock Agents with action groups
- Knowledge Base integration
- Multi-agent collaboration patterns

**Advanced Agents:**
- Strands framework with AgentCore deployment
- Knowledge Base with S3 Vectors (90% cost savings)
- Guardrails for content safety
- Production-ready secure agents

#### 4️⃣ **RAG Implementations** (Bedrock RAG/)
Comprehensive RAG patterns from basic to advanced:

**Foundation RAG:**
- Basic RAG with Bedrock Knowledge Bases
- S3 Vectors for 90% cost reduction
- Embedding model comparison and selection

**Advanced Patterns:**
- Hybrid search (vector + keyword fusion)
- Re-ranking pipeline for improved accuracy
- Multi-collection enterprise RAG
- Document chunking strategies
- RAG evaluation with RAGAS metrics

#### 5️⃣ **Production Application** (S3VectorsApp/)
Complete serverless RAG application:

**Features:**
- API Gateway with authentication
- Lambda-based vector operations
- Streamlit chat interface
- CDK infrastructure as code
- Production security practices

## 📖 Key Concepts

### Amazon Bedrock AgentCore

**What:** Serverless platform for deploying AI agents at scale  
**Why:** Zero infrastructure, built-in memory, observability, security  
**When:** Production deployments requiring scale and reliability

**Key Features:**
- Runtime: Serverless agent execution
- Memory: Persistent conversation history
- Gateway: Transform APIs into tools
- Browser: Cloud-based automation
- Code Interpreter: Secure code execution
- Identity: Authentication & access control
- Observability: Real-time monitoring
- Policy: Security controls

📄 See [AGENTCORE_SUMMARY.md](AGENTCORE_SUMMARY.md) for details

### Strands Agents Framework

**What:** Open-source, lightweight Python SDK for building AI agents  
**Why:** Model-driven approach, framework-agnostic, minimal code  
**When:** Rapid agent development with any LLM provider

**Key Features:**
- Model-agnostic (Bedrock, OpenAI, Anthropic, Ollama, etc.)
- Multi-agent patterns (Agents as Tools, Swarm, Graph, Workflow)
- Native MCP (Model Context Protocol) support
- Hot reloading for rapid development
- Bidirectional streaming for voice/audio

📄 See [STRANDS_AGENTS_SUMMARY.md](STRANDS_AGENTS_SUMMARY.md) for details

### Knowledge Bases with S3 Vectors

**What:** Cost-effective RAG with native S3 vector storage  
**Why:** 90% cost reduction vs traditional vector databases  
**When:** Large-scale knowledge bases with subsecond latency tolerance

**Key Features:**
- Native S3 vector storage (no separate DB)
- Subsecond query performance
- Tens of millions of vectors per index
- Rich metadata filtering
- Fully managed, serverless

📄 See [BEDROCK_KB_S3_VECTORS_SUMMARY.md](BEDROCK_KB_S3_VECTORS_SUMMARY.md) for details

## 🎯 Use Case Guides

### Building a Secure RAG Agent

**Goal:** Production-ready agent with knowledge base and content safety

**Steps:**
1. Run `5-knowledge_base_s3_vectors.ipynb` - Create KB with equipment specs
2. Run `7-bedrock_guardrails.ipynb` - Set up content filters
3. Run `8-strands_guardrails_kb_agentcore.ipynb` - Deploy secure agent

**Result:** Agent with RAG, guardrails, deployed to AgentCore

### Multi-Agent Collaboration

**Goal:** Specialized agents working together

**Steps:**
1. Run `3-multi_agent_collaboration.ipynb` - Learn patterns
2. Run `4-strands_with_agentcore.ipynb` - Deploy with Strands
3. Choose pattern: Agents as Tools, Swarm, Graph, or Workflow

**Result:** Coordinated multi-agent system

### Building a Production RAG Application

**Goal:** Complete serverless RAG app with authentication and UI

**Steps:**
1. Navigate to `S3VectorsApp/` folder
2. Follow deployment guide in README
3. Deploy with CDK: `cdk deploy`
4. Get API key and test endpoints
5. Launch Streamlit UI for chat interface

**Result:** Production-ready RAG application with API Gateway, Lambda, and chat UI

### Advanced RAG Patterns

**Goal:** Master comprehensive RAG implementations and optimizations

**Steps:**
1. **Foundation**: `Demo1-Basic-RAG/` - Fully managed Bedrock KB
2. **Cost Optimization**: `Demo2-S3-Vectors/` - 90% cost reduction
3. **Search Enhancement**: `Demo3-Hybrid-Search/` - Vector + keyword fusion
4. **Quality Improvement**: `Demo4-Reranking-Pipeline/` - Two-stage retrieval
5. **Enterprise Scale**: `Demo5-Multi-Collection/` - Multi-index routing
6. **Optimization**: `Demo-Chunking-Strategies/` - Document processing
7. **Evaluation**: `Demo-RAGAS-Evaluation/` - Quality metrics
8. **Model Selection**: `embedding_comparison_demo.ipynb` - Embedding comparison

**Result:** Complete RAG expertise from basic to production-grade implementations

### Async Media Generation

**Goal:** Serverless image-to-video pipeline

**Steps:**
1. Run `async_pipeline_setup.ipynb` - Provision infrastructure
2. Test with API Gateway endpoints
3. Monitor with CloudWatch

**Result:** Scalable async generation pipeline

## 🛠️ Common Patterns

### Pattern 1: Simple Agent with Tools

```python
from strands import Agent, tool

@tool
def search_docs(query: str) -> str:
    """Search documentation."""
    # Your implementation
    return results

agent = Agent(tools=[search_docs])
response = agent("Find information about X")
```

### Pattern 2: Agent with Knowledge Base

```python
@tool
def search_kb(query: str) -> str:
    """Search knowledge base."""
    response = bedrock_runtime.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': KB_ID,
                'modelArn': MODEL_ARN
            }
        }
    )
    return response['output']['text']

agent = Agent(tools=[search_kb])
```

### Pattern 3: Agent with Guardrails

```python
response = bedrock_runtime.retrieve_and_generate(
    input={'text': query},
    retrieveAndGenerateConfiguration={
        'knowledgeBaseConfiguration': {
            'generationConfiguration': {
                'guardrailConfiguration': {
                    'guardrailId': GUARDRAIL_ID,
                    'guardrailVersion': VERSION
                }
            }
        }
    }
)
```

### Pattern 4: Deploy to AgentCore

```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    prompt = payload.get("prompt")
    response = agent(prompt)
    return {"result": str(response)}

if __name__ == "__main__":
    app.run()
```

Then deploy:
```bash
agentcore configure -e agent.py -r us-east-1
agentcore deploy
agentcore invoke '{"prompt": "Hello"}'
```

**Test in UI:**
1. Copy Agent ARN from deployment output
2. Launch Streamlit UI: `cd UI && streamlit run app.py`
3. Select "🤖 Equipment Agent" or "🔒 Secure Agent"
4. Paste Agent ARN and start chatting

## 📊 Cost Optimization

### S3 Vectors vs Traditional Vector DBs

| Aspect | S3 Vectors | OpenSearch Serverless | Savings |
|--------|------------|----------------------|---------|
| Storage | ~$0.023/GB/month | ~$0.24/OCU-hour | **90%** |
| Queries | ~$0.40/million | Included in OCU | **90%** |
| Upload | ~$0.40/million | Included in OCU | **90%** |

### Model Selection

| Model | Use Case | Cost | Speed |
|-------|----------|------|-------|
| Nova Micro | Simple tasks | Lowest | Fastest (200+ tokens/sec) |
| Nova Lite | General purpose | Low | Fast |
| Nova Pro | Complex reasoning | Medium | Moderate |
| Claude Sonnet | Advanced tasks | Higher | Moderate |

## 🔒 Security Best Practices

1. **Use Guardrails** - Content filtering, PII redaction, topic blocking
2. **IAM Policies** - Least privilege access
3. **Application Profiles** - Separate cost tracking and quotas
4. **VPC Endpoints** - Private connectivity
5. **Encryption** - KMS for sensitive data
6. **Monitoring** - CloudWatch logs and metrics

## 🎨 Interactive Demo UI

### Quick Demo

The included Streamlit UI provides an interactive way to explore all Bedrock capabilities:

```bash
cd UI
streamlit run app.py
```

### Available Demos

| Demo | Description | Requirements |
|------|-------------|--------------|
| 💬 **Chat** | Conversation with models | None |
| 📚 **RAG** | Knowledge Base queries | Run notebook 5 |
| 🛡️ **Guardrails** | Content safety testing | Run notebook 7 |
| 🤖 **Equipment Agent** | Agent with KB integration | Deploy notebook 6 to AgentCore |
| 🔒 **Secure Agent** | Agent with Guardrails + KB | Deploy notebook 8 to AgentCore |
| 🎨 **Images** | Generate with Nova Canvas | None |
| 🎬 **Videos** | Generate with Nova Reel | None |

### Features

- **Auto-Configuration** - Loads KB and guardrail configs automatically
- **Chat History** - Maintains conversation context
- **Source Citations** - Shows RAG sources and confidence
- **Real-time Blocking** - See guardrails in action
- **Media Download** - Save generated images and videos

### Screenshots

**Chat Interface:**
- Select model (Nova Lite, Nova Pro, Claude Sonnet)
- Natural conversation with history
- Token usage tracking

**Knowledge Base RAG:**
- Query equipment specifications
- View source documents
- See relevance scores

**Guardrails Demo:**
- Test safe and unsafe prompts
- Real-time content filtering
- Example test cases provided

**Agent Demos:**
- Equipment Agent: Chat with KB-enabled agent
- Secure Agent: Agent with guardrails + KB
- Requires AgentCore deployment (see notebooks 6 & 8)
- Paste Agent ARN from deployment output

## 🚢 Deployment Options

### Interactive UI
```bash
cd UI
streamlit run app.py  # Runs on localhost:8501
```

### Local Development
```bash
python agent.py  # Runs on localhost:8080
```

### AgentCore (Recommended)
```bash
agentcore configure -e agent.py
agentcore deploy
```

### Lambda + API Gateway
Use notebooks in `Async Pipeline/` folder

### ECS/EKS
Container-based deployment (not covered in this repo)

## 📈 Monitoring & Observability

### CloudWatch Integration
- Agent logs: `/aws/bedrock-agentcore/runtimes/{agent-id}`
- Knowledge Base logs: Configure during KB creation
- Lambda logs: Automatic

### AgentCore Observability
```bash
# Enable in agent configuration
agentcore configure --enable-observability
```

### Metrics to Track
- Invocation count
- Latency (p50, p99)
- Error rate
- Token usage
- Cost per request

## 🤝 Contributing

This is a learning repository. Feel free to:
- Add new notebooks
- Improve existing examples
- Share use cases
- Report issues

## 📚 Additional Resources

### AWS Documentation
- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)

### Frameworks
- [Strands Agents](https://strandsagents.com)
- [AgentCore Starter Toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)

### Blogs
- [Building cost-effective RAG with S3 Vectors](https://aws.amazon.com/blogs/machine-learning/building-cost-effective-rag-applications-with-amazon-bedrock-knowledge-bases-and-amazon-s3-vectors/)
- [Multi-Agent Collaboration with Strands](https://aws.amazon.com/blogs/machine-learning/multi-agent-collaboration-patterns-with-strands-agents-and-amazon-nova/)

## 📝 License

This project is for educational purposes. See individual component licenses:
- Strands Agents: Apache 2.0
- AWS Services: AWS Customer Agreement

## 🎓 Learning Objectives

By completing this repository, you will:

✅ Understand Bedrock core capabilities  
✅ Build agents with action groups and knowledge bases  
✅ Implement multi-agent collaboration patterns  
✅ Deploy production-ready agents to AgentCore  
✅ Optimize costs with S3 Vectors  
✅ Implement content safety with guardrails  
✅ Create async serverless pipelines  
✅ Monitor and observe agent behavior  
✅ Build interactive UIs for AI applications  

---

**Ready to build?** 

🎨 **Quick Demo:** `cd UI && streamlit run app.py`  
📚 **Learn:** Start with `Basic Bedrock/1-bedrock_intro.ipynb`  
🚀 **Deploy:** Follow guides in `Bedrock Agents/`
