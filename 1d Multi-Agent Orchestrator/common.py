"""
common.py — Shared configuration and helpers for the 1d Multi-Agent Orchestrator.

Centralizes region, resource names, the model ID, and reusable boto3 helpers so every
setup script stays consistent. All lessons from the 1c deploy are baked in here:
  - harness responses are wrapped under a 'harness' key
  - get_harness status lives at harness.status
  - Claude Sonnet 4.6 must be invoked via the us. inference profile (not the bare model ID)
  - execution-role trust must be scoped to all AgentCore resources (not just harness/*),
    because a harness is backed by an AgentCore Runtime
  - create_harness can conflict briefly after a same-name delete (retry)
"""

import json
import time
import uuid
import zipfile
from io import BytesIO

import boto3

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REGION = "us-west-2"
PROJECT = "orgintel"                      # short prefix for all resources
MODEL_ID = "us.anthropic.claude-sonnet-4-6"   # cross-region inference profile (on-demand-invocable)

# Harness names (letters/digits/underscore, start with a letter, <= 40 chars)
RESEARCH_HARNESS_NAME = "org_research_agent"      # reused from 1c
DOCUMENT_HARNESS_NAME = "orgintel_document_agent"
STRATEGY_HARNESS_NAME = "orgintel_strategy_agent"
ORCHESTRATOR_HARNESS_NAME = "orgintel_orchestrator"

GATEWAY_NAME = "orgintel-gateway"
JOB_TABLE = "orgintel-chat-jobs"
API_NAME = "orgintel-chat-api"
SITE_BUCKET_PREFIX = "orgintel-chat-site"         # + account id

# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
ACCOUNT_ID = boto3.client("sts").get_caller_identity()["Account"]
control = boto3.client("bedrock-agentcore-control", region_name=REGION)
runtime = boto3.client("bedrock-agentcore", region_name=REGION)
iam = boto3.client("iam", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)


# ---------------------------------------------------------------------------
# IAM helpers
# ---------------------------------------------------------------------------
def harness_trust_policy():
    """Trust policy for a harness execution role (scoped to all AgentCore resources)."""
    return {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {"aws:SourceAccount": ACCOUNT_ID},
                # Scope to all AgentCore resources: a harness is backed by a Runtime, so a
                # harness/*-only condition fails role validation.
                "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock-agentcore:{REGION}:{ACCOUNT_ID}:*"},
            },
        }],
    }


