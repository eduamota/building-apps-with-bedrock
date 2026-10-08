# Bedrock Prompt Management Demo

This demo illustrates the end-to-end lifecycle of **AWS Bedrock Prompt Management** using Boto3 (`bedrock-agent` and `bedrock-runtime`).

> **Presentation Reference:** Slide 30 (*"Hands-On RAG with AWS"*)

---

## Architecture & Lifecycle

```
       +---------------------------------------------+
       |   bedrock-agent: create_prompt              |
       |   - Template: {{context}}, {{query}}        |
       |   - Model & Inference Configurations        |
       +----------------------+----------------------+
                              |
                              v
       +---------------------------------------------+
       |   bedrock-agent: create_prompt_version      |
       |   - Freezes immutable snapshot (e.g. '1')   |
       +----------------------+----------------------+
                              |
                              v
       +---------------------------------------------+
       |   bedrock-agent: get_prompt                 |
       |   - Retrieve variant metadata & template    |
       +----------------------+----------------------+
                              |
                              v
       +---------------------------------------------+
       |   Parameter Hydration & Validation          |
       |   - Replace {{context}}, {{query}}          |
       +----------------------+----------------------+
                              |
                              v
       +---------------------------------------------+
       |   bedrock-runtime: converse                 |
       |   - Execute model inference with Claude/Nova|
       +---------------------------------------------+
```

---

## Files

- `prompt_management_demo.py`: Python CLI tool and importable module (`BedrockPromptManager`). Supports live Bedrock execution as well as mock mode (`--mock`) when credentials are not configured.
- `prompt_management_demo.ipynb`: Step-by-step Jupyter Notebook walkthrough.

---

## Quickstart

Run the command-line script directly:
```bash
# Run with automatic credential detection (falls back to mock mode if offline)
python prompt_management_demo.py

# Force mock mode
python prompt_management_demo.py --mock
```
