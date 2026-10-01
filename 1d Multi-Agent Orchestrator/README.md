# 1d — Multi-Agent Org Intelligence Orchestrator (AgentCore)

A full-stack, multi-agent application on **Amazon Bedrock AgentCore**. You enter an organization in a
web chat; an **orchestrator agent** coordinates three specialist agents and returns a complete
intelligence package: **Research → Strategy → Briefing Document**.

Built on top of the `1c Research Agent` (its research harness is reused here as the research
specialist). All agents are **AgentCore Harnesses** (config-based, no orchestration code) and the
sub-agents are exposed to the orchestrator as tools through an **AgentCore Gateway**.

## Architecture

```
Browser (static site on S3)
      │  HTTPS fetch (POST /chat, GET /chat/{jobId})
      ▼
Amazon API Gateway (HTTP API)  ──AWS_PROXY──▶  Backend Lambda (async)
                                                   │  POST: create job (DynamoDB) + async self-invoke
                                                   │  worker: invoke_harness(orchestrator)  ← long run
                                                   │  GET: poll job status/result
                                                   ▼
                                        Orchestrator Harness  (Claude Sonnet 4.6)
                                                   │  agentcore_gateway tool "orgtools"
                                                   ▼
                                        AgentCore Gateway (MCP, AWS_IAM)
                                                   │  3 Lambda targets
                        ┌──────────────────────────┼──────────────────────────┐
                        ▼                           ▼                          ▼
              research-tool Lambda        strategy-tool Lambda        document-tool Lambda
                        │                           │                          │
                        ▼                           ▼                          ▼
              Research Harness             Strategy Harness            Document Harness
              (reused 1c, Browser)         (LLM-only)                  (LLM-only)
```

**Why async?** A full run (research browses the web, then strategy, then document) takes minutes —
well past API Gateway's 30s limit. So `POST /chat` returns a `jobId` immediately and the frontend
polls `GET /chat/{jobId}`; the actual orchestration runs in a background Lambda worker and writes
status/result to DynamoDB.

## The agents

| Agent | Type | Tool(s) | Role |
|-------|------|---------|------|
| **Research** | Harness (reused from 1c) | AgentCore Browser | Deep web research → structured summary |
| **Strategy** | Harness (LLM-only) | `file_operations` | SWOT, options, prioritized recommendations |
| **Document** | Harness (LLM-only) | `file_operations` | Polished executive briefing document |
| **Orchestrator** | Harness | AgentCore Gateway (`run_research`, `create_strategy`, `create_document`) | Coordinates: research → strategy → document → synthesize |

The orchestrator's system prompt enforces the workflow (research first; pass full research text to
both strategy and document; emit three verbatim sections `# Research`, `# Strategy`,
`# Briefing Document`).

## Files

| File | Purpose |
|------|---------|
| `common.py` | Shared config + boto3 helpers (harness create/poll/invoke, lambda zip/deploy, IAM) |
| `01_setup_subagents.py` | Create the document + strategy harnesses (research is reused from 1c) |
| `02_setup_tool_lambdas.py` | Deploy 3 tool Lambdas that `invoke_harness` each sub-agent |
| `03_setup_gateway.py` | Create the AgentCore Gateway (MCP) with the 3 Lambda targets + tool schemas |
| `04_setup_orchestrator.py` | Create the orchestrator harness wired to the gateway |
| `05_setup_backend.py` | DynamoDB job table + async backend chat Lambda |
| `06_setup_api.py` | HTTP API Gateway (`POST /chat`, `GET /chat/{jobId}`) with CORS |
| `08_setup_apikey.py` | API key auth: Secrets Manager key + Lambda authorizer on both routes |
| `07_setup_site.py` | Deploy the static chat website to S3 |
| `site/index.html` | The chat UI (plain HTML/JS; polls the API, renders Markdown) |

Each step writes a small `.json` state file (`.tool_lambda_arns.json`, `.gateway.json`,
`.orchestrator.json`, `.backend.json`, `.api.json`, `.site.json`) that the next step reads.

## Deploy (in order)

