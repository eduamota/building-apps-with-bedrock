# AWS Bedrock Flows Visual Workflow Demo

This demo illustrates building, deploying, and managing automated Directed Acyclic Graph (DAG) workflows in **Amazon Bedrock Flows** using Boto3 (`bedrock-agent`) and Infrastructure-as-Code (CDK / CloudFormation).

> **Presentation Reference:** Slide 38 (*"Hands-On RAG with AWS"*)

---

## Architectural Flow

```
                      +-------------------+
                      |     FlowInput     | (User query)
                      +---------+---------+
                                |
                                v
                   +------------+------------+
                   |  RetrieveKnowledgeBase  | (Bedrock KB retrieval)
                   +------------+------------+
                                |
                                v
                   +------------+------------+
                   |   CheckRetrievalScore   | (Condition Node)
                   +------------+------------+
                                |
             +------------------+------------------+
             | (HasResults)                        | (EmptyResults fallback)
             v                                     v
   +---------+--------------+            +---------+---------+
   | SynthesizeAnswerPrompt |            | Default Response  |
   +---------+--------------+            +---------+---------+
             |                                     |
             +------------------+------------------+
                                |
                                v
                      +---------+---------+
                      |    FlowOutput     | (Final synthesized answer)
                      +-------------------+
```

---

## Files

- `bedrock_flows_demo.py`: Python CLI tool and `BedrockFlowManager` class. Supports node generation, topological validation, flow creation, preparation, and teardown. Supports `--mock` mode.
- `bedrock_flows_demo.ipynb`: Interactive Jupyter Notebook tutorial.
- `bedrock_flow_cdk.py`: AWS CDK and CloudFormation representation (`AWS::Bedrock::Flow` / `CfnFlow`).

---

## Quickstart

```bash
# Run CLI demo (falls back to mock mode if offline)
python bedrock_flows_demo.py

# Force mock mode
python bedrock_flows_demo.py --mock
```
