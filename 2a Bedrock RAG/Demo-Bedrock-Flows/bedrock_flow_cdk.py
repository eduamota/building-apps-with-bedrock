"""AWS CDK Definition for Bedrock Flows (CfnFlow).

Provides an Infrastructure-as-Code (IaC) declaration of an AWS Bedrock Flow
using AWS CloudFormation / CDK L1 constructs (`CfnFlow`).

Includes nodes:
- Input node
- KnowledgeBase node
- Condition node
- Prompt node
- Agent node (delegation)
- Output node

Reference: Slide 38 ("Hands-On RAG with AWS")
"""

from typing import Any, Dict
try:
    from aws_cdk import (
        Stack,
        aws_iam as iam,
        aws_bedrock as bedrock,
    )
    from constructs import Construct
    CDK_AVAILABLE = True
except ImportError:
    CDK_AVAILABLE = False
    Construct = object  # type: ignore
    Stack = object  # type: ignore


class BedrockFlowCdkStack(Stack):
    """CDK Stack defining an enterprise Bedrock Flow with Prompt, KB, Condition, and Agent nodes."""

    def __init__(
        self,
        scope: Any,
        construct_id: str,
        knowledge_base_id: str = "SAMPLE_KB_ID",
        agent_id: str = "SAMPLE_AGENT_ID",
        agent_alias_id: str = "SAMPLE_ALIAS_ID",
        **kwargs: Any,
    ) -> None:
        if not CDK_AVAILABLE:
            raise RuntimeError("aws-cdk-lib is not installed. Use this construct in a CDK project environment.")

        super().__init__(scope, construct_id, **kwargs)

        # 1. Flow Execution Role
        flow_role = iam.Role(
            self,
            "BedrockFlowExecutionRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            description="IAM execution role for Bedrock Flow execution",
        )
        flow_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:Retrieve",
                    "bedrock:InvokeAgent",
                ],
                resources=["*"],
            )
        )

        # 2. Bedrock Flow L1 CloudFormation Resource (CfnFlow)
        self.flow = bedrock.CfnFlow(
            self,
            "EnterpriseRagFlow",
            name="EnterpriseRagFlow",
            description="RAG Workflow connecting Input, KB, Condition, Prompt, and Agent nodes",
            execution_role_arn=flow_role.role_arn,
            definition=bedrock.CfnFlow.FlowDefinitionProperty(
                nodes=[
                    # Node 1: Input
                    bedrock.CfnFlow.FlowNodeProperty(
                        name="FlowInput",
                        type="Input",
                        outputs=[bedrock.CfnFlow.FlowNodeOutputProperty(name="document", type="String")],
                    ),
                    # Node 2: Knowledge Base
                    bedrock.CfnFlow.FlowNodeProperty(
                        name="KnowledgeBaseNode",
                        type="KnowledgeBase",
                        configuration=bedrock.CfnFlow.FlowNodeConfigurationProperty(
                            knowledge_base=bedrock.CfnFlow.KnowledgeBaseFlowNodeConfigurationProperty(
                                knowledge_base_id=knowledge_base_id,
                                model_id="anthropic.claude-3-haiku-20240307-v1:0",
                            )
                        ),
                        inputs=[bedrock.CfnFlow.FlowNodeInputProperty(name="query", type="String", expression="$.data")],
                        outputs=[bedrock.CfnFlow.FlowNodeOutputProperty(name="output", type="Array")],
                    ),
                    # Node 3: Condition
                    bedrock.CfnFlow.FlowNodeProperty(
                        name="ConfidenceConditionNode",
                        type="Condition",
                        configuration=bedrock.CfnFlow.FlowNodeConfigurationProperty(
                            condition=bedrock.CfnFlow.ConditionFlowNodeConfigurationProperty(
                                conditions=[
                                    bedrock.CfnFlow.FlowConditionProperty(name="Confident", expression="size($.data) > 0"),
                                    bedrock.CfnFlow.FlowConditionProperty(name="Fallback", expression="default"),
                                ]
                            )
                        ),
                        inputs=[bedrock.CfnFlow.FlowNodeInputProperty(name="data", type="Array", expression="$.data")],
                        outputs=[
                            bedrock.CfnFlow.FlowNodeOutputProperty(name="Confident", type="Array"),
                            bedrock.CfnFlow.FlowNodeOutputProperty(name="Fallback", type="Array"),
                        ],
                    ),
                    # Node 4: Agent Node (Delegation)
                    bedrock.CfnFlow.FlowNodeProperty(
                        name="ResearchAgentNode",
                        type="Agent",
                        configuration=bedrock.CfnFlow.FlowNodeConfigurationProperty(
                            agent=bedrock.CfnFlow.AgentFlowNodeConfigurationProperty(
                                agent_alias_arn=f"arn:aws:bedrock:{self.region}:{self.account}:agent-alias/{agent_id}/{agent_alias_id}"
                            )
                        ),
                        inputs=[bedrock.CfnFlow.FlowNodeInputProperty(name="inputText", type="String", expression="$.data")],
                        outputs=[bedrock.CfnFlow.FlowNodeOutputProperty(name="outputText", type="String")],
                    ),
                    # Node 5: Output
                    bedrock.CfnFlow.FlowNodeProperty(
                        name="FlowOutput",
                        type="Output",
                        inputs=[bedrock.CfnFlow.FlowNodeInputProperty(name="document", type="String", expression="$.data")],
                    ),
                ],
                connections=[
                    bedrock.CfnFlow.FlowConnectionProperty(
                        name="InputToKB",
                        type="Data",
                        source="FlowInput",
                        target="KnowledgeBaseNode",
                        configuration=bedrock.CfnFlow.FlowConnectionConfigurationProperty(
                            data=bedrock.CfnFlow.FlowDataConnectionConfigurationProperty(
                                source_output="document", target_input="query"
                            )
                        ),
                    ),
                    bedrock.CfnFlow.FlowConnectionProperty(
                        name="KBToCondition",
                        type="Data",
                        source="KnowledgeBaseNode",
                        target="ConfidenceConditionNode",
                        configuration=bedrock.CfnFlow.FlowConnectionConfigurationProperty(
                            data=bedrock.CfnFlow.FlowDataConnectionConfigurationProperty(
                                source_output="output", target_input="data"
                            )
                        ),
                    ),
                    bedrock.CfnFlow.FlowConnectionProperty(
                        name="ConditionToAgent",
                        type="Data",
                        source="ConfidenceConditionNode",
                        target="ResearchAgentNode",
                        configuration=bedrock.CfnFlow.FlowConnectionConfigurationProperty(
                            data=bedrock.CfnFlow.FlowDataConnectionConfigurationProperty(
                                source_output="Confident", target_input="inputText"
                            )
                        ),
                    ),
                    bedrock.CfnFlow.FlowConnectionProperty(
                        name="AgentToOutput",
                        type="Data",
                        source="ResearchAgentNode",
                        target="FlowOutput",
                        configuration=bedrock.CfnFlow.FlowConnectionConfigurationProperty(
                            data=bedrock.CfnFlow.FlowDataConnectionConfigurationProperty(
                                source_output="outputText", target_input="document"
                            )
                        ),
                    ),
                ],
            ),
        )


