"""Bedrock Flows Visual Workflow Example (boto3 bedrock-agent).

Demonstrates creating, validating, and managing an automated visual DAG workflow
using AWS Bedrock Flows (`create_flow`, `prepare_flow`, `validate_flow_definition`).

Nodes demonstrated:
- FlowInputNode: Accepts input query
- KnowledgeBaseNode: Retrieves context chunks from Bedrock Knowledge Base
- ConditionNode: Evaluates retrieval results / confidence threshold
- PromptNode: Synthesizes final answer with Claude / Nova model
- FlowOutputNode: Returns structured output

Reference: Slide 38 ("Hands-On RAG with AWS")
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockFlowManager:
    """Orchestrates Bedrock Flow creation, validation, and lifecycle operations."""

    def __init__(
        self,
        region_name: str = "us-east-1",
        execution_role_arn: Optional[str] = None,
        mock_mode: bool = False,
    ):
        self.region_name = region_name
        self.execution_role_arn = execution_role_arn or "arn:aws:iam::123456789012:role/BedrockFlowExecutionRole"
        self.mock_mode = mock_mode
        self._mock_flows: Dict[str, Dict[str, Any]] = {}

        if not self.mock_mode:
            try:
                self.client = boto3.client("bedrock-agent", region_name=self.region_name)
                boto3.client("sts", region_name=self.region_name).get_caller_identity()
            except (NoCredentialsError, ClientError) as e:
                print(f"[BedrockFlowManager] AWS credentials unavailable ({e}). Running in mock mode.")
                self.mock_mode = True

    def build_rag_flow_definition(
        self,
        kb_id: str = "SAMPLE_KB_ID",
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
    ) -> Dict[str, Any]:
        """Construct a multi-node Bedrock Flow definition with Input, KB, Condition, Prompt, and Output nodes."""
        nodes = [
            # 1. Flow Input Node
            {
                "name": "FlowInput",
                "type": "Input",
                "outputs": [
                    {"name": "document", "type": "String"}
                ],
            },
            # 2. Bedrock Knowledge Base Node
            {
                "name": "RetrieveKnowledgeBase",
                "type": "KnowledgeBase",
                "configuration": {
                    "knowledgeBase": {
                        "knowledgeBaseId": kb_id,
                        "modelId": model_id,
                    }
                },
                "inputs": [
                    {"name": "query", "type": "String", "expression": "$.data"}
                ],
                "outputs": [
                    {"name": "output", "type": "Array"}
                ],
            },
            # 3. Condition Branching Node (Inspects retrieval results)
            {
                "name": "CheckRetrievalScore",
                "type": "Condition",
                "configuration": {
                    "condition": {
                        "conditions": [
                            {"name": "HasResults", "expression": "size($.data) > 0"},
                            {"name": "EmptyResults", "expression": "default"}
                        ]
                    }
                },
                "inputs": [
                    {"name": "data", "type": "Array", "expression": "$.data"}
                ],
                "outputs": [
                    {"name": "HasResults", "type": "Array"},
                    {"name": "EmptyResults", "type": "Array"},
                ],
            },
            # 4. Prompt Node (Synthesizes answer from retrieved context)
            {
                "name": "SynthesizeAnswerPrompt",
                "type": "Prompt",
                "configuration": {
                    "prompt": {
                        "sourceConfiguration": {
                            "inline": {
                                "modelId": model_id,
                                "templateType": "TEXT",
                                "inferenceConfiguration": {
                                    "text": {"temperature": 0.2, "maxTokens": 1024}
                                },
                                "templateConfiguration": {
                                    "text": {
                                        "text": (
                                            "You are a helpful AI assistant.\n"
                                            "Context:\n{{context}}\n\n"
                                            "Question:\n{{question}}\n\n"
                                            "Answer concisely based on the context."
                                        ),
                                        "inputVariables": [
                                            {"name": "context"},
                                            {"name": "question"}
                                        ]
                                    }
                                }
                            }
                        }
                    }
                },
                "inputs": [
                    {"name": "context", "type": "String", "expression": "$.data"},
                    {"name": "question", "type": "String", "expression": "$.data"}
                ],
                "outputs": [
                    {"name": "modelCompletion", "type": "String"}
                ],
            },
            # 5. Flow Output Node
            {
                "name": "FlowOutput",
                "type": "Output",
                "inputs": [
                    {"name": "document", "type": "String", "expression": "$.data"}
                ],
            },
        ]

        connections = [
            # Input -> Knowledge Base
            {
                "name": "InputToKB",
                "type": "Data",
                "source": "FlowInput",
                "target": "RetrieveKnowledgeBase",
                "configuration": {
                    "data": {"sourceOutput": "document", "targetInput": "query"}
                },
            },
            # KB -> Condition
            {
                "name": "KBToCondition",
                "type": "Data",
                "source": "RetrieveKnowledgeBase",
                "target": "CheckRetrievalScore",
                "configuration": {
                    "data": {"sourceOutput": "output", "targetInput": "data"}
                },
            },
            # Condition (HasResults) -> Prompt Node
            {
                "name": "ConditionToPromptContext",
                "type": "Data",
                "source": "CheckRetrievalScore",
                "target": "SynthesizeAnswerPrompt",
                "configuration": {
                    "data": {"sourceOutput": "HasResults", "targetInput": "context"}
                },
            },
            # Input -> Prompt Node (pass original question)
            {
                "name": "InputToPromptQuestion",
                "type": "Data",
                "source": "FlowInput",
                "target": "SynthesizeAnswerPrompt",
                "configuration": {
                    "data": {"sourceOutput": "document", "targetInput": "question"}
                },
            },
            # Prompt -> Flow Output
            {
                "name": "PromptToOutput",
                "type": "Data",
                "source": "SynthesizeAnswerPrompt",
                "target": "FlowOutput",
                "configuration": {
                    "data": {"sourceOutput": "modelCompletion", "targetInput": "document"}
                },
            },
        ]

        return {
            "nodes": nodes,
            "connections": connections,
        }

    def validate_flow(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Validate topological integrity and schema of the flow definition."""
        node_names = {node["name"] for node in definition.get("nodes", [])}
        issues: List[str] = []

        if len(node_names) != len(definition.get("nodes", [])):
            issues.append("Duplicate node names found in flow definition.")

        if "FlowInput" not in node_names:
            issues.append("Missing required Input node.")
        if "FlowOutput" not in node_names:
            issues.append("Missing required Output node.")

        for conn in definition.get("connections", []):
            if conn["source"] not in node_names:
                issues.append(f"Connection source '{conn['source']}' does not exist.")
            if conn["target"] not in node_names:
                issues.append(f"Connection target '{conn['target']}' does not exist.")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "node_count": len(definition.get("nodes", [])),
            "connection_count": len(definition.get("connections", [])),
        }

    def create_flow(
        self,
        name: str,
        definition: Dict[str, Any],
        description: str = "Enterprise RAG Visual Flow",
    ) -> Dict[str, Any]:
        """Create a new Bedrock Flow."""
        validation = self.validate_flow(definition)
        if not validation["valid"]:
            raise ValueError(f"Invalid flow definition: {validation['issues']}")

        if self.mock_mode:
            flow_id = f"flow-{int(time.time())}"
            flow_data = {
                "id": flow_id,
                "arn": f"arn:aws:bedrock:{self.region_name}:123456789012:flow/{flow_id}",
                "name": name,
                "description": description,
                "status": "NotPrepared",
                "definition": definition,
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "version": "DRAFT",
            }
            self._mock_flows[flow_id] = flow_data
            return flow_data

        try:
            response = self.client.create_flow(
                name=name,
                description=description,
                executionRoleArn=self.execution_role_arn,
                definition=definition,
            )
            return response
        except ClientError as e:
            print(f"Error creating Bedrock Flow: {e}")
            raise

    def prepare_flow(self, flow_id: str) -> Dict[str, Any]:
        """Prepare/compile flow to validate execution readiness."""
        if self.mock_mode:
            if flow_id in self._mock_flows:
                self._mock_flows[flow_id]["status"] = "Prepared"
            return {"id": flow_id, "status": "Prepared"}

        try:
            return self.client.prepare_flow(flowIdentifier=flow_id)
        except ClientError as e:
            print(f"Error preparing flow {flow_id}: {e}")
            raise

    def delete_flow(self, flow_id: str) -> bool:
        """Teardown flow."""
        if self.mock_mode:
            if flow_id in self._mock_flows:
                del self._mock_flows[flow_id]
            return True

        try:
            self.client.delete_flow(flowIdentifier=flow_id)
            return True
        except ClientError as e:
            print(f"Error deleting flow {flow_id}: {e}")
            return False