def harness_permissions(include_gateway=False):
    """Least-privilege-ish execution-role permissions for a harness (AWS sample + memory + browser)."""
    r, a = REGION, ACCOUNT_ID
    stmts = [
        {"Sid": "BedrockModelInvocation", "Effect": "Allow",
         "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
         "Resource": ["arn:aws:bedrock:*::foundation-model/*",
                      f"arn:aws:bedrock:*:{a}:inference-profile/*",
                      f"arn:aws:bedrock:{r}:{a}:*"]},
        {"Sid": "EcrPublicTokenAccess", "Effect": "Allow",
         "Action": ["ecr-public:GetAuthorizationToken"], "Resource": "*"},
        {"Sid": "StsForEcrPublicPull", "Effect": "Allow",
         "Action": ["sts:GetServiceBearerToken"], "Resource": "*"},
        {"Sid": "XRay", "Effect": "Allow",
         "Action": ["xray:PutTraceSegments", "xray:PutTelemetryRecords",
                    "xray:GetSamplingRules", "xray:GetSamplingTargets"], "Resource": "*"},
        {"Sid": "LogsGroup", "Effect": "Allow",
         "Action": ["logs:CreateLogGroup", "logs:DescribeLogStreams"],
         "Resource": f"arn:aws:logs:{r}:{a}:log-group:/aws/bedrock-agentcore/runtimes/*"},
        {"Sid": "LogsDescribe", "Effect": "Allow",
         "Action": ["logs:DescribeLogGroups"], "Resource": f"arn:aws:logs:{r}:{a}:log-group:*"},
        {"Sid": "LogsStream", "Effect": "Allow",
         "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
         "Resource": f"arn:aws:logs:{r}:{a}:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"},
        {"Sid": "LogsResourcePolicy", "Effect": "Allow",
         "Action": ["logs:PutResourcePolicy"], "Resource": "*"},
        {"Sid": "Metrics", "Effect": "Allow", "Resource": "*",
         "Action": "cloudwatch:PutMetricData",
         "Condition": {"StringEquals": {"cloudwatch:namespace": "bedrock-agentcore"}}},
        {"Sid": "WorkloadIdentity", "Effect": "Allow",
         "Action": ["bedrock-agentcore:GetWorkloadAccessToken",
                    "bedrock-agentcore:GetWorkloadAccessTokenForJWT"],
         "Resource": [
             f"arn:aws:bedrock-agentcore:{r}:{a}:workload-identity-directory/default",
             f"arn:aws:bedrock-agentcore:{r}:{a}:workload-identity-directory/default/workload-identity/*"]},
        {"Sid": "Browser", "Effect": "Allow",
         "Action": ["bedrock-agentcore:StartBrowserSession", "bedrock-agentcore:StopBrowserSession",
                    "bedrock-agentcore:GetBrowserSession", "bedrock-agentcore:ListBrowserSessions",
                    "bedrock-agentcore:UpdateBrowserStream",
                    "bedrock-agentcore:ConnectBrowserAutomationStream",
                    "bedrock-agentcore:ConnectBrowserLiveViewStream"],
         "Resource": f"arn:aws:bedrock-agentcore:{r}:aws:browser/*"},
        {"Sid": "Memory", "Effect": "Allow",
         "Action": ["bedrock-agentcore:CreateEvent", "bedrock-agentcore:DeleteEvent",
                    "bedrock-agentcore:GetEvent", "bedrock-agentcore:ListEvents",
                    "bedrock-agentcore:RetrieveMemoryRecords"],
         "Resource": f"arn:aws:bedrock-agentcore:{r}:{a}:memory/*"},
    ]
    if include_gateway:
        stmts.append({"Sid": "GatewayInvoke", "Effect": "Allow",
                      "Action": ["bedrock-agentcore:InvokeGateway"],
                      "Resource": f"arn:aws:bedrock-agentcore:{r}:{a}:gateway/*"})
    return {"Version": "2012-10-17", "Statement": stmts}


def ensure_harness_role(role_name, include_gateway=False):
    """Create or refresh an execution role for a harness; returns its ARN."""
    trust = json.dumps(harness_trust_policy())
    perms = json.dumps(harness_permissions(include_gateway=include_gateway))
    try:
        arn = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=trust)["Role"]["Arn"]
        iam.put_role_policy(RoleName=role_name, PolicyName="HarnessAccess", PolicyDocument=perms)
        print(f"OK Created role {role_name}")
        time.sleep(10)
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=role_name)["Role"]["Arn"]
        iam.update_assume_role_policy(RoleName=role_name, PolicyDocument=trust)
        iam.put_role_policy(RoleName=role_name, PolicyName="HarnessAccess", PolicyDocument=perms)
        print(f"OK Refreshed role {role_name}")
        time.sleep(5)
    return arn


# ---------------------------------------------------------------------------
# Harness helpers
# ---------------------------------------------------------------------------
def find_harness(name):
    """Return (arn, status) of a harness by name, or (None, None)."""
    for h in control.list_harnesses().get("harnesses", []):
        if h.get("harnessName") == name:
            return h.get("arn"), h.get("status")
    return None, None


def wait_harness_ready(harness_id, timeout=360):
    deadline = time.time() + timeout
    while time.time() < deadline:
        h = control.get_harness(harnessId=harness_id).get("harness", {})
        status = h.get("status")
        print(f"  {harness_id}: {status}")
        if status == "READY":
            return h
        if status in ("CREATE_FAILED", "UPDATE_FAILED", "DELETE_FAILED"):
            reason = h.get("failureReason") or h.get("statusReason") or "(no reason)"
            raise RuntimeError(f"{harness_id} {status}: {reason}")
        time.sleep(10)
    raise TimeoutError(f"{harness_id} not READY within {timeout}s")