```bash
cd "1d Multi-Agent Orchestrator"
pip install boto3

# Prerequisite: the 1c research harness (org_research_agent) must already exist and be READY.
python 01_setup_subagents.py     # document + strategy harnesses
python 02_setup_tool_lambdas.py  # 3 tool Lambdas
python 03_setup_gateway.py       # AgentCore Gateway + targets
python 04_setup_orchestrator.py  # orchestrator harness
python 05_setup_backend.py       # DynamoDB + backend Lambda
python 06_setup_api.py           # HTTP API Gateway
python 08_setup_apikey.py        # API key auth (Lambda authorizer + Secrets Manager)
python 07_setup_site.py          # S3 static website
```

The final step prints the website URL. Open it, **enter your API key** (printed by
`08_setup_apikey.py`, also saved to `.apikey.json`), type an organization (e.g. `Anthropic`), and
watch the three-part package stream back after a few minutes. A conversational message (e.g. "what
can you do?") returns in seconds without invoking the tools.

## Prerequisites

- AWS credentials for an account with **AgentCore + Bedrock** access in **us-west-2**.
- Bedrock model access to **Claude Sonnet 4.6** via the inference profile `us.anthropic.claude-sonnet-4-6`.
- The **1c research harness** (`org_research_agent`) deployed and READY (this demo reuses it).
- Python 3.10+ with `boto3 >= 1.43`.

## Region & model notes

- Everything is in **us-west-2**. The sub-agent tool Lambdas call `invoke_harness` in-region.
- The model is invoked via the **`us.` inference profile** (the bare `anthropic.claude-sonnet-4-6`
  base ID is not on-demand-invocable).
- Gateway **target names** must match `([0-9a-zA-Z][-]?)+` (no underscores); the gateway prepends
  `<targetName>___` to each tool, which the tool Lambdas strip.

## Security notes

- **Harness execution roles** are scoped per agent, with confused-deputy conditions
  (`aws:SourceAccount` + `aws:SourceArn` across AgentCore resources). Internal hops are IAM-only.
- **API key authentication.** Both chat routes are protected by a **Lambda REQUEST authorizer**
  (`08_setup_apikey.py`) that validates an `x-api-key` header against a key stored in **AWS Secrets
  Manager** (HTTP APIs don't support native API keys/usage plans — that's a REST API v1 feature).
  No key → `401`. The authorizer uses a 0-second result TTL so a rotated/removed key takes effect
  immediately. The chat UI takes the key as a **field** (stored in the browser's `localStorage`) and
  sends it per request — the key is **not** baked into the served HTML.
  - Caveat: an API key is an identifier for throttling/basic gating, **not** strong user auth, and a
    browser-entered key is still visible to that user. For real end-user auth, add a Cognito/JWT
    authorizer; keep per-client keys server-side where possible.
- For production also: put **AWS WAF** in front, add rate limiting, and rotate the Secrets Manager
  key periodically.
- **S3 website hosting serves over HTTP.** For HTTPS + a custom domain, front the bucket with
  **CloudFront** (and lock the bucket to the CloudFront OAC instead of public-read).
- Web-search/browse results are untrusted; sub-agent prompts treat page content as data, not
  instructions (prompt-injection hygiene).

## Cost & cleanup

Live, billable resources: 4 harnesses (+ managed memory), 6 Lambdas (incl. the API-key authorizer),
1 Gateway, 1 DynamoDB table, 1 HTTP API, 1 Secrets Manager secret, 1 S3 bucket, Browser sessions per
research run. To tear down:

```bash
# harnesses
aws bedrock-agentcore-control delete-harness --harness-id <id> --region us-west-2   # orchestrator, document, strategy
# gateway targets + gateway
aws bedrock-agentcore-control delete-gateway-target --gateway-identifier <gw> --target-id <t> --region us-west-2
aws bedrock-agentcore-control delete-gateway --gateway-identifier <gw> --region us-west-2
# lambdas, table, api, bucket
aws lambda delete-function --function-name orgintel-<name> --region us-west-2
aws dynamodb delete-table --table-name orgintel-chat-jobs --region us-west-2
aws secretsmanager delete-secret --secret-id orgintel-chat-api-key --force-delete-without-recovery --region us-west-2
aws apigatewayv2 delete-api --api-id <apiId> --region us-west-2
aws s3 rb s3://orgintel-chat-site-<account> --force
```
(The IAM roles created by the scripts are left in place; delete them manually if desired. The 1c
research harness is shared — don't delete it unless you're also tearing down 1c.)

## Status

Deployed and verified end-to-end in us-west-2: a `POST /chat` for an organization runs the full
research → strategy → document chain and returns the synthesized three-section package through the
public API and the S3 chat site.
