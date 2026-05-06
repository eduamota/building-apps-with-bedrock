# 🏎️ F1 Pit Wall — AI Command Center

An AI-powered Formula 1 command center showcasing all AWS AI agent capabilities: multi-agent collaboration, RAG, tool use, memory, and full AgentCore deployment.

## Architecture

```
Next.js UI → API Gateway → Lambda → Supervisor Agent
                                        ├── Race Strategist (tools: predictions, calendar)
                                        ├── Data Analyst (tools: standings, lap times)
                                        ├── Historian (RAG: history, famous moments)
                                        └── Technical Expert (RAG: regulations)
                                              ↕
                                    Bedrock Knowledge Base (S3)
                                    AgentCore Memory (user prefs)
                                    AgentCore Policy (read-only)
```

## Features Demonstrated

| AWS Feature | How It's Used |
|-------------|---------------|
| **Multi-Agent (Strands)** | Supervisor routes to 4 specialist agents |
| **RAG (Knowledge Base)** | F1 data grounding (season, history, regulations) |
| **Tool Use** | Standings, predictions, lap times, calendar |
| **AgentCore Runtime** | Hosts the agent system |
| **AgentCore Memory** | User preferences + conversation history |
| **AgentCore Gateway** | Tool connectivity via MCP |
| **AgentCore Policy** | Read-only access enforcement |
| **AgentCore Observability** | CloudWatch metrics + traces |
| **CDK (Python)** | 3-stack infrastructure deployment |
| **Next.js Frontend** | F1-themed chat UI with streaming |

## Quick Start

### Prerequisites
- AWS CLI configured with credentials
- Python 3.12+
- Node.js 18+
- AWS CDK CLI (`npm install -g aws-cdk`)
- Model access: Amazon Nova Pro enabled in us-west-2

### 1. Deploy Infrastructure

```bash
cd cdk
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy --all
```

### 2. Test Agent Locally

```bash
cd agent
pip install -r requirements.txt
python f1_agent.py
# In another terminal:
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Who leads the championship?"}'
```

### 3. Run Frontend Locally

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=<API_GATEWAY_URL> npm run dev
# Open http://localhost:3000
```

## Project Structure

```
4-f1-pit-wall/
├── README.md
├── knowledge-base/data/       # F1 RAG documents (markdown)
├── agent/                     # Python agent code
│   ├── f1_agent.py           # AgentCore entry point
│   ├── handler.py            # Lambda handler
│   ├── agents/               # Supervisor + specialists
│   └── tools/                # Standings, predictions, etc.
├── cdk/                       # CDK infrastructure
│   ├── app.py                # CDK app entry
│   └── stacks/               # Infra, Agent, Frontend stacks
└── frontend/                  # Next.js chat UI
    └── app/                  # Pages + styles
```

## Example Queries

- "What tire strategy should Red Bull use at Monza?"
- "Compare Verstappen and Norris lap times at Silverstone"
- "Who has the most wins in F1 history?"
- "Explain the 2026 active aerodynamics rules"
- "Show me the current championship standings"
- "What happened at Abu Dhabi 2021?"
- "When is the next race?"

## Cost Estimate

| Resource | Estimated Cost |
|----------|---------------|
| Lambda (demo usage) | < $0.10/day |
| API Gateway | < $0.01/day |
| S3 (KB + frontend) | < $0.05/month |
| Bedrock (Nova Pro) | ~$0.01 per query |
| **Total (idle)** | **< $1/month** |
| **Total (active demo)** | **< $5/day** |

## Cleanup

```bash
cd cdk
cdk destroy --all
```
