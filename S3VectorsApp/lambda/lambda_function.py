import json
import boto3
import os
import time
from typing import List, Dict, Any

# Initialize clients
bedrock_runtime = boto3.client('bedrock-runtime')
s3vectors = boto3.client('s3vectors')

# Environment variables
VECTOR_BUCKET = os.environ['VECTOR_BUCKET']
VECTOR_INDEX = os.environ['VECTOR_INDEX']
EMBEDDING_MODEL = os.environ['EMBEDDING_MODEL']

def get_embedding(text: str) -> List[float]:
    """Get embedding using Titan model"""
    response = bedrock_runtime.invoke_model(
        modelId=EMBEDDING_MODEL,
        body=json.dumps({"inputText": text})
    )
    return json.loads(response['body'].read())['embedding']

def ensure_vector_infrastructure():
    """Ensure vector bucket and index exist"""
    try:
        # Try to create bucket (idempotent)
        try:
            s3vectors.create_vector_bucket(vectorBucketName=VECTOR_BUCKET)
        except s3vectors.exceptions.ConflictException:
            pass  # Bucket already exists
        
        # Try to create index (idempotent)
        try:
            s3vectors.create_index(
                vectorBucketName=VECTOR_BUCKET,
                indexName=VECTOR_INDEX,
                dataType="float32",
                dimension=1536,
                distanceMetric="cosine"
            )
        except s3vectors.exceptions.ConflictException:
            pass  # Index already exists
            
    except Exception as e:
        print(f"Error ensuring infrastructure: {str(e)}")

def add_document(document_id: str, title: str, content: str) -> Dict[str, Any]:
    """Add document to S3 Vectors"""
    try:
        ensure_vector_infrastructure()
        
        # Generate embedding
        embedding = get_embedding(content)
        
        # Store in S3 Vectors
        s3vectors.put_vectors(
            vectorBucketName=VECTOR_BUCKET,
            indexName=VECTOR_INDEX,
            vectors=[{
                "key": document_id,
                "data": {
                    "float32": embedding
                },
                "metadata": {
                    "title": title,
                    "content": content,
                    "timestamp": str(int(time.time()))
                }
            }]
        )
        
        return {
            "success": True,
            "message": f"Document {document_id} added successfully",
            "document_id": document_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def search_documents(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search documents in S3 Vectors"""
    try:
        # Generate query embedding
        query_embedding = get_embedding(query)
        
        # Search vectors
        response = s3vectors.query_vectors(
            vectorBucketName=VECTOR_BUCKET,
            indexName=VECTOR_INDEX,
            queryVector={"float32": query_embedding},
            topK=max_results,
            returnMetadata=True,
            returnDistance=True
        )
        
        results = []
        for result in response['vectors']:
            results.append({
                "document_id": result['key'],
                "title": result['metadata']['title'],
                "content": result['metadata']['content'],
                "score": 1 - result['distance'],  # Convert distance to similarity
                "timestamp": result['metadata'].get('timestamp', '')
            })
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def ask_question(question):
    """Ask a question using RAG with S3 Vectors and Nova Pro"""
    try:
        # Get embedding for question
        embedding_response = bedrock_runtime.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body=json.dumps({"inputText": question})
        )
        query_embedding = json.loads(embedding_response['body'].read())['embedding']
        
        # Search vectors
        response = s3vectors.query_vectors(
            vectorBucketName=VECTOR_BUCKET,
            indexName=VECTOR_INDEX,
            queryVector={"float32": query_embedding},
            topK=3,
            returnMetadata=True,
            returnDistance=True
        )
        
        # Build context from search results
        context = "\n".join([f"Document: {v['metadata']['title']}\nContent: {v['metadata']['content']}" 
                           for v in response['vectors']])
        
        # Generate answer with Nova Pro
        prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        
        nova_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-pro-v1:0',
            body=json.dumps({
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
                "inferenceConfig": {"maxTokens": 500, "temperature": 0.7}
            })
        )
        
        answer = json.loads(nova_response['body'].read())['output']['message']['content'][0]['text']
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources": [{"title": v['metadata']['title'], "score": 1 - v['distance']} 
                       for v in response['vectors']]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        # Parse request
        http_method = event['httpMethod']
        path = event['path']
        
        # Health check
        if path == '/health':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'S3 Vectors API',
                    'timestamp': int(time.time())
                })
            }
        
        # Add document
        elif path == '/documents' and http_method == 'POST':
            body = json.loads(event['body'])
            document_id = body.get('id', f"doc_{int(time.time())}")
            title = body.get('title', '')
            content = body.get('content', '')
            
            if not content:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Content is required'})
                }
            
            result = add_document(document_id, title, content)
            status_code = 200 if result['success'] else 500
            
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
        
        # Search documents
        elif path == '/search' and http_method == 'GET':
            query_params = event.get('queryStringParameters', {}) or {}
            query = query_params.get('q', '')
            max_results = int(query_params.get('max_results', 5))
            
            if not query:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Query parameter "q" is required'})
                }
            
            result = search_documents(query, max_results)
            status_code = 200 if result['success'] else 500
            
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
        
        # Ask question (RAG)
        elif path == '/ask' and http_method == 'POST':
            body = json.loads(event['body'])
            question = body.get('question', '')
            
            if not question:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Question is required'})
                }
            
            result = ask_question(question)
            status_code = 200 if result['success'] else 500
            
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
