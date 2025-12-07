"""
Async Image-to-Video Pipeline Infrastructure Setup
Provisions API Gateway, Step Functions, Lambda, and S3 using boto3
"""

import boto3
import json
import time
from datetime import datetime

# Configuration
REGION = 'us-east-1'
PROJECT_NAME = 'bedrock-async-pipeline'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

# Initialize clients
s3 = boto3.client('s3', region_name=REGION)
iam = boto3.client('iam', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
sfn = boto3.client('stepfunctions', region_name=REGION)
apigateway = boto3.client('apigatewayv2', region_name=REGION)

print(f"Account ID: {ACCOUNT_ID}")
print(f"Region: {REGION}")

# Step 1: Create S3 Bucket
def create_s3_bucket():
    bucket_name = f"{PROJECT_NAME}-artifacts-{ACCOUNT_ID}"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"✓ Created S3 bucket: {bucket_name}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"✓ S3 bucket already exists: {bucket_name}")
    return bucket_name

BUCKET_NAME = create_s3_bucket()

# Step 2: Create IAM Roles
def create_lambda_role():
    role_name = f"{PROJECT_NAME}-lambda-role"
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = response['Role']['Arn']
        
        # Attach policies
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess')
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
        
        time.sleep(10)  # Wait for role propagation
        print(f"✓ Created Lambda role: {role_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print(f"✓ Lambda role already exists: {role_name}")
    
    return role_arn

def create_sfn_role():
    role_name = f"{PROJECT_NAME}-sfn-role"
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "states.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = response['Role']['Arn']
        
        # Attach policies
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AWSLambda_FullAccess')
        
        time.sleep(10)
        print(f"✓ Created Step Functions role: {role_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print(f"✓ Step Functions role already exists: {role_name}")
    
    return role_arn

LAMBDA_ROLE_ARN = create_lambda_role()
SFN_ROLE_ARN = create_sfn_role()

# Step 3: Create Lambda Functions
def create_lambda_function(name, code, handler, env_vars=None):
    function_name = f"{PROJECT_NAME}-{name}"
    
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.12',
            Role=LAMBDA_ROLE_ARN,
            Handler=handler,
            Code={'ZipFile': code},
            Timeout=300,
            MemorySize=512,
            Environment={'Variables': env_vars or {}}
        )
        print(f"✓ Created Lambda: {function_name}")
        return response['FunctionArn']
    except lambda_client.exceptions.ResourceConflictException:
        lambda_client.update_function_code(FunctionName=function_name, ZipFile=code)
        response = lambda_client.get_function(FunctionName=function_name)
        print(f"✓ Updated Lambda: {function_name}")
        return response['Configuration']['FunctionArn']

# Lambda 1: Improve Prompt
improve_prompt_code = b'''
import json
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    prompt = event['prompt']
    
    body = {
        "messages": [{"role": "user", "content": f"Improve this image generation prompt: {prompt}"}],
        "inferenceConfig": {"maxTokens": 200, "temperature": 0.7}
    }
    
    response = bedrock.converse(modelId='us.amazon.nova-lite-v1:0', **body)
    improved = response['output']['message']['content'][0]['text']
    
    return {'prompt': prompt, 'improved_prompt': improved}
'''

# Lambda 2: Generate Image
generate_image_code = b'''
import json
import boto3
import base64
import os

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    prompt = event['improved_prompt']
    job_id = event['job_id']
    bucket = os.environ['BUCKET_NAME']
    
    body = {
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {"text": prompt},
        "imageGenerationConfig": {"width": 1280, "height": 720, "numberOfImages": 1}
    }
    
    response = bedrock.invoke_model(
        modelId='amazon.nova-canvas-v1:0',
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    image_b64 = result['images'][0]
    
    # Save to S3
    s3.put_object(Bucket=bucket, Key=f"{job_id}/image.png", Body=base64.b64decode(image_b64))
    
    return {'job_id': job_id, 'image_s3_key': f"{job_id}/image.png", 'image_b64': image_b64}
'''

# Lambda 3: Generate Video
generate_video_code = b'''
import json
import boto3
import base64
import os
import time

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    image_b64 = event['image_b64']
    job_id = event['job_id']
    bucket = os.environ['BUCKET_NAME']
    
    body = {
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": {"text": "Animate this image with smooth camera movement"},
        "videoGenerationConfig": {"durationSeconds": 6, "fps": 24, "dimension": "1280x720", "seed": 42}
    }
    
    if image_b64:
        body["textToVideoParams"]["images"] = [{"format": "png", "source": {"bytes": image_b64}}]
    
    response = bedrock.invoke_model(
        modelId='amazon.nova-reel-v1:0',
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    video_b64 = result['video']
    
    # Save to S3
    s3.put_object(Bucket=bucket, Key=f"{job_id}/video.mp4", Body=base64.b64decode(video_b64))
    
    return {'job_id': job_id, 'video_s3_key': f"{job_id}/video.mp4", 'status': 'COMPLETED'}
'''

IMPROVE_PROMPT_ARN = create_lambda_function('improve-prompt', improve_prompt_code, 'index.lambda_handler')
GENERATE_IMAGE_ARN = create_lambda_function('generate-image', generate_image_code, 'index.lambda_handler', {'BUCKET_NAME': BUCKET_NAME})
GENERATE_VIDEO_ARN = create_lambda_function('generate-video', generate_video_code, 'index.lambda_handler', {'BUCKET_NAME': BUCKET_NAME})

# Step 4: Create Step Functions State Machine
def create_state_machine():
    state_machine_name = f"{PROJECT_NAME}-workflow"
    
    definition = {
        "Comment": "Async image-to-video generation pipeline",
        "StartAt": "ImprovePrompt",
        "States": {
            "ImprovePrompt": {
                "Type": "Task",
                "Resource": IMPROVE_PROMPT_ARN,
                "Next": "GenerateImage"
            },
            "GenerateImage": {
                "Type": "Task",
                "Resource": GENERATE_IMAGE_ARN,
                "Next": "GenerateVideo"
            },
            "GenerateVideo": {
                "Type": "Task",
                "Resource": GENERATE_VIDEO_ARN,
                "End": True
            }
        }
    }
    
    try:
        response = sfn.create_state_machine(
            name=state_machine_name,
            definition=json.dumps(definition),
            roleArn=SFN_ROLE_ARN,
            type='STANDARD'
        )
        print(f"✓ Created State Machine: {state_machine_name}")
        return response['stateMachineArn']
    except sfn.exceptions.StateMachineAlreadyExists:
        machines = sfn.list_state_machines()['stateMachines']
        arn = next(m['stateMachineArn'] for m in machines if m['name'] == state_machine_name)
        sfn.update_state_machine(stateMachineArn=arn, definition=json.dumps(definition))
        print(f"✓ Updated State Machine: {state_machine_name}")
        return arn

STATE_MACHINE_ARN = create_state_machine()

# Step 5: Create API Lambda Functions
# Lambda: Start Execution
start_execution_code = f'''
import json
import boto3
import uuid
import os

sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{{}}'))
    prompt = body.get('prompt', '')
    
    if not prompt:
        return {{'statusCode': 400, 'body': json.dumps({{'error': 'prompt required'}})}}
    
    job_id = str(uuid.uuid4())
    
    response = sfn.start_execution(
        stateMachineArn='{STATE_MACHINE_ARN}',
        input=json.dumps({{'prompt': prompt, 'job_id': job_id}})
    )
    
    return {{
        'statusCode': 200,
        'body': json.dumps({{'job_id': job_id, 'execution_arn': response['executionArn']}})
    }}
'''.encode()

# Lambda: Check Status
check_status_code = b'''
import json
import boto3

sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    execution_arn = event['queryStringParameters'].get('execution_arn')
    
    if not execution_arn:
        return {'statusCode': 400, 'body': json.dumps({'error': 'execution_arn required'})}
    
    response = sfn.describe_execution(executionArn=execution_arn)
    
    result = {
        'status': response['status'],
        'start_date': response['startDate'].isoformat()
    }
    
    if response['status'] == 'SUCCEEDED':
        output = json.loads(response.get('output', '{}'))
        result['artifacts'] = {
            'image': output.get('image_s3_key'),
            'video': output.get('video_s3_key')
        }
    
    return {'statusCode': 200, 'body': json.dumps(result)}
'''

START_EXECUTION_ARN = create_lambda_function('start-execution', start_execution_code, 'index.lambda_handler')
CHECK_STATUS_ARN = create_lambda_function('check-status', check_status_code, 'index.lambda_handler')

# Step 6: Create API Gateway
def create_api_gateway():
    api_name = f"{PROJECT_NAME}-api"
    
    # Create API
    api = apigateway.create_api(
        Name=api_name,
        ProtocolType='HTTP',
        Target=START_EXECUTION_ARN
    )
    api_id = api['ApiId']
    
    # Add Lambda permissions
    lambda_client.add_permission(
        FunctionName=START_EXECUTION_ARN.split(':')[-1],
        StatementId='apigateway-invoke-start',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f"arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{api_id}/*/*"
    )
    
    lambda_client.add_permission(
        FunctionName=CHECK_STATUS_ARN.split(':')[-1],
        StatementId='apigateway-invoke-status',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f"arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{api_id}/*/*"
    )
    
    # Create integrations
    start_integration = apigateway.create_integration(
        ApiId=api_id,
        IntegrationType='AWS_PROXY',
        IntegrationUri=START_EXECUTION_ARN,
        PayloadFormatVersion='2.0'
    )
    
    status_integration = apigateway.create_integration(
        ApiId=api_id,
        IntegrationType='AWS_PROXY',
        IntegrationUri=CHECK_STATUS_ARN,
        PayloadFormatVersion='2.0'
    )
    
    # Create routes
    apigateway.create_route(
        ApiId=api_id,
        RouteKey='POST /generate',
        Target=f"integrations/{start_integration['IntegrationId']}"
    )
    
    apigateway.create_route(
        ApiId=api_id,
        RouteKey='GET /status',
        Target=f"integrations/{status_integration['IntegrationId']}"
    )
    
    # Create stage
    apigateway.create_stage(ApiId=api_id, StageName='prod', AutoDeploy=True)
    
    api_endpoint = f"https://{api_id}.execute-api.{REGION}.amazonaws.com/prod"
    print(f"✓ Created API Gateway: {api_endpoint}")
    
    return api_endpoint

API_ENDPOINT = create_api_gateway()

print("\n" + "="*60)
print("INFRASTRUCTURE SETUP COMPLETE")
print("="*60)
print(f"API Endpoint: {API_ENDPOINT}")
print(f"S3 Bucket: {BUCKET_NAME}")
print(f"\nUsage:")
print(f"  Start job: POST {API_ENDPOINT}/generate")
print(f"  Check status: GET {API_ENDPOINT}/status?execution_arn=<arn>")
print("="*60)
