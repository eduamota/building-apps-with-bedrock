# Amazon Bedrock Knowledge Bases with S3 Vectors Summary

## Overview

Amazon Bedrock Knowledge Bases with S3 Vectors provides **cost-effective, scalable RAG (Retrieval Augmented Generation)** applications by combining Bedrock's managed knowledge base capabilities with S3's native vector storage.

**Key Innovation**: First cloud object storage with built-in vector support - no need for specialized vector databases.

**Cost Savings**: Up to **90% reduction** in vector upload, storage, and query costs compared to traditional vector databases.

**Status**: Preview (as of July 2025)

## What is S3 Vectors?

S3 Vectors is Amazon S3's native capability to store and query vector embeddings directly in S3 buckets, designed for:

- **Durable storage** of large vector datasets
- **Cost-optimized** storage (pay-as-you-go at low price points)
- **Subsecond query performance** (not millisecond like high-QPS databases)
- **Massive scale** - tens of millions of vectors per index

## Architecture Components

```
Documents (S3) → Bedrock KB → Chunking → Embedding Model → S3 Vector Index → Query
```

### Components:

1. **S3 Data Source** - Store your documents (text, PDF, etc.)
2. **Bedrock Knowledge Base** - Manages ingestion and retrieval
3. **Embedding Model** - Converts text to vectors (e.g., Titan Embeddings V2)
4. **S3 Vector Bucket** - Stores vector embeddings
5. **S3 Vector Index** - Enables similarity search

## Key Features

| Feature | Description |
|---------|-------------|
| **Cost Optimization** | 90% cheaper than traditional vector DBs |
| **Scalability** | Tens of millions of vectors per index |
| **Performance** | Subsecond query latency |
| **Metadata Filtering** | Rich filtering by dates, categories, sources |
| **Durability** | S3's 99.999999999% durability |
| **No Infrastructure** | Fully managed, serverless |
| **Encryption** | SSE-S3 by default, KMS optional |

## When to Use S3 Vectors

### ✅ Ideal For:

- **Large-scale knowledge bases** with millions of documents
- **Historical/archival data** that needs to remain searchable
- **Cost-sensitive applications** with massive vector volumes
- **Applications tolerating subsecond latency** (not millisecond)
- **Long-term storage** of vector datasets

### ❌ Not Ideal For:

- **High QPS requirements** (thousands of queries per second)
- **Millisecond latency requirements**
- **Real-time, high-throughput applications**

## Setup Options

### Option 1: Quick Create (Recommended)

Bedrock automatically creates S3 vector bucket and index during knowledge base creation.

**Pros**: Simplest, fully automated  
**Cons**: Less control over configuration

### Option 2: Use Existing Vector Store

Create S3 vector bucket and index first, then connect to knowledge base.

**Pros**: Full control, reusable across knowledge bases  
**Cons**: More setup steps

## Creating S3 Vector Index (Python)

```python
import boto3

s3vectors = boto3.client('s3vectors', region_name='us-east-1')

# Create vector bucket
response = s3vectors.create_vector_bucket(
    vectorBucketName='my-vector-bucket'
)

# Create vector index
response = s3vectors.create_index(
    vectorBucketName='my-vector-bucket',
    indexName='my-vector-index',
    dimension=1024,  # Must match embedding model
    distanceMetric='cosine',  # or 'euclidean', 'dot_product'
    dataType='float32',
    metadataConfiguration={
        'nonFilterableMetadataKeys': ['AMAZON_BEDROCK_TEXT']  # Large text chunks
    }
)

print(f"Index ARN: {response['indexArn']}")
```

## Creating Knowledge Base with S3 Vectors

