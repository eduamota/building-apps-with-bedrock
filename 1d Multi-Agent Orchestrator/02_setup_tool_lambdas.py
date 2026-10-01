"""
02_setup_tool_lambdas.py — Deploy the 3 tool Lambdas that the AgentCore Gateway will target.

Each Lambda wraps one sub-agent harness: it receives the tool arguments (flat event), calls
invoke_harness on its sub-agent, collects the streamed text, and returns JSON. These Lambdas are
the Gateway targets; the orchestrator calls them as tools.

Gateway Lambda contract (from AWS docs):
  - event    = flat map of the tool inputSchema properties
  - toolName = context.client_context.custom['bedrockAgentCoreToolName'], prefixed '<target>___'
  - return   = JSON the gateway can parse
"""

import json
import common as c

# Shared body: a helper that invokes a harness ARN with a single text prompt and returns text.
# (Each Lambda gets its harness ARN via the HARNESS_ARN env var.)
INVOKE_HELPER = '''
import json, os, uuid
import boto3

REGION = os.environ["REGION"]
HARNESS_ARN = os.environ["HARNESS_ARN"]
_runtime = boto3.client("bedrock-agentcore", region_name=REGION)

def invoke_subagent(prompt_text):
    session_id = str(uuid.uuid4())  # >= 33 chars
    resp = _runtime.invoke_harness(
        harnessArn=HARNESS_ARN,
        runtimeSessionId=session_id,
        messages=[{"role": "user", "content": [{"text": prompt_text}]}],
    )
    chunks = []
    for event in resp["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            if delta.get("text"):
                chunks.append(delta["text"])
        elif "runtimeClientError" in event:
            raise Exception(event["runtimeClientError"].get("message", "runtime error"))
    return "".join(chunks).strip()

def tool_name_from_context(context):
    try:
        raw = context.client_context.custom["bedrockAgentCoreToolName"]
        return raw.split("___", 1)[-1]  # strip the '<target>___' prefix
    except Exception:
        return None
'''

RESEARCH_LAMBDA = INVOKE_HELPER + '''
def lambda_handler(event, context):
    org = event.get("organization") or event.get("input") or ""
    if not org:
        return {"error": "organization is required"}
    prompt = f'Research the organization "{org}" and produce the structured Markdown summary exactly as specified in your instructions.'
    return {"result": invoke_subagent(prompt)}
'''

DOCUMENT_LAMBDA = INVOKE_HELPER + '''
def lambda_handler(event, context):
    research = event.get("research") or event.get("input") or ""
    strategy = event.get("strategy") or ""
    if not research:
        return {"error": "research is required"}
    prompt = "Create the briefing document from the following research"
    if strategy:
        prompt += " and strategy"
    prompt += ".\\n\\n=== RESEARCH ===\\n" + research
    if strategy:
        prompt += "\\n\\n=== STRATEGY ===\\n" + strategy
    return {"result": invoke_subagent(prompt)}
'''

STRATEGY_LAMBDA = INVOKE_HELPER + '''
def lambda_handler(event, context):
    research = event.get("research") or event.get("input") or ""
    if not research:
        return {"error": "research is required"}
    prompt = "Create the strategy brief from the following organization research.\\n\\n=== RESEARCH ===\\n" + research
    return {"result": invoke_subagent(prompt)}
'''


def invoke_harness_statement(harness_arn):
    """IAM allowing a Lambda to invoke a specific harness + its underlying runtime."""
    runtime_arn = harness_arn.replace(":harness/", ":runtime/")  # best-effort; also allow all in acct
    return [
        {"Effect": "Allow",
         "Action": ["bedrock-agentcore:InvokeHarness", "bedrock-agentcore:InvokeAgentRuntime"],
         "Resource": [
             harness_arn,
             f"arn:aws:bedrock-agentcore:{c.REGION}:{c.ACCOUNT_ID}:harness/*",
             f"arn:aws:bedrock-agentcore:{c.REGION}:{c.ACCOUNT_ID}:runtime/*",
         ]},
    ]


def main():
    # Resolve sub-agent harness ARNs
    research_arn, _ = c.find_harness(c.RESEARCH_HARNESS_NAME)
    document_arn, _ = c.find_harness(c.DOCUMENT_HARNESS_NAME)
    strategy_arn, _ = c.find_harness(c.STRATEGY_HARNESS_NAME)
    assert research_arn and document_arn and strategy_arn, "sub-agent harnesses must exist (run 01 first)"

    specs = [
        ("research-tool", RESEARCH_LAMBDA, research_arn),
        ("document-tool", DOCUMENT_LAMBDA, document_arn),
        ("strategy-tool", STRATEGY_LAMBDA, strategy_arn),
    ]

    arns = {}
    for short, src, harness_arn in specs:
        fn_name = f"{c.PROJECT}-{short}"
        role = c.ensure_lambda_role(f"{fn_name}-role", invoke_harness_statement(harness_arn))
        fn_arn = c.deploy_lambda(
            fn_name, src, role,
            timeout=300,  # research (browser) can take minutes
            memory=256,
            env={"REGION": c.REGION, "HARNESS_ARN": harness_arn},
        )
        arns[short] = fn_arn
        print(f"  {short}: {fn_arn}  -> harness {harness_arn.split('/')[-1]}")

    # Persist the Lambda ARNs for the gateway setup step.
    with open(".tool_lambda_arns.json", "w") as f:
        json.dump(arns, f, indent=2)

    print("\n" + "=" * 60)
    print("TOOL LAMBDAS DEPLOYED")
    print("=" * 60)
    for k, v in arns.items():
        print(f"{k}: {v}")
    print("Saved ARNs to .tool_lambda_arns.json")
    print("=" * 60)
    return arns


if __name__ == "__main__":
    main()
