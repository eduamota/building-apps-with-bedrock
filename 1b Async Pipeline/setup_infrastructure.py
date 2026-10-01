"""
Async Image Generation + Upscale Pipeline Infrastructure Setup
Provisions API Gateway, Step Functions, Lambda, and S3 using boto3.

Pipeline stages (all use ACTIVE Bedrock models):
  1. Improve prompt  - Amazon Nova Lite        (us.amazon.nova-lite-v1:0,  us-east-1)
  2. Generate image  - Stable Image Core       (stability.stable-image-core-v1:1, base model, us-west-2)
  3. Upscale image   - Stable Creative Upscale (us.stability.stable-creative-upscale-v1:0, inference profile, us-west-2)

Notes:
- The previous Nova Canvas (image) and Nova Reel (video) models are LEGACY/retired.
- Stable Image Core is only an on-demand BASE model in us-west-2 (no 'us.' inference profile),
  while Creative Upscale is a 'us.' inference profile - so both image Lambdas call us-west-2.
- The Stability image APIs are synchronous InvokeModel calls; the pipeline's async behavior
  comes from Step Functions orchestration plus API Gateway job submission and status polling.

This script is idempotent: re-running reuses existing resources and updates Lambda code.

Run as a standalone script:
    python setup_infrastructure.py            # provision only
    python setup_infrastructure.py --test     # provision, then run one end-to-end job
"""

import sys
import json
import time
import zipfile
from io import BytesIO

import boto3

# Configuration
REGION = 'us-east-1'
PROJECT_NAME = 'bedrock-async-pipeline'
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

# Clients
s3 = boto3.client('s3', region_name=REGION)
iam = boto3.client('iam', region_name=REGION)
lambda_client = boto3.client('lambda', region_name=REGION)
sfn = boto3.client('stepfunctions', region_name=REGION)
apigateway = boto3.client('apigatewayv2', region_name=REGION)


# --------------------------------------------------------------------------- #
# Lambda source (extracted verbatim from async_pipeline_setup.ipynb)
# --------------------------------------------------------------------------- #

improve_prompt_code = b'''
import json
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    prompt = event['prompt']
    body = {
        "messages": [{"role": "user", "content": [{"text": f"Improve this image generation prompt: {prompt}"}]}],
        "inferenceConfig": {"maxTokens": 200, "temperature": 0.7}
    }
    response = bedrock.converse(modelId='us.amazon.nova-lite-v1:0', **body)
    improved = response['output']['message']['content'][0]['text']
    return {'prompt': prompt, 'improved_prompt': improved, 'job_id': event['job_id']}
'''

generate_image_code = b'''
import json, boto3, base64, os

# Stable Image Core is a text-to-image generator available as an on-demand BASE model
# in us-west-2 (there is no 'us.' inference profile for it), so this client targets us-west-2.
bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    prompt = event['improved_prompt']
    job_id = event['job_id']
    bucket = os.environ['BUCKET_NAME']

    # Stability uses a flat body (no taskType wrapper)
    body = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "output_format": "png",
        "seed": 42
    }

    response = bedrock.invoke_model(modelId='stability.stable-image-core-v1:1', body=json.dumps(body))
    result = json.loads(response['body'].read())

    if result.get('finish_reasons', [None])[0]:
        raise Exception(f"Image generation filtered: {result['finish_reasons'][0]}")

    image_b64 = result['images'][0]
    s3.put_object(Bucket=bucket, Key=f"{job_id}/image.png", Body=base64.b64decode(image_b64))

    # NOTE: do NOT return image_b64 - Step Functions caps state payloads at 256KB and a
    # base64 PNG exceeds that (States.DataLimitExceeded). The next stage reads it from S3.
    return {'job_id': job_id, 'improved_prompt': prompt, 'image_s3_key': f"{job_id}/image.png"}
'''

