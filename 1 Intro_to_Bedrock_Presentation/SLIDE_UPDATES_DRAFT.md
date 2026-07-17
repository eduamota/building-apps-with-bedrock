# Slide Updates Draft — June 2026 Refresh

This document contains draft content for all slide updates and new slides across all 6 modules.

---

# MODULE 1: GenAI on AWS

---

## Slide 2 — Amazon Bedrock (UPDATE)

**Changes:** Update model count, add new 2026 additions

### Updated "2026 Additions" section:

**2026 Additions**
- OpenAI GPT-5.5 & GPT-5.4 (Limited Preview)
- OpenAI Codex coding agent on Bedrock
- Amazon Nova 2 Lite (GA) & Nova 2 Pro (Preview)
- OpenAI gpt-oss-120b & gpt-oss-20b
- DeepSeek V3.2, MiniMax M2.1, GLM 4.7
- Kimi K2.5, Qwen3 Coder Next
- NVIDIA Nemotron (Nano 9B/12B/30B, Super 120B)
- Google Gemma 3, Mistral Large 3

**Updated Model Providers line:**
Amazon, Anthropic, OpenAI, Meta, Mistral AI, DeepSeek, Google, NVIDIA, AI21 Labs, Cohere, Stability AI, MiniMax, Moonshot AI, Qwen, Writer, and more.

---

## NEW Slide — Project Mantle (INSERT after Slide 5)

### Project Mantle: Distributed Inference Engine

A new distributed inference engine powering large-scale model serving on Amazon Bedrock — the backbone for open-weight and partner models.

**What It Does**
- Simplifies and accelerates onboarding of new foundation models
- Provides reliable, performant serverless inference at scale
- Delivers OpenAI API compatibility out-of-the-box
- Offers sophisticated quality-of-service controls per model

**OpenAI API Compatibility**
- Access models via `bedrock-mantle.{region}.api.aws` endpoint
- Use existing OpenAI SDKs with only a base URL change
- Supports Chat Completions API and Responses API
- Reasoning effort parameter support for compatible models

**Higher Default Quotas**
- Mantle-powered models ship with higher default customer quotas than legacy endpoints
- Reduced throttling risk for open-weight model workloads

**Supported Providers**
DeepSeek, Google, MiniMax, Mistral, Moonshot AI, NVIDIA, OpenAI (OSS), Qwen, and expanding.

---

## Slide 6 — Flagship Providers (UPDATE)

**Changes:** Add Nova 2, update OpenAI section

### Amazon Nova 2 (NEW — replace or expand Nova section)

**Amazon Nova 2**
Next-generation multimodal models with extended thinking capabilities.

- **Nova 2 Lite (GA):** Cost-effective for everyday workloads — chatbots, document processing, business automation. Extended thinking with 3 intensity levels. 1M token context window. Built-in code interpreter and web grounding.
- **Nova 2 Pro (Preview):** Highly complex agentic tasks — multi-document analysis, video reasoning, software migrations. Early access via Nova Forge customers.
- **Nova Premier:** Most capable teacher model for distillation. 87.4% MMLU, 82.0% Math500. 1M token context.

### OpenAI on Bedrock (UPDATE section)

**OpenAI**
- gpt-oss-120b & gpt-oss-20b — open-weight, Apache 2.0, 128K context
- GPT-5.5 & GPT-5.4 (Limited Preview) — frontier proprietary models with full Bedrock enterprise controls
- Codex coding agent — authenticate with AWS credentials, use via CLI/desktop/VS Code

---

## Slide 7 — Extended Provider Ecosystem (UPDATE)

**Add these entries:**

**NVIDIA Nemotron**
Nano 9B/12B/30B v2 and Super 120B — high compute efficiency, open weights/datasets/recipes. Available in commercial and GovCloud regions. docs.aws.amazon

**Google Gemma 3**
Available via Project Mantle endpoint. Multimodal and edge AI capabilities. docs.aws.amazon