def generate_cloudformation_template() -> Dict[str, Any]:
    """Generate pure CloudFormation template representation without requiring installed CDK CLI."""
    return {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "AWS Bedrock Flow with Prompt, KnowledgeBase, Condition, and Agent nodes",
        "Resources": {
            "BedrockFlowRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "AssumeRolePolicyDocument": {
                        "Statement": [{
                            "Effect": "Allow",
                            "Principal": {"Service": "bedrock.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }]
                    }
                }
            },
            "EnterpriseRagFlow": {
                "Type": "AWS::Bedrock::Flow",
                "Properties": {
                    "Name": "EnterpriseRagFlow",
                    "ExecutionRoleArn": {"Fn::GetAtt": ["BedrockFlowRole", "Arn"]},
                    "Definition": {
                        "Nodes": [
                            {"Name": "FlowInput", "Type": "Input", "Outputs": [{"Name": "document", "Type": "String"}]},
                            {"Name": "KnowledgeBaseNode", "Type": "KnowledgeBase", "Inputs": [{"Name": "query", "Type": "String", "Expression": "$.data"}]},
                            {"Name": "ConfidenceConditionNode", "Type": "Condition", "Inputs": [{"Name": "data", "Type": "Array", "Expression": "$.data"}]},
                            {"Name": "ResearchAgentNode", "Type": "Agent", "Inputs": [{"Name": "inputText", "Type": "String", "Expression": "$.data"}]},
                            {"Name": "FlowOutput", "Type": "Output", "Inputs": [{"Name": "document", "Type": "String", "Expression": "$.data"}]},
                        ],
                        "Connections": [
                            {"Name": "InputToKB", "Type": "Data", "Source": "FlowInput", "Target": "KnowledgeBaseNode"},
                            {"Name": "KBToCondition", "Type": "Data", "Source": "KnowledgeBaseNode", "Target": "ConfidenceConditionNode"},
                            {"Name": "ConditionToAgent", "Type": "Data", "Source": "ConfidenceConditionNode", "Target": "ResearchAgentNode"},
                            {"Name": "AgentToOutput", "Type": "Data", "Source": "ResearchAgentNode", "Target": "FlowOutput"},
                        ]
                    }
                }
            }
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(generate_cloudformation_template(), indent=2))
