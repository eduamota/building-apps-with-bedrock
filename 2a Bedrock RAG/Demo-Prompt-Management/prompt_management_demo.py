"""Bedrock Prompt Management Demo (boto3 bedrock-agent + bedrock-runtime).

Demonstrates the complete lifecycle of AWS Bedrock Prompt Management:
1. Creating managed prompts with variants and template variables (`create_prompt`)
2. Freezing immutable prompt versions (`create_prompt_version`)
3. Retrieving prompt definitions and variants (`get_prompt`)
4. Dynamic parameter hydration with input validation
5. Execution with Bedrock Converse API (`converse`)
6. Lifecycle cleanup / deletion (`delete_prompt`)

Reference: Slide 30 ('Hands-On RAG with AWS')
"""

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockPromptManager:
    """Manages prompt templates, versions, and Converse API execution on AWS Bedrock."""

    def __init__(
        self,
        region_name: str = "us-east-1",
        mock_mode: bool = False,
    ):
        self.region_name = region_name
        self.mock_mode = mock_mode
        self._mock_store: Dict[str, Dict[str, Any]] = {}

        if not self.mock_mode:
            try:
                self.agent_client = boto3.client("bedrock-agent", region_name=self.region_name)
                self.runtime_client = boto3.client("bedrock-runtime", region_name=self.region_name)
                # Verify credentials
                boto3.client("sts", region_name=self.region_name).get_caller_identity()
            except (NoCredentialsError, ClientError) as e:
                print(f"[BedrockPromptManager] AWS credentials not available or invalid ({e}). Switching to Mock Mode.")
                self.mock_mode = True

    def create_prompt(
        self,
        name: str,
        template_text: str,
        input_variables: List[str],
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        description: str = "RAG Context Synthesis Prompt",
        variant_name: str = "variant-1",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Create a new managed prompt in AWS Bedrock Prompt Management."""
        if self.mock_mode:
            prompt_id = f"mock-p-{int(time.time())}"
            prompt_data = {
                "id": prompt_id,
                "arn": f"arn:aws:bedrock:{self.region_name}:123456789012:prompt/{prompt_id}",
                "name": name,
                "description": description,
                "version": "DRAFT",
                "defaultVariant": variant_name,
                "variants": [
                    {
                        "name": variant_name,
                        "templateType": "TEXT",
                        "modelId": model_id,
                        "templateConfiguration": {
                            "text": {
                                "text": template_text,
                                "inputVariables": [{"name": v} for v in input_variables],
                            }
                        },
                        "inferenceConfiguration": {
                            "text": {
                                "temperature": temperature,
                                "topP": top_p,
                                "maxTokens": max_tokens,
                            }
                        },
                    }
                ],
                "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            self._mock_store[prompt_id] = prompt_data
            return prompt_data

        try:
            response = self.agent_client.create_prompt(
                name=name,
                description=description,
                defaultVariant=variant_name,
                variants=[
                    {
                        "name": variant_name,
                        "templateType": "TEXT",
                        "modelId": model_id,
                        "templateConfiguration": {
                            "text": {
                                "text": template_text,
                                "inputVariables": [{"name": var_name} for var_name in input_variables],
                            }
                        },
                        "inferenceConfiguration": {
                            "text": {
                                "temperature": temperature,
                                "topP": top_p,
                                "maxTokens": max_tokens,
                            }
                        },
                    }
                ],
            )
            return response
        except ClientError as e:
            print(f"Error creating prompt: {e}")
            raise

    def create_prompt_version(
        self,
        prompt_id: str,
        description: str = "Production release version",
    ) -> Dict[str, Any]:
        """Create an immutable version of an existing prompt."""
        if self.mock_mode:
            if prompt_id not in self._mock_store:
                raise ValueError(f"Prompt {prompt_id} not found in mock store")
            parent = self._mock_store[prompt_id]
            version_num = str(len([k for k in self._mock_store if k.startswith(f"{prompt_id}:")]) + 1)
            version_id = f"{prompt_id}:{version_num}"
            version_data = dict(parent)
            version_data["version"] = version_num
            version_data["description"] = description
            self._mock_store[version_id] = version_data
            return version_data

        try:
            response = self.agent_client.create_prompt_version(
                promptIdentifier=prompt_id,
                description=description,
            )
            return response
        except ClientError as e:
            print(f"Error creating prompt version: {e}")
            raise

    def get_prompt(
        self,
        prompt_id: str,
        prompt_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve prompt metadata, template text, and inference configurations."""
        if self.mock_mode:
            key = f"{prompt_id}:{prompt_version}" if prompt_version and prompt_version != "DRAFT" else prompt_id
            if key not in self._mock_store:
                raise ValueError(f"Prompt {key} not found in mock store")
            return self._mock_store[key]

        params: Dict[str, Any] = {"promptIdentifier": prompt_id}
        if prompt_version:
            params["promptVersion"] = prompt_version

        try:
            response = self.agent_client.get_prompt(**params)
            return response
        except ClientError as e:
            print(f"Error retrieving prompt: {e}")
            raise

    @staticmethod
    def hydrate_prompt(template_text: str, variables: Dict[str, str], expected_variables: List[str]) -> str:
        """Replace {{variable_name}} placeholders with provided values and validate completeness."""
        missing = [v for v in expected_variables if v not in variables]
        if missing:
            raise ValueError(f"Missing required prompt variables: {missing}")

        hydrated = template_text
        for var_name, var_value in variables.items():
            pattern = re.compile(r"\{\{\s*" + re.escape(var_name) + r"\s*\}\}")
            hydrated = pattern.sub(str(var_value), hydrated)

        # Check that no expected variables remain unhydrated
        remaining = [v for v in expected_variables if re.search(r"\{\{\s*" + re.escape(v) + r"\s*\}\}", hydrated)]
        if remaining:
            raise ValueError(f"Found unresolved variables in hydrated prompt: {remaining}")

        return hydrated

    def execute_with_converse(
        self,
        prompt_id: str,
        variables: Dict[str, str],
        prompt_version: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve prompt, hydrate parameters, and invoke Bedrock Converse API."""
        prompt_meta = self.get_prompt(prompt_id=prompt_id, prompt_version=prompt_version)
        default_variant_name = prompt_meta.get("defaultVariant")
        variants = prompt_meta.get("variants", [])

        variant = next((v for v in variants if v["name"] == default_variant_name), variants[0])
        template_text = variant["templateConfiguration"]["text"]["text"]
        input_vars = [iv["name"] for iv in variant["templateConfiguration"]["text"].get("inputVariables", [])]
        model_id = variant["modelId"]
        inf_config = variant.get("inferenceConfiguration", {}).get("text", {})

        hydrated_user_message = self.hydrate_prompt(template_text, variables, input_vars)

        if self.mock_mode:
            return {
                "mock": True,
                "modelId": model_id,
                "hydratedPrompt": hydrated_user_message,
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "text": (
                                    f"[Mock Converse Response]\nBased on the retrieved context provided, "
                                    f"here is the synthesized answer for '{variables.get('query', 'query')}':\n"
                                    f"The requested analysis aligns with the provided grounding context."
                                )
                            }
                        ],
                    }
                },
                "usage": {
                    "inputTokens": len(hydrated_user_message.split()) * 2,
                    "outputTokens": 45,
                    "totalTokens": len(hydrated_user_message.split()) * 2 + 45,
                },
                "stopReason": "end_turn",
            }

        converse_params: Dict[str, Any] = {
            "modelId": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": hydrated_user_message}],
                }
            ],
            "inferenceConfig": {
                "temperature": inf_config.get("temperature", 0.2),
                "topP": inf_config.get("topP", 0.9),
                "maxTokens": inf_config.get("maxTokens", 1024),
            },
        }

        if system_prompt:
            converse_params["system"] = [{"text": system_prompt}]

        try:
            response = self.runtime_client.converse(**converse_params)
            return response
        except ClientError as e:
            print(f"Error during Converse execution: {e}")
            raise

    def delete_prompt(self, prompt_id: str) -> bool:
        """Clean up/delete a prompt."""
        if self.mock_mode:
            to_delete = [k for k in self._mock_store if k == prompt_id or k.startswith(f"{prompt_id}:")]
            for k in to_delete:
                del self._mock_store[k]
            return True

        try:
            self.agent_client.delete_prompt(promptIdentifier=prompt_id)
            return True
        except ClientError as e:
            print(f"Error deleting prompt {prompt_id}: {e}")
            return False


def run_demo(mock_mode: bool = False):
    """Run end-to-end prompt management lifecycle demonstration."""
    print("=" * 70)
    print(" AWS Bedrock Prompt Management Demo (Slide 30 Alignment)")
    print("=" * 70)

    manager = BedrockPromptManager(mock_mode=mock_mode)
    print(f"[*] Initialized BedrockPromptManager (Mock Mode: {manager.mock_mode})")

    # 1. Define Prompt Template
    prompt_name = f"rag-synthesis-demo-{int(time.time())}"
    template = (
        "You are an expert AI assistant specializing in AWS architectures.\n"
        "Context:\n{{context}}\n\n"
        "User Question: {{query}}\n\n"
        "Provide a concise, grounded response based ONLY on the context above."
    )
    variables = ["context", "query"]

    # 2. Create Prompt
    print("\n--- Step 1: Create Prompt ---")
    created = manager.create_prompt(
        name=prompt_name,
        template_text=template,
        input_variables=variables,
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        description="Demo prompt for RAG synthesis with dynamic variables",
    )
    prompt_id = created.get("id")
    print(f"[+] Created Prompt ID: {prompt_id}")
    print(f"[+] Version: {created.get('version', 'DRAFT')}")

    # 3. Create Version
    print("\n--- Step 2: Create Immutable Version ---")
    version_res = manager.create_prompt_version(
        prompt_id=prompt_id,
        description="v1.0.0 Golden Prompt",
    )
    version_number = version_res.get("version", "1")
    print(f"[+] Published Immutable Version: {version_number}")

    # 4. Retrieve Versioned Prompt
    print(f"\n--- Step 3: Retrieve Version {version_number} ---")
    retrieved = manager.get_prompt(prompt_id=prompt_id, prompt_version=version_number)
    print(f"[+] Retrieved Prompt Name: {retrieved.get('name')}")
    print(f"[+] Variant Model ID: {retrieved['variants'][0]['modelId']}")

    # 5. Hydrate & Execute with Converse API
    print("\n--- Step 4: Hydrate Variables & Execute via Converse API ---")
    payload_vars = {
        "context": (
            "AWS Bedrock Prompt Management enables developers to create, evaluate, "
            "version, and share prompts across foundational models. It supports dynamic "
            "variables using the {{variable}} syntax and integrates seamlessly with "
            "Bedrock Converse API and Agents."
        ),
        "query": "What are the primary benefits of Bedrock Prompt Management?",
    }

    result = manager.execute_with_converse(
        prompt_id=prompt_id,
        variables=payload_vars,
        prompt_version=version_number,
    )
    response_text = result["output"]["message"]["content"][0]["text"]
    print(f"[+] Converse API Output:\n{response_text}")

    # 6. Clean Up
    print("\n--- Step 5: Clean Up Prompt ---")
    deleted = manager.delete_prompt(prompt_id)
    print(f"[+] Deleted Prompt {prompt_id}: {deleted}")
    print("\n[✓] Prompt Management Demo completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bedrock Prompt Management Demo")
    parser.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser.parse_args()
    run_demo(mock_mode=args.mock)