**Updated intro line:**
In December 2025, AWS added 18 fully managed open-weight models — the largest single expansion in Bedrock's history.

---

## NEW Slide — Automatic Model Enablement (INSERT after Slide 9)

### Simplified Access: Automatic Model Enablement

As of October 2025, Amazon Bedrock automatically enables access to all serverless foundation models in commercial AWS regions.

**What Changed**
- No more manual activation per model in the console
- Models immediately available via Console Playground, SDK, and all Bedrock features (Agents, Flows, Guardrails, Knowledge Bases, Evaluations)

**Exception: Anthropic Models**
- Still require a one-time usage form submission before first use
- Submit via API or Console in the organization management account
- Once submitted, Anthropic models are enabled across all member accounts

**Access Control**
- Use IAM policies and Service Control Policies (SCPs) to restrict model access as needed
- Automatic enablement does not bypass IAM — it only removes the manual opt-in step

---

# MODULE 2: Getting to Know Amazon Bedrock

---

## Slide 3 — API Patterns Deep Dive (UPDATE)

**Update the Responses API entry:**

### 1. Responses API (UPDATED)

Recommended for new projects. OpenAI Responses API-compatible schema via `bedrock-mantle.{region}.api.aws`. Now GA (Dec 2025).

**Key capabilities:**
- Stateful conversation management — no manual history tracking
- **Server-side custom tools (Jan 2026):** Bedrock calls Lambda functions directly without client round-trips
- Asynchronous inference for long-running workloads
- Streaming and non-streaming modes
- Multimodal inputs
- Built-in tool use with AWS-provided tools (notes, tasks) or custom Lambda functions

**Server-Side Tool Use:**
Previously, all Bedrock APIs required client-side tool orchestration. With server-side tools, Bedrock executes multi-step actions (web search, code execution, DB updates) autonomously — reducing latency and simplifying application code.

Available in: us-east-1, us-east-2, us-west-2, ap-northeast-1, ap-south-1, sa-east-1, eu-west-1, eu-west-2, eu-south-1.

---

## Slide 5 — Model Selection Criteria (UPDATE)

**Add a new dimension:**

### Extended Thinking / Reasoning
Some models support step-by-step reasoning with configurable intensity levels. Nova 2 Lite offers 3 thinking intensity levels — trade off latency for reasoning depth. Useful for complex multi-step tasks, math, and code generation. Extended thinking increases token usage but improves accuracy on hard problems.

---

## NEW Slide — Reinforcement Fine-Tuning (INSERT after Slide 6)

### Reinforcement Fine-Tuning (RFT)

A new model customization technique that delivers 66% average accuracy gains over base models — without requiring labeled datasets or deep ML expertise.

**How It Works**
1. Upload a small set of prompts (no labeled answers needed)
2. Define reward functions — rule-based graders or AI-based judges
3. Model learns from feedback on multiple possible responses per prompt
4. Deploy the fine-tuned model for on-demand inference — no extra deployment steps

**Key Benefits**
- 66% average accuracy improvement over base models
- No labeled training data required
- Fully managed — no infrastructure to configure
- Proprietary data stays within AWS secure environment
- Intermediate checkpoints for evaluation and debugging

**Supported Models**
- Amazon Nova 2 Lite (Dec 2025)
- OpenAI GPT-OSS-20B (Feb 2026)
- Qwen3 32B (Feb 2026)
- Additional models coming

**Use Cases**
- Domain-specific Q&A where labeled data is scarce
- Improving agent tool-calling accuracy
- Customizing tone, style, or reasoning patterns
- Creating smaller, faster model variants that match larger model quality

**vs. Model Distillation**
- Distillation: teacher model generates training data → student learns to mimic
- RFT: model learns from reward signals → improves its own judgment
- Complementary: use RFT to improve a base model, then distill for cost savings

---

## NEW Slide — Advanced Prompt Optimization (INSERT after RFT slide)

### Advanced Prompt Optimization & Migration Tool

Automatically optimize prompts for any model on Bedrock — compare performance across up to 5 models simultaneously.

