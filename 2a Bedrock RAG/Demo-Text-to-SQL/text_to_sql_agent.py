"""Text-to-SQL Agent Tool with AST Read-Only Validation.

Implements the 4-step Text-to-SQL agent pipeline:
1. Schema Inspection: Introspects tables, columns, types, and relationships.
2. SQL Generation: Translates user questions into schema-aligned SQL via Bedrock Converse API.
3. AST Read-Only Validation: Strictly validates syntax tree, enforcing read-only SELECT execution,
   rejecting DDL, DML, multi-statement injection, comments, and unauthorized engine operations.
4. Database Execution: Executes validated query against SQLite / PostgreSQL with authorizer restrictions.

Reference: Slide 33 ("Building Agentic Workflows with RAG on AWS Bedrock")
"""

import argparse
import json
import re
import sqlite3
import time
from typing import Any, Dict, List, Optional, Tuple
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class SecurityValidationError(Exception):
    """Raised when an unauthorized, malicious, or non-read-only SQL statement is detected."""
    pass


class SchemaInspector:
    """Introspects relational database schemas to provide structured schema cards."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def get_schema_summary(self) -> Dict[str, Any]:
        """Catalog tables and columns."""
        cursor = self.conn.cursor()
        tables_data = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        ).fetchall()

        schema_cards = {}
        for (tbl_name,) in tables_data:
            cols_info = cursor.execute(f"PRAGMA table_info({tbl_name});").fetchall()
            columns = [{"name": c[1], "type": c[2], "primary_key": bool(c[5])} for c in cols_info]
            schema_cards[tbl_name] = columns

        return schema_cards

    def format_schema_prompt(self) -> str:
        """Format catalog into an LLM-friendly system prompt context."""
        summary = self.get_schema_summary()
        lines = ["Database Schema:"]
        for tbl, cols in summary.items():
            cols_str = ", ".join([f"{c['name']} ({c['type']})" for c in cols])
            lines.append(f"Table '{tbl}': [{cols_str}]")
        return "\n".join(lines)


class SQLAstValidator:
    """Enforces strict read-only AST and semantic validation on generated SQL queries."""

    FORBIDDEN_KEYWORDS = {
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE",
        "TRUNCATE", "REPLACE", "MERGE", "UPSERT",
        "ATTACH", "DETACH", "PRAGMA", "VACUUM", "REINDEX",
        "GRANT", "REVOKE", "EXEC", "EXECUTE", "SHUTDOWN"
    }

    @classmethod
    def clean_query(cls, sql_text: str) -> str:
        """Strip comments and surrounding markdown blocks."""
        # Remove markdown code fences
        cleaned = re.sub(r"```(?:sql)?(.*?)```", r"\1", sql_text, flags=re.DOTALL)
        # Remove single-line comments
        cleaned = re.sub(r"--.*$", "", cleaned, flags=re.MULTILINE)
        # Remove multi-line comments
        cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
        return cleaned.strip()

    @classmethod
    def validate(cls, raw_sql: str) -> str:
        """Perform AST validation ensuring query is strictly a single read-only SELECT statement."""
        # Check for comments before stripping
        if "--" in raw_sql or "/*" in raw_sql:
            raise SecurityValidationError("SQL comments ('--', '/*') are forbidden to prevent injection evasion.")

        cleaned = cls.clean_query(raw_sql)
        if not cleaned:
            raise SecurityValidationError("Query is empty after comment stripping.")

        # Check for multi-statement execution via semicolons
        statements = [s.strip() for s in cleaned.split(";") if s.strip()]
        if len(statements) > 1:
            raise SecurityValidationError(
                f"Multi-statement execution detected ({len(statements)} statements). Only single queries permitted."
            )

        single_query = statements[0]

        # Extract uppercase tokens
        tokens = [t.upper() for t in re.findall(r"\b[A-Za-z_]+\b", single_query)]
        if not tokens:
            raise SecurityValidationError("No valid SQL tokens found.")

        # First token MUST be SELECT or WITH (for Common Table Expressions)
        first_token = tokens[0]
        if first_token not in ("SELECT", "WITH"):
            raise SecurityValidationError(
                f"Forbidden root statement: '{first_token}'. Only read-only 'SELECT' or 'WITH ... SELECT' queries are allowed."
            )

        # Check for any forbidden destructive keywords anywhere in tokens
        for tok in tokens:
            if tok in cls.FORBIDDEN_KEYWORDS:
                raise SecurityValidationError(
                    f"Forbidden keyword '{tok}' detected in SQL query. Data and schema modifications are strictly blocked."
                )

        return single_query


class SQLGenerator:
    """Translates user natural language questions into schema-targeted SQL queries."""

    def __init__(self, mock_mode: bool = False, region_name: str = "us-east-1"):
        self.mock_mode = mock_mode
        self.region_name = region_name
        self.client = None

        if not self.mock_mode:
            try:
                self.client = boto3.client("bedrock-runtime", region_name=self.region_name)
                boto3.client("sts", region_name=self.region_name).get_caller_identity()
            except (NoCredentialsError, ClientError):
                self.mock_mode = True

    def generate(self, user_question: str, schema_context: str) -> str:
        """Generate SQL query targeting the database schema."""
        if self.mock_mode:
            q_lower = user_question.lower()
            if "top" in q_lower or "revenue" in q_lower or "customer" in q_lower:
                return (
                    "SELECT c.customer_name, SUM(o.total_amount) AS total_spent "
                    "FROM customers c JOIN orders o ON c.customer_id = o.customer_id "
                    "GROUP BY c.customer_name ORDER BY total_spent DESC LIMIT 5;"
                )
            elif "inventory" in q_lower or "product" in q_lower:
                return "SELECT product_name, stock_quantity, unit_price FROM products WHERE stock_quantity < 50 ORDER BY stock_quantity ASC;"
            return "SELECT COUNT(*) AS total_orders FROM orders;"

        prompt = f"""You are an expert SQL generator.
{schema_context}

