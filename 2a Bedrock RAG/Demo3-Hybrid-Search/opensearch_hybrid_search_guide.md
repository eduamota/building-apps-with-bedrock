# OpenSearch Hybrid Search with FAISS and HNSW

## Overview

This document explains the OpenSearch Hybrid Search solution that combines BM25 keyword search with k-NN vector similarity search using Amazon Bedrock embeddings.

## Architecture Diagrams

### 1. Full Hybrid Search Architecture

![Hybrid Search Architecture](opensearch_flow.png)

The complete hybrid search flow combines both lexical and semantic search:

1. **Query Input** → User submits a search query
2. **Amazon Bedrock** → Converts query text into a 1024-dimensional embedding vector
3. **OpenSearch Hybrid Search** → Processes query through two parallel paths:
   - BM25 keyword search (30% weight) for exact matches
   - k-NN vector search (70% weight) for semantic similarity
   - Normalization pipeline combines both scores
4. **Ranked Results** → Returns unified, relevance-ranked results

### 2. BM25 Keyword Search Only

![BM25 Search Flow](bm25_search_flow.png)

Traditional lexical search approach:

1. **User Query** → Plain text search query (e.g., "machine learning")
2. **OpenSearch BM25** → Keyword matching algorithm that:
   - Searches across text fields (title and content)
   - Applies field boosting (title^2 gets double weight)
   - Uses term frequency and document frequency scoring
3. **Ranked Results** → Documents scored based on keyword relevance

This is pure lexical matching - it finds documents containing the exact query terms without understanding semantic meaning.

### 3. k-NN Vector Search Only

![k-NN Vector Search Flow](knn_vector_search_flow.png)

Semantic search approach:

1. **User Query** → Plain text query (e.g., "machine learning")
2. **Amazon Bedrock** → Converts query into a 1024-dimensional embedding vector using Titan Embed v2 model
3. **OpenSearch k-NN** → Vector similarity search that:
   - Uses FAISS with HNSW algorithm for efficient nearest neighbor search
   - Calculates cosine similarity between query vector and document vectors
   - Finds semantically related content (not just keyword matches)
4. **Ranked Results** → Documents scored by semantic similarity

This approach understands meaning and context rather than just matching keywords. For example, a query about "ML" could find documents about "machine learning" or "artificial intelligence" even without those exact terms.

---

## FAISS (Facebook AI Similarity Search)

### What is FAISS?

FAISS is an open-source library developed by Meta (formerly Facebook) designed to efficiently search through billions of high-dimensional vectors. Traditional databases struggle with similarity searches because they're optimized for exact matches (like SQL queries), not for finding "near neighbors" in vector space.

### Core Capabilities

- **Scalability**: Handles datasets from thousands to billions of vectors
- **Flexibility**: Supports both exact and approximate nearest neighbor search
- **Multiple Indexes**: Offers various indexing methods (IVF, PQ, HNSW) for different speed-accuracy tradeoffs
- **GPU Acceleration**: Faster processing with GPU support
- **Memory Efficiency**: Compression techniques to reduce memory footprint

### Key Indexing Methods

FAISS provides several indexing strategies:

1. **Flat**: Brute-force exact search (slowest but most accurate)
2. **IVF (Inverted File Index)**: Clusters vectors into groups and searches only relevant clusters
3. **PQ (Product Quantization)**: Compresses vectors into smaller codes while preserving similarity
4. **HNSW**: Graph-based approximate search (fast and accurate)

---

## HNSW (Hierarchical Navigable Small World)

### What is HNSW?

HNSW is a graph-based algorithm that organizes vectors into a multi-layered proximity graph structure. Think of it like a highway system with different levels of roads.

### Hierarchical Layer Structure

HNSW builds multiple graph layers:

- **Top layers** (sparse): Few nodes with long connections, like highways for fast traversal across the vector space
- **Middle layers**: Progressively denser with shorter connections
- **Bottom layer (Layer 0)**: Contains all vectors with shortest, most precise connections

### How the Hierarchy Works

Each vector is assigned to layers probabilistically using exponential decay:

- Most vectors exist only in Layer 0 (bottom)
- Fewer vectors reach middle layers
- Very few vectors reach the top layer
- This creates natural "expressways" at higher levels

### HNSW Search Process

When searching for similar vectors:

1. **Start at top layer**: Enter at a predefined entry point with long-range connections
2. **Greedy traversal**: Move to the nearest neighbor at each step (like following highway exits)
3. **Find local minimum**: When no closer node exists in current layer
4. **Descend**: Drop to the same node in the layer below
5. **Repeat**: Continue until reaching Layer 0
6. **Final result**: Return the k-nearest neighbors found at the bottom layer

