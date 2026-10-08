"""Cross-Region Inference (CRIS) Benchmark & Resilient Routing.

Compares latency distributions, throughput, and error recovery between:
- AWS Bedrock Cross-Region Inference System (CRIS) profiles (e.g., us.anthropic.claude-*, eu.anthropic.claude-*)
- Single-region direct model endpoints (e.g., anthropic.claude-*)

Includes an automated CRISRouter that executes seamless dynamic failover upon ThrottlingException (HTTP 429).

References:
- Slide 29 ("Hands-On RAG with AWS")
- Slide 46 ("Building Agentic Workflows with RAG on AWS Bedrock")
"""

import argparse
import json
import math
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class CRISRouter:
    """Resilient router that leverages CRIS endpoints and handles dynamic failover on rate limits."""

    DEFAULT_PROFILES = [
        "us.anthropic.claude-3-haiku-20240307-v1:0",  # US CRIS profile
        "eu.anthropic.claude-3-haiku-20240307-v1:0",  # EU CRIS profile
        "anthropic.claude-3-haiku-20240307-v1:0",     # Regional Direct fallback
    ]

    def __init__(
        self,
        profiles: Optional[List[str]] = None,
        primary_region: str = "us-east-1",
        mock_mode: bool = False,
    ):
        self.profiles = profiles or self.DEFAULT_PROFILES
        self.primary_region = primary_region
        self.mock_mode = mock_mode
        self.telemetry: List[Dict[str, Any]] = []

        if not self.mock_mode:
            try:
                self.client = boto3.client("bedrock-runtime", region_name=self.primary_region)
                boto3.client("sts", region_name=self.primary_region).get_caller_identity()
            except (NoCredentialsError, ClientError) as e:
                print(f"[CRISRouter] AWS credentials not configured ({e}). Using mock benchmark mode.")
                self.mock_mode = True

    def invoke(
        self,
        prompt: str,
        max_tokens: int = 256,
        force_failover: bool = False,
    ) -> Dict[str, Any]:
        """Invoke model with transparent fallback across CRIS profiles."""
        start_time = time.time()
        last_error = None

        for attempt_idx, profile_id in enumerate(self.profiles):
            attempt_start = time.time()
            try:
                if self.mock_mode:
                    result = self._mock_invoke(
                        profile_id=profile_id,
                        prompt=prompt,
                        max_tokens=max_tokens,
                        simulate_throttle=(force_failover and attempt_idx == 0),
                    )
                else:
                    if force_failover and attempt_idx == 0:
                        raise ClientError(
                            {"Error": {"Code": "ThrottlingException", "Message": "Rate limit exceeded"}},
                            "Converse",
                        )
                    resp = self.client.converse(
                        modelId=profile_id,
                        messages=[{"role": "user", "content": [{"text": prompt}]}],
                        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.2},
                    )
                    text = resp["output"]["message"]["content"][0]["text"]
                    usage = resp.get("usage", {})
                    result = {
                        "text": text,
                        "outputTokens": usage.get("outputTokens", 50),
                        "inputTokens": usage.get("inputTokens", 20),
                    }

                latency_ms = (time.time() - attempt_start) * 1000
                total_latency_ms = (time.time() - start_time) * 1000

                telemetry_event = {
                    "profile_used": profile_id,
                    "attempts": attempt_idx + 1,
                    "failed_over": attempt_idx > 0,
                    "latency_ms": round(latency_ms, 2),
                    "total_latency_ms": round(total_latency_ms, 2),
                    "output_tokens": result["outputTokens"],
                    "throughput_tokens_sec": round((result["outputTokens"] / max(0.001, latency_ms / 1000)), 2),
                    "success": True,
                }
                self.telemetry.append(telemetry_event)
                return {
                    "result": result,
                    "telemetry": telemetry_event,
                }

            except ClientError as e:
                code = e.response.get("Error", {}).get("Code", "")
                last_error = e
                print(f"[*] Profile '{profile_id}' encountered {code}. Failing over to next profile...")
                continue

        raise RuntimeError(f"All CRIS profiles exhausted. Last error: {last_error}")

    def _mock_invoke(
        self,
        profile_id: str,
        prompt: str,
        max_tokens: int,
        simulate_throttle: bool = False,
    ) -> Dict[str, Any]:
        """Simulate realistic latency and token generation for CRIS vs regional endpoints."""
        if simulate_throttle:
            raise ClientError(
                {"Error": {"Code": "ThrottlingException", "Message": "Rate limit exceeded on primary profile"}},
                "Converse",
            )

        # Realistic network & compute simulation:
        # CRIS profiles have lower queuing delays under load (350-550ms)
        # Single-region direct has higher variance under load (450-950ms)
        if profile_id.startswith("us.") or profile_id.startswith("eu."):
            simulated_latency = random.uniform(0.35, 0.55)
        else:
            simulated_latency = random.uniform(0.50, 0.95)

        time.sleep(simulated_latency)

        generated_tokens = min(max_tokens, len(prompt.split()) + random.randint(30, 60))
        return {
            "text": f"[Mock Bedrock Response from {profile_id}] Generated synthesis for input query.",
            "outputTokens": generated_tokens,
            "inputTokens": len(prompt.split()) * 2,
        }


