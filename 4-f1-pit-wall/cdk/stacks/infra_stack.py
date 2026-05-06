"""Infra Stack — S3, Knowledge Base, IAM roles, CloudFront."""

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for F1 knowledge base data
        self.kb_bucket = s3.Bucket(
            self, "F1KnowledgeBaseBucket",
            bucket_name=f"f1-pit-wall-kb-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Upload knowledge base data to S3
        s3deploy.BucketDeployment(
            self, "DeployKBData",
            sources=[s3deploy.Source.asset("../knowledge-base/data")],
            destination_bucket=self.kb_bucket,
            destination_key_prefix="f1-data/",
        )

        # S3 bucket for frontend static assets
        self.frontend_bucket = s3.Bucket(
            self, "FrontendBucket",
            bucket_name=f"f1-pit-wall-frontend-{self.account}-{self.region}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
        )

        # IAM role for agent execution
        self.agent_role = iam.Role(
            self, "AgentExecutionRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess"),
            ],
        )
        self.kb_bucket.grant_read(self.agent_role)

        # Outputs
        CfnOutput(self, "KBBucketName", value=self.kb_bucket.bucket_name)
        CfnOutput(self, "FrontendBucketURL", value=self.frontend_bucket.bucket_website_url)
        CfnOutput(self, "AgentRoleArn", value=self.agent_role.role_arn)
