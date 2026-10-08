"""Multimodal & Layout-Aware Document Parsing for Advanced RAG.

Demonstrates parsing visually complex documents (tables, charts, architecture diagrams)
into clean, structured Markdown using Claude 3.5 Sonnet / Claude 3 Haiku via Bedrock Converse API,
and contrasts naive chunking with layout-aware markdown chunking.

References:
- Slide 19 ("Hands-On RAG with AWS")
- Slide 20 ("Building Agentic Workflows with RAG on AWS Bedrock")
"""

import argparse
import base64
import io
import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class MultimodalDocumentParser:
    """Parses visual layouts (images/PDFs) into structured Markdown using Bedrock Converse API."""

    EXTRACTION_PROMPT = """You are an advanced layout-aware document parser.
Analyze this visual document page and transcribe it into high-fidelity structured Markdown:
1. Preserve heading hierarchies strictly (# for Title, ## for Sections, ### for Subsections).
2. Format all financial and tabular data as clean GitHub-Flavored Markdown tables. Never flatten tables into plain prose.
3. For charts or data graphs, extract the quantitative data points into a markdown table and summarize trends in a bullet list.
4. For architecture diagrams or workflows, provide a structured text representation or Mermaid diagram block.
5. Do not hallucinate content; transcribe what is visually present with maximum fidelity."""

    def __init__(
        self,
        model_id: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        region_name: str = "us-east-1",
        mock_mode: bool = False,
    ):
        self.model_id = model_id
        self.region_name = region_name
        self.mock_mode = mock_mode

        if not self.mock_mode:
            try:
                self.runtime = boto3.client("bedrock-runtime", region_name=self.region_name)
                boto3.client("sts", region_name=self.region_name).get_caller_identity()
            except (NoCredentialsError, ClientError) as e:
                print(f"[MultimodalDocumentParser] AWS credentials unavailable ({e}). Using mock parser.")
                self.mock_mode = True

    def parse_image_bytes(
        self,
        image_bytes: bytes,
        image_format: str = "png",
    ) -> str:
        """Send image to Claude Multimodal Converse API to extract structured Markdown."""
        if self.mock_mode:
            return self._generate_mock_markdown()

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "image": {
                            "format": image_format,
                            "source": {"bytes": image_bytes},
                        }
                    },
                    {"text": self.EXTRACTION_PROMPT},
                ],
            }
        ]

        try:
            response = self.runtime.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig={"temperature": 0.0, "maxTokens": 4096},
            )
            return response["output"]["message"]["content"][0]["text"]
        except ClientError as e:
            print(f"Error calling Bedrock Converse API: {e}")
            raise

    def _generate_mock_markdown(self) -> str:
        """Return high-fidelity sample parsed document with headers, tables, and charts."""
        return """# AWS Cloud Financial & Architectural Summary Q3 2025

## Executive Overview
Cloud migration and serverless adoption accelerated total throughput while driving down unit computing costs.

## Infrastructure Compute Matrix
The table below illustrates regional compute nodes, memory thresholds, and p99 response latencies.

| Service Tier | Node Type | vCPUs | Memory (GB) | Hourly Cost ($) | p99 Latency (ms) |
|---|---|---|---|---|---|
| Ingestion API | c7g.xlarge | 4 | 8 | 0.145 | 14.2 |
| RAG Retrieval Vector | r7g.2xlarge | 8 | 64 | 0.432 | 22.8 |
| Background Embeddings | g5.xlarge | 4 | 24 | 1.006 | 45.0 |
| Edge Router | t4g.medium | 2 | 4 | 0.033 | 8.5 |

## Monthly Cost Trend Analysis
Summary of cloud spend across quarters:
* Q1 2025: $142,500 total spend (Compute: 62%, Storage: 24%, Network: 14%)
* Q2 2025: $128,000 total spend (Compute: 55%, Storage: 28%, Network: 17%)
* Q3 2025: $115,200 total spend (Compute: 49%, Storage: 31%, Network: 20%)

## Architecture Ingestion Pipeline
```
[User Query] -> [API Gateway] -> [Lambda Auth]
                      |
                      v
             [Bedrock Knowledge Base]
                      |
        +-------------+-------------+
        |                           |
  [OpenSearch Vector]      [Claude 3.5 Sonnet]
```
"""