**How It Works**
1. Input your prompt template + example user inputs
2. Optionally provide ground truth answers and evaluation criteria
3. Tool iteratively optimizes in a feedback loop
4. Output: original vs. optimized prompts, evaluation scores, cost estimates, latency

**Key Features**
- Compare across up to 5 models in one run
- Supports multimodal inputs (images, PDFs)
- Natural language evaluation criteria (no custom code needed)
- Cost and latency estimates per model
- Available via Console and APIs

**Use Cases**
- Migrating prompts from one model to another (e.g., Claude 3.5 → Nova 2)
- Optimizing existing prompts for better quality at lower cost
- Finding the cheapest model that meets your quality threshold
- A/B testing prompt variants with built-in scoring

---

# MODULE 3: RAG on Bedrock

---

## Slide 5 — Vector Databases: Supported Options (UPDATE)

**Add new entry (position first or prominently):**

### Amazon S3 Vectors (NEW — GA Dec 2025)

First cloud object storage with native vector support. Cost-optimized for AI agents, RAG, and semantic search at billion-vector scale.

**Key specs:**
- Up to 2 billion vectors per index
- 10,000 indexes per vector bucket
- Sub-second queries (infrequent); ~100ms (frequent)
- Up to 90% cost reduction vs. traditional vector databases
- S3-grade durability, elasticity, and availability
- No infrastructure provisioning required

**Security:** SSE-S3 or SSE-KMS encryption, tagging for access control

**Integration:** Native with Bedrock Knowledge Bases; hybrid search with OpenSearch Service

**Available in:** 31 AWS Regions

**Best for:** Large-scale vector workloads with cost sensitivity, infrequent queries, long-term vector archival, and AI agent memory stores. Not ideal for sustained high-QPS (use OpenSearch for hot data).

---

## Slide 12 — Cost Optimization for RAG (UPDATE)

**Update "Vector Storage" section:**

### Vector Storage (UPDATED)

- **Amazon S3 Vectors:** Up to 90% cheaper than alternatives. Best for large-scale, infrequent-query workloads. Native KB integration.
- **OpenSearch Serverless:** OCUs + storage. Best for hot data with sustained query volume.
- **Aurora pgvector:** Instances + storage + I/O. Best when you already run PostgreSQL.
- **Third-party (Pinecone, Redis, MongoDB):** Vendor pricing per index/capacity.

**NEW Optimization Strategy:**

**Tiered Vector Storage**
Use S3 Vectors for cold/archival embeddings and OpenSearch for hot, frequently-queried data. Migrate vectors between tiers based on access patterns — similar to S3 storage class tiering for objects.

---

## Slide 13 — Key Takeaways (UPDATE)

**Update item 02:**

### 02 Vector Store Selection (UPDATED)

Build a decision matrix comparing S3 Vectors (cost-optimized, infrequent query), OpenSearch Serverless (auto-scaling, hybrid search), OpenSearch Managed (tuning control), Aurora pgvector (relational + vector), Neptune Analytics (graph), and third-party stores across latency, scale, cost, query frequency, and existing infrastructure.

---

# MODULE 4: Agents on Amazon Bedrock

---

## Slides 4-5 — AgentCore (UPDATE)

**Add new section to AgentCore capabilities:**

### AgentCore Payments (Preview — April 2026)

Enables AI agents to autonomously access and pay for APIs, MCP servers, web content, and other agents.

**How It Works**
- Agents discover, negotiate, and pay for services autonomously
- Built with Coinbase (x402 protocol) and Stripe
- Spending limits enforced deterministically at the infrastructure layer
- Every transaction observable through existing AgentCore logs, metrics, and traces

**Coinbase x402 Bazaar**
- 10,000+ x402 endpoints available through AgentCore Gateway
- Agents can search, discover, and pay for endpoints autonomously

**Governance**
- Same identity system, gateway, and observability as all other agent actions
- Not a bolted-on module — native to the AgentCore platform
- Per-agent and per-user spending controls

