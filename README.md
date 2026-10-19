# Advanced RAG — Banking Knowledge System & AI Agent

Production-oriented, governed banking customer support system featuring **Hybrid RAG** (Dense Pinecone + Lexical Elasticsearch BM25), **LangGraph** agent orchestration, **NVIDIA NeMo Guardrails**, **LangSmith** observability, and an **Executive Streamlit Web Interface**.

The agent is strictly governed by the **Knowledge-Base-Only Policy**: banking claims must be supported by the governed banking knowledge base.

---

## Architecture Overview

```
                      User / Client
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
   Streamlit Web UI (8501)       FastAPI Backend (8000)
             │                           │
             └─────────────┬─────────────┘
                           ▼
                 1. Input Guardrails
         (Length, Regex Injection, PII Redaction)
                           ▼
             2. NeMo Guardrails & Colang Flows
             (Off-Topic, Speculation, Jailbreaks)
                           ▼
          3. Multi-Turn Context & Query Understanding
         (Pronoun Resolution, Antecedent Entity Inheritance)
                           ▼
          4. Multi-Query Expansion & Hybrid Retrieval
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
   Pinecone (Dense 384d)           Elasticsearch (Native BM25)
         └─────────────────┬─────────────────┘
                           ▼
           5. Reciprocal Rank Fusion (RRF)
                           ▼
          6. Semantic Cross-Encoder Reranking
                           ▼
          7. Governed Context Assembly & Budgeting
                           ▼
         8. Claim-Level Grounding Assessment (GPT-4o-mini)
                           ▼
          9. Output Guardrails & Safety Sanitization
                           ▼
                 Grounded Response Envelope
```

---

## Repository Structure

```
├── knowledge-base/       ← Governed banking documentation, taxonomy, templates & guidelines
├── Backend/              ← FastAPI modular monolith backend service
│   ├── app/
│   │   ├── ai/           ← RAG pipeline, graphs, embeddings, memory, guardrails, prompts
│   │   ├── api/          ← Versioned API routers (/api/v1)
│   │   ├── core/         ← Middleware, settings, responses, exceptions
│   │   └── modules/      ← Domain modules (chat, system, knowledge)
│   ├── evaluation/       ← RAGAS & custom evaluation benchmark datasets & runner
│   ├── tests/            ← Unit, integration, guardrail & memory test suite (170+ tests)
│   ├── ingest.py         ← Governed knowledge base ingestion & vector indexer
│   ├── run.py            ← Uvicorn application entry point
│   └── requirements.txt  ← Python dependencies
├── frontend/             ← Executive Streamlit UI frontend
│   ├── app.py            ← Main Streamlit chat & reasoning inspector application
│   ├── api_client.py     ← Typed HTTP client communicating with backend
│   └── styles.css        ← Glassmorphic obsidian executive banking theme
├── docs/                 ← Specifications (PRD, Architecture, RAG, Agent, Security, Guardrails)
└── README.md             ← Root repository overview & setup instructions
```

---

## Quick Start — Step-by-Step Setup

### 1. Prerequisites

- **Python 3.10 – 3.12** (Recommended: **Python 3.10**).
- **Git**
- Active credentials for:
  - **OpenAI API Key** (for query expansion, grounding assessment, and generation)
  - **Elasticsearch Cloud** (or local cluster for native BM25 lexical search)
  - **Pinecone** (optional: if omitted, an in-memory dense vector store is used)
  - **LangSmith** (optional: for distributed tracing)

---

### 2. Virtual Environment & Dependencies

From the repository root:

```powershell
# 1. Navigate to Backend
cd Backend

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

### 3. Environment Configuration

Copy the example environment configuration in `Backend`:

```powershell
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```

Open `Backend/.env` and supply your API keys:

```env
# LLM Provider
OPENAI_API_KEY=sk-...

# Lexical Search (Elasticsearch)
ELASTICSEARCH_URL=https://your-elastic-cluster:443
ELASTICSEARCH_INDEX=knowledge-chunks
ELASTICSEARCH_API_KEY=your-api-key

