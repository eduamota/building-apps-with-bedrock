"""
03_setup_gateway.py — Create the AgentCore Gateway (MCP, AWS_IAM) with 3 Lambda targets.

Each target wraps one tool Lambda and declares its tool schema. The orchestrator harness attaches
this gateway and calls the tools: run_research, create_strategy, create_document.

Pieces created:
  - gateway service role (trusts bedrock-agentcore, can lambda:InvokeFunction the 3 Lambdas)
  - MCP gateway with AWS_IAM inbound auth
  - 3 Lambda targets with inline tool schemas
  - resource-based permission on each Lambda allowing the gateway to invoke it
"""

import json
import time
import common as c

# Tool schemas (ToolDefinition shape). Tool names become '<target>___<toolName>' at call time.
TOOL_SCHEMAS = {
    "research-tool": [{
        "name": "run_research",
        "description": "Research an organization on the web and return a structured Markdown research summary.",
        "inputSchema": {
            "type": "object",
            "properties": {"organization": {"type": "string", "description": "The organization name to research"}},
            "required": ["organization"],
        },
    }],
    "strategy-tool": [{
        "name": "create_strategy",
        "description": "Given an organization research summary, produce a strategy brief (SWOT, options, priorities).",
        "inputSchema": {
            "type": "object",
            "properties": {"research": {"type": "string", "description": "The organization research summary text"}},
            "required": ["research"],
        },
    }],
    "document-tool": [{
        "name": "create_document",
        "description": "Given research (and optionally a strategy), produce a polished briefing document.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "research": {"type": "string", "description": "The organization research summary text"},
                "strategy": {"type": "string", "description": "Optional strategy brief text to incorporate"},
            },
            "required": ["research"],
        },
    }],
}


def ensure_gateway_role(lambda_arns):
    role_name = f"{c.PROJECT}-gateway-role"
    trust = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {"aws:SourceAccount": c.ACCOUNT_ID},
                "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{c.REGION}:{c.ACCOUNT_ID}:*"},
            },
        }],
    }
    perms = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["lambda:InvokeFunction"],
            "Resource": list(lambda_arns),
        }],
    }
    try:
        arn = c.iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
        c.iam.put_role_policy(RoleName=role_name, PolicyName="InvokeTargets", PolicyDocument=json.dumps(perms))
        print(f"OK Created gateway role {role_name}")
        time.sleep(10)
    except c.iam.exceptions.EntityAlreadyExistsException:
        arn = c.iam.get_role(RoleName=role_name)["Role"]["Arn"]
        c.iam.update_assume_role_policy(RoleName=role_name, PolicyDocument=json.dumps(trust))
        c.iam.put_role_policy(RoleName=role_name, PolicyName="InvokeTargets", PolicyDocument=json.dumps(perms))
        print(f"OK Refreshed gateway role {role_name}")
        time.sleep(5)
    return arn


def find_gateway(name):
    for g in c.control.list_gateways().get("items", c.control.list_gateways().get("gateways", [])):
        if g.get("name") == name:
            return g.get("gatewayId") or g.get("gatewayArn", "").split("/")[-1], g
    return None, None


def wait_gateway_ready(gateway_id, timeout=180):
    deadline = time.time() + timeout
    while time.time() < deadline:
        g = c.control.get_gateway(gatewayIdentifier=gateway_id)
        status = g.get("status")
        print(f"  gateway {gateway_id}: {status}")
        if status in ("READY", "ACTIVE"):
            return g
        if status and "FAIL" in status:
            raise RuntimeError(f"gateway {status}: {g.get('statusReasons') or g.get('statusReason')}")
        time.sleep(8)
    raise TimeoutError("gateway not ready")


def main():
    with open(".tool_lambda_arns.json") as f:
        lambda_arns = json.load(f)   # {"research-tool": arn, ...}

    gateway_role = ensure_gateway_role(list(lambda_arns.values()))

    # Create (or reuse) the gateway
    gid, _ = find_gateway(c.GATEWAY_NAME)
    if gid:
        print(f"OK Reusing gateway {gid}")
    else:
        resp = c.control.create_gateway(
            name=c.GATEWAY_NAME,
            roleArn=gateway_role,
            protocolType="MCP",
            authorizerType="AWS_IAM",
            description="OrgIntel multi-agent tool gateway",
        )
        gid = resp.get("gatewayId") or resp.get("gatewayArn", "").split("/")[-1]
        print(f"OK Created gateway {gid}")
    g = wait_gateway_ready(gid)
    gateway_arn = g.get("gatewayArn")

    # Existing targets (so re-runs don't duplicate)
    existing_targets = {t.get("name") for t in
                        c.control.list_gateway_targets(gatewayIdentifier=gid).get("items", [])}

    for short, tool_schema in TOOL_SCHEMAS.items():
        # Target name must match ([0-9a-zA-Z][-]?){1,100} - no underscores. The gateway prepends
        # '<targetName>___' to each tool at call time; our Lambdas strip at '___'.
        target_name = short.replace("-", "")  # e.g. "research-tool" -> "researchtool"
        lambda_arn = lambda_arns[short]

        # Allow the gateway to invoke this Lambda (resource-based policy).
        try:
            c.lambda_client.add_permission(
                FunctionName=lambda_arn,
                StatementId=f"gw-{c.GATEWAY_NAME}-{target_name}",
                Action="lambda:InvokeFunction",
                Principal="bedrock-agentcore.amazonaws.com",
                SourceArn=gateway_arn,
            )
            print(f"OK Granted gateway invoke on {short}")
        except c.lambda_client.exceptions.ResourceConflictException:
            print(f"OK Lambda permission already present on {short}")

        if target_name in existing_targets:
            print(f"OK Target {target_name} already exists")
            continue

        c.control.create_gateway_target(
            gatewayIdentifier=gid,
            name=target_name,
            description=f"{short} tool",
            targetConfiguration={"mcp": {"lambda": {
                "lambdaArn": lambda_arn,
                "toolSchema": {"inlinePayload": tool_schema},
            }}},
            credentialProviderConfigurations=[{"credentialProviderType": "GATEWAY_IAM_ROLE"}],
        )
        print(f"OK Created target {target_name} -> {short}")

    with open(".gateway.json", "w") as f:
        json.dump({"gatewayId": gid, "gatewayArn": gateway_arn}, f, indent=2)

    print("\n" + "=" * 60)
    print("GATEWAY READY")
    print("=" * 60)
    print(f"Gateway ID : {gid}")
    print(f"Gateway ARN: {gateway_arn}")
    print("Tools: run_research, create_strategy, create_document")
    print("=" * 60)
    return gid, gateway_arn


if __name__ == "__main__":
    main()