---

## Slide 9 — Multi-Agent Architectures (UPDATE)

**Update to reflect GA status and new features:**

### Multi-Agent Collaboration (GA — March 2025)

Amazon Bedrock now natively supports multi-agent collaboration with supervisor-based coordination.

**Architecture Patterns** (existing — keep Sequential, Parallel, Hierarchical, Collaborative)

**New GA Features:**

**Inline Agents**
Dynamically adjust agent roles and behaviors at runtime — no redeployment needed. Enables adaptive workflows that respond to changing conditions.

**Payload Referencing**
Supervisor agents reference linked data instead of embedding it in every request. Reduces data transfer, improves response times, and lowers operational costs.

**Infrastructure as Code**
CloudFormation and CDK support for creating reusable teams of agents as templates. Version and deploy multi-agent systems like any other infrastructure.

**Enhanced Observability**
Built-in monitoring for agent-to-agent interactions — track delegation chains, debug coordination failures, and optimize handoff patterns.

---

## NEW Slide — Bedrock Managed Agents (INSERT after Slide 9)

### Bedrock Managed Agents (Limited Preview)

Production-ready, OpenAI-powered agents deployed on AWS with zero infrastructure management.

**What They Are**
- Pre-built agents using latest OpenAI frontier models + OpenAI agent harness
- Faster execution, sharper reasoning, reliable steering of long-running tasks
- Each agent has its own identity, logs all actions, runs in your environment

**Key Characteristics**
- All inference runs on Amazon Bedrock (not external)
- Full enterprise controls: IAM, PrivateLink, Guardrails, encryption, CloudTrail
- Integrates with AgentCore (default compute environment)
- Usage applies toward existing AWS cloud commitments

**vs. Standard Bedrock Agents**
| | Standard Agents | Managed Agents |
|---|---|---|
| Model | Any Bedrock FM | OpenAI frontier models |
| Orchestration | Custom instructions + action groups | OpenAI agent harness |
| Setup | Build from components | Pre-configured, deploy fast |
| Best for | Custom workflows, multi-model | Complex reasoning, rapid deployment |

---

## Slide 14 — Cost Optimization for Agents (UPDATE)

**Add under "Tool & KB Calls":**

**Payload Referencing (Multi-Agent)**
In multi-agent setups, use payload referencing to avoid duplicating large context across agent handoffs. Supervisor agents pass references instead of full payloads — significantly reduces token consumption in hierarchical architectures.

---

# MODULE 5: LLM Security and Observability

---

## Slide 3 — Content Filter Tiers & Multimodal (UPDATE)

**Add new section:**

### Coding Use Case Support (November 2025)

Guardrails now detect and filter harmful content within code structures:

**What's Covered**
- Code comments and documentation strings
- Variable and function names
- String literals and embedded text
- System prompt content within code contexts

**Standard Tier Additions for Code**
- **Prompt leakage detection:** Prevents unintended disclosure of system prompt information in model responses containing code
- **Denied topics in code:** Safeguards against vulnerabilities using code within restricted topics
- **PII in code:** Prevents inclusion of personally identifiable information within code structures

**Available in:** All regions where Bedrock Guardrails is supported.

---

## NEW Slide — Cross-Account Guardrails (INSERT after Slide 9)

### Cross-Account Guardrails (GA — April 2026)

Centralized enforcement of safety controls across all AWS accounts in an organization — from a single management account.

**The Problem**
Previously, guardrails had to be configured per-account. In large organizations with dozens or hundreds of accounts, this created inconsistency, gaps, and operational overhead.

**The Solution**
Central security teams implement guardrails once in the management account. Controls are automatically enforced for all foundation model interactions across the organization.

**Enforcement Levels**

1. **Organization-wide:** Baseline safety policies applied to every account automatically
2. **Account-level:** Additional restrictions for specific accounts (e.g., production vs. dev)
3. **Application-specific:** Fine-grained policies for individual applications within accounts

