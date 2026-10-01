"""
research_org.py — Invoke the org-research AgentCore Harness and save a Markdown summary.

Reads the harness ARN from --harness-arn or the .harness_arn file written by
setup_research_agent.py. Streams the response to the terminal and saves it to
summaries/<org>.md.

Usage:
    python research_org.py --org "Anthropic" --region us-east-1
    python research_org.py --org "Hugging Face" --harness-arn arn:aws:bedrock-agentcore:...:harness/...
"""

import argparse
import os
import re
import sys
import uuid

import boto3

ARN_CACHE = ".harness_arn"
OUT_DIR = "summaries"


def load_harness_arn(explicit):
    if explicit:
        return explicit
    if os.path.exists(ARN_CACHE):
        with open(ARN_CACHE) as f:
            arn = f.read().strip()
            if arn:
                return arn
    sys.exit("ERROR: no harness ARN. Pass --harness-arn or run setup_research_agent.py first.")


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "org"


def research(org, region, harness_arn):
    client = boto3.client("bedrock-agentcore", region_name=region)

    # runtimeSessionId MUST be at least 33 chars; a UUID (36 w/ hyphens) satisfies this.
    session_id = str(uuid.uuid4())

    prompt = (
        f"Research the organization \"{org}\" and produce the structured Markdown summary "
        f"exactly as specified in your instructions."
    )

    print(f"Researching: {org}")
    print(f"Harness: {harness_arn}")
    print(f"Session: {session_id}")
    print("=" * 70)

    response = client.invoke_harness(
        harnessArn=harness_arn,
        runtimeSessionId=session_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )

    collected = []
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            text = delta.get("text")
            if text:
                print(text, end="", flush=True)
                collected.append(text)
            # Surface tool activity so you can see the agent searching the web.
            tool_use = delta.get("toolUse")
            if tool_use and tool_use.get("name"):
                print(f"\n[tool: {tool_use['name']}]", flush=True)
        elif "messageStop" in event:
            reason = event["messageStop"].get("stopReason")
            if reason and reason not in ("end_turn", "tool_use", "tool_result"):
                print(f"\n[stop reason: {reason}]", flush=True)
        elif "runtimeClientError" in event:
            print(f"\nERROR: {event['runtimeClientError'].get('message')}", flush=True)

    summary = "".join(collected).strip()
    if not summary:
        print("\n(no text returned)")
        return None

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{slugify(org)}.md")
    with open(path, "w") as f:
        f.write(summary + "\n")

    print("\n" + "=" * 70)
    print(f"Saved summary to: {path}")
    print("=" * 70)
    return path


def main():
    ap = argparse.ArgumentParser(description="Research an organization with the AgentCore Harness.")
    ap.add_argument("--org", required=True, help="Organization name to research")
    ap.add_argument("--region", default="us-east-1")
    ap.add_argument("--harness-arn", help="Harness ARN (defaults to .harness_arn cache)")
    args = ap.parse_args()

    harness_arn = load_harness_arn(args.harness_arn)
    research(args.org, args.region, harness_arn)


if __name__ == "__main__":
    main()