```python
import boto3

bedrock = boto3.client('bedrock-agent', region_name='us-east-1')

# Create knowledge base
response = bedrock.create_knowledge_base(
    name='my-knowledge-base',
    description='KB with S3 Vectors',
    roleArn='arn:aws:iam::123456789012:role/BedrockKBRole',
    knowledgeBaseConfiguration={
        'type': 'VECTOR',
        'vectorKnowledgeBaseConfiguration': {
            'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0',
            'embeddingModelConfiguration': {
                'bedrockEmbeddingModelConfiguration': {
                    'dimensions': 1024,  # Must match index dimension
                    'embeddingDataType': 'FLOAT32'
                }
            }
        }
    },
    storageConfiguration={
        'type': 'S3_VECTORS',
        's3VectorsConfiguration': {
            'indexArn': 'arn:aws:s3vectors:us-east-1:123456789012:bucket/my-vector-bucket/index/my-vector-index'
        }
    }
)

kb_id = response['knowledgeBase']['knowledgeBaseId']
print(f"Knowledge Base ID: {kb_id}")
```

## Adding Data Source

```python
# Create data source
response = bedrock.create_data_source(
    knowledgeBaseId=kb_id,
    name='s3-documents',
    dataSourceConfiguration={
        'type': 'S3',
        's3Configuration': {
            'bucketArn': 'arn:aws:s3:::my-documents-bucket',
            'inclusionPrefixes': ['documents/']  # Optional
        }
    },
    vectorIngestionConfiguration={
        'chunkingConfiguration': {
            'chunkingStrategy': 'FIXED_SIZE',
            'fixedSizeChunkingConfiguration': {
                'maxTokens': 300,
                'overlapPercentage': 20
            }
        }
    }
)

data_source_id = response['dataSource']['dataSourceId']
```

## Syncing Data

```python
# Start ingestion job
response = bedrock.start_ingestion_job(
    knowledgeBaseId=kb_id,
    dataSourceId=data_source_id
)

job_id = response['ingestionJob']['ingestionJobId']

# Check status
import time
while True:
    status = bedrock.get_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=data_source_id,
        ingestionJobId=job_id
    )
    
    if status['ingestionJob']['status'] in ['COMPLETE', 'FAILED']:
        print(f"Status: {status['ingestionJob']['status']}")
        break
    
    time.sleep(10)
```

## Querying Knowledge Base

```python
bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# Retrieve only
response = bedrock_runtime.retrieve(
    knowledgeBaseId=kb_id,
    retrievalQuery={'text': 'What is machine learning?'},
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5,
            'overrideSearchType': 'SEMANTIC'  # Only semantic supported for S3 Vectors
        }
    }
)

for result in response['retrievalResults']:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content']['text']}")
    print(f"Location: {result['location']['s3Location']['uri']}")
    print("---")
```

## Retrieve and Generate

```python
# Retrieve and generate response
response = bedrock_runtime.retrieve_and_generate(
    input={'text': 'Explain machine learning'},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb_id,
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0',
            'retrievalConfiguration': {
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        }
    }
)

print(response['output']['text'])
```

## Metadata Filtering

```python
# Query with metadata filters
response = bedrock_runtime.retrieve(
    knowledgeBaseId=kb_id,
    retrievalQuery={'text': 'machine learning'},
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5,
            'filter': {
                'andAll': [
                    {
                        'equals': {
                            'key': 'category',
                            'value': 'technical'
                        }
                    },
                    {
                        'greaterThan': {
                            'key': 'year',
                            'value': 2020
                        }
                    }
                ]
            }
        }
    }
)
```

