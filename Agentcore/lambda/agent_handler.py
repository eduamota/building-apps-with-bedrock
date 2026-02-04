from strands import Agent
from strands.models import BedrockModel
from typing import Dict, Any
import json

# Define system prompt
SYSTEM_PROMPT = """You are a helpful AI assistant. Provide concise, accurate responses."""

def handler(event: Dict[str, Any], _context) -> Any:
    """
    Lambda handler for Strands agent.
    Supports both direct invocation and Function URL (API Gateway format).
    
    Expected event formats:
    Direct: {"prompt": "user question"}
    Function URL: {"body": "{\"prompt\": \"user question\"}"}
    """
    try:
        # Handle Function URL format (body is JSON string)
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            prompt = body.get('prompt', '')
            
            # Function URL response format
            agent = Agent(
                system_prompt=SYSTEM_PROMPT,
                model=BedrockModel(model_id="us.amazon.nova-micro-v1:0", region="us-east-1")
            )
            
            response = agent(prompt)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'response': str(response)})
            }
        else:
            # Direct invocation format
            agent = Agent(
                system_prompt=SYSTEM_PROMPT,
                model=BedrockModel(model_id="us.amazon.nova-micro-v1:0", region="us-east-1")
            )
            
            response = agent(event.get('prompt', ''))
            return str(response)
            
    except Exception as e:
        if 'body' in event:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        else:
            raise
