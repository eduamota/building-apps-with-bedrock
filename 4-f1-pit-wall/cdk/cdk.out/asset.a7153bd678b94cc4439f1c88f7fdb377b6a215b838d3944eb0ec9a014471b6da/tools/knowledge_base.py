"""RAG tool — retrieves context from F1 knowledge base documents in S3."""

import json
import os
import boto3
from strands import tool

REGION = os.environ.get("BEDROCK_REGION", "us-west-2")
KB_BUCKET = os.environ.get("KB_BUCKET", "f1-pit-wall-kb-058264544288-us-west-2")
KB_ID = os.environ.get("KB_ID", "")

# If no KB configured, fall back to reading S3 directly
s3 = boto3.client("s3", region_name=REGION)

# Load all F1 docs into memory for simple retrieval
_DOCS_CACHE = None


def _load_docs():
    global _DOCS_CACHE
    if _DOCS_CACHE is not None:
        return _DOCS_CACHE

    _DOCS_CACHE = {}
    try:
        resp = s3.list_objects_v2(Bucket=KB_BUCKET, Prefix="f1-data/")
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".md"):
                body = s3.get_object(Bucket=KB_BUCKET, Key=key)["Body"].read().decode()
                name = key.split("/")[-1].replace(".md", "").replace("-", " ")
                _DOCS_CACHE[name] = body
    except Exception as e:
        # Fallback: load from local files if S3 not accessible
        import pathlib
        data_dir = pathlib.Path(__file__).parent.parent / "knowledge-base" / "data"
        if data_dir.exists():
            for f in data_dir.glob("*.md"):
                _DOCS_CACHE[f.stem.replace("-", " ")] = f.read_text()
    return _DOCS_CACHE


def _simple_search(query: str, top_k: int = 3) -> list:
    """Simple keyword-based retrieval from loaded docs."""
    docs = _load_docs()
    query_terms = set(query.lower().split())
    scored = []
    for name, content in docs.items():
        # Score by keyword overlap
        content_lower = content.lower()
        score = sum(1 for term in query_terms if term in content_lower)
        if score > 0:
            scored.append((score, name, content))
    scored.sort(reverse=True)
    return scored[:top_k]


@tool
def search_f1_knowledge(query: str) -> str:
    """Search the F1 knowledge base for information about Formula 1.
    Use this for questions about regulations, history, records, season data, teams, and drivers.

    Args:
        query: The search query about F1 topics
    """
    # Try Bedrock KB retrieve API first
    if KB_ID:
        try:
            client = boto3.client("bedrock-agent-runtime", region_name=REGION)
            resp = client.retrieve(
                knowledgeBaseId=KB_ID,
                retrievalQuery={"text": query},
                retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 3}},
            )
            results = []
            for r in resp.get("retrievalResults", []):
                text = r.get("content", {}).get("text", "")
                if text:
                    results.append(text)
            if results:
                return json.dumps({"source": "bedrock_kb", "results": results})
        except Exception:
            pass  # Fall through to simple search

    # Fallback: simple keyword search over loaded docs
    matches = _simple_search(query)
    if not matches:
        return json.dumps({"source": "local", "results": ["No relevant F1 information found for this query."]})

    results = []
    for score, name, content in matches:
        # Return relevant chunks (first 1500 chars of matching doc)
        results.append(f"[Source: {name}]\n{content[:1500]}")

    return json.dumps({"source": "local", "results": results})
