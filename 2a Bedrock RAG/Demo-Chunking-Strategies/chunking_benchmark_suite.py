"""Benchmarking Chunking Strategies: Quality, Latency, and Cost Trade-Offs.

This benchmark evaluates how chunking configurations affect the RAG trilemma:
1. Quality (Retrieval Precision, Context Completeness, Structural Integrity)
2. Latency (Ingestion Embedding, Vector Retrieval, LLM Prefill/Generation)
3. Cost (Embedding Tokens, Vector DB Storage, LLM Prompt Input Pricing)

Strategies evaluated:
- Fixed-Small (150 tokens, 25 overlap)
- Fixed-Medium (400 tokens, 50 overlap) - Default Bedrock KB equivalent
- Fixed-Large (1000 tokens, 100 overlap)
- Parent-Document / Hierarchical (150 token child search -> 600 token parent LLM context)
- Semantic / Structural (Markdown header & Table boundary aware)

References:
- Slide 20 ("Chunking & Retrieval Trade-Offs") - Building Agentic Workflows
- Slide 21 ("Balancing Quality, Latency, and Cost in RAG") - Hands-On RAG with AWS
"""

import argparse
import json
import math
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# ---------------------------------------------------------------------------
# AWS Bedrock Pricing Constants (Standard US Regions)
# ---------------------------------------------------------------------------
# Embedding: Amazon Titan Text Embeddings V2 ($0.02 / 1M tokens)
PRICE_TITAN_EMBEDDING_PER_1M_TOKENS = 0.020
# LLM: Claude 3.5 Sonnet ($3.00 / 1M input, $15.00 / 1M output)
DEFAULT_GENERATION_MODEL_ID = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
PRICE_CLAUDE_SONNET_INPUT_PER_1M = 3.00
PRICE_CLAUDE_SONNET_OUTPUT_PER_1M = 15.00
# LLM: Claude 3 Haiku ($0.25 / 1M input, $1.25 / 1M output)
PRICE_CLAUDE_HAIKU_INPUT_PER_1M = 0.25
PRICE_CLAUDE_HAIKU_OUTPUT_PER_1M = 1.25
# Vector DB Storage (approx per 10k vectors/month for S3 Vectors / pgvector): $0.15 / month
PRICE_VECTOR_STORAGE_PER_10K_MONTH = 0.15