upscale_image_code = b'''
import json, boto3, base64, os

# Creative Upscale runs via the us.stability inference profile (available in us-west-2).
bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    job_id = event['job_id']
    bucket = os.environ['BUCKET_NAME']

    # The image is read from S3 (the generate stage does not pass bytes through Step
    # Functions, which caps state payloads at 256KB).
    obj = s3.get_object(Bucket=bucket, Key=event['image_s3_key'])
    image_b64 = base64.b64encode(obj['Body'].read()).decode('utf-8')

    body = {
        "image": image_b64,
        "prompt": event.get('improved_prompt', 'high quality, sharp detail, professional photography'),
        "creativity": 0.3,
        # Creative Upscale produces ~4K output; a PNG response can exceed Bedrock's 16MB
        # InvokeModel response limit, so request JPEG (much smaller for photographic images).
        "output_format": "jpeg"
    }

    response = bedrock.invoke_model(modelId='us.stability.stable-creative-upscale-v1:0', body=json.dumps(body))
    result = json.loads(response['body'].read())

    if result.get('finish_reasons', [None])[0]:
        raise Exception(f"Upscale filtered: {result['finish_reasons'][0]}")

    upscaled_b64 = result['images'][0]
    s3.put_object(Bucket=bucket, Key=f"{job_id}/upscaled.jpg", Body=base64.b64decode(upscaled_b64))

    return {'job_id': job_id, 'image_s3_key': event.get('image_s3_key'),
            'upscaled_s3_key': f"{job_id}/upscaled.jpg", 'status': 'COMPLETED'}
'''

check_status_code = b'''
import json, boto3
sfn = boto3.client('stepfunctions')

def lambda_handler(event, context):
    execution_arn = event['queryStringParameters'].get('execution_arn')
    if not execution_arn:
        return {'statusCode': 400, 'body': json.dumps({'error': 'execution_arn required'})}

    response = sfn.describe_execution(executionArn=execution_arn)
    result = {'status': response['status'], 'start_date': response['startDate'].isoformat()}

    if response['status'] == 'SUCCEEDED':
        output = json.loads(response.get('output', '{}'))
        result['artifacts'] = {'image': output.get('image_s3_key'), 'upscaled': output.get('upscaled_s3_key')}

    return {'statusCode': 200, 'body': json.dumps(result)}
'''


def build_start_execution_code(STATE_MACHINE_ARN):
    """Build the start-execution Lambda source with the state machine ARN embedded."""
    return f'''
import json, boto3, uuid
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
    return {{'statusCode': 200, 'body': json.dumps({{'job_id': job_id, 'execution_arn': response['executionArn']}})}}
'''.encode()


# --------------------------------------------------------------------------- #
# Provisioning helpers
# --------------------------------------------------------------------------- #

def create_s3_bucket():
    bucket_name = f"{PROJECT_NAME}-artifacts-{ACCOUNT_ID}"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"OK Created S3 bucket: {bucket_name}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"OK S3 bucket already exists: {bucket_name}")
    return bucket_name


def _put_sfn_access(role_name):
    """Allow the start-execution / check-status Lambdas to drive Step Functions."""
    sfn_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["states:StartExecution", "states:DescribeExecution"],
            "Resource": [
                f"arn:aws:states:{REGION}:{ACCOUNT_ID}:stateMachine:{PROJECT_NAME}-*",
                f"arn:aws:states:{REGION}:{ACCOUNT_ID}:execution:{PROJECT_NAME}-*"
            ]
        }]
    }
    iam.put_role_policy(RoleName=role_name, PolicyName='StepFunctionsAccess',
                        PolicyDocument=json.dumps(sfn_policy))


