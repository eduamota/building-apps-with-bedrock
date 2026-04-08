#!/usr/bin/env python3
import aws_cdk as cdk
from s3vectors_app.s3vectors_app_stack import S3VectorsAppStack

app = cdk.App()
S3VectorsAppStack(app, "S3VectorsAppStack")

app.synth()
