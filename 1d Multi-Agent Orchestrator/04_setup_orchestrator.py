"""
04_setup_orchestrator.py — Create the orchestrator harness.

The orchestrator is a Harness whose only tool is the AgentCore Gateway (which exposes
run_research, create_strategy, create_document). Its system prompt coordinates the workflow:
research -> (strategy + document) -> synthesize a final answer. The chat backend invokes this
harness; it fans out to the sub-agents through the gateway.
"""

import json
import common as c

ORCHESTRATOR_PROMPT = """You are OrgIntel, an orchestrator that produces a complete organization \
intelligence package by coordinating three specialist tools.

You have these tools (via the gateway):
- run_research(organization): deep web research -> a research summary
- create_strategy(research): a strategy brief from the research
- create_document(research, strategy): a polished briefing document

Workflow for a request about an organization:
1. Call run_research with the organization name. Wait for the research summary.
2. Call create_strategy with that research summary.
3. Call create_document with the research summary AND the strategy.
4. Produce a final response to the user that contains THREE clearly separated Markdown sections,
   in this order, using the tool outputs verbatim (do not rewrite them):

# Research
<the run_research output>

# Strategy
<the create_strategy output>

# Briefing Document
<the create_document output>

Rules:
- Always run research FIRST; strategy and document both depend on it.
- Pass the FULL research text to create_strategy and create_document (don't summarize it yourself).
- If the user's message is not about researching an organization, answer briefly and conversationally without calling tools.
- Do not fabricate content; rely on the tool outputs. If a tool fails, say so and continue with what you have."""


def main():
    gw = json.load(open(".gateway.json"))
    gateway_arn = gw["gatewayArn"]

    role = c.ensure_harness_role(f"{c.PROJECT}-orchestrator-harness-role", include_gateway=True)

    tools = [{
        "type": "agentcore_gateway",
        "name": "orgtools",
        "config": {"agentCoreGateway": {
            "gatewayArn": gateway_arn,
            "outboundAuth": {"awsIam": {}},
        }},
    }]
    # Allow all gateway tools + file_operations (orchestrator may draft the final answer).
    allowed = ["@orgtools", "@builtin/file_operations"]

    arn = c.create_or_update_harness(
        c.ORCHESTRATOR_HARNESS_NAME, role, ORCHESTRATOR_PROMPT, tools, allowed,
        max_iterations=20, max_tokens=8192, timeout_seconds=900,  # full chain can be minutes
    )

    with open(".orchestrator.json", "w") as f:
        json.dump({"harnessArn": arn}, f, indent=2)

    print("\n" + "=" * 60)
    print("ORCHESTRATOR READY")
    print("=" * 60)
    print(f"Harness ARN: {arn}")
    print("Saved to .orchestrator.json")
    print("=" * 60)
    return arn


if __name__ == "__main__":
    main()