def create_lambda_role():
    role_name = f"{PROJECT_NAME}-lambda-role"
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    try:
        role_arn = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))['Role']['Arn']
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess')
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')
        _put_sfn_access(role_name)
        time.sleep(10)  # role propagation
        print(f"OK Created Lambda role: {role_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        _put_sfn_access(role_name)
        print(f"OK Lambda role already exists: {role_name}")
    return role_arn


def create_sfn_role():
    role_name = f"{PROJECT_NAME}-sfn-role"
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "states.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    try:
        role_arn = iam.create_role(RoleName=role_name, AssumeRolePolicyDocument=json.dumps(trust_policy))['Role']['Arn']
        iam.attach_role_policy(RoleName=role_name, PolicyArn='arn:aws:iam::aws:policy/AWSLambda_FullAccess')
        time.sleep(10)
        print(f"OK Created Step Functions role: {role_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = iam.get_role(RoleName=role_name)['Role']['Arn']
        print(f"OK Step Functions role already exists: {role_name}")
    return role_arn


def create_lambda_function(name, code, handler, role_arn, env_vars=None):
    function_name = f"{PROJECT_NAME}-{name}"
    # Lambda requires a real ZIP archive, not raw source bytes.
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('index.py', code.decode('utf-8'))
    zip_buffer.seek(0)
    zip_content = zip_buffer.read()
    try:
        arn = lambda_client.create_function(
            FunctionName=function_name, Runtime='python3.12', Role=role_arn, Handler=handler,
            Code={'ZipFile': zip_content}, Timeout=300, MemorySize=512,
            Environment={'Variables': env_vars or {}}
        )['FunctionArn']
        print(f"OK Created Lambda: {function_name}")
        return arn
    except lambda_client.exceptions.ResourceConflictException:
        lambda_client.update_function_code(FunctionName=function_name, ZipFile=zip_content)
        arn = lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']
        print(f"OK Updated Lambda: {function_name}")
        return arn


def create_state_machine(sfn_role_arn, improve_arn, image_arn, upscale_arn):
    name = f"{PROJECT_NAME}-workflow"
    definition = {
        "Comment": "Async image generation + upscale pipeline",
        "StartAt": "ImprovePrompt",
        "States": {
            "ImprovePrompt": {"Type": "Task", "Resource": improve_arn, "Next": "GenerateImage"},
            "GenerateImage": {"Type": "Task", "Resource": image_arn, "Next": "UpscaleImage"},
            "UpscaleImage": {"Type": "Task", "Resource": upscale_arn, "End": True}
        }
    }
    try:
        arn = sfn.create_state_machine(name=name, definition=json.dumps(definition),
                                       roleArn=sfn_role_arn, type='STANDARD')['stateMachineArn']
        print(f"OK Created State Machine: {name}")
        return arn
    except sfn.exceptions.StateMachineAlreadyExists:
        arn = next(m['stateMachineArn'] for m in sfn.list_state_machines()['stateMachines'] if m['name'] == name)
        sfn.update_state_machine(stateMachineArn=arn, definition=json.dumps(definition))
        print(f"OK Updated State Machine: {name}")
        return arn


def create_api_gateway(start_arn, status_arn):
    api_name = f"{PROJECT_NAME}-api"
    existing = [a for a in apigateway.get_apis()['Items'] if a['Name'] == api_name]
    if existing:
        api_id = existing[0]['ApiId']
        print(f"OK Reusing existing API: {api_id}")
    else:
        api_id = apigateway.create_api(Name=api_name, ProtocolType='HTTP', Target=start_arn)['ApiId']
        print(f"OK Created API: {api_id}")

    # Unique StatementId PER API ID so re-runs always authorize the current API.
    def grant_invoke(function_arn, suffix):
        fn = function_arn.split(':')[-1]
        try:
            lambda_client.add_permission(
                FunctionName=fn, StatementId=f"apigw-{api_id}-{suffix}",
                Action='lambda:InvokeFunction', Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{api_id}/*/*"
            )
            print(f"OK Granted invoke on {fn} for API {api_id}")
        except lambda_client.exceptions.ResourceConflictException:
            print(f"OK Invoke permission already present on {fn}")

    grant_invoke(start_arn, 'start')
    grant_invoke(status_arn, 'status')

    existing_integrations = {i['IntegrationUri']: i['IntegrationId']
                             for i in apigateway.get_integrations(ApiId=api_id)['Items'] if i.get('IntegrationUri')}

    def ensure_integration(uri):
        if uri in existing_integrations:
            return existing_integrations[uri]
        return apigateway.create_integration(ApiId=api_id, IntegrationType='AWS_PROXY',
                                             IntegrationUri=uri, PayloadFormatVersion='2.0')['IntegrationId']

    start_int = ensure_integration(start_arn)
    status_int = ensure_integration(status_arn)

    existing_routes = {r['RouteKey'] for r in apigateway.get_routes(ApiId=api_id)['Items']}
    if 'POST /generate' not in existing_routes:
        apigateway.create_route(ApiId=api_id, RouteKey='POST /generate', Target=f"integrations/{start_int}")
    if 'GET /status' not in existing_routes:
        apigateway.create_route(ApiId=api_id, RouteKey='GET /status', Target=f"integrations/{status_int}")

    existing_stages = {s['StageName'] for s in apigateway.get_stages(ApiId=api_id)['Items']}
    if 'prod' not in existing_stages:
        apigateway.create_stage(ApiId=api_id, StageName='prod', AutoDeploy=True)

    endpoint = f"https://{api_id}.execute-api.{REGION}.amazonaws.com/prod"
    print(f"OK API ready: {endpoint}")
    return endpoint


def run_end_to_end_test(api_endpoint, prompt="A serene mountain landscape at sunset", timeout=300):
    """Submit one job and poll /status until it completes (or times out)."""
    import urllib.request, urllib.error, urllib.parse
    print("\n" + "=" * 60)
    print("END-TO-END TEST")
    print("=" * 60)
    req = urllib.request.Request(f"{api_endpoint}/generate",
                                 data=json.dumps({"prompt": prompt}).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            job = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"FAIL /generate: HTTP {e.code} - {e.read().decode(errors='replace')}")
        return False
    execution_arn = job["execution_arn"]
    print(f"OK Job started: {job['job_id']}")
    deadline = time.time() + timeout
    while time.time() < deadline:
        url = f"{api_endpoint}/status?execution_arn={urllib.parse.quote(execution_arn)}"
        with urllib.request.urlopen(url, timeout=30) as resp:
            status = json.loads(resp.read())
        state = status.get("status")
        print(f"  status: {state}")
        if state == "SUCCEEDED":
            print(f"OK Artifacts: {json.dumps(status.get('artifacts', {}))}")
            return True
        if state in ("FAILED", "TIMED_OUT", "ABORTED"):
            print(f"FAIL Execution {state}")
            return False
        time.sleep(10)
    print("FAIL Timed out waiting for execution")
    return False


def main(run_test=False):
    print(f"Account ID: {ACCOUNT_ID}")
    print(f"Region: {REGION}")

    bucket = create_s3_bucket()
    lambda_role = create_lambda_role()
    sfn_role = create_sfn_role()

    improve_arn = create_lambda_function('improve-prompt', improve_prompt_code, 'index.lambda_handler', lambda_role)
    image_arn = create_lambda_function('generate-image', generate_image_code, 'index.lambda_handler', lambda_role, {'BUCKET_NAME': bucket})
    upscale_arn = create_lambda_function('upscale-image', upscale_image_code, 'index.lambda_handler', lambda_role, {'BUCKET_NAME': bucket})

    state_machine_arn = create_state_machine(sfn_role, improve_arn, image_arn, upscale_arn)

    start_code = build_start_execution_code(state_machine_arn)
    start_arn = create_lambda_function('start-execution', start_code, 'index.lambda_handler', lambda_role)
    status_arn = create_lambda_function('check-status', check_status_code, 'index.lambda_handler', lambda_role)

    api_endpoint = create_api_gateway(start_arn, status_arn)

    print("\n" + "=" * 60)
    print("INFRASTRUCTURE SETUP COMPLETE")
    print("=" * 60)
    print(f"API Endpoint: {api_endpoint}")
    print(f"S3 Bucket: {bucket}")
    print("\nUsage:")
    print(f"  Start job: POST {api_endpoint}/generate")
    print(f"  Check status: GET {api_endpoint}/status?execution_arn=<arn>")
    print("=" * 60)

    if run_test:
        run_end_to_end_test(api_endpoint)
    return api_endpoint


if __name__ == '__main__':
    main(run_test='--test' in sys.argv)
