# Indirect Prompt Injection Red-Teaming & Multi-Agent Defense from Scratch

This module demonstrates and tests how **indirect prompt injection** attacks embedded inside untrusted ingested documents (e.g., poisoned invoices, earnings PDFs, SEC filings) attempt to hijack autonomous RAG agents. It then presents a **Multi-Agent RAG System built from scratch** on AWS Bedrock using **Bedrock Contextual Grounding Guardrails** ($\ge 0.75$ threshold) and **Cryptographic Tool-Level Authorization** to neutralize the threat.

> **Presentation References:**
> - Slide 40 (*Indirect Prompt Injection via Ingested Documents*) - *Building Agentic Workflows with RAG on AWS Bedrock*
> - Slide 58 (*Agent Security & Poisoned Retrieval*) - *Building Agentic Workflows with RAG on AWS Bedrock*
> - Slide 64 (*Dual-Agent Defense & Tool Authorization*) - *Building Agentic Workflows with RAG on AWS Bedrock*
> - Slide 43 (*Bedrock Guardrails*) - *Hands-On RAG with AWS*

---

## Architecture: Attack Vector vs. Multi-Agent Defense

```
    [Attacker uploads poisoned invoice/PDF]
                      |
                      v
        [Ingested into RAG / KB]
                      |
                      v
    [Legitimate User asks: "Summarize revenue"]
                      |
                      v
        [RAG retrieves poisoned context]
                      |
                      v
  [LLM encounters: "SYSTEM INSTRUCTION: TransferFundsTool..."]
         /                                         \
        / (Vulnerable Single Agent)                 \ (Multi-Agent Architecture from Scratch)
       v                                             v
  [Executes TransferFundsTool]              1. RAGIngestionAgent reads context (unprivileged)
   *** $250,000 STOLEN! ***                  2. SecuritySupervisorAgent checks Grounding:
                                                Score: 0.05 < 0.75 --> INJECTION FLAGGED!
                                             3. Context is sanitized & filtered
                                             4. FinancialAnalystAgent computes revenue
                                             5. PrivilegedExecutionAgent rejects unauthorized calls!
                                                     |
                                                     v
                                            [Clean Summary Returned to User]
```

---

## Multi-Agent Architecture Built from Scratch (`multi_agent_rag.py`)

- **`BaseAgent`**: Pure-Python ReAct autonomous loop implementing Bedrock Converse API tool-calling schemas (`toolSpec`, `toolUse`, `toolResult`), conversation state, and reasoning trace.
- **`RAGIngestionAgent`**: Sandboxed unprivileged worker that retrieves & extracts document chunks.
- **`SecuritySupervisorAgent`**: Orchestrator that evaluates Bedrock Guardrail Contextual Grounding ($\ge 0.75$), detects prompt injection tokens, strips malicious instructions, and dispatches sanitized tasks.
- **`FinancialAnalystAgent`**: Domain specialist that performs calculations over verified data.
- **`PrivilegedExecutionAgent`**: Isolated executor for sensitive operations (e.g. fund transfers), requiring scoped supervisor cryptographic authorization tokens.

---

## Quickstart

```bash
# 1. Run the Multi-Agent RAG System built from scratch (Mock / Simulation mode)
python multi_agent_rag.py --mock

# 2. Run the Single-Agent Red-Teaming Harness (Exploit vs. Hardened)
python red_teaming_harness.py --mock

# 3. Generate a sample poisoned document (Markdown or PDF)
python generate_poisoned_document.py
python generate_poisoned_document.py --pdf

# 4. Interactive Jupyter Notebook
# Open red_teaming_demo.ipynb in Jupyter or VS Code / Cursor
```
