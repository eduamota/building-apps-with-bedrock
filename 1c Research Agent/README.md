# 1c — Org Research Agent (Amazon Bedrock AgentCore Harness)

A deep-research agent built on the **AgentCore Harness** (the managed, config-based agent loop).
You give it an organization name; it researches the organization on the web and produces a
structured Markdown **org summary** (overview, products, market, leadership, recent news, risks,
and sources).

Unlike the code-based agents in `3a`/`3b` (which you write and deploy yourself), this demo writes
**no orchestration code** — the agent is pure configuration (model + system prompt + a web-search
tool + limits). AgentCore runs the reasoning → tool-call → result → response loop for you.

## Architecture

```
                      invoke_harness(messages=[org name])
   research_org.py  ───────────────────────────────────────▶  AgentCore Harness
   (or notebook)                                               (managed Strands loop)
        ▲                                                            │
        │  streamed events (text / toolUse / toolResult)            │ calls web-search tool
        │                                                            ▼
        └──────────────  Markdown org summary  ◀──────────  Web Search (AWS Gateway connector)
```

- **Harness** — managed loop; model is Claude Sonnet 4.6 via the US cross-region inference profile
  (`us.anthropic.claude-sonnet-4-6` — the bare base model ID is not invocable on-demand).
- **Web search tool** — how the agent reads the web (see options below).
- **Client** (`research_org.py` / notebook) — submits the org name, streams the response,
  and saves the summary to `summaries/<org>.md`.

## Web-search options

The Harness has built-in `shell` and `file_operations` but **no built-in web search**. Pick one:

| Option | What it is | Setup | Notes |
|--------|-----------|-------|-------|
| **A. AgentCore Browser** (default here) | Agent drives a managed headless browser | Add `agentcore_browser` tool — **no gateway, no key** | Zero prerequisites; works in any AgentCore region. "Deepest" (reads live pages) but slower/costlier. |
| **B. AWS Web Search Gateway** | AWS-native `WebSearch` MCP tool behind an AgentCore Gateway | Create a Gateway (MCP, `AWS_IAM`) + `web-search` connector target; grant IAM | Faster, index-based. Queries served entirely within AWS. **`us-east-1` only.** |

Both options are fully AWS-native (no third-party services). `setup_research_agent.py` uses
**Option A (Browser)** by default so the demo runs with **no extra setup**. Switch to the AWS Web
Search Gateway with `--search aws-gateway`; for that you must first create the Web Search gateway
(see [Set up Web Search Tool](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-add-target-api-target-config.html))
and pass its ARN via `--gateway-arn`.

## Prerequisites

- AWS credentials for an account with **AgentCore + Bedrock** access in your chosen region
  (**`us-east-1`** if you use the AWS Web Search Gateway).
- Model access to the harness model (**Claude Sonnet 4.6**, used via the inference profile
  `us.anthropic.claude-sonnet-4-6`) enabled in Bedrock.
- Python 3.10+ and the packages in `requirements.txt` (`pip install -r requirements.txt`).
- An IAM **execution role** the harness can assume (`bedrock-agentcore.amazonaws.com` trust with
  confused-deputy conditions). `setup_research_agent.py` creates one if you don't pass `--role-arn`.
- For the **AWS Web Search Gateway** path only: a Web Search **Gateway** already created, and its ARN.
  The default **Browser** path needs none of this.

> API shapes follow the GA AgentCore Harness APIs (`bedrock-agentcore-control` for create/get,
> `bedrock-agentcore` for invoke). AgentCore evolves quickly — if a parameter is rejected, check
> the [CreateHarness API reference](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/API_CreateHarness.html).

## Files

| File | Purpose |
|------|---------|
| `setup_research_agent.py` | Idempotent: create/reuse the harness (model, system prompt, web-search tool, limits), poll until `READY`, print the harness ARN. |
| `research_org.py` | Invoke the harness for a given org, stream the response, save `summaries/<org>.md`. |
| `research_agent_demo.ipynb` | Notebook walking through create → poll → invoke → render, with explanation. |
| `requirements.txt` | Python dependencies. |

## Quick start

```bash
cd "1c Research Agent"
pip install -r requirements.txt

# 1) Create the harness (default — AgentCore Browser; no gateway/key needed)
python setup_research_agent.py --region us-east-1 --search browser

#    …or the AWS-native search path (Option B — Web Search Gateway; us-east-1), needs a gateway ARN:
# python setup_research_agent.py --region us-east-1 --search aws-gateway \
#   --gateway-arn arn:aws:bedrock-agentcore:us-east-1:<acct>:gateway/<web-search-gw>

# 2) Research an organization (writes summaries/<org>.md)
python research_org.py --org "Anthropic" --region us-east-1
```

The harness ARN from step 1 is cached in `.harness_arn` so `research_org.py` can find it
(or pass `--harness-arn`).

## How the agent is configured (no code)

- **System prompt** instructs the agent to run multiple targeted web searches, corroborate across
  sources, avoid speculation, and emit a fixed Markdown section layout with inline source URLs.
- **Limits** (`maxIterations`, `maxTokens`, `timeoutSeconds`) are set explicitly as cost/abuse
  guardrails (deep research can loop through many searches).
- **Tools** are restricted with `allowedTools` to just the web-search tool plus `file_operations`
  (so it can draft the summary) — keeping tool-definition token overhead and blast radius down.

## Cleanup

The harness persists until deleted:

```bash
aws bedrock-agentcore-control delete-harness --harness-id <id> --region <region>
```

(The IAM role created by the setup script, if any, is left in place; delete it manually if you
don't need it.)

## Security notes

- The execution role is least-privilege and scoped with `aws:SourceAccount` / `aws:SourceArn`
  confused-deputy conditions.
- Treat all `invoke_harness` input as trusted — anyone who can invoke gets the full session + tools.
  Put API Gateway/WAF and rate limiting in front for any shared deployment.
- Web-search results are untrusted content; the system prompt tells the agent to treat page content
  as data, not instructions (prompt-injection hygiene).
