# Agentic RAG Patterns: Corrective RAG (CRAG) & Self-RAG

This demo illustrates advanced agentic self-correction patterns for RAG architectures.

> **Presentation References:**
> - Slide 10 (*Corrective RAG (CRAG)*) - *Building Agentic Workflows with RAG on AWS Bedrock*
> - Slide 11 (*Self-RAG Reflection Tokens*) - *Building Agentic Workflows with RAG on AWS Bedrock*
> - Slide 35 (*Agentic Loops & Query Rewriting*) - *Building Agentic Workflows with RAG on AWS Bedrock*

---

## Architectural Flow: Corrective RAG (CRAG)

```
                       +-------------------+
                       |    User Query     |
                       +---------+---------+
                                 |
                                 v
                       +-------------------+
                       | Vector Retrieval  |
                       +---------+---------+
                                 |
                                 v
                       +-------------------+
                       | Chunk Evaluator   | (CORRECT, INCORRECT, AMBIGUOUS)
                       +---------+---------+
                                 |
                     +-----------+-----------+
    Confidence < 0.65|                       | Confidence >= 0.65
                     v                       v
          +--------------------+   +-------------------+
          |   Query Rewriter   |   | Direct Synthesis  |
          +---------+----------+   +-------------------+
                    |
                    v
          +--------------------+
          | Secondary Retrieve |
          +---------+----------+
                    |
                    v
          +--------------------+
          | Synthesis & Output |
          +--------------------+
```

---

## Self-RAG Reflection Tokens

- `[RETRIEVE]`: Determines whether retrieval is necessary (`yes` / `no`).
- `[IS-REL]`: Assesses whether retrieved chunks are relevant to the query.
- `[IS-SUP]`: Assesses factual grounding (`fully_supported` / `partially_supported` / `no_support`).
- `[IS-USE]`: Evaluates utility of the answer (score 1 to 5).

---

## Quickstart

```bash
# Run CLI demo (supports --mock mode)
python crag_and_self_rag.py --mock
```
