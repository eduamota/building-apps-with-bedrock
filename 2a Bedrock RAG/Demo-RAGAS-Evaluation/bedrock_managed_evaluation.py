"""Bedrock Managed Model Evaluation API (boto3.client('bedrock')).

Demonstrates automated RAG pipeline evaluation using AWS Bedrock's fully managed
evaluation service (`create_evaluation_job`), assessing built-in RAG metrics:
- Faithfulness (groundedness in context)
- Answer Relevance (relevance to user prompt)
- Context Relevance (retrieval precision)

Contrasts Bedrock Managed Model Evaluation with the client-side RAGAS framework.

Reference: Slide 40 ("Hands-On RAG with AWS")
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockManagedEvaluator:
    """Manages automated evaluation jobs for Bedrock RAG applications."""

    BUILTIN_RAG_METRICS = [
        "Faithfulness",
        "AnswerRelevance",
        "ContextRelevance",
    ]

    def __init__(
        self,
        region_name: str = "us-east-1",
        role_arn: Optional[str] = None,
        output_s3_uri: Optional[str] = None,
        mock_mode: bool = False,
    ):
        self.region_name = region_name
        self.role_arn = role_arn or "arn:aws:iam::123456789012:role/BedrockEvaluationRole"
        self.output_s3_uri = output_s3_uri or "s3://bedrock-evaluation-output/results/"
        self.mock_mode = mock_mode
        self._mock_jobs: Dict[str, Dict[str, Any]] = {}

        if not self.mock_mode:
            try:
                self.client = boto3.client("bedrock", region_name=self.region_name)
                boto3.client("sts", region_name=self.region_name).get_caller_identity()
            except (NoCredentialsError, ClientError) as e:
                print(f"[BedrockManagedEvaluator] AWS credentials unavailable ({e}). Using mock evaluation mode.")
                self.mock_mode = True

    def create_rag_dataset(
        self,
        samples: Optional[List[Dict[str, Any]]] = None,
        output_path: str = "rag_evaluation_dataset.jsonl",
    ) -> str:
        """Create a standard JSONL evaluation dataset formatted for Bedrock evaluation."""
        default_samples = [
            {
                "prompt": "What are the primary vector search metrics supported by Amazon OpenSearch Serverless?",
                "referenceResponse": "Amazon OpenSearch Serverless vector search supports Euclidean distance (L2), cosine similarity, and dot product (inner product) metrics for nearest neighbor search.",
                "retrievedContext": "Amazon OpenSearch Serverless provides scalable vector search capabilities. For k-NN vector search indexes, the engine supports Euclidean distance (L2), cosine similarity, and dot product metrics, with HNSW and IVF algorithms.",
            },
            {
                "prompt": "How does Bedrock Cross-Region Inference maintain high availability?",
                "referenceResponse": "Cross-Region Inference aggregates model capacity across multiple AWS geographic regions, dynamically routing traffic around regional bursts and quotas.",
                "retrievedContext": "Bedrock Cross-Region Inference (CRIS) allows applications to seamlessly route inference requests across designated AWS regions, absorbing burst traffic and increasing request throughput.",
            },
            {
                "prompt": "What is the maximum token limit for Claude 3.5 Sonnet context window in Bedrock?",
                "referenceResponse": "Claude 3.5 Sonnet supports a 200,000 token context window in Amazon Bedrock.",
                "retrievedContext": "Anthropic Claude 3.5 Sonnet is available in Amazon Bedrock with a 200k token context window, supporting both multimodal visual inputs and text generation.",
            },
        ]

        dataset_records = samples or default_samples
        with open(output_path, "w") as f:
            for record in dataset_records:
                f.write(json.dumps(record) + "\n")

        print(f"[+] Created evaluation dataset at: {output_path} ({len(dataset_records)} records)")
        return output_path

    def trigger_evaluation_job(
        self,
        job_name: str,
        dataset_s3_uri: str,
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        judge_model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
        metrics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Submit automated evaluation job to Bedrock."""
        eval_metrics = metrics or self.BUILTIN_RAG_METRICS

        if self.mock_mode:
            job_arn = f"arn:aws:bedrock:{self.region_name}:123456789012:evaluation-job/{job_name}"
            job_data = {
                "jobArn": job_arn,
                "jobName": job_name,
                "status": "InProgress",
                "creationTime": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "modelId": model_id,
                "judgeModelId": judge_model_id,
                "metrics": eval_metrics,
                "datasetUri": dataset_s3_uri,
            }
            self._mock_jobs[job_name] = job_data
            return {"jobArn": job_arn, "jobName": job_name, "status": "InProgress"}

        evaluation_config: Dict[str, Any] = {
            "automated": {
                "datasetMetricConfigs": [
                    {
                        "taskType": "QuestionAndAnswer",
                        "dataset": {
                            "name": f"{job_name}-dataset",
                            "datasetLocation": {"s3Uri": dataset_s3_uri},
                        },
                        "metricNames": eval_metrics,
                    }
                ],
                "evaluatorModelConfig": {
                    "bedrockEvaluatorModels": [
                        {"modelIdentifier": judge_model_id}
                    ]
                },
            }
        }

        inference_config: Dict[str, Any] = {
            "models": [
                {
                    "bedrockModel": {
                        "modelIdentifier": model_id,
                        "inferenceParams": json.dumps({"temperature": 0.0, "maxTokens": 1024}),
                    }
                }
            ]
        }

        output_data_config: Dict[str, Any] = {
            "s3Uri": self.output_s3_uri
        }

        try:
            response = self.client.create_evaluation_job(
                jobName=job_name,
                jobDescription="Automated RAG Performance Evaluation",
                roleArn=self.role_arn,
                evaluationConfig=evaluation_config,
                inferenceConfig=inference_config,
                outputDataConfig=output_data_config,
            )
            return response
        except ClientError as e:
            print(f"Error creating evaluation job: {e}")
            raise

    def get_job_status(self, job_name: str) -> Dict[str, Any]:
        """Poll the evaluation job status and metrics."""
        if self.mock_mode:
            job = self._mock_jobs.get(job_name, {})
            # Simulate transition to Completed
            return {
                "jobArn": job.get("jobArn", f"arn:aws:bedrock:mock:job/{job_name}"),
                "jobName": job_name,
                "status": "Completed",
                "creationTime": job.get("creationTime", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                "evaluationResults": {
                    "Faithfulness": 0.94,
                    "AnswerRelevance": 0.91,
                    "ContextRelevance": 0.88,
                },
            }

        try:
            return self.client.get_evaluation_job(jobIdentifier=job_name)
        except ClientError as e:
            print(f"Error checking evaluation job status: {e}")
            raise


def compare_evaluation_frameworks() -> Dict[str, Dict[str, str]]:
    """Return architectural comparison matrix between Bedrock Managed Evaluation vs RAGAS."""
    return {
        "Bedrock Managed Evaluation (CreateEvaluationJob)": {
            "Architecture": "Fully Managed AWS Service (Serverless)",
            "Execution Infrastructure": "AWS Managed Compute (no local worker needed)",
            "Metrics": "Faithfulness, Answer Relevance, Context Relevance, Robustness, Toxicity",
            "Data Governance": "Audited in CloudTrail, IAM permission boundaries, S3 KMS encryption",
            "Judge Models": "Bedrock Claude 3.5 Sonnet / Amazon Nova Judge models",
            "Best For": "CI/CD pipelines, production compliance audits, enterprise governance",
        },
        "Client-Side RAGAS Library": {
            "Architecture": "Client-side Python Library (`ragas`)",
            "Execution Infrastructure": "Local machine / Jupyter kernel / ECS task",
            "Metrics": "Faithfulness, Answer Relevancy, Context Precision, Context Recall",
            "Data Governance": "Runs on user-managed compute with local API keys",
            "Judge Models": "Configured via LangChain / LlamaIndex LLM wrapper",
            "Best For": "Local experimentation, fast prototyping, custom bespoke metrics",
        },
    }


def run_demo(mock_mode: bool = False):
    """Run CLI demonstration of Bedrock Managed Evaluation."""
    print("=" * 75)
    print(" AWS Bedrock Managed Model Evaluation API Demo (Slide 40 Alignment)")
    print("=" * 75)

    evaluator = BedrockManagedEvaluator(mock_mode=mock_mode)
    print(f"[*] Initialized BedrockManagedEvaluator (Mock Mode: {evaluator.mock_mode})")

    # 1. Create dataset
    dataset_file = evaluator.create_rag_dataset()

    # 2. Trigger Evaluation Job
    job_name = f"rag-eval-{int(time.time())}"
    print(f"\n--- Submitting Evaluation Job '{job_name}' ---")
    job_resp = evaluator.trigger_evaluation_job(
        job_name=job_name,
        dataset_s3_uri=f"s3://my-rag-eval-bucket/{dataset_file}",
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        judge_model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )
    print(f"[+] Job Created. ARN: {job_resp.get('jobArn')}")

    # 3. Poll Status & Metrics
    print("\n--- Polling Job Status & Retrieving RAG Metrics ---")
    status = evaluator.get_job_status(job_name)
    print(f"[+] Job Status: {status.get('status')}")
    if "evaluationResults" in status:
        print("[+] Automated RAG Metric Scores:")
        for metric, score in status["evaluationResults"].items():
            print(f"    - {metric:<20}: {score:.2f} ({score * 100:.0f}%)")

    # 4. Framework Comparison
    print("\n" + "=" * 75)
    print(" ARCHITECTURAL COMPARISON: MANAGED EVALUATION VS CLIENT-SIDE RAGAS")
    print("=" * 75)
    matrix = compare_evaluation_frameworks()
    for fw, details in matrix.items():
        print(f"\n### {fw}")
        for k, v in details.items():
            print(f"  * {k:<25}: {v}")

    # Cleanup local dataset
    if os.path.exists(dataset_file):
        os.remove(dataset_file)
    print("\n[✓] Bedrock Managed Evaluation demo completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bedrock Managed Evaluation Demo")
    parser.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser.parse_args()
    run_demo(mock_mode=args.mock)