def run_demo(mock_mode: bool = False):
    """Run CLI demonstration of Bedrock Flows."""
    print("=" * 75)
    print(" AWS Bedrock Flows Visual Workflow Demo (Slide 38 Alignment)")
    print("=" * 75)

    manager = BedrockFlowManager(mock_mode=mock_mode)
    print(f"[*] Initialized BedrockFlowManager (Mock Mode: {manager.mock_mode})")

    # 1. Build Definition
    print("\n--- Step 1: Build Multi-Node RAG Flow Definition ---")
    definition = manager.build_rag_flow_definition()
    print(f"[+] Total Nodes: {len(definition['nodes'])}")
    for node in definition['nodes']:
        print(f"    - [{node['type']:<15}] Node: {node['name']}")
    print(f"[+] Total Connections: {len(definition['connections'])}")
    for conn in definition['connections']:
        print(f"    - {conn['source']} --> ({conn['configuration']['data']['targetInput']}) --> {conn['target']}")

    # 2. Validate
    print("\n--- Step 2: Validate Flow Topology ---")
    val_result = manager.validate_flow(definition)
    print(f"[+] Validation Passed: {val_result['valid']}")

    # 3. Create Flow
    flow_name = f"rag-workflow-{int(time.time())}"
    print(f"\n--- Step 3: Create Flow '{flow_name}' ---")
    created = manager.create_flow(name=flow_name, definition=definition)
    flow_id = created.get("id")
    print(f"[+] Created Flow ID: {flow_id} (Status: {created.get('status')})")

    # 4. Prepare Flow
    print(f"\n--- Step 4: Prepare Flow for Execution ---")
    prepared = manager.prepare_flow(flow_id)
    print(f"[+] Flow Status: {prepared.get('status')}")

    # 5. Teardown
    print(f"\n--- Step 5: Teardown Flow ---")
    deleted = manager.delete_flow(flow_id)
    print(f"[+] Flow Deleted: {deleted}")

    print("\n[✓] Bedrock Flows demo completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bedrock Flows Demo")
    parser.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser.parse_args()
    run_demo(mock_mode=args.mock)
