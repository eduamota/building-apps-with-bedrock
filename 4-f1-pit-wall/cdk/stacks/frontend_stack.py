"""Frontend Stack — Placeholder (frontend runs locally or deploys separately)."""

from aws_cdk import Stack, CfnOutput
from constructs import Construct


class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, agent, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        CfnOutput(self, "ApiEndpoint", value=agent.api_url,
                  description="API Gateway URL — set as NEXT_PUBLIC_API_URL for frontend")
        CfnOutput(self, "FrontendInstructions", value="Run: cd frontend && NEXT_PUBLIC_API_URL=<ApiEndpoint> npm run dev")