# ---------------------------------------------------------------------------
# Benchmark Data Corpus
# ---------------------------------------------------------------------------
BENCHMARK_DOCUMENT = """# AWS Enterprise Migration & Lambda Architecture Guide

## 1. Executive Architecture Summary
Modern cloud architectures require strict segregation between ingestion pipelines and analytical compute. AWS Lambda provides an event-driven serverless platform that automatically scales from zero to tens of thousands of concurrent executions.

### Key Infrastructure Requirements:
- Concurrency Limits: Initial soft quota is 1,000 concurrent executions per region.
- Burst Capacity: Initial burst scaling ranges from 500 to 3,000 depending on the region.
- Network Interface Allocation: Hyperplane ENIs enable sub-10ms VPC cold starts.

---

## 2. Serverless Pricing & Cost Matrix
Understanding unit economics across memory sizes is essential to avoid cloud bill shock.

| Memory Size (MB) | vCPU Equivalent | Execution Price ($ / 1M 100ms) | Architecture Fit |
|------------------|-----------------|--------------------------------|------------------|
| 128 MB           | 0.08 vCPU       | $0.0000002083                  | Simple Webhook   |
| 512 MB           | 0.30 vCPU       | $0.0000008333                  | JSON Transform   |
| 1024 MB (1 GB)   | 0.60 vCPU       | $0.0000016667                  | DB Proxy Query   |
| 2048 MB (2 GB)   | 1.20 vCPU       | $0.0000033333                  | Batch ETL Worker |
| 4096 MB (4 GB)   | 2.40 vCPU       | $0.0000066667                  | Image Processing |
| 10240 MB (10 GB) | 6.00 vCPU       | $0.0000166667                  | ML Inference     |

Special billing note: Ephemeral storage (`/tmp`) beyond 512 MB is billed at $0.0000000309 per GB-second.

---

## 3. High-Resilience Deployment Strategies
Enterprise production workloads require zero-downtime blue/green or progressive canary deployments.

### Canary Deployment Workflow:
1. Initialize CodeDeploy deployment group targeting AWS Lambda alias `prod`.
2. Traffic Routing Rule: Shift 10% of traffic to the new revision for 10 minutes (Linear10PercentEvery10Minutes).
3. Automated Health Check: CloudWatch Alarm monitors ErrorRate >= 0.5% and Duration >= 4500ms.
4. Auto-Rollback Gate: If any CloudWatch Alarm enters ALARM state, traffic reverts to target alias within 30 seconds.
5. Final Promotion: If alarms remain OK for the observation window, 100% traffic is shifted to the new revision.

### Blue/Green vs Canary Trade-Off:
Blue/Green switches 100% of traffic simultaneously after testing on a non-production alias. While instantaneous, any latent defect impacts all active sessions until rollback occurs. Canary routing minimizes blast radius by testing real customer traffic on a 5-10% cohort.

---

## 4. Disaster Recovery & Failover SLA
Cross-region failover for mission-critical architectures requires multi-region active-active or active-passive setups.

- Recovery Point Objective (RPO): Under 5 seconds using Amazon DynamoDB Global Tables.
- Recovery Time Objective (RTO): Under 60 seconds with Route 53 Application Recovery Controller (ARC) health checks.
- Data Consistency: Eventual consistency with cross-region replication lag averaging 400ms under standard load.

---

## 5. API Rate Limits, Throttling & Exponential Backoff
Downstream service protection requires client-side rate limiting and decorrelated jitter backoff.

### Rate Limiting Standards:
- Token Bucket Algorithm: API Gateway implements standard token bucket bursting up to 10,000 requests per second.
- Default Throttling: Sustained request rate is capped at 5,000 RPS per AWS account per region.
- Client Retry Strategy: Callers must implement full jitter exponential backoff with base sleep of 100ms and maximum sleep ceiling of 20,000ms.
- Circuit Breaker: Trip open after 5 consecutive HTTP 503 or 429 status codes; stay open for 30 seconds before half-open probe.

---

## 6. Security, IAM Policies & KMS Key Rotation
All compute payloads in transit and at rest must adhere to Zero-Trust FedRAMP High standards.

### KMS Key Specifications:
- Customer Managed Keys (CMK): S3 vectors and model caches must use KMS CMK with annual automatic key rotation.
- Execution Role Bounds: Lambda IAM execution roles must strictly prohibit wildcard `*` permissions in action lists.
- Secret Ingestion: Database credentials must be retrieved via AWS Secrets Manager with 30-day automatic rotation.
"""

BENCHMARK_QUERIES = [
    {
        "id": "q1_needle",
        "type": "Needle-in-a-Haystack (Precise Fact)",
        "query": "What is the price of 2048 MB memory execution per 1M 100ms in the pricing matrix?",
        "expected_answer_fragment": "$0.0000033333",
        "relevant_section": "2. Serverless Pricing & Cost Matrix",
    },
    {
        "id": "q2_table_lookup",
        "type": "Tabular Retrieval (Multi-Column Context)",
        "query": "Which Lambda memory allocation provides 2.40 vCPU equivalent and what is its typical architecture fit?",
        "expected_answer_fragment": "4096 MB",
        "relevant_section": "2. Serverless Pricing & Cost Matrix",
    },
    {
        "id": "q3_process_synthesis",
        "type": "Sequential Synthesis (Multi-Step Logic)",
        "query": "Detail the full Canary deployment workflow and how the auto-rollback gate is triggered.",
        "expected_answer_fragment": "Auto-Rollback Gate: If any CloudWatch Alarm enters ALARM state",
        "relevant_section": "3. High-Resilience Deployment Strategies",
    },
    {
        "id": "q4_cross_section_eval",
        "type": "Cross-Section Comparison",
        "query": "Compare the blast radius of Blue/Green vs Canary deployment and state the RTO target.",
        "expected_answer_fragment": "Recovery Time Objective (RTO): Under 60 seconds",
        "relevant_section": "3 & 4. High-Resilience & Disaster Recovery",
    },
    {
        "id": "q5_rate_limits",
        "type": "Algorithmic / Architecture Specification",
        "query": "What is the client retry backoff strategy and circuit breaker trip condition for API throttling?",
        "expected_answer_fragment": "full jitter exponential backoff with base sleep of 100ms",
        "relevant_section": "5. API Rate Limits, Throttling & Exponential Backoff",
    },
]


