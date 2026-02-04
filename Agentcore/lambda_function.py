import json
from strands import Agent
from strands.models import BedrockModel

# Initialize agent
agent = Agent(
    name="lambda_agent",
    system_prompt="You are a helpful assistant. Provide concise, accurate responses.",
    model=BedrockModel(model_id="us.amazon.nova-micro-v1:0", region="us-east-1")
)

def lambda_handler(event, context):
    """
    Lambda handler for Strands agent.
    
    Expected event format:
    {
        "query": "user question here",
        "session_id": "optional-session-id"
    }
    """
    try:
        # Extract query from event
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event
        query = body.get('query', body.get('message', ''))
        session_id = body.get('session_id')
        
        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No query provided'})
            }
        
        # Call agent
        if session_id:
            response = agent(query, session_id=session_id)
        else:
            response = agent(query)
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': str(response),
                'session_id': session_id
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