class NaiveFixedSizeChunker:
    """Fixed-size character chunker with overlap (splits blindly without structure awareness)."""

    def __init__(self, chunk_size: int = 350, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[Dict[str, Any]]:
        chunks = []
        start = 0
        chunk_idx = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            content = text[start:end]
            chunks.append({
                "chunk_id": chunk_idx,
                "strategy": "naive_fixed_size",
                "content": content,
                "length": len(content),
            })
            if end >= len(text):
                break
            start += self.chunk_size - self.chunk_overlap
            chunk_idx += 1
        return chunks


class LayoutAwareMarkdownChunker:
    """Structure-aware chunker that preserves tables, code/diagram blocks, and header hierarchies."""

    def __init__(self, target_chunk_size: int = 600):
        self.target_chunk_size = target_chunk_size

    def chunk(self, markdown_text: str) -> List[Dict[str, Any]]:
        # Split markdown into structural blocks (headers, tables, code blocks, paragraphs)
        lines = markdown_text.splitlines()
        blocks: List[Tuple[str, str]] = []  # (block_type, text)
        current_block: List[str] = []
        current_type = "text"
        in_code_block = False
        in_table = False

        for line in lines:
            stripped = line.strip()

            # Code block detection
            if stripped.startswith("```"):
                if in_code_block:
                    current_block.append(line)
                    blocks.append(("code_block", "\n".join(current_block)))
                    current_block = []
                    in_code_block = False
                    current_type = "text"
                    continue
                else:
                    if current_block:
                        blocks.append((current_type, "\n".join(current_block)))
                        current_block = []
                    in_code_block = True
                    current_type = "code_block"
                    current_block.append(line)
                    continue

            if in_code_block:
                current_block.append(line)
                continue

            # Table detection
            if stripped.startswith("|") and stripped.endswith("|"):
                if not in_table:
                    if current_block:
                        blocks.append((current_type, "\n".join(current_block)))
                        current_block = []
                    in_table = True
                    current_type = "table"
                current_block.append(line)
                continue
            else:
                if in_table:
                    blocks.append(("table", "\n".join(current_block)))
                    current_block = []
                    in_table = False
                    current_type = "text"

            # Heading detection
            if stripped.startswith("#"):
                if current_block:
                    blocks.append((current_type, "\n".join(current_block)))
                    current_block = []
                blocks.append(("header", line))
                continue

            if stripped == "":
                if current_block and not in_table:
                    blocks.append((current_type, "\n".join(current_block)))
                    current_block = []
                continue

            current_block.append(line)

        if current_block:
            blocks.append((current_type, "\n".join(current_block)))

        # Group blocks into cohesive chunks respecting atomic units (tables/code blocks are never split)
        chunks: List[Dict[str, Any]] = []
        current_chunk_blocks: List[str] = []
        current_chunk_len = 0
        current_section = "General"
        chunk_idx = 0

        for b_type, b_text in blocks:
            if b_type == "header":
                current_section = b_text.strip()

            b_len = len(b_text)
            # If adding this block exceeds target size and current chunk is non-empty, flush current chunk
            if current_chunk_len + b_len > self.target_chunk_size and current_chunk_blocks:
                chunks.append({
                    "chunk_id": chunk_idx,
                    "strategy": "layout_aware",
                    "section": current_section,
                    "content": "\n\n".join(current_chunk_blocks),
                    "length": current_chunk_len,
                    "contains_table": any("|---|" in b or ("|" in b and "\n|" in b) for b in current_chunk_blocks),
                    "contains_code_or_diagram": any("```" in b for b in current_chunk_blocks),
                })
                chunk_idx += 1
                current_chunk_blocks = []
                current_chunk_len = 0

            current_chunk_blocks.append(b_text)
            current_chunk_len += b_len

        if current_chunk_blocks:
            chunks.append({
                "chunk_id": chunk_idx,
                "strategy": "layout_aware",
                "section": current_section,
                "content": "\n\n".join(current_chunk_blocks),
                "length": current_chunk_len,
                "contains_table": any("|---|" in b or ("|" in b and "\n|" in b) for b in current_chunk_blocks),
                "contains_code_or_diagram": any("```" in b for b in current_chunk_blocks),
            })

        return chunks


def evaluate_table_integrity(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Measure whether markdown tables are intact or fractured across chunk boundaries."""
    fractured_tables = 0
    intact_tables = 0

    for ch in chunks:
        content = ch["content"]
        # Strip fenced code/diagram blocks so ascii art isn't mistaken for markdown tables
        cleaned_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        table_lines = [line.strip() for line in cleaned_content.splitlines() if line.strip().startswith("|") and line.strip().endswith("|")]
        if not table_lines:
            continue

        # Check if table has both header and separator and data
        has_separator = any(re.match(r"^\|(\s*:?-+:?\s*\|)+$", l) for l in table_lines)
        if has_separator and len(table_lines) >= 3:
            intact_tables += 1
        else:
            # Fragmented table: lines exist but header/separator was detached
            fractured_tables += 1

    total = intact_tables + fractured_tables
    return {
        "intact_tables": intact_tables,
        "fractured_tables": fractured_tables,
        "table_integrity_score": intact_tables / max(1, total) if total > 0 else 1.0,
    }


def run_demo(mock_mode: bool = False):
    """Run multimodal parsing and chunking evaluation demo."""
    print("=" * 75)
    print(" Multimodal & Layout-Aware Document Parsing Demo (Slides 19 & 20 Alignment)")
    print("=" * 75)

    parser = MultimodalDocumentParser(mock_mode=mock_mode)
    print(f"[*] Initialized MultimodalDocumentParser (Mock Mode: {parser.mock_mode})")

    # 1. Parse Document Page
    print("\n--- Step 1: Layout-Aware Parsing into Structured Markdown ---")
    parsed_markdown = parser.parse_image_bytes(b"dummy_image_data")
    print("Extracted Markdown Preview:")
    print("-" * 50)
    print("\n".join(parsed_markdown.splitlines()[:15]) + "\n...")
    print("-" * 50)

    # 2. Run Naive Fixed-Size Chunking
    print("\n--- Step 2: Naive Fixed-Size Chunking ---")
    naive_chunker = NaiveFixedSizeChunker(chunk_size=300, chunk_overlap=50)
    naive_chunks = naive_chunker.chunk(parsed_markdown)
    naive_eval = evaluate_table_integrity(naive_chunks)
    print(f"Total Naive Chunks: {len(naive_chunks)}")
    print(f"Naive Table Integrity: {naive_eval['table_integrity_score']:.1%} "
          f"({naive_eval['fractured_tables']} fractured tables detected!)")

    # Sample fractured chunk
    for ch in naive_chunks:
        if "|" in ch["content"] and not any("|---|" in l for l in ch["content"].splitlines()):
            print(f"\n[Example Fractured Chunk #{ch['chunk_id']}]:\n{ch['content'][:150]}...")
            break

    # 3. Run Layout-Aware Markdown Chunking
    print("\n--- Step 3: Layout-Aware Markdown Chunking ---")
    layout_chunker = LayoutAwareMarkdownChunker(target_chunk_size=600)
    layout_chunks = layout_chunker.chunk(parsed_markdown)
    layout_eval = evaluate_table_integrity(layout_chunks)
    print(f"Total Layout-Aware Chunks: {len(layout_chunks)}")
    print(f"Layout-Aware Table Integrity: {layout_eval['table_integrity_score']:.1%} "
          f"({layout_eval['fractured_tables']} fractured tables)")

    for ch in layout_chunks:
        if ch.get("contains_table"):
            print(f"\n[Preserved Table Chunk #{ch['chunk_id']}]:\n{ch['content']}")
            break

    print("\n--- Summary Benchmark ---")
    print(f"Naive Chunker Fractures: {naive_eval['fractured_tables']}")
    print(f"Layout-Aware Fractures: {layout_eval['fractured_tables']}")
    print("[✓] Layout-Aware Parsing & Chunking demo completed successfully!")


if __name__ == "__main__":
    parser_arg = argparse.ArgumentParser(description="Multimodal & Layout-Aware Parsing Demo")
    parser_arg.add_argument("--mock", action="store_true", help="Force mock/simulation mode")
    args = parser_arg.parse_args()
    run_demo(mock_mode=args.mock)
