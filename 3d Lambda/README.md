# Strands Agent Lambda Deployment

Deploy a Strands AI agent to AWS Lambda with a public Function URL.

## Prerequisites

- AWS CLI configured with credentials
- Python 3.12
- IAM permissions for Lambda, IAM roles, and Bedrock

## Project Structure

```
lambda/
├── agent_handler.py    # Strands agent Lambda handler
├── requirements.txt    # Python dependencies
├── deploy.sh          # Deployment script
└── README.md          # This file
```

## Quick Start

### 1. Deploy

```bash
cd lambda
./deploy.sh
```

The script will:
- Create IAM role with Bedrock permissions
- Package the agent code
- Deploy to Lambda using official Strands layer
- Create a public Function URL
- Display the Function URL for testing

### 2. Test

**Using AWS CLI:**
```bash
aws lambda invoke \
  --function-name strands-agent-lambda \
  --cli-binary-format raw-in-base64-out \
  --payload '{"prompt": "What is AI?"}' \
  --region us-east-1 \
  response.json && cat response.json
```

**Using curl (Function URL):**
```bash
curl -X POST https://YOUR-FUNCTION-URL.lambda-url.us-east-1.on.aws/ \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What is AI?"}'
```

**Using httpie:**
```bash
http POST https://YOUR-FUNCTION-URL.lambda-url.us-east-1.on.aws/ \
  prompt="What is AI?"
```

## Configuration

Edit `agent_handler.py` to customize:

- **System Prompt**: Change `SYSTEM_PROMPT` variable
- **Model**: Change `model_id` (e.g., `us.amazon.nova-lite-v1:0`)
- **Region**: Change `region` parameter

Edit `deploy.sh` to customize:

- `FUNCTION_NAME`: Lambda function name
- `ROLE_NAME`: IAM role name
- `TIMEOUT`: Function timeout (default: 60s)
- `MEMORY`: Memory allocation (default: 512MB)
- `LAYER_ARN`: Strands Lambda layer ARN

## Lambda Layer

Uses official Strands Lambda layer:
```
arn:aws:lambda:us-east-1:856699698935:layer:strands-agents-py3_12-x86_64:1
```

Available for:
- Python: 3.10, 3.11, 3.12, 3.13
- Architectures: x86_64, aarch64
- Regions: All major AWS regions

## Event Formats

**Direct Invocation:**
```json
{
  "prompt": "Your question here"
}
```

**Function URL (HTTP):**
```json
{
  "prompt": "Your question here"
}
```

**Response Format:**
```json
{
  "response": "Agent's answer here"
}
```

## Adding Tools

To add tools to your agent, modify `agent_handler.py`:

```python
from strands import Agent, tool
from strands.models import BedrockModel

@tool
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Weather in {city}: Sunny, 72°F"

def handler(event, _context):
    agent = Agent(
        system_prompt="You are a helpful assistant with weather tools.",
        model=BedrockModel(model_id="us.amazon.nova-micro-v1:0", region="us-east-1"),
        tools=[get_weather]  # Add tools here
    )
    # ... rest of handler
```

Then redeploy:
```bash
./deploy.sh
```

## Cleanup

To delete the Lambda function and role:

```bash
# Delete function
aws lambda delete-function \
  --function-name strands-agent-lambda \
  --region us-east-1

# Detach policies
aws iam detach-role-policy \
  --role-name strands-agent-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam detach-role-policy \
  --role-name strands-agent-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Delete role
aws iam delete-role \
  --role-name strands-agent-lambda-role
```

## Troubleshooting

**Import Error:**
- Ensure the Strands layer is attached
- Check handler name is `agent_handler.handler`

**Timeout:**
- Increase timeout in `deploy.sh` (max 900s)
- Optimize system prompt for faster responses

**Bedrock Access Denied:**
- Verify IAM role has `AmazonBedrockFullAccess` policy
- Check model ID is correct for your region

**Function URL 500 Error:**
- Check CloudWatch Logs: `/aws/lambda/strands-agent-lambda`
- Verify event format matches expected structure

## Resources

- [Strands Agents Documentation](https://strandsagents.com)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon Bedrock Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
