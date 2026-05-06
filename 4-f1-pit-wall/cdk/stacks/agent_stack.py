"""Agent Stack — AgentCore Runtime, Gateway, Memory, Policy via CDK."""

import os
from aws_cdk import (
    Stack,
    Duration,
    BundlingOptions,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput,
)
from aws_cdk.aws_bedrock_agentcore_alpha import (
    Runtime as AgentCoreRuntime,
    AgentRuntimeArtifact,
    Gateway,
    GatewayAuthorizer,
    McpProtocolConfiguration,
    McpGatewaySearchType,
    MCPProtocolVersion,
    ToolSchema,
    ToolDefinition,
    SchemaDefinition,
    SchemaDefinitionType,
    Memory,
    MemoryStrategy,
    PolicyEngine,
    PolicyStatement,
    PolicyValidationMode,
    GatewayPolicyEngineConfig,
)
from constructs import Construct


class AgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, infra, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # --- AgentCore Runtime ---
        self.runtime = AgentCoreRuntime(self, "F1PitWallRuntime",
            runtime_name="f1_pit_wall_v3",
            agent_runtime_artifact=AgentRuntimeArtifact.from_asset(
                os.path.join(os.path.dirname(__file__), "../../agent"),
            ),
            environment_variables={
                "MODEL_ID": "us.amazon.nova-pro-v1:0",
                "KB_BUCKET": infra.kb_bucket.bucket_name,
                "MEMORY_ID": "f1_pit_wall_memory",
            },
            description="F1 Pit Wall multi-agent system",
        )

        # Grant Bedrock model invocation + Memory access
        self.runtime.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=["*"],
        ))
        self.runtime.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock-agentcore:CreateEvent", "bedrock-agentcore:RetrieveMemoryRecords",
                     "bedrock-agentcore:ListMemoryRecords", "bedrock-agentcore:GetMemoryRecord"],
            resources=["*"],
        ))
        infra.kb_bucket.grant_read(self.runtime)

        # --- AgentCore Memory ---
        self.memory = Memory(self, "F1PitWallMemory",
            memory_name="f1_pit_wall_memory",
            description="Stores user preferences (favorite team/driver) and conversation history",
            expiration_duration=Duration.days(90),
            memory_strategies=[
                MemoryStrategy.using_built_in_user_preference(),
                MemoryStrategy.using_built_in_summarization(),
            ],
        )

        # --- AgentCore Gateway ---
        self.policy_engine = PolicyEngine(self, "F1PolicyEngine",
            policy_engine_name="f1_pit_wall_policy",
            description="Read-only access enforcement for F1 knowledge base",
        )

        self.gateway = Gateway(self, "F1PitWallGateway",
            gateway_name="f1-pit-wall-gateway",
            description="Tool gateway for F1 agent tools",
            protocol_configuration=McpProtocolConfiguration(
                instructions="F1 Pit Wall tools: standings, predictions, lap times, calendar",
                search_type=McpGatewaySearchType.SEMANTIC,
                supported_versions=[MCPProtocolVersion.MCP_2025_03_26],
            ),
            authorizer_configuration=GatewayAuthorizer.with_no_auth(),
            policy_engine_configuration=GatewayPolicyEngineConfig(
                policy_engine=self.policy_engine,
            ),
        )

        # --- Tools Lambda (exposed via Gateway) ---
        self.tools_lambda = _lambda.Function(self, "F1ToolsFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="tools_handler.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "../../agent")),
            timeout=Duration.seconds(30),
            memory_size=256,
        )

        # Register tools Lambda on Gateway
        self.gateway.add_lambda_target("F1Tools",
            gateway_target_name="f1-tools",
            description="F1 data tools: standings, predictions, lap times, calendar",
            lambda_function=self.tools_lambda,
            tool_schema=ToolSchema.from_inline([
                ToolDefinition(name="get_standings", description="Get current F1 championship standings",
                    input_schema=SchemaDefinition(type=SchemaDefinitionType.OBJECT,
                        properties={"category": SchemaDefinition(type=SchemaDefinitionType.STRING, description="drivers or constructors")},
                        required=["category"])),
                ToolDefinition(name="predict_race", description="Predict race outcome for a track",
                    input_schema=SchemaDefinition(type=SchemaDefinitionType.OBJECT,
                        properties={"track": SchemaDefinition(type=SchemaDefinitionType.STRING, description="Track name")},
                        required=["track"])),
                ToolDefinition(name="compare_lap_times", description="Compare lap times between two drivers",
                    input_schema=SchemaDefinition(type=SchemaDefinitionType.OBJECT,
                        properties={
                            "driver1": SchemaDefinition(type=SchemaDefinitionType.STRING, description="First driver"),
                            "driver2": SchemaDefinition(type=SchemaDefinitionType.STRING, description="Second driver"),
                            "track": SchemaDefinition(type=SchemaDefinitionType.STRING, description="Track name"),
                        }, required=["driver1", "driver2", "track"])),
                ToolDefinition(name="get_calendar", description="Get upcoming F1 races",
                    input_schema=SchemaDefinition(type=SchemaDefinitionType.OBJECT,
                        properties={"next_n": SchemaDefinition(type=SchemaDefinitionType.STRING, description="Number of races")},
                        required=[])),
            ]),
        )

        # --- Policy: Read-only enforcement ---
        self.policy_engine.add_policy("AllowReadOnly",
            statement=PolicyStatement.permit().for_all_principals().on_all_actions().on_resource("AgentCore::Gateway", self.gateway.gateway_arn),
            description="Allow all read-only F1 tool operations",
            validation_mode=PolicyValidationMode.IGNORE_ALL_FINDINGS,
        )

        # --- API Gateway (frontend proxy to AgentCore Runtime) ---
        self.api = apigw.RestApi(self, "F1PitWallAPI",
            rest_api_name="F1 Pit Wall API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        # Proxy Lambda to invoke AgentCore Runtime
        self.proxy_lambda = _lambda.Function(self, "F1ProxyFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="proxy_handler.handler",
            code=_lambda.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "../../agent"),
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_12.bundling_image,
                    command=["bash", "-c",
                        "pip install -r proxy_requirements.txt -t /asset-output && "
                        "cp proxy_handler.py /asset-output/"
                    ],
                ),
            ),
            timeout=Duration.seconds(120),
            memory_size=256,
            environment={
                "AGENTCORE_RUNTIME_ID": self.runtime.agent_runtime_id,
                "ACCOUNT_ID": self.account,
            },
        )
        self.runtime.grant_invoke(self.proxy_lambda)

        chat_resource = self.api.root.add_resource("chat")
        chat_resource.add_method("POST", apigw.LambdaIntegration(self.proxy_lambda))

        # --- Outputs ---
        self.api_url = self.api.url
        CfnOutput(self, "ApiUrl", value=self.api.url)
        CfnOutput(self, "RuntimeId", value=self.runtime.agent_runtime_id)
        CfnOutput(self, "GatewayId", value=self.gateway.gateway_id)
        CfnOutput(self, "MemoryId", value=self.memory.memory_id)
        CfnOutput(self, "PolicyEngineId", value=self.policy_engine.policy_engine_id)
