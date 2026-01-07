# S3 Vectors RAG Application

A complete serverless RAG (Retrieval-Augmented Generation) application using Amazon S3 Vectors, AWS Lambda, and Amazon Bedrock Nova Pro.

## Architecture

- **S3 Vectors**: Native AWS vector storage for document embeddings
- **AWS Lambda**: Serverless compute for API operations
- **API Gateway**: RESTful API with authentication
- **Amazon Bedrock**: Titan embeddings + Nova Pro for RAG
- **Streamlit**: Chat interface UI

## API Endpoints

All endpoints require API key authentication via `x-api-key` header.

- `GET /health` - Health check
- `POST /documents` - Add documents with embeddings
- `GET /search?q=query&max_results=5` - Vector similarity search
- `POST /ask` - RAG question answering

## Quick Start

### 1. Deploy Infrastructure

```bash
# Install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Deploy with CDK
cdk bootstrap
cdk deploy
```

### 2. Get API Key

After deployment, get the API key:
```bash
aws apigateway get-api-key --api-key <API_KEY_ID> --include-value --region us-east-1
```

### 3. Add Documents

```bash
curl -X POST https://<API_ENDPOINT>/prod/documents \
  -H "Content-Type: application/json" \
  -H "x-api-key: <YOUR_API_KEY>" \
  -d '{"id":"doc1","title":"AWS Lambda Guide","content":"AWS Lambda is a serverless compute service..."}'
```

### 4. Ask Questions

```bash
curl -X POST https://<API_ENDPOINT>/prod/ask \
  -H "Content-Type: application/json" \
  -H "x-api-key: <YOUR_API_KEY>" \
  -d '{"question":"What is serverless computing?"}'
```

### 5. Run Streamlit UI

```bash
pip install -r requirements-ui.txt
export API_KEY=<YOUR_API_KEY>
streamlit run streamlit_app.py
```

## Configuration

Environment variables in Lambda:
- `VECTOR_BUCKET`: S3 Vectors bucket name
- `VECTOR_INDEX`: Vector index name
- `EMBEDDING_MODEL`: Bedrock embedding model

## Security

- API key authentication on all endpoints
- Rate limiting: 100 req/sec, 10K req/day
- IAM roles with least privilege access
- CORS enabled for web clients

## Cost Optimization

- Serverless architecture (pay per use)
- S3 Vectors (no vector DB infrastructure)
- Efficient embedding caching
- Usage plan limits prevent overuse

## Cleanup

```bash
cdk destroy
```
