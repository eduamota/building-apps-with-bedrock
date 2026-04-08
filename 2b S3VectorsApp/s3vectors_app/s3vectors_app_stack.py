from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_bedrock as bedrock,
    Duration,
)
from constructs import Construct
import json

class S3VectorsAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bedrock Guardrail
        guardrail = bedrock.CfnGuardrail(
            self, "BasicSafetyGuardrail",
            name="gdrail-basic-safety",
            blocked_input_messaging="I can't process that request. Please ask something else.",
            blocked_outputs_messaging="I can't provide that information. Please ask something else.",
            content_policy_config=bedrock.CfnGuardrail.ContentPolicyConfigProperty(
                filters_config=[
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        input_strength="HIGH",
                        output_strength="HIGH",
                        type="HATE"
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        input_strength="HIGH", 
                        output_strength="HIGH",
                        type="VIOLENCE"
                    ),
                    bedrock.CfnGuardrail.ContentFilterConfigProperty(
                        input_strength="HIGH",
                        output_strength="HIGH", 
                        type="SEXUAL"
                    )
                ]
            )
        )

        # IAM role for Lambda to access S3 Vectors
        lambda_role = iam.Role(
            self, "S3VectorsLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            inline_policies={
                "S3VectorsPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "s3vectors:CreateVectorBucket",
                                "s3vectors:CreateIndex",
                                "s3vectors:PutVectors",
                                "s3vectors:QueryVectors",
                                "s3vectors:GetVectors",
                                "s3vectors:ListVectors",
                                "s3vectors:DeleteVectors"
                            ],
                            resources=["*"]
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeModel"
                            ],
                            resources=[
                                "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1",
                                "arn:aws:bedrock:*::foundation-model/amazon.nova-pro-v1:0"
                            ]
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:ApplyGuardrail"
                            ],
                            resources=[guardrail.attr_guardrail_arn]
                        )
                    ]
                )
            }
        )

        # Lambda function for S3 Vectors operations
        s3vectors_lambda = _lambda.Function(
            self, "S3VectorsFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            role=lambda_role,
            timeout=Duration.seconds(30),
            environment={
                "VECTOR_BUCKET": "s3vectors-app-bucket",
                "VECTOR_INDEX": "documents-index",
                "EMBEDDING_MODEL": "amazon.titan-embed-text-v1",
                "GUARDRAIL_ID": guardrail.attr_guardrail_id
            }
        )

        # API Gateway
        api = apigateway.RestApi(
            self, "S3VectorsApi",
            rest_api_name="S3 Vectors Service",
            description="API for S3 Vectors operations",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"]
            )
        )

        # API Key
        api_key = api.add_api_key("S3VectorsApiKey")
        
        # Usage Plan
        usage_plan = api.add_usage_plan(
            "S3VectorsUsagePlan",
            throttle=apigateway.ThrottleSettings(
                rate_limit=100,
                burst_limit=200
            ),
            quota=apigateway.QuotaSettings(
                limit=10000,
                period=apigateway.Period.DAY
            )
        )
        usage_plan.add_api_key(api_key)

        # Lambda integration
        lambda_integration = apigateway.LambdaIntegration(s3vectors_lambda)

        # API endpoints
        # POST /documents - Add document
        documents = api.root.add_resource("documents")
        documents.add_method("POST", lambda_integration, api_key_required=True)

        # GET /search?q=query - Search documents
        search = api.root.add_resource("search")
        search.add_method("GET", lambda_integration, api_key_required=True)

        # POST /ask - Ask question (RAG)
        ask = api.root.add_resource("ask")
        ask.add_method("POST", lambda_integration, api_key_required=True)

        # GET /health - Health check
        health = api.root.add_resource("health")
        health.add_method("GET", lambda_integration, api_key_required=True)

        # Add usage plan to deployment stage
        usage_plan.add_api_stage(
            stage=api.deployment_stage
        )

        # Output API key
        CfnOutput(
            self, "ApiKey",
            value=api_key.key_id,
            description="API Key ID for S3 Vectors API"
        )