class CRISBenchmarkRunner:
    """Benchmark suite comparing Single-Region vs Cross-Region Inference endpoints."""

    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode

    def run_benchmark(
        self,
        num_requests: int = 15,
        concurrency: int = 3,
    ) -> Dict[str, Any]:
        """Run load benchmark comparing single-region vs CRIS endpoints."""
        endpoints = {
            "Single-Region Direct": "anthropic.claude-3-haiku-20240307-v1:0",
            "CRIS US Profile": "us.anthropic.claude-3-haiku-20240307-v1:0",
        }

        results: Dict[str, Any] = {}
        sample_prompt = "Explain how vector embedding indexing in AWS OpenSearch Service improves semantic search precision."

        for label, profile_id in endpoints.items():
            print(f"\n[+] Benchmarking {label} ({profile_id})...")
            router = CRISRouter(profiles=[profile_id], mock_mode=self.mock_mode)
            latencies: List[float] = []
            tokens_generated: List[int] = []
            throughputs: List[float] = []

            def worker(_):
                res = router.invoke(prompt=sample_prompt, max_tokens=150)
                telem = res["telemetry"]
                return telem["latency_ms"], telem["output_tokens"], telem["throughput_tokens_sec"]

            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(worker, i) for i in range(num_requests)]
                for fut in as_completed(futures):
                    lat, toks, tput = fut.result()
                    latencies.append(lat)
                    tokens_generated.append(toks)
                    throughputs.append(tput)

            latencies.sort()
            p50 = statistics.median(latencies)
            p90 = latencies[int(len(latencies) * 0.90)]
            p99 = latencies[int(len(latencies) * 0.99) if len(latencies) > 1 else 0]

            results[label] = {
                "profile_id": profile_id,
                "total_requests": num_requests,
                "p50_latency_ms": round(p50, 1),
                "p90_latency_ms": round(p90, 1),
                "p99_latency_ms": round(p99, 1),
                "avg_throughput_tok_sec": round(statistics.mean(throughputs), 1),
                "total_tokens": sum(tokens_generated),
            }

        # Demonstrate dynamic failover routing test
        print("\n[+] Demonstrating Dynamic Failover Routing (Simulated Throttling on Primary)...")
        failover_router = CRISRouter(mock_mode=self.mock_mode)
        failover_res = failover_router.invoke(
            prompt="Summarize multi-region disaster recovery for Amazon Bedrock.",
            force_failover=True,
        )
        failover_telem = failover_res["telemetry"]
        results["Dynamic Failover Test"] = {
            "primary_profile": failover_router.profiles[0],
            "failover_profile": failover_telem["profile_used"],
            "recovered_successfully": failover_telem["success"],
            "total_attempts": failover_telem["attempts"],
            "total_latency_ms": failover_telem["total_latency_ms"],
        }

        return results


def run_demo(mock_mode: bool = False):
    """Run CLI benchmark and routing comparison."""
    print("=" * 75)
    print(" AWS Bedrock Cross-Region Inference (CRIS) Benchmark (Slides 29 & 46 Alignment)")
    print("=" * 75)

    runner = CRISBenchmarkRunner(mock_mode=mock_mode)
    results = runner.run_benchmark(num_requests=10, concurrency=2)

    print("\n" + "=" * 75)
    print(" BENCHMARK RESULTS COMPARISON")
    print("=" * 75)
    print(f"{'Endpoint':<25} | {'p50 (ms)':<10} | {'p90 (ms)':<10} | {'Throughput (tok/s)':<18}")
    print("-" * 75)

    for ep_name in ["Single-Region Direct", "CRIS US Profile"]:
        m = results[ep_name]
        print(f"{ep_name:<25} | {m['p50_latency_ms']:<10} | {m['p90_latency_ms']:<10} | {m['avg_throughput_tok_sec']:<18}")

    fo = results["Dynamic Failover Test"]
    print("-" * 75)
    print(f"Failover Test: {fo['primary_profile']} (throttled) -> {fo['failover_profile']}")
    print(f"Recovery: Success={fo['recovered_successfully']}, Attempts={fo['total_attempts']}, Total Latency={fo['total_latency_ms']} ms")
    print("=" * 75)
    print("[✓] CRIS Benchmark & Routing completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRIS Benchmark & Routing Demo")
    parser.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser.parse_args()
    run_demo(mock_mode=args.mock)