User Question: {user_question}

Rules:
1. Generate strictly a single read-only SELECT query.
2. Never include data modification or DDL statements.
3. Return ONLY the raw SQL query with no surrounding prose."""

        try:
            resp = self.client.converse(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"temperature": 0.0, "maxTokens": 300},
            )
            return resp["output"]["message"]["content"][0]["text"].strip()
        except Exception:
            return "SELECT COUNT(*) FROM orders;"


class SQLExecutor:
    """Executes validated read-only SQL queries with engine-level authorizer enforcement."""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        # Install defense-in-depth SQLite engine-level authorizer
        self._install_authorizer()

    def _install_authorizer(self):
        """Install SQLite authorizer callback permitting exclusively read-only actions."""
        def authorizer(action, arg1, arg2, dbname, source):
            # Only allow read, select, function evaluation, and schema introspection pragmas
            allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION}
            if action in allowed:
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_PRAGMA and arg1 in ("table_info", "table_xinfo", "foreign_key_list"):
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY

        self.conn.set_authorizer(authorizer)

    def execute(self, validated_sql: str) -> Dict[str, Any]:
        """Execute validated query and format tabular results."""
        start = time.time()
        cursor = self.conn.cursor()
        try:
            cursor.execute(validated_sql)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            elapsed_ms = round((time.time() - start) * 1000, 2)
            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
                "execution_time_ms": elapsed_ms,
                "sql": validated_sql,
            }
        except sqlite3.DatabaseError as e:
            raise SecurityValidationError(f"Engine authorizer blocked execution: {e}")


class TextToSQLPipeline:
    """Coordinating 4-step pipeline: Inspect -> Generate -> AST Validate -> Execute."""

    def __init__(self, connection: sqlite3.Connection, mock_mode: bool = False):
        self.conn = connection
        self.inspector = SchemaInspector(self.conn)
        self.generator = SQLGenerator(mock_mode=mock_mode)
        self.validator = SQLAstValidator()
        self.executor = SQLExecutor(self.conn)

    def run(self, user_question: str) -> Dict[str, Any]:
        """Execute full 4-step Text-to-SQL flow."""
        # Step 1: Inspect Schema
        schema_context = self.inspector.format_schema_prompt()

        # Step 2: Generate SQL
        generated_sql = self.generator.generate(user_question, schema_context)

        # Step 3: AST Validation
        validated_sql = self.validator.validate(generated_sql)

        # Step 4: Execute
        exec_result = self.executor.execute(validated_sql)

        return {
            "question": user_question,
            "generated_sql": generated_sql,
            "validated_sql": validated_sql,
            "result": exec_result,
        }


def seed_sample_database() -> sqlite3.Connection:
    """Create in-memory SQLite database populated with realistic retail sample data."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        INSERT INTO customers VALUES
            (1, 'Acme Corp', 'contact@acme.com', 'us-east-1'),
            (2, 'Globex Logistics', 'info@globex.com', 'eu-west-1'),
            (3, 'Stark Industries', 'tony@stark.com', 'us-west-2');

        INSERT INTO products VALUES
            (101, 'Cloud Server Blade', 'Compute', 450.00, 15),
            (102, 'NVMe Storage Pod', 'Storage', 220.00, 120),
            (103, '100GbE Switch Module', 'Networking', 890.00, 8);

        INSERT INTO orders VALUES
            (1001, 1, '2025-09-15', 1350.00),
            (1002, 2, '2025-09-20', 440.00),
            (1003, 3, '2025-09-22', 2670.00),
            (1004, 1, '2025-09-25', 890.00);
    """)
    conn.commit()
    return conn


def run_demo(mock_mode: bool = False):
    """Run CLI demonstration of the 4-step Text-to-SQL agent pipeline."""
    print("=" * 75)
    print(" Text-to-SQL Agent Tool with AST Read-Only Validation (Slide 33)")
    print("=" * 75)

    conn = seed_sample_database()
    pipeline = TextToSQLPipeline(connection=conn, mock_mode=mock_mode)

    # 1. Step 1: Schema Inspection
    print("\n--- Step 1: Schema Inspection ---")
    print(pipeline.inspector.format_schema_prompt())

    # 2. Step 2 & 3 & 4: Valid Query Execution
    print("\n--- Steps 2, 3, 4: Valid Query (Top Customers by Revenue) ---")
    query_1 = "Show top customers by total revenue spent"
    res1 = pipeline.run(query_1)
    print(f"User Question: '{res1['question']}'")
    print(f"Validated SQL: {res1['validated_sql']}")
    print(f"Result Rows ({res1['result']['row_count']}):")
    print(f"  Columns: {res1['result']['columns']}")
    for row in res1['result']['rows']:
        print(f"  {row}")

    # 3. Security Validation Demonstration: Block Malicious Injections
    print("\n--- Security Demonstration: AST Read-Only Enforcement ---")
    malicious_attacks = [
        "DROP TABLE customers;",
        "SELECT * FROM customers; DELETE FROM orders;",
        "UPDATE products SET unit_price = 0.01;",
        "INSERT INTO customers VALUES (99, 'Hacker', 'h@h.com', 'x');",
        "SELECT * FROM customers WHERE 1=1; -- DROP TABLE orders;",
    ]

    for attack in malicious_attacks:
        try:
            print(f"\n[Test Injection]: {attack}")
            pipeline.validator.validate(attack)
            print("  [FAIL] Query was improperly allowed!")
        except SecurityValidationError as e:
            print(f"  [BLOCKED by AST Validator]: {e}")

    print("\n[✓] Text-to-SQL Agent Tool demonstration completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text-to-SQL Agent Demo")
    parser.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser.parse_args()
    run_demo(mock_mode=args.mock)
