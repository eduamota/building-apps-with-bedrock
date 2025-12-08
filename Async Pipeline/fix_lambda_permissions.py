import boto3
import json

iam = boto3.client('iam')
PROJECT_NAME = 'bedrock-async-pipeline'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
REGION = 'us-east-1'

lambda_role_name = f"{PROJECT_NAME}-lambda-role"

# Add Step Functions permission
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "states:StartExecution",
                "states:DescribeExecution"
            ],
            "Resource": f"arn:aws:states:{REGION}:{ACCOUNT_ID}:stateMachine:{PROJECT_NAME}-*"
        }
    ]
}

iam.put_role_policy(
    RoleName=lambda_role_name,
    PolicyName='StepFunctionsAccess',
    PolicyDocument=json.dumps(policy_document)
)

print(f"✓ Added Step Functions permissions to {lambda_role_name}")