def delete_harness_if_failed(name):
    """If a harness exists in a failed state, delete it and wait for removal."""
    arn, status = find_harness(name)
    if arn and status in ("CREATE_FAILED", "UPDATE_FAILED", "DELETE_FAILED"):
        hid = arn.split("/")[-1]
        print(f"Deleting failed harness {hid} ({status})...")
        control.delete_harness(harnessId=hid)
        for _ in range(30):
            try:
                control.get_harness(harnessId=hid)
                time.sleep(5)
            except Exception:
                break


def create_or_update_harness(name, role_arn, system_prompt, tools, allowed_tools,
                             max_iterations=25, max_tokens=8192, timeout_seconds=600):
    """Idempotently create/update a harness and wait for READY. Returns its ARN."""
    delete_harness_if_failed(name)
    arn, status = find_harness(name)
    model = {"bedrockModelConfig": {"modelId": MODEL_ID, "maxTokens": max_tokens}}
    kwargs = dict(
        model=model,
        systemPrompt=[{"text": system_prompt}],
        tools=tools,
        allowedTools=allowed_tools,
        maxIterations=max_iterations,
        maxTokens=max_tokens,
        timeoutSeconds=timeout_seconds,
    )
    if arn:
        hid = arn.split("/")[-1]
        wait_harness_ready(hid)
        print(f"Updating harness {name}...")
        control.update_harness(harnessId=hid, **kwargs)
        wait_harness_ready(hid)
        return arn

    print(f"Creating harness {name}...")
    resp = None
    for attempt in range(12):
        try:
            resp = control.create_harness(harnessName=name, executionRoleArn=role_arn, **kwargs)
            break
        except control.exceptions.ConflictException:
            print(f"  name in use (delete settling), retry {attempt + 1}")
            time.sleep(10)
    if resp is None:
        raise RuntimeError(f"create_harness kept conflicting for {name}")
    h = resp.get("harness", resp)
    arn = h.get("arn") or h.get("harnessArn")
    hid = arn.split("/")[-1]
    wait_harness_ready(hid)
    return arn


# ---------------------------------------------------------------------------
# Lambda helpers
# ---------------------------------------------------------------------------
def zip_source(src_code):
    """Package inline source (str) as a Lambda deployment ZIP (handler file index.py)."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("index.py", src_code)
    buf.seek(0)
    return buf.read()


def ensure_lambda_role(role_name, extra_statements):
    """Create/refresh a Lambda execution role with basic logs + the given extra statements."""
    trust = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"},
                       "Action": "sts:AssumeRole"}],
    }
    perms = {"Version": "2012-10-17", "Statement": extra_statements}
    try:
        arn = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust))["Role"]["Arn"]
        iam.attach_role_policy(RoleName=role_name,
                               PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
        iam.put_role_policy(RoleName=role_name, PolicyName="Access", PolicyDocument=json.dumps(perms))
        print(f"OK Created lambda role {role_name}")
        time.sleep(10)
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=role_name)["Role"]["Arn"]
        iam.put_role_policy(RoleName=role_name, PolicyName="Access", PolicyDocument=json.dumps(perms))
        print(f"OK Refreshed lambda role {role_name}")
        time.sleep(5)
    return arn


def deploy_lambda(name, src_code, role_arn, handler="index.lambda_handler",
                  timeout=120, memory=256, env=None):
    """Create or update a Lambda from inline source; returns its ARN."""
    zip_bytes = zip_source(src_code)
    try:
        resp = lambda_client.create_function(
            FunctionName=name, Runtime="python3.12", Role=role_arn, Handler=handler,
            Code={"ZipFile": zip_bytes}, Timeout=timeout, MemorySize=memory,
            Environment={"Variables": env or {}},
        )
        print(f"OK Created lambda {name}")
        return resp["FunctionArn"]
    except lambda_client.exceptions.ResourceConflictException:
        lambda_client.update_function_code(FunctionName=name, ZipFile=zip_bytes)
        # wait for code update, then push config (env/timeout)
        time.sleep(3)
        lambda_client.update_function_configuration(
            FunctionName=name, Timeout=timeout, MemorySize=memory,
            Environment={"Variables": env or {}},
        )
        arn = lambda_client.get_function(FunctionName=name)["Configuration"]["FunctionArn"]
        print(f"OK Updated lambda {name}")
        return arn


def new_session_id():
    """A runtimeSessionId must be >= 33 chars; a UUID (36) satisfies this."""
    return str(uuid.uuid4())