**Key Benefits**
- Single control point in management account
- No manual per-account configuration
- Consistent safety posture across the organization
- Blocks up to 88% of harmful multimodal content
- Filters hallucinated responses from foundation models
- Available via Console and APIs

**Access:** All AWS commercial and GovCloud regions where Bedrock Guardrails is supported.

---

## Slide 10 — Guardrails Best Practices (UPDATE)

**Add 5th best practice:**

### 5. Enforce Organization-Wide with Cross-Account Safeguards

For multi-account environments, configure baseline guardrails in the management account and enforce across the organization. Layer account-specific and application-specific policies on top. This eliminates the risk of teams deploying models without safety controls in new accounts.

---

# MODULE 6: Cost Optimization

---

## NEW Slide — On-Demand Custom Model Deployment (INSERT after Slide 4)

### On-Demand Deployment for Custom Models (July 2025)

Custom Nova models (fine-tuned or distilled) can now run on-demand without pre-provisioned compute — pay only for actual inference.

**Before (Provisioned Only)**
- Required always-on infrastructure for custom models
- Paying for idle capacity during low-traffic periods
- Higher barrier to deploying custom models in production

**After (On-Demand)**
- Process requests in real-time without pre-provisioned resources
- Pay only for tokens consumed — no idle cost
- Same model quality and performance
- Available for models fine-tuned or distilled on/after July 16, 2025

**Impact on Cost Strategy**
- Eliminates the "custom model tax" — custom models now have the same cost profile as standard on-demand
- Makes model distillation and RFT more attractive: create a custom model, deploy on-demand, pay less per token than the teacher model
- Removes the break-even calculation for custom model infrastructure

**Best For**
- Variable-traffic custom model workloads
- Dev/test environments for fine-tuned models
- Low-volume but high-value specialized models

---

## Slide 5 — Prompt Caching (UPDATE)

**Update "Supported Models" section:**

### Supported Models (UPDATED)

- Anthropic Claude models (original support)
- Amazon Nova models (expanded 2025/2026)
- Coverage actively expanding — verify per-model documentation

**Note:** Prompt caching now works with Nova 2 Lite and Nova Premier, making it applicable to the most cost-effective and most capable Amazon models simultaneously.

---

## Slide 7 — Model Distillation (UPDATE)

**Add complementary section:**

### Complementary: Reinforcement Fine-Tuning

Model Distillation and Reinforcement Fine-Tuning (RFT) are complementary optimization techniques:

| | Distillation | RFT |
|---|---|---|
| Goal | Smaller model mimics larger model | Model improves its own judgment |
| Data needed | Teacher-generated responses | Small set of prompts (no labels) |
| Result | 5x faster, 75% cheaper, <2% accuracy loss | 66% accuracy gain over base |
| Best for | Known-good teacher model exists | No labeled data; improve base model |

**Combined Strategy:**
1. Use RFT to improve a base model's accuracy on your domain
2. Use the RFT-improved model as a teacher for distillation
3. Deploy the distilled student on-demand
4. Result: smallest, cheapest, most accurate model for your use case

---

## Slide 8 — Intelligent Prompt Routing (UPDATE)

**Update the example routing pattern:**

### Example Routing Pattern (UPDATED)

| Complexity | Route To | Approximate Cost |
|---|---|---|
| Simple FAQs & Classification | GPT-OSS-20B or small Llama | Lowest |
| Standard Production Tasks | Claude Sonnet / Nova 2 Lite | Moderate |
| Complex Multi-Step Reasoning | Nova 2 Pro / Claude Opus | Higher |
| Frontier Expert Tasks | GPT-5.5 / Nova Premier | Highest |

**New:** With the expanded model catalog (18+ open-weight models), routing becomes even more impactful. The cost spread between GPT-OSS-20B and GPT-5.5 can be 10-50x per token — routing simple queries to cheap models delivers compounding savings at scale.

---

## Slide 12 — Knowledge Base Optimization (UPDATE)

**Add new section:**

### Vector Storage Tiering with S3 Vectors