## IAM Permissions Required

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::my-documents-bucket",
                "arn:aws:s3:::my-documents-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3vectors:GetIndex",
                "s3vectors:QueryVectors",
                "s3vectors:PutVectors",
                "s3vectors:GetVectors",
                "s3vectors:DeleteVectors"
            ],
            "Resource": "arn:aws:s3vectors:*:*:bucket/*/index/*"
        }
    ]
}
```

## Metadata Configuration Best Practices

### Filterable vs Non-Filterable Metadata

- **Filterable** (default): Can be used in query filters (max 2 KB per vector)
- **Non-Filterable**: Cannot be filtered but can store larger data (up to 40 KB per vector)

**Best Practice**: Add `AMAZON_BEDROCK_TEXT` to `nonFilterableMetadataKeys` to store large text chunks while preserving filtering on other attributes.

```python
metadataConfiguration={
    'nonFilterableMetadataKeys': [
        'AMAZON_BEDROCK_TEXT',  # Large document chunks
        'full_content'           # Other large fields
    ]
}
```

### Supported Metadata Types

- **String**: Text values
- **Number**: Numeric values
- **Boolean**: True/False
- **List**: Arrays of values

## Chunking Strategies

| Strategy | Best For | Configuration |
|----------|----------|---------------|
| **Fixed Size** | Predictable token sizing | maxTokens, overlapPercentage |
| **Hierarchical** | Nested document structure | maxParentTokens, maxChildTokens |
| **Semantic** | Meaning-based boundaries | breakpointPercentile, bufferSize |
| **None** | Pre-chunked documents | N/A |

## Embedding Models

| Model | Dimensions | Use Case |
|-------|------------|----------|
| **Titan Text Embeddings V2** | 256, 512, 1024 | General purpose, cost-effective |
| **Titan Multimodal Embeddings** | 1024, 384 | Text + images |
| **Cohere Embed** | 1024 | Multilingual |

**Critical**: Index dimension must match embedding model dimension.

## Cost Comparison

| Service | Storage Cost | Query Cost | Upload Cost |
|---------|--------------|------------|-------------|
| **S3 Vectors** | ~$0.023/GB/month | ~$0.40/million queries | ~$0.40/million vectors |
| **OpenSearch Serverless** | ~$0.24/OCU-hour | Included | Included |
| **Traditional Vector DB** | $$$$ | $$$$ | $$$$ |

**Savings**: Up to 90% with S3 Vectors for large-scale deployments.

## Limitations

- **Preview status** - Features may change
- **Semantic search only** - No hybrid search yet
- **Subsecond latency** - Not millisecond
- **Index immutability** - Cannot change dimension, distance metric, or non-filterable keys after creation
- **10,000 indexes per bucket** maximum
- **Tens of millions of vectors per index** (exact limit not specified)

## Cleanup

```python
# Delete knowledge base
bedrock.delete_knowledge_base(knowledgeBaseId=kb_id)

# Delete S3 vector index
s3vectors.delete_index(
    vectorBucketName='my-vector-bucket',
    indexName='my-vector-index'
)

# Delete S3 vector bucket
s3vectors.delete_vector_bucket(
    vectorBucketName='my-vector-bucket'
)
```

## Use Case Examples

### 1. Enterprise Document Search
- Millions of internal documents
- Long-term archival with search capability
- Cost-sensitive deployment

### 2. Customer Support Knowledge Base
- Historical support tickets and resolutions
- Product documentation
- FAQ database

### 3. Research Paper Repository
- Academic papers with metadata (year, author, topic)
- Semantic search across large corpus
- Metadata filtering by publication date

### 4. Legal Document Analysis
- Case law and legal precedents
- Contract repository
- Compliance documentation

## Best Practices

1. **Match Dimensions**: Ensure index dimension matches embedding model
2. **Optimize Metadata**: Use non-filterable keys for large text chunks
3. **Batch Ingestion**: Upload documents in batches for efficiency
4. **Monitor Costs**: Track storage and query costs
5. **Test Chunking**: Experiment with chunking strategies for your content
6. **Use Filters**: Leverage metadata filtering to improve relevance
7. **Plan for Scale**: S3 Vectors excels at massive scale

## Resources

- **AWS Blog**: Building cost-effective RAG with S3 Vectors
- **Documentation**: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html
- **Bedrock KB Docs**: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- **Sample Notebook**: https://github.com/aws-samples/amazon-bedrock-samples

---

**Last Updated**: December 2025  
**Status**: Preview  
**Recommended For**: Large-scale, cost-sensitive RAG applications