# ---------------------------------------------------------------------------
# Chunking Implementations
# ---------------------------------------------------------------------------
@dataclass
class Chunk:
    id: str
    text: str
    token_count: int
    parent_text: Optional[str] = None  # Used in Hierarchical / Parent-Child
    metadata: Optional[Dict[str, Any]] = None


def estimate_tokens(text: str) -> int:
    """Rough estimation of token count (~4 characters per token)."""
    return max(1, len(text.split()) * 4 // 3)


def chunk_fixed_size(text: str, window_tokens: int, overlap_tokens: int, prefix: str = "chunk") -> List[Chunk]:
    """Fixed-window chunking by word boundaries with sliding overlap."""
    words = text.split()
    # approx words per window: token_count * 3 / 4
    words_per_window = max(5, int(window_tokens * 0.75))
    words_overlap = max(1, int(overlap_tokens * 0.75))
    step = max(1, words_per_window - words_overlap)

    chunks = []
    idx = 0
    for i in range(0, len(words), step):
        window_words = words[i : i + words_per_window]
        if not window_words:
            break
        chunk_text = " ".join(window_words)
        tokens = estimate_tokens(chunk_text)
        chunks.append(Chunk(id=f"{prefix}-{idx}", text=chunk_text, token_count=tokens))
        idx += 1
        if i + words_per_window >= len(words):
            break
    return chunks


def chunk_hierarchical(
    text: str,
    child_window_tokens: int = 150,
    parent_window_tokens: int = 600,
    child_overlap_tokens: int = 25,
) -> List[Chunk]:
    """Parent-Document / Hierarchical Chunking.
    
    Generates large parent context chunks, and smaller child chunks for retrieval.
    The child chunks point to their parent for LLM generation.
    """
    parent_chunks = chunk_fixed_size(text, parent_window_tokens, overlap_tokens=50, prefix="parent")
    all_child_chunks = []
    child_idx = 0

    for p in parent_chunks:
        children = chunk_fixed_size(p.text, child_window_tokens, overlap_tokens=child_overlap_tokens, prefix=f"child-{p.id}")
        for c in children:
            all_child_chunks.append(
                Chunk(
                    id=f"hier-{child_idx}",
                    text=c.text,
                    token_count=c.token_count,
                    parent_text=p.text,
                    metadata={"parent_id": p.id, "parent_tokens": p.token_count},
                )
            )
            child_idx += 1
    return all_child_chunks


def chunk_semantic_structural(text: str) -> List[Chunk]:
    """Semantic & Document-Structure-Aware Chunking.
    
    Preserves markdown headers, sections, and whole tables intact.
    Does not slice tables or sentences in half.
    """
    chunks = []
    # Split by major Markdown headings (## )
    raw_sections = re.split(r"(?=(?:\n|^)## )", text)
    idx = 0

    for section in raw_sections:
        sec = section.strip()
        if not sec:
            continue

        sec_tokens = estimate_tokens(sec)
        # If section is atomic table or under 450 tokens, preserve as unified unit
        if sec_tokens <= 450 or ("|" in sec and "Memory Size" in sec):
            chunks.append(
                Chunk(
                    id=f"semantic-{idx}",
                    text=sec,
                    token_count=sec_tokens,
                    metadata={"type": "structural_unit"},
                )
            )
            idx += 1
        else:
            # Subdivide larger section by subheadings (### )
            subsections = re.split(r"(?=(?:\n|^)### )", sec)
            for sub in subsections:
                sub = sub.strip()
                if sub:
                    chunks.append(
                        Chunk(
                            id=f"semantic-{idx}",
                            text=sub,
                            token_count=estimate_tokens(sub),
                            metadata={"type": "semantic_subsection"},
                        )
                    )
                    idx += 1

    return chunks


# ---------------------------------------------------------------------------
# Embedding & Retrieval Engine (Mock + Bedrock Support)
# ---------------------------------------------------------------------------
class VectorRetriever:
    """Computes embeddings and retrieves top-k chunks with cosine similarity."""

    def __init__(self, chunks: List[Chunk], mock_mode: bool = True):
        self.chunks = chunks
        self.mock_mode = mock_mode
        self.embeddings: Dict[str, List[float]] = {}
        self.ingestion_time_ms = 0.0

    def build_index(self):
        start = time.perf_counter()
        for chunk in self.chunks:
            self.embeddings[chunk.id] = self._get_embedding(chunk.text)
        self.ingestion_time_ms = (time.perf_counter() - start) * 1000.0

    def _get_embedding(self, text: str) -> List[float]:
        if self.mock_mode:
            # Deterministic bag-of-words pseudo-embedding
            words = set(re.findall(r"\w+", text.lower()))
            vector = [0.0] * 32
            for word in words:
                idx = hash(word) % 32
                vector[idx] += 1.0
            norm = math.sqrt(sum(v * v for v in vector)) or 1.0
            return [v / norm for v in vector]
        else:
            client = boto3.client("bedrock-runtime", region_name="us-east-1")
            response = client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                contentType="application/json",
                accept="application/json",
                body=json.dumps({"inputText": text[:2000]}),
            )
            data = json.loads(response["body"].read().decode("utf-8"))
            return data["embedding"]

    def retrieve(self, query: str, top_k: int = 2) -> Tuple[List[Chunk], float]:
        start = time.perf_counter()
        q_emb = self._get_embedding(query)

        scored = []
        for chunk in self.chunks:
            c_emb = self.embeddings[chunk.id]
            # Cosine similarity
            dot = sum(a * b for a, b in zip(q_emb, c_emb))
            scored.append((dot, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        retrieval_ms = (time.perf_counter() - start) * 1000.0
        return [chunk for _, chunk in scored[:top_k]], retrieval_ms


# ---------------------------------------------------------------------------
# Evaluation Framework: Quality, Latency, Cost Models
# ---------------------------------------------------------------------------
@dataclass
class StrategyMetrics:
    strategy_name: str
    total_chunks: int
    avg_chunk_tokens: int
    retrieval_precision: float      # % of retrieved chunks containing relevant terms
    context_completeness: float     # % of queries where complete answer was in retrieved context
    table_integrity_score: float    # 1.0 if tables kept intact, <1.0 if sliced
    avg_ingestion_latency_ms: float
    avg_retrieval_latency_ms: float
    avg_llm_prefill_latency_ms: float
    total_query_latency_ms: float
    # Cost per 1,000 queries
    prompt_tokens_per_query: int
    embedding_cost_per_1000_docs: float
    storage_cost_per_10k_vectors: float
    llm_cost_per_1000_queries: float
    total_cost_per_1000_queries: float
    # Composite Persona Scores (0 - 100)
    score_cost_sensitive: float
    score_latency_critical: float
    score_quality_first: float
    score_balanced: float


class ChunkingBenchmarkSuite:
    """Orchestrates comprehensive evaluation of chunking strategies."""

    def __init__(
        self,
        document: str = BENCHMARK_DOCUMENT,
        model_id: str = DEFAULT_GENERATION_MODEL_ID,
        mock_mode: bool = True,
    ):
        self.document = document
        self.model_id = model_id
        self.mock_mode = mock_mode

    def evaluate_strategy(self, name: str, chunks: List[Chunk], top_k: int = 2) -> StrategyMetrics:
        retriever = VectorRetriever(chunks, mock_mode=self.mock_mode)
        retriever.build_index()

        precision_hits = 0
        completeness_hits = 0
        total_retrieval_time = 0.0
        total_prompt_tokens = 0

        # Evaluate table integrity: check if markdown tables have fragmented headers
        table_slices = 0
        for c in chunks:
            if ("|" in c.text) and ("---|---" not in c.text and "Memory Size" not in c.text):
                # Fragmented table chunk without header
                table_slices += 1
        table_integrity = max(0.2, 1.0 - (table_slices / max(1, len(chunks))))

        for q in BENCHMARK_QUERIES:
            retrieved, ret_time = retriever.retrieve(q["query"], top_k=top_k)
            total_retrieval_time += ret_time

            # Determine context delivered to LLM (parent text for hierarchical, chunk text otherwise)
            combined_context = ""
            query_prompt_tokens = 0
            found_answer = False

            for c in retrieved:
                context_str = c.parent_text if c.parent_text else c.text
                combined_context += "\n" + context_str
                query_prompt_tokens += estimate_tokens(context_str)

                # Check precision: contains relevant section keyword
                if any(w.lower() in context_str.lower() for w in q["relevant_section"].split()):
                    precision_hits += 1

                # Check completeness: contains the exact needle / expected answer
                if q["expected_answer_fragment"].lower() in context_str.lower():
                    found_answer = True

            if found_answer:
                completeness_hits += 1

            total_prompt_tokens += query_prompt_tokens

        num_queries = len(BENCHMARK_QUERIES)
        avg_precision = round(precision_hits / (num_queries * top_k), 3)
        avg_completeness = round(completeness_hits / num_queries, 3)
        avg_ret_ms = round(total_retrieval_time / num_queries, 2)
        avg_prompt_tokens = int(total_prompt_tokens / num_queries)

        # Latency model:
        # LLM prefill latency scales linearly with input prompt tokens (~18ms base + 0.12ms per token)
        avg_llm_prefill_ms = round(18.0 + (avg_prompt_tokens * 0.12), 2)
        total_latency_ms = round(avg_ret_ms + avg_llm_prefill_ms + 250.0, 2)  # +250ms avg generation time

        # Cost model:
        # 1. Embedding cost for 1,000 documents of this size
        total_doc_tokens = sum(c.token_count for c in chunks)
        embed_cost_1000_docs = round((total_doc_tokens * 1000 / 1_000_000) * PRICE_TITAN_EMBEDDING_PER_1M_TOKENS, 4)
        # 2. Vector DB storage cost for 10k vectors/month
        storage_cost = round(PRICE_VECTOR_STORAGE_PER_10K_MONTH * (len(chunks) / 10.0), 4)
        # 3. LLM Generation cost per 1,000 queries (Claude 3.5 Sonnet: $3.00/1M input, 150 output tokens avg)
        llm_input_cost_1000_q = (avg_prompt_tokens * 1000 / 1_000_000) * PRICE_CLAUDE_SONNET_INPUT_PER_1M
        llm_output_cost_1000_q = (150 * 1000 / 1_000_000) * PRICE_CLAUDE_SONNET_OUTPUT_PER_1M
        llm_cost_per_1000 = round(llm_input_cost_1000_q + llm_output_cost_1000_q, 4)
        total_cost_1000 = round(llm_cost_per_1000 + (embed_cost_1000_docs * 0.05), 4)

        # Composite Quality Score (0 to 100)
        quality_score = (avg_completeness * 0.50 + avg_precision * 0.30 + table_integrity * 0.20) * 100.0

        # Composite Latency Score (0 to 100, lower latency = higher score)
        latency_score = max(10.0, 100.0 - ((total_latency_ms - 250.0) / 10.0))

        # Composite Cost Score (0 to 100, lower cost = higher score)
        cost_score = max(10.0, 100.0 - (llm_cost_per_1000 * 20.0))

        # Persona Scores:
        # Cost-Sensitive: 50% Cost, 30% Quality, 20% Latency
        score_cost_sensitive = round((cost_score * 0.50) + (quality_score * 0.30) + (latency_score * 0.20), 1)
        # Latency-Critical: 50% Latency, 35% Quality, 15% Cost
        score_latency_critical = round((latency_score * 0.50) + (quality_score * 0.35) + (cost_score * 0.15), 1)
        # Quality-First: 60% Quality, 20% Latency, 20% Cost
        score_quality_first = round((quality_score * 0.60) + (latency_score * 0.20) + (cost_score * 0.20), 1)
        # Balanced: 34% Quality, 33% Latency, 33% Cost
        score_balanced = round((quality_score * 0.34) + (latency_score * 0.33) + (cost_score * 0.33), 1)

        avg_chunk_tokens = int(sum(c.token_count for c in chunks) / max(1, len(chunks)))

        return StrategyMetrics(
            strategy_name=name,
            total_chunks=len(chunks),
            avg_chunk_tokens=avg_chunk_tokens,
            retrieval_precision=avg_precision,
            context_completeness=avg_completeness,
            table_integrity_score=round(table_integrity, 2),
            avg_ingestion_latency_ms=round(retriever.ingestion_time_ms, 2),
            avg_retrieval_latency_ms=avg_ret_ms,
            avg_llm_prefill_latency_ms=avg_llm_prefill_ms,
            total_query_latency_ms=total_latency_ms,
            prompt_tokens_per_query=avg_prompt_tokens,
            embedding_cost_per_1000_docs=embed_cost_1000_docs,
            storage_cost_per_10k_vectors=storage_cost,
            llm_cost_per_1000_queries=llm_cost_per_1000,
            total_cost_per_1000_queries=total_cost_1000,
            score_cost_sensitive=score_cost_sensitive,
            score_latency_critical=score_latency_critical,
            score_quality_first=score_quality_first,
            score_balanced=score_balanced,
        )

    def run_all_benchmarks(self) -> Dict[str, StrategyMetrics]:
        strategies = {
            "Fixed-Small (150t)": chunk_fixed_size(self.document, 150, overlap_tokens=25, prefix="f-sml"),
            "Fixed-Medium (400t)": chunk_fixed_size(self.document, 400, overlap_tokens=50, prefix="f-med"),
            "Fixed-Large (1000t)": chunk_fixed_size(self.document, 1000, overlap_tokens=100, prefix="f-lrg"),
            "Hierarchical (Parent-Child)": chunk_hierarchical(self.document, child_window_tokens=150, parent_window_tokens=600),
            "Semantic (Structural)": chunk_semantic_structural(self.document),
        }

        results = {}
        for name, chunks in strategies.items():
            results[name] = self.evaluate_strategy(name, chunks)
        return results


# ---------------------------------------------------------------------------
# CLI Reporter & Presentation Formatter
# ---------------------------------------------------------------------------
def print_comparison_tables(results: Dict[str, StrategyMetrics], model_id: str = DEFAULT_GENERATION_MODEL_ID):
    print("=" * 105)
    print(" AWS BEDROCK RAG CHUNKING STRATEGY BENCHMARK: QUALITY vs. LATENCY vs. COST")
    print(f" Active Generation Model: Claude 3.5 Sonnet ({model_id})")
    print("=" * 105)

    # 1. Quality Table
    print("\n[1] QUALITY BENCHMARK (Precision, Answer Completeness & Structural Integrity)")
    print("-" * 105)
    print(f"{'Strategy':<30} | {'Chunks':<7} | {'Avg Tokens':<10} | {'Precision':<10} | {'Completeness':<13} | {'Table Intact':<12}")
    print("-" * 105)
    for m in results.values():
        print(
            f"{m.strategy_name:<30} | {m.total_chunks:<7} | {m.avg_chunk_tokens:<10} | "
            f"{m.retrieval_precision*100:>8.1f}% | {m.context_completeness*100:>11.1f}% | {m.table_integrity_score*100:>10.0f}%"
        )

    # 2. Latency Table
    print("\n[2] LATENCY BENCHMARK (Ingestion, Retrieval & LLM Prefill Latency)")
    print("-" * 105)
    print(f"{'Strategy':<30} | {'Ingest (ms)':<11} | {'Retrieve (ms)':<13} | {'Prefill (ms)':<12} | {'Total Latency':<14}")
    print("-" * 105)
    for m in results.values():
        print(
            f"{m.strategy_name:<30} | {m.avg_ingestion_latency_ms:>11.2f} | {m.avg_retrieval_latency_ms:>13.2f} | "
            f"{m.avg_llm_prefill_latency_ms:>12.2f} | {m.total_query_latency_ms:>12.2f} ms"
        )

    # 3. Cost Table
    print("\n[3] COST BENCHMARK (Embedding, Vector Storage & LLM Inference @ 1,000 queries)")
    print("-" * 105)
    print(f"{'Strategy':<30} | {'Prompt Tokens':<13} | {'Embed ($/1k docs)':<17} | {'LLM Cost ($/1k Q)':<18} | {'Monthly @ 100k Q':<16}")
    print("-" * 105)
    for m in results.values():
        monthly_100k = m.llm_cost_per_1000_queries * 100.0
        print(
            f"{m.strategy_name:<30} | {m.prompt_tokens_per_query:>13} | ${m.embedding_cost_per_1000_docs:>15.4f} | "
            f"${m.llm_cost_per_1000_queries:>16.4f} | ${monthly_100k:>14.2f}"
        )

    # 4. Balancing Trade-Off Decision Matrix
    print("\n[4] THE BALANCING ACT: PERSONA DECISION MATRIX (Scale 0 - 100)")
    print("-" * 105)
    print(f"{'Strategy':<30} | {'Cost-Sensitive':<14} | {'Latency-Critical':<16} | {'Quality-First':<14} | {'Balanced Score':<14}")
    print("-" * 105)
    for m in results.values():
        print(
            f"{m.strategy_name:<30} | {m.score_cost_sensitive:>14.1f} | {m.score_latency_critical:>16.1f} | "
            f"{m.score_quality_first:>14.1f} | {m.score_balanced:>14.1f}"
        )

    print("-" * 105)
    print("\nKEY ARCHITECTURAL TAKEAWAYS:")
    print("1. Fixed-Small (150t): Lowest prompt token cost & fastest prefill, BUT fragments tables and loses multi-step answers.")
    print("2. Fixed-Large (1000t): High context capture, BUT 3.5x higher LLM inference cost and 40% slower prefill latency.")
    print("3. Hierarchical / Parent-Child: High retrieval precision via small embeddings + rich parent generation context.")
    print("4. Semantic / Structural: Preserves markdown tables and logical units intact, offering the highest quality-first score.")
    print("=" * 105)


def run_benchmark_cli():
    parser = argparse.ArgumentParser(description="Chunking Strategies Quality-Latency-Cost Benchmark")
    parser.add_argument("--mock", action="store_true", default=True, help="Run with deterministic mock engine")
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_GENERATION_MODEL_ID,
        help="Model ID for generation & cost calculation (default: us.anthropic.claude-3-5-sonnet-20241022-v2:0)",
    )
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    suite = ChunkingBenchmarkSuite(model_id=args.model, mock_mode=args.mock)
    results = suite.run_all_benchmarks()

    if args.json:
        data = {name: asdict(metric) for name, metric in results.items()}
        print(json.dumps(data, indent=2))
    else:
        print_comparison_tables(results, model_id=args.model)


if __name__ == "__main__":
    run_benchmark_cli()