Amazon S3 Vectors (GA Dec 2025) reduces vector storage costs by up to 90% compared to traditional vector databases.

**Tiered Storage Strategy:**
- **Hot tier (OpenSearch):** Frequently queried vectors, sub-10ms latency, sustained QPS
- **Warm/Cold tier (S3 Vectors):** Large-scale archival, infrequent queries, sub-second latency, 90% cheaper

**When to Use S3 Vectors for RAG:**
- Knowledge bases with millions+ of vectors where most are rarely queried
- Historical document archives that need to remain searchable
- Multi-tenant RAG where per-tenant vector counts are large but query frequency is low
- Agent memory stores that grow over time

**Integration:** Native with Bedrock Knowledge Bases — no custom code needed for basic RAG patterns.

---

## Slide 18 — Real-World Cost Optimization Patterns (UPDATE)

**Update examples with new levers:**

### Customer Service Chatbot (UPDATED)

**Before:** Frontier model for all queries, Priority tier, no caching — ~$5,000/month.

**After (2026 optimizations):**
- Intelligent Prompt Routing: simple queries → GPT-OSS-20B, complex → Nova 2 Lite, escalation → Claude Sonnet
- Prompt caching for shared system prompt (Nova 2 Lite supported)
- App-level FAQ caching via ElastiCache
- Standard tier for most traffic
- **New:** RFT-customized Nova 2 Lite for domain accuracy without frontier model cost

**Result:** ~$800/month (~85% savings)

### RAG Application (UPDATED)

**Before:** Large model for all queries, 20 chunks from OpenSearch, no caching — ~$3,500/month.

**After (2026 optimizations):**
- Intelligent Prompt Routing + Nova 2 Lite as default model
- **New:** S3 Vectors for archival corpus (90% storage savings)
- OpenSearch only for hot/recent documents
- Top-k reduced from 20 to 8 after evaluation
- Prompt caching for shared RAG instructions
- Frequent-query result caching

**Result:** ~$600/month (~83% savings)

---

# SUMMARY OF ALL CHANGES

## New Slides (7 total)
1. **Module 1:** Project Mantle
2. **Module 1:** Automatic Model Enablement
3. **Module 2:** Reinforcement Fine-Tuning
4. **Module 2:** Advanced Prompt Optimization
5. **Module 4:** Bedrock Managed Agents
6. **Module 5:** Cross-Account Guardrails
7. **Module 6:** On-Demand Custom Model Deployment

## Updated Slides (18 total)
1. Module 1, Slide 2: Bedrock overview (model count, new additions)
2. Module 1, Slide 6: Flagship Providers (Nova 2, OpenAI update)
3. Module 1, Slide 7: Extended Providers (NVIDIA, Google, 18-model expansion)
4. Module 2, Slide 3: API Patterns (Responses API GA, server-side tools)
5. Module 2, Slide 5: Model Selection (extended thinking dimension)
6. Module 2, Slide 6: Pricing Models (RFT as cost lever)
7. Module 3, Slide 5: Vector Databases (S3 Vectors)
8. Module 3, Slide 12: Cost Optimization (S3 Vectors, tiered storage)
9. Module 3, Slide 13: Key Takeaways (updated decision matrix)
10. Module 4, Slides 4-5: AgentCore (Payments)
11. Module 4, Slide 9: Multi-Agent (GA features, Inline Agents, Payload Referencing)
12. Module 4, Slide 14: Cost Optimization (Payload Referencing)
13. Module 5, Slide 3: Content Filters (coding use cases)
14. Module 5, Slide 10: Best Practices (cross-account enforcement)
15. Module 6, Slide 5: Prompt Caching (Nova support)
16. Module 6, Slide 7: Model Distillation (RFT complement)
17. Module 6, Slide 8: Intelligent Prompt Routing (updated routing table)
18. Module 6, Slide 12: KB Optimization (S3 Vectors tiering)
19. Module 6, Slide 18: Real-World Patterns (updated savings examples)
