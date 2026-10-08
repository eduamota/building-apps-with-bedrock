# Text-to-SQL Agent Tool with AST Read-Only Validation

Demonstrates a secure, enterprise-grade Text-to-SQL agent pipeline with defense-in-depth AST validation and database authorizer enforcement.

> **Presentation Reference:** Slide 33 (*"Building Agentic Workflows with RAG on AWS Bedrock"*)

---

## 4-Step Pipeline Architecture

```
  +--------------------+
  | 1. Schema Inspect  | Introspects tables, columns, primary/foreign keys
  +---------+----------+
            |
            v
  +--------------------+
  |  2. SQL Generator  | Bedrock Claude/Nova translates query based on schema
  +---------+----------+
            |
            v
  +--------------------+
  | 3. AST Validator   | Strict Read-Only Validation:
  |                    | - Permits only SELECT / WITH ... SELECT
  |                    | - Rejects DML (INSERT, UPDATE, DELETE)
  |                    | - Rejects DDL (DROP, ALTER, CREATE, TRUNCATE)
  |                    | - Blocks comments and multi-statement chaining
  +---------+----------+
            | (Passed)
            v
  +--------------------+
  | 4. Database Exec   | Executes with SQLite / Aurora DB authorizer restrictions
  +--------------------+
```

---

## Quickstart

```bash
# Run CLI demo (supports --mock mode)
python text_to_sql_agent.py --mock
```
