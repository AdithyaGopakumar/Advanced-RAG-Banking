# Cognibank AI — Hybrid, Multi-Turn RAG Agent — Frontend

Executive conversational interface and deep pipeline reasoning inspector for Cognibank AI — Hybrid, Multi-Turn RAG Agent.

## Features

- 🏛️ **Executive Banking Design**: Custom glassmorphic dark theme (Obsidian & Platinum with Electric Sapphire highlights) built for professional banking operations.
- 💬 **Multi-Turn Chat Continuity**: Maintains dialogue session context (`conversationId`) across follow-up queries with automatic pronoun and antecedent banking product resolution.
- 🔬 **Deep Pipeline Trace & Reasoning Inspector**:
  - **Input Guardrails & PII Protection**: Real-time detection and masking of customer PII (PAN, Aadhaar, account numbers).
  - **Query Contextualization**: Shows how short follow-ups are reformulated into standalone banking questions.
  - **Multi-Query Expansion (MQE)**: Inspects parallel query variants generated for retrieval.
  - **Hybrid Search & RRF**: View dense (Pinecone) and lexical (Elasticsearch BM25) rankings fused via Reciprocal Rank Fusion.
  - **Semantic Reranking**: Cross-Encoder relevance scores for top candidate chunks.
  - **Evidence Context**: Breadcrumbs, heading paths, and token budget estimation.
  - **Claim-Level Grounding**: Claim-by-claim verification table against governed knowledge.
  - **Output Safety Rails**: NeMo Guardrails check and leak protection validation.
- 🛡️ **Support Level Badges**: Visual indicators for `Fully Supported`, `Partially Supported`, `Ambiguous`, `Unavailable`, and `Rejected`.
- ⚡ **Live System Health Polling**: Real-time indicators for backend server, NeMo Guardrails (Colang), and LangSmith tracing.

---

## Quick Start

### 1. Ensure Backend is Running

In one terminal, start the FastAPI backend:

```powershell
cd Backend
.\.venv\Scripts\Activate.ps1
python run.py
```

The backend API will be live at `http://localhost:8000`.

### 2. Start the Streamlit UI

In another terminal, start the Streamlit application:

```powershell
cd Backend
.\.venv\Scripts\streamlit.exe run ../frontend/app.py
```

Or from the project root:

```powershell
.\Backend\.venv\Scripts\streamlit.exe run frontend/app.py
```

The Streamlit UI will open in your browser at `http://localhost:8501`.

---

## Configuration

The frontend automatically connects to `http://localhost:8000` by default. You can override the backend URL by setting the `BACKEND_URL` environment variable:

```powershell
$env:BACKEND_URL="http://localhost:8000"
.\Backend\.venv\Scripts\streamlit.exe run frontend/app.py
```