This "zoom out, then zoom in" approach dramatically reduces comparisons. Instead of comparing against all vectors (brute force), you navigate efficiently through the graph structure.

### Small World Property

The "small world" aspect means that any two nodes can be reached through a short path of connections. This ensures fast navigation even in massive datasets, similar to the "six degrees of separation" concept in social networks.

---

## Why OpenSearch Uses FAISS with HNSW

### Configuration in Code

```python
'method': {
    'engine': 'faiss',
    'name': 'hnsw',
    'space_type': 'cosinesimil'  # Cosine similarity metric
}
```

### Performance Benefits

- **Speed**: HNSW graph traversal is much faster than brute-force search
- **Scalability**: Handles millions to billions of vectors efficiently
- **Accuracy**: Maintains high recall (finding the right neighbors)
- **Memory efficiency**: FAISS optimizes memory usage through indexing strategies

### Trade-offs

- **Build time**: Creating the HNSW graph takes longer than simple flat indexes
- **Memory**: All data must fit in RAM for optimal performance
- **Approximate results**: Returns near-neighbors, not guaranteed exact matches (acceptable for most ML applications)

### Configuration Parameters

The implementation uses:

- **1024-dimensional vectors**: Each document embedding has 1024 numbers
- **Cosine similarity**: Distance measured using angle between vectors
- **HNSW graph**: Navigates the 1024-dimensional space efficiently
- **Hierarchical structure**: Makes searches feasible even though visualizing 1024 dimensions is impossible

This combination provides sub-millisecond query times even with thousands of documents, and scales to millions with proper tuning.

---

## Hybrid Search Implementation

### Index Configuration

```python
index_body = {
    'settings': {
        'index.knn': True
    },
    'mappings': {
        'properties': {
            'vector': {
                'type': 'knn_vector',
                'dimension': 1024,
                'method': {
                    'engine': 'faiss',
                    'name': 'hnsw',
                    'space_type': 'cosinesimil'
                }
            },
            'text': {
                'type': 'text'
            }
        }
    }
}
```

### Normalization Pipeline

The hybrid search uses a normalization pipeline to combine scores from both search methods:

```python
pipeline_body = {
    "description": "Hybrid search normalization pipeline",
    "phase_results_processors": [
        {
            "normalization-processor": {
                "normalization": {
                    "technique": "min_max"
                },
                "combination": {
                    "technique": "arithmetic_mean",
                    "parameters": {
                        "weights": [0.3, 0.7]  # BM25: 0.3, Vector: 0.7
                    }
                }
            }
        }
    ]
}
```

### Weighting Strategy

- **BM25 weight: 0.3** - Captures exact keyword matches and specific terminology
- **k-NN weight: 0.7** - Emphasizes semantic understanding and contextual relevance

This weighting favors semantic relevance while still capturing exact keyword matches, providing the best of both worlds.

---

## Use Cases and Benefits

### When Hybrid Search Excels

1. **Ambiguous queries**: Understanding user intent beyond exact words
2. **Synonyms and variations**: Finding "ML" when searching for "machine learning"
3. **Conceptual searches**: Locating documents about related concepts
4. **Multilingual content**: Semantic similarity across languages
5. **Technical documentation**: Combining exact term matching with conceptual understanding

### Performance Characteristics

- **Query latency**: Sub-millisecond to single-digit milliseconds
- **Scalability**: Millions of documents with proper infrastructure
- **Accuracy**: Higher relevance scores compared to single-method approaches
- **Flexibility**: Adjustable weights for different use cases

---

## Security Components

The OpenSearch Serverless implementation includes three security layers:

1. **Network Policy**: Controls public/private access to the collection
2. **Encryption Policy**: Uses AWS-owned keys for data encryption at rest
3. **Data Access Policy**: Granular permissions for collection and index operations

---

## RAG (Retrieval-Augmented Generation) Integration

The hybrid search serves as the retrieval component in a complete RAG pipeline:

1. **Retrieval**: Hybrid search finds the most relevant documents
2. **Context Building**: Top results are formatted as context
3. **Generation**: Amazon Bedrock (Nova Pro) generates comprehensive answers using the retrieved context
4. **Citation**: Source documents are provided with relevance scores

This approach ensures AI-generated responses are grounded in actual, relevant data from your document collection.

---

## Conclusion

The combination of FAISS and HNSW in OpenSearch Serverless provides a powerful foundation for hybrid search. By leveraging both lexical (BM25) and semantic (k-NN) search methods with intelligent score normalization, the system delivers highly relevant results that understand both exact terminology and contextual meaning.

This architecture scales efficiently, maintains high accuracy, and provides the flexibility needed for production RAG applications and advanced search use cases.
