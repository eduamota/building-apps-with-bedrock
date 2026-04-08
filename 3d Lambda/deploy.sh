#!/bin/bash

# Configuration
FUNCTION_NAME="strands-agent-lambda"
ROLE_NAME="strands-agent-lambda-role"
REGION="us-east-1"
RUNTIME="python3.12"
TIMEOUT=60
MEMORY=512
LAYER_ARN="arn:aws:lambda:us-east-1:856699698935:layer:strands-agents-py3_12-x86_64:1"

echo "🚀 Deploying Strands Agent to Lambda..."

# Create deployment package (just the handler code)
echo "📦 Creating deployment package..."
cd "$(dirname "$0")"
rm -f agent-deployment.zip
zip -j agent-deployment.zip agent_handler.py

echo "✅ Deployment package created"

# Check if IAM role exists
echo "🔍 Checking IAM role..."
if ! aws iam get-role --role-name $ROLE_NAME 2>/dev/null; then
    echo "📝 Creating IAM role..."
    
    # Create trust policy
    cat > /tmp/trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

    # Create role
    aws iam create-role \
        --role-name $ROLE_NAME \
        --assume-role-policy-document file:///tmp/trust-policy.json \
        --region $REGION

    # Attach policies
    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    aws iam attach-role-policy \
        --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

    echo "⏳ Waiting for role to propagate..."
    sleep 10
    
    rm /tmp/trust-policy.json
fi

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
echo "✅ Using role: $ROLE_ARN"

# Check if function exists
if aws lambda get-function --function-name $FUNCTION_NAME --region $REGION 2>/dev/null; then
    echo "🔄 Updating existing function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://agent-deployment.zip \
        --region $REGION
    
    aws lambda update-function-configuration \
        --function-name $FUNCTION_NAME \
        --timeout $TIMEOUT \
        --memory-size $MEMORY \
        --layers $LAYER_ARN \
        --region $REGION
else
    echo "🆕 Creating new function..."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime $RUNTIME \
        --role $ROLE_ARN \
        --handler agent_handler.handler \
        --zip-file fileb://agent-deployment.zip \
        --timeout $TIMEOUT \
        --memory-size $MEMORY \
        --layers $LAYER_ARN \
        --region $REGION
    
    # Wait for function to be active
    echo "⏳ Waiting for function to be active..."
    aws lambda wait function-active --function-name $FUNCTION_NAME --region $REGION
fi

echo "✅ Lambda function deployed successfully!"

# Create function URL if it doesn't exist
echo ""
echo "🌐 Creating Lambda Function URL..."

if ! aws lambda get-function-url-config --function-name $FUNCTION_NAME --region $REGION 2>/dev/null; then
    aws lambda create-function-url-config \
        --function-name $FUNCTION_NAME \
        --auth-type NONE \
        --cors '{
            "AllowOrigins": ["*"],
            "AllowMethods": ["POST", "GET"],
            "AllowHeaders": ["content-type"],
            "MaxAge": 86400
        }' \
        --region $REGION
    
    # Add permission for public access
    aws lambda add-permission \
        --function-name $FUNCTION_NAME \
        --statement-id FunctionURLAllowPublicAccess \
        --action lambda:InvokeFunctionUrl \
        --principal "*" \
        --function-url-auth-type NONE \
        --region $REGION 2>/dev/null || true
fi

FUNCTION_URL=$(aws lambda get-function-url-config --function-name $FUNCTION_NAME --region $REGION --query 'FunctionUrl' --output text)

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Function ARN:"
aws lambda get-function --function-name $FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text

echo ""
echo "📍 Function URL:"
echo "$FUNCTION_URL"

echo ""
echo "🧪 Test with AWS CLI:"
echo "aws lambda invoke --function-name $FUNCTION_NAME --payload '{\"prompt\": \"What is AI?\"}' --region $REGION response.json && cat response.json"

echo ""
echo "🧪 Test with curl:"
echo "curl -X POST $FUNCTION_URL -H 'Content-Type: application/json' -d '{\"prompt\": \"What is AI?\"}'"

# Cleanup
rm -f agent-deployment.zip

echo ""
echo "✨ Done!"