# Dense Vector Search (Pinecone - Optional; in-memory fallback if omitted)
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
PINECONE_NAMESPACE=knowledge

# Guardrails
ENABLE_NEMO_GUARDRAILS=true
NEMO_GUARDRAILS_CONFIG_PATH="app/ai/guardrails/nemo"

# Conversation Memory
ENABLE_CONVERSATION_MEMORY=true
MAX_MEMORY_TURNS=5

# Distributed Tracing (LangSmith - Optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=rag-bank-development
```

---

### 4. Ingest Knowledge Base

Index and validate the governed banking documents (`knowledge-base/`):

```powershell
# From Backend/ with virtual environment activated:
python ingest.py
```

This parses governed markdown files, computes deterministic chunk IDs and content hashes, indexes text into Elasticsearch BM25, and embeds chunks into the vector store.

---

### 5. Start the FastAPI Backend Server

In your backend terminal:

```powershell
# From Backend/ with virtual environment activated:
python run.py
```

- API server will start at: **`http://localhost:8000`**
- Interactive Swagger docs: **`http://localhost:8000/docs`**
- Health check: **`http://localhost:8000/api/v1/system/health`**

---

### 6. Launch the Streamlit Web Interface

Open a new terminal window:

```powershell
# From repository root:
.\Backend\.venv\Scripts\streamlit.exe run frontend/app.py
```

Or from `frontend/`:

```powershell
cd frontend
..\Backend\.venv\Scripts\streamlit.exe run app.py
```

- Streamlit Web UI will be live at: **`http://localhost:8501`**

---

## Using the Application

### Interactive Chat & Multi-Turn Reasoning

1. Open **`http://localhost:8501`** in your browser.
2. Observe the **🟢 Backend Online** indicator in the sidebar.
3. Ask an initial question (e.g. *"Who can open a BSBDA account?"*).
4. View the response, support level category badge (`✅ Fully Supported`), and cited source chunks.
5. Click **🔬 Deep Pipeline Trace & Reasoning Inspector** to inspect:
   - Input Guardrails & PII sanitization
   - Multi-Query Expansion (MQE) variants
   - Reciprocal Rank Fusion (RRF) dense + lexical scores
   - Cross-Encoder reranking
   - Claim-level grounding checks
6. Ask a follow-up query with a pronoun (e.g. *"What is the minimum balance for it?"*).
   - Notice the automatic query resolution: `Query Resolved As: What is the minimum balance for BSBDA?`.
   - The agent maintains conversational continuity without violating grounding boundaries.

---

## Testing & Verification

### Running the Test Suite

Run the complete automated test suite (170+ unit, integration, and guardrail tests):

```powershell
# From Backend/ with virtual environment activated:
pytest -v
```

### Running Benchmark Evaluations

Run the offline benchmark evaluation runner against curated banking datasets:

```powershell
# Run the complete benchmark evaluation suite
python eval.py

# Run a specific category:
python eval.py --category fully_supported
python eval.py --category partially_supported
python eval.py --category unsupported
python eval.py --category ambiguous
python eval.py --category adversarial
```

Reports are automatically saved in `evaluation/reports/` in both JSON and Markdown formats.

---

## Key Design Principles

1. **Governed Knowledge Base Authority**: The LLM's pretrained knowledge is **not** an authoritative source. Factual banking claims must be supported by governed retrieved evidence.
2. **Deterministic Controls First**: Regex safety, input length, and PII masking run *before* model invocation to eliminate unnecessary token latency and prevent sensitive data leakage.
3. **Claim-Level Grounding**: Claims are verified individually rather than relying on aggregate vector similarity.
4. **Multi-Turn Context Primacy**: Dialogue history resolves anaphoric references and pronouns, but cannot introduce ungrounded banking facts.

---

## License

Copyright (c) 2026 The Bank. All rights reserved. See [LICENSE](LICENSE) for terms.
