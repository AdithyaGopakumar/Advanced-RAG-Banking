# Cognibank AI — Hybrid, Multi-Turn RAG Agent — Architecture

**Document Status:** Architecture Baseline & Implementation Specification\
**Version:** 2.0 (Post-Implementation Baseline)\
**Related Document:** `PRD.md`

------------------------------------------------------------------------

## 1. Architecture Overview

Cognibank AI is a **modular monolith** built around a governed banking knowledge base, hybrid dual-path retrieval, an explicit LangGraph multi-turn conversational agent, layered deterministic and NeMo guardrails, and an Executive Streamlit Web Interface with end-to-end reasoning telemetry.

The system is strictly an **information-answering agent**, governed by the **Knowledge-Base-Only Policy**: banking claims must be supported by the governed banking knowledge base.

``` mermaid
flowchart TB
    subgraph UI["Executive User Interface (Streamlit :8501)"]
        ChatUI["Glassmorphic Chat UI"]
        Inspector["Deep Reasoning Pipeline Inspector"]
        HealthUI["Live Health Monitor"]
    end

    subgraph API["FastAPI Modular Monolith (:8000)"]
        Router["/api/v1/chat"]
        HealthRouter["/api/v1/system/health"]
    end

    subgraph Graph["LangGraph State Machine (AgentState)"]
        InputGuard["1. input_guard<br/>(Deterministic + NeMo Colang Rails)"]
        LoadContext["2. load_context<br/>(SessionStore + Pronoun / Anaphora Engine)"]
        Retrieve["3. retrieve<br/>(MQE + Dense + Sparse BM25 + Soft Pre-Filter)"]
        Assess["4. assess<br/>(Claim Grounding Assessment)"]
        Generate["5a. generate / 5b. policy<br/>(Evidence Synthesis / Unavailable Policy)"]
        OutputGuard["6. output_guard<br/>(Deterministic + NeMo Output Rails + PII Masking)"]
        Fallback["7. fallback<br/>(Safe Static Output Fallback)"]
        Persist["8. persist<br/>(Audited Session Memory Commit)"]
    end

    subgraph Search["Hybrid Retrieval Subsystem"]
        MQE["Multi-Query Expansion + Keyword Extraction"]
        Pinecone[("Pinecone (384d Dense)")]
        ES[("Elasticsearch (Native BM25)")]
        RRF["Reciprocal Rank Fusion (k=60)"]
        Reranker["Cross-Encoder Reranker (ms-marco)"]
        ContextBuild["Context Assembly (Token Budget)"]
    end

    subgraph Knowledge["Governed Knowledge Base"]
        KB["Markdown Knowledge Base"]
        Ingest["Ingestion Pipeline (ingest.py)"]
    end

    ChatUI --> Router
    HealthUI --> HealthRouter
    Router --> InputGuard

    InputGuard --> LoadContext
    LoadContext --> Retrieve
    Retrieve --> MQE
    MQE --> Pinecone
    MQE --> ES
    Pinecone --> RRF
    ES --> RRF
    RRF --> Reranker
    Reranker --> ContextBuild
    ContextBuild --> Assess
    Assess --> Generate
    Generate --> OutputGuard
    OutputGuard --> Persist
    OutputGuard --> Fallback
    Fallback --> Persist
    Persist --> Router
    Router --> ChatUI
    Router --> Inspector

    KB --> Ingest
    Ingest --> Pinecone
    Ingest --> ES
```

    Agent --> Query["Query Understanding"]
    Query --> MQE["Multi-Query Expansion"]

    MQE --> Dense["Dense Retrieval"]
    MQE --> Lexical["BM25 Lexical Retrieval"]

    Dense --> Pinecone[("Pinecone")]
    Lexical --> ES[("Elasticsearch")]

    Pinecone --> RRF["Reciprocal Rank Fusion"]
    ES --> RRF

    RRF --> Reranker["Semantic Reranker"]
    Reranker --> Context["Context Validation"]

    Context --> LLM["LLM"]
    LLM --> OutputGuard["Output Guardrails"]
    OutputGuard --> Response["Grounded Response"]
    Response --> User

    KB["Governed Banking Knowledge Base"] --> Indexing["Knowledge Indexing Pipeline"]
    Indexing --> Pinecone
    Indexing --> ES

    Agent -.-> Memory[("Conversation Memory")]
    Agent -.-> LangSmith["LangSmith Tracing"]
    Evaluation["Ragas + Custom Evaluators + JEV"] -.-> Agent
    Evaluation -.-> Retrieval["Retrieval Evaluation"]
    Evaluation -.-> OutputGuard
```

------------------------------------------------------------------------

## 2. Architectural Goals

1.  **Groundedness** --- banking answers must be supported by the
    governed knowledge base.
2.  **Retrieval quality** --- combine semantic and lexical retrieval.
3.  **Controlled agent behavior** --- use agentic reasoning only where
    useful.
4.  **Defense in depth** --- combine deterministic and semantic
    guardrails.
5.  **Traceability** --- make important execution steps observable.
6.  **Evaluability** --- make evaluation a first-class component.
7.  **Knowledge governance** --- preserve document identity, version,
    status, and effective dates.
8.  **Maintainability** --- keep components modular.
9.  **Future extensibility** --- allow later controlled additions
    without expanding the initial scope.

------------------------------------------------------------------------

## 3. Architectural Principles

### 3.1 Knowledge Base as Source of Truth

The governed banking knowledge base is the authoritative source for
banking information. The LLM's pretrained knowledge is not treated as an
authoritative banking source.

``` mermaid
flowchart LR
    User["User Question"] --> RAG["RAG Pipeline"]
    KB["Governed Knowledge Base"] --> RAG

    RAG --> Evidence["Retrieved Evidence"]
    Evidence --> Decision{"Evidence Support?"}

    Decision -->|Fully Supported| LLM["LLM"]
    Decision -->|Partially Supported| LLM
    Decision -->|Insufficient / Unsupported| LLM

    LLM -->|Generate supported response| Answer["Answer"]
    LLM -->|Restrict to supported claims| Partial["Partial Answer"]
    LLM -->|Request clarification or state unavailable| Safe["Clarification / Unavailable"]
```

### 3.2 Deterministic-First

Use deterministic controls wherever deterministic logic is sufficient:

-   Authentication and authorization
-   Rate limiting
-   Schema validation
-   Metadata and version filtering
-   Retrieval execution
-   RRF
-   Response validation
-   Request limits

Use model-based decisions for semantic problems such as intent
understanding, query expansion, ambiguity, grounding, and
unsupported-claim detection.

### 3.3 Evidence Is Data, Not Instructions

Retrieved documents are untrusted data from the perspective of agent
control flow. Retrieved text must never override system instructions,
change guardrail policy, execute tools, or expose hidden prompts.

------------------------------------------------------------------------

## 4. High-Level System Architecture

``` mermaid
flowchart TB
    subgraph Client["Client"]
    Web["Executive Streamlit Web Client (:8501)"]
    end

    subgraph API["FastAPI Modular Monolith (:8000)"]
        Router["API Router (/api/v1)"]
        Auth["Authentication / Request ID"]
        Chat["Chat Module (/chat)"]
        Health["System Module (/system/health)"]
    end

    subgraph Guardrails["Layered Guardrails"]
        Input["Input Guardrails (Regex + Length + PII Redaction)"]
        NemoInput["NeMo Colang Rails (Off-Topic, Jailbreaks, Greetings)"]
        Output["Output Guardrails (Instruction Leak Check)"]
        NemoOutput["NeMo Colang Output Rails (Forbidden Operational Claims)"]
    end

    subgraph Agent["Agent Orchestration (LangGraph)"]
        StateGraph["StateGraph(AgentState)"]
        ContextNode["Context Loading & Anaphora Substitution"]
        AssessNode["Grounding Assessment (Claim Support)"]
        GenNode["Evidence-Bounded Generation"]
        PolicyNode["Deterministic Unavailable / Clarification Policy"]
    end

    subgraph Retrieval["Hybrid RAG Retrieval"]
        MQE["MQE + Domain Keyword Extraction"]
        Dense["Dense Retrieval (Pinecone / InMemory)"]
        Lexical["Lexical Retrieval (Elasticsearch Native BM25)"]
        Filter["Strategy 2 Soft Pre-Filtering + Fallback"]
        Fusion["Reciprocal Rank Fusion (k=60)"]
        Rerank["Semantic Cross-Encoder (ms-marco-MiniLM)"]
        ContextAssemble["Context Assembly (Token Budgeting)"]
    end

    subgraph Storage["Persistence & Memory"]
        PineconeStore[("Pinecone Vector Store")]
        ESIndex[("Elasticsearch BM25 Index")]
        SessionMem[("SessionStore (LRU Multi-Turn Memory)")]
    end

    subgraph Observability["Observability & Benchmarks"]
        LangSmith["LangSmith Tracing"]
        BenchmarkRunner["Benchmark Runner (eval.py)"]
    end

    Web --> Router
    Router --> Auth
    Auth --> Chat
    Chat --> Input
    Input --> NemoInput
    NemoInput --> StateGraph
    StateGraph --> ContextNode
    ContextNode <--> SessionMem
    ContextNode --> MQE
    MQE --> Dense
    MQE --> Lexical
    Dense --> PineconeStore
    Lexical --> ESIndex
    PineconeStore --> Filter
    ESIndex --> Filter
    Filter --> Fusion
    Fusion --> Rerank
    Rerank --> ContextAssemble
    ContextAssemble --> AssessNode
    AssessNode --> GenNode
    AssessNode --> PolicyNode
    GenNode --> Output
    PolicyNode --> Output
    Output --> NemoOutput
    NemoOutput --> Response["ChatResponseData Envelope"]
    Response --> Web

    StateGraph -. tracing .-> LangSmith
    BenchmarkRunner -. evaluates .-> Chat
```

------------------------------------------------------------------------

## 5. Existing FastAPI Foundation

The existing FastAPI boilerplate provides the application foundation and
should be extended rather than replaced.

``` mermaid
flowchart TD
    Request["HTTP Request"] --> Logger["Request Logger"]
    Logger --> RequestID["Request ID"]
    RequestID --> Security["Security Headers"]
    Security --> CORS["CORS"]
    CORS --> Host["Trusted Host"]
    Host --> GZip["GZip"]
    GZip --> Router["API Router"]
    Router --> Rate["Route Rate Limit"]
    Rate --> Auth["Authentication"]
    Auth --> Handler["Domain Handler"]
    Handler --> Service["Service Layer"]
    Handler --> Exceptions["Exception Handlers"]
    Service --> Response["Response Envelope"]
    Exceptions --> Response
```

Existing foundations include configuration, exception handling, response
envelopes, lifecycle hooks, CORS, GZip, trusted hosts, security headers,
request IDs, request logging, rate limiting, Docker, and tests.

Authentication remains a stub and must be implemented before production
deployment.

------------------------------------------------------------------------

## 6. Backend Architecture

The backend remains a modular monolith.

Backend/
├── app/
│   ├── ai/
│   │   ├── embeddings/          # sentence-transformers & OpenAI embedding adapters
│   │   ├── graphs/              # workflow.py (LangGraph state machine), state.py (AgentState)
│   │   ├── guardrails/          # input.py, output.py, pii.py, scope.py, nemo_adapter.py, nemo/
│   │   ├── memory/              # store.py (SessionStore), context.py (anaphora engine), models.py
│   │   ├── observability/       # tracer.py (LangSmith run config & metadata tagging)
│   │   ├── prompts/             # generation.py, mqe.py
│   │   ├── providers/           # llm.py (OpenAI provider with exponential backoff & fakes)
│   │   └── rag/
│   │       ├── generation/      # answer.py, grounding.py, models.py
│   │       ├── indexing/        # vector_store.py, lexical.py, filters.py
│   │       └── retrieval/       # hybrid.py, mqe.py, rrf.py, reranker.py, context.py
│   │
│   ├── api/v1/                  # router.py (mounts module routers under /api/v1)
│   ├── core/                    # config.py, exceptions.py, responses.py, lifecycle.py
│   ├── modules/
│   │   ├── chat/                # router.py, schemas.py, service.py, dependencies.py
│   │   ├── knowledge/           # loader.py, parser.py, chunker.py, governance.py
│   │   └── system/              # health.py
│   ├── db/                      # Database boundary
│   ├── models/                  # Shared domain data models
│   └── shared/                  # Shared utilities
│
├── evaluation/                  # Benchmark CLI (eval.py), datasets/, evaluators/, runners/
├── tests/                       # Unit, integration, guardrail & memory test suite (170+ tests)
├── ingest.py                    # Knowledge base ingestion & indexing CLI
├── run.py                       # Uvicorn entry point
└── requirements.txt

frontend/
├── app.py                       # Streamlit executive chat & reasoning inspector UI
├── api_client.py                # Typed HTTP client to FastAPI backend
└── styles.css                   # Obsidian glassmorphic styling
```

This represents the intended architecture; implementation should create
components incrementally as their phases begin.

------------------------------------------------------------------------

## 7. Request Lifecycle

``` mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant API as FastAPI
    participant IG as Input Guard
    participant G as LangGraph
    participant Q as Query Analysis
    participant M as MQE
    participant R as Hybrid Retrieval
    participant F as RRF
    participant RR as Reranker
    participant CV as Context Validation
    participant L as LLM
    participant OG as Output Guard
    participant LS as LangSmith

    U->>API: POST /chat
    API->>IG: Validate input
    IG->>G: Approved query
    G->>Q: Analyze query
    Q->>M: Generate retrieval queries
    M->>R: Expanded queries
    R->>F: Dense + BM25 results
    F->>RR: Candidate pool
    RR->>CV: Ranked candidates
    CV->>L: Validated context + query
    L->>OG: Generated answer
    OG->>API: Validated response
    API->>U: Final answer

    API-->>LS: Request trace
    G-->>LS: Agent trace
    R-->>LS: Retrieval trace
    L-->>LS: LLM trace
    OG-->>LS: Guardrail trace
```

------------------------------------------------------------------------

## 8. Chat API Boundary

The chat endpoint is served at:

``` text
POST /api/v1/chat
```

### Request Envelope (`ChatRequest`):

``` json
{
  "question": "How can I open one?",
  "conversationId": "45e8db12-b0f3-47b7-8486-8ffe3e04bfb2",
  "fullTrace": true
}
```
*(Accepts `question`, `query`, or `message` interchangeably; `conversationId` and `fullTrace` camelCase or snake_case).*

### Response Envelope (`ChatResponseData`):

``` json
{
  "success": true,
  "data": {
    "conversation_id": "45e8db12-b0f3-47b7-8486-8ffe3e04bfb2",
    "question": "How can I open one?",
    "query": "How can I open one?",
    "resolved_query": "How can I open a Savings Account?",
    "response": "To open a Savings Account, you must submit a completed Account Opening Form, Proof of Identity (Aadhaar, Passport, or PAN), Proof of Address, and recent passport-size photographs at any branch or online via Video-KYC.",
    "response_type": "answer",
    "support_level": "fully_supported",
    "reason_code": "FULLY_SUPPORTED",
    "chunk_ids": ["ACCT-SAV-001#c0004", "DOC-KYC-001#c0002"],
    "errors": [],
    "trace": {
      "input_guardrail": { "allowed": true, "normalized_query": "How can I open one?" },
      "conversation": { "conversation_id": "45e8db12-b0f3-47b7-8486-8ffe3e04bfb2", "resolved_query": "How can I open a Savings Account?" },
      "mqe": { "queries": ["..."], "keywords": ["Savings Account", "account opening"] },
      "vector_search": [...],
      "bm25_search": [...],
      "rrf": { "total_fused": 16 },
      "reranking": { "total_ranked": 5 },
      "context": { "item_count": 2, "estimated_tokens": 580 },
      "grounding": { "status": "fully_supported" },
      "output_guardrail": { "output_ok": true }
    },
    "request_id": "req-123456"
  }
}
```

Runtime `support_level` categories:
- `fully_supported`
- `partially_supported`
- `ambiguous`
- `insufficient_evidence`
- `contradictory_evidence`

------------------------------------------------------------------------

## 9. Agent Architecture

The agent is an explicit graph rather than an unrestricted autonomous
loop.

``` mermaid
flowchart TD
    START((START)) --> InputGuard["1. input_guard<br/>(Deterministic + NeMo Colang)"]

    InputGuard -->|reject| Rejection["END<br/>(Rejection Envelope)"]
    InputGuard -->|allowed| LoadContext["2. load_context<br/>(SessionStore + Pronoun Substitution)"]

    LoadContext --> Retrieve["3. retrieve<br/>(MQE + Pinecone + BM25 + Soft Filter + RRF + Cross-Encoder)"]

    Retrieve -->|fail| OutputGuard["6. output_guard<br/>(Deterministic + NeMo Output Rails)"]
    Retrieve -->|assess| Assess["4. assess<br/>(Claim Grounding Assessment)"]

    Assess -->|generate| Generate["5a. generate<br/>(Evidence-Bounded Synthesis)"]
    Assess -->|policy| Policy["5b. policy<br/>(Unavailable / Clarification Policy)"]
    Assess -->|fail| OutputGuard

    Generate --> OutputGuard
    Policy --> OutputGuard

    OutputGuard -->|fallback| Fallback["7. fallback<br/>(Safe Static Output Fallback)"]
    OutputGuard -->|done| Persist["8. persist<br/>(SessionStore Audited Turn Commit)"]

    Fallback --> Persist
    Persist --> END((END))
    Rejection --> END
```

------------------------------------------------------------------------

## 10. Query Understanding

Query understanding identifies:

-   Primary intent
-   Banking topic
-   Entities
-   Multiple requested information units
-   Ambiguity
-   Conversational references
-   Scope
-   Retrieval requirements

Example:

``` text
"What are the eligibility requirements and minimum balance for BSBDA?"
```

can be represented as:

``` text
Intent:
    Banking product information

Entity:
    BSBDA

Information requests:
    1. Eligibility requirements
    2. Minimum balance
```

This decomposition enables partial-answer behavior.

------------------------------------------------------------------------

## 11. Multi-Query Expansion

MQE generates alternative formulations of the same information need.

``` mermaid
flowchart TD
    Query["Original User Query"] --> Analyzer["Query Analyzer"]
    Analyzer --> Q1["Query Variant 1"]
    Analyzer --> Q2["Query Variant 2"]
    Analyzer --> Q3["Query Variant 3"]
    Analyzer --> QN["Query Variant N"]

    Q1 --> Retrieval["Hybrid Retrieval"]
    Q2 --> Retrieval
    Q3 --> Retrieval
    QN --> Retrieval
```

MQE must preserve user intent, entities, scope, and constraints. It must
not introduce unsupported facts or unrelated intents.

------------------------------------------------------------------------

## 12. Hybrid Retrieval

``` mermaid
flowchart LR
    Query["Expanded Query"] --> Dense["Dense Retrieval"]
    Query --> Lexical["BM25 Retrieval"]

    Dense --> D["Dense Ranked Results"]
    Lexical --> L["Lexical Ranked Results"]

    D --> RRF["Reciprocal Rank Fusion"]
    L --> RRF

    RRF --> Candidate["Unified Candidate Pool"]
    Candidate --> Reranker["Semantic Reranker"]
    Reranker --> TopK["Top-K Evidence"]
```

The hybrid approach combines semantic similarity with exact lexical
matching, which is particularly useful for banking terminology, product
names, policy terms, and natural-language questions.

### Strategy 2 Soft Pre-Filtering with Graceful Fallback
To ensure high precision without risking false-negative recall collapse:
1. **Combined MQE + Domain Keyword Extraction**: In a single LLM call, `LLMQueryExpander.expand_detailed` generates diverse search formulations and extracts key banking entities/keywords.
2. **Casing Expansion**: Extracted keywords are automatically expanded to lowercase, uppercase, and title-case variants before filter construction.
3. **Soft Filter Execution & Fallback**: Searches on Pinecone and Elasticsearch initially apply active keyword constraints. If the candidate pool size falls below `min_fallback_candidates` (default 3), the system automatically triggers an unfiltered hybrid search fallback (retaining authoritative status and date constraints) to eliminate zero-result recall drops.

------------------------------------------------------------------------

## 13. Dense Retrieval

``` mermaid
flowchart TD
    Document["Knowledge Chunk"] --> Embed["Embedding Model"]
    Embed --> Vector["Embedding Vector"]
    Vector --> Pinecone[("Pinecone")]

    Query["User Query"] --> QEmbed["Query Embedding"]
    QEmbed --> Pinecone
    Pinecone --> Results["Semantic Candidates"]
```

The final embedding model remains a benchmark-driven decision.

------------------------------------------------------------------------

## 14. Lexical Retrieval

Elasticsearch provides lexical retrieval. Scoring is native BM25 (`k1 = 1.5`, `b = 0.75`) over chunk text. The application sends eligible chunks and metadata filters to Elasticsearch and reads back ranked hits. It does not keep a second in-memory BM25 index.

``` mermaid
flowchart TD
    KB["Knowledge Chunks"] --> ES[("Elasticsearch")]
    Query["Query"] --> ES
    ES --> Results["BM25 Candidates"]
```

------------------------------------------------------------------------

## 15. Reciprocal Rank Fusion

RRF combines the ranked outputs of dense and lexical retrieval.

``` mermaid
flowchart LR
    Dense["Dense Results"] --> RRF["Reciprocal Rank Fusion"]
    Lexical["BM25 Results"] --> RRF
    RRF --> Ranked["Fused Candidate Ranking"]
```

RRF is the rank-fusion stage. It is not the final semantic reranker.

------------------------------------------------------------------------

## 16. Semantic Reranking

The reranker receives the RRF candidate pool and scores
query-to-document relevance.

``` mermaid
flowchart TD
    Query["Information Need"] --> Reranker["Semantic Reranker"]
    Candidates["RRF Candidate Pool"] --> Reranker
    Reranker --> Scores["Relevance Scores"]
    Scores --> TopK["Selected Evidence"]
```

------------------------------------------------------------------------

## 17. Context Validation

Before generation, retrieved context is checked for:

-   Knowledge version
-   Document status
-   Source authority
-   Metadata validity
-   Effective date
-   Relevance threshold
-   Duplicate content
-   Context size
-   Instruction-like content

``` mermaid
flowchart TD
    Candidates["Reranked Candidates"] --> Metadata["Metadata Validation"]
    Metadata --> Version["Version Validation"]
    Version --> Authority["Source Validation"]
    Authority --> Relevance["Relevance Validation"]
    Relevance --> Decision{"Valid Context?"}

    Decision -->|Yes| LLM["Generation"]
    Decision -->|No| Safe["Clarification / Unavailable"]
```

------------------------------------------------------------------------

## 18. Knowledge Architecture

The knowledge layer is upstream of retrieval.

``` mermaid
flowchart LR
    Sources["Source Banking Documents"]
    Sources --> Parse["Document Parsing"]
    Parse --> Structure["Structure / Section Extraction"]
    Structure --> Chunk["Context-Aware Chunking"]
    Chunk --> Metadata["Metadata Enrichment"]
    Metadata --> Validate["Knowledge Validation"]
    Validate --> Version["Knowledge Versioning"]
    Version --> Publish["Approved Knowledge"]
    Publish --> Index["Indexing"]

    Index --> Pinecone[("Pinecone")]
    Index --> Elasticsearch[("Elasticsearch")]
```

------------------------------------------------------------------------

## 19. Knowledge Governance

``` mermaid
stateDiagram-v2
    [*] --> Ingested
    Ingested --> Parsed
    Parsed --> Chunked
    Chunked --> Validated
    Validated --> Approved
    Approved --> Published
    Published --> Superseded
    Published --> Archived

    Validated --> Rejected
    Rejected --> Ingested
```

Only approved/published knowledge should be eligible for production
retrieval according to the configured knowledge policy.

------------------------------------------------------------------------

## 20. Knowledge Versioning

Knowledge metadata should support:

-   Document ID
-   Document version
-   Source
-   Status
-   Effective date
-   Expiry or supersession information
-   Section/chunk identity

``` mermaid
flowchart LR
    V1["Document v1"] --> V2["Document v2"]
    V2 --> V3["Document v3"]
    V1 --> Sup1["Superseded"]
    V2 --> Sup2["Superseded"]
    V3 --> Current["Current"]
```

Retrieval should use version-aware filtering rather than blindly
searching historical representations.

------------------------------------------------------------------------

## 21. Chunk Architecture

Chunks should remain meaningful when retrieved independently.

Context breadcrumbs are included in the chunk representation:

``` text
# Document Title
## Product
### Eligibility

<chunk content>
```

``` mermaid
flowchart TD
    Document["Document"] --> H1["Document Title"]
    H1 --> H2["H2 Section"]
    H2 --> H3["H3 Section"]
    H3 --> Content["Content"]

    H1 --> Breadcrumb["Context Breadcrumb"]
    H2 --> Breadcrumb
    H3 --> Breadcrumb
    Content --> Chunk["Final Chunk"]
    Breadcrumb --> Chunk
```

Scenario/decision-guide documents may remain cohesive as a larger chunk
when they fit configured limits.

------------------------------------------------------------------------

## 22. Conversation Memory

Conversation memory exists for continuity, not factual authority.

``` mermaid
flowchart LR
    User["Current Query"] --> ContextBuilder["Conversation Context Builder"]
    Memory[("Conversation Memory")] --> ContextBuilder
    ContextBuilder --> QueryAnalysis["Query Analysis"]

    KB["Knowledge Base"] --> Retrieval["Retrieval"]
    QueryAnalysis --> Retrieval
    Retrieval --> Answer["Grounded Answer"]
```

Memory may resolve conversational references such as "its" or "one" to a
previously discussed product, but the factual answer must still be
retrieved from the current governed knowledge base.

### Multi-Turn Contextual Query Resolution Engine
Implemented in `app/ai/memory/context.py` and `store.py`:
- **SessionStore**: Thread-safe LRU session memory maintaining the last `MAX_MEMORY_TURNS` (default 5).
- **Deterministic Anaphora Engine**:
  - `_ANAPHORA_PATTERN`: Detects pronouns and elliptical phrases (`it`, `its`, `one`, `that account`, `this account`, `this card`, `that deposit`, `the same`).
  - `_substitute_anaphora`: Grammatically substitutes pronouns with the antecedent entity (e.g. `"How can I open one?"` with entity `"Savings Account"` -> `"How can I open a Savings Account?"`).
  - `extract_recent_entity`: Deterministically scans recent turns for canonical banking products.
- **Model-Based Contextualization Fallback**: If anaphoric reference cannot be resolved deterministically, invokes GPT-4o-mini with `_CONTEXTUALIZE_PROMPT` to rewrite the question as a standalone query without altering user intent or introducing new facts.

------------------------------------------------------------------------

## 23. Guardrail Architecture

``` mermaid
flowchart TB
    User["User Input"] --> DInput["Deterministic Input Controls"]
    DInput --> SemanticInput["Semantic Input Guardrails"]
    SemanticInput --> Agent["Agent / RAG Workflow"]

    Agent --> RetrievalGuard["Retrieval Guardrails"]
    RetrievalGuard --> LLM["LLM"]
    LLM --> OutputGuard["Output Guardrails"]
    OutputGuard --> Final["Final Response"]
```

------------------------------------------------------------------------

## 24. Deterministic Guardrails

Deterministic controls include:

-   Authentication
-   Authorization
-   Rate limits
-   Request size limits
-   Schema validation
-   Knowledge version filtering
-   Source status filtering
-   Metadata validation
-   Response schema validation
-   Known PII patterns where appropriate

Deterministic security controls must not depend on an LLM when
deterministic enforcement is possible.

------------------------------------------------------------------------

## 25. Semantic Guardrails

NeMo Guardrails is integrated as an embedded semantic control layer (`app/ai/guardrails/nemo_adapter.py`):

- **Singleton Lifecycle**: Compiled once at application startup into `AgentResources` closures to eliminate per-turn initialization latency.
- **Embedded Colang 1.0 Flows**:
  - `banking_dialog.co`: Recognizes canonical banking queries and emits the sentinel `PROCEED_TO_RETRIEVAL`; intercepts greetings, thanks, and capability inquiries without RAG overhead.
  - `jailbreaks.co`: Intercepts system prompt overrides, DAN persona hacks, and instruction bypasses.
  - `off_topic.co`: Intercepts generic off-topic questions (recipes, poems, homework) and speculative investment/stock advice requests.
  - `output_rails.co`: Runs the `check forbidden claims` flow with the custom Python action `check_forbidden_operational_claims` to block unauthorized transaction execution promises, fabricated account balances, or card block confirmations.

NeMo Guardrails operates alongside application-level deterministic controls, failing safely if disabled.

------------------------------------------------------------------------

## 26. JEV / Judge Architecture

JEV / System One models are planned primarily as an evaluation and
judging layer.

``` mermaid
flowchart TD
    Trace["Agent Execution Trace"] --> Judge["JEV / System One Judge"]

    Judge --> Ground["Groundedness"]
    Judge --> Relevance["Relevance"]
    Judge --> Claims["Unsupported Claims"]
    Judge --> Policy["Policy / Guardrail Behavior"]

    Ground --> Score["Evaluation Result"]
    Relevance --> Score
    Claims --> Score
    Policy --> Score
```

The judge should be independently evaluated against curated datasets
before being trusted for critical runtime decisions.

------------------------------------------------------------------------

## 27. Response Decision Model

``` mermaid
flowchart TD
    Evidence["Retrieved Evidence"] --> Assess["Evidence Assessment"]
    Assess --> Full{"Fully Supported?"}

    Full -->|Yes| Answer["Answer"]
    Full -->|No| Partial{"Some Requested Information Supported?"}

    Partial -->|Yes| PartialAnswer["Answer Supported Portion"]
    Partial -->|No| Ambiguous{"Ambiguous / Missing Context?"}

    Ambiguous -->|Yes| Clarify["Ask Clarification"]
    Ambiguous -->|No| Unavailable["Information Unavailable"]

    Answer --> Output["Validated Response"]
    PartialAnswer --> Output
    Clarify --> Output
    Unavailable --> Output
```

This directly implements the product policy:

1.  Answer only what exists in the knowledge base.
2.  Return supported portions while rejecting unsupported portions.
3.  Provide available information and ask for clarification when
    required.

------------------------------------------------------------------------

## 28. Evaluation Architecture

Evaluation is a parallel first-class system.

``` mermaid
flowchart TB
    Dataset["Evaluation Dataset"]

    Dataset --> RetrievalEval["Retrieval Evaluation"]
    Dataset --> AgentEval["End-to-End Agent Evaluation"]
    Dataset --> GuardEval["Guardrail Evaluation"]

    RetrievalEval --> Metrics1["Recall / Precision / MRR / NDCG"]
    AgentEval --> Ragas["Ragas"]
    AgentEval --> Custom["Custom Evaluators"]
    GuardEval --> JEV["JEV / System One"]

    Ragas --> Results["Evaluation Results"]
    Custom --> Results
    JEV --> Results
    Metrics1 --> Results

    Results --> Regression["Regression Gate"]
```

------------------------------------------------------------------------

## 29. Retrieval Evaluation

Retrieval should be evaluated independently from generation.

Metrics include:

-   Recall@K
-   Precision@K
-   MRR
-   NDCG
-   Context Recall
-   Context Precision

This helps distinguish poor retrieval from good retrieval followed by
poor generation.

------------------------------------------------------------------------

## 30. Generation Evaluation

Ragas and custom evaluators should evaluate:

``` mermaid
mindmap
  root((Answer Quality))
    Faithfulness
    Answer Relevancy
    Completeness
    Groundedness
    Unsupported Claims
    Scope Adherence
    Partial Answer Correctness
    Clarification Correctness
```

------------------------------------------------------------------------

## 31. Evaluation Dataset

The evaluation dataset should include:

``` mermaid
flowchart TD
    Dataset["Banking Evaluation Dataset"]
    Dataset --> Supported["Supported Questions"]
    Dataset --> Partial["Partially Supported"]
    Dataset --> Ambiguous["Ambiguous"]
    Dataset --> Unsupported["Unsupported"]
    Dataset --> OOS["Out of Scope"]
    Dataset --> Injection["Prompt Injection"]
    Dataset --> Indirect["Indirect Injection"]
    Dataset --> Followup["Conversation Follow-ups"]
    Dataset --> Adversarial["Adversarial Retrieval"]
```

This dataset should become a regression suite as the system evolves.

------------------------------------------------------------------------

## 32. Observability Architecture

LangSmith provides end-to-end tracing.

``` mermaid
flowchart LR
    Request["Request"] --> Trace["LangSmith Trace"]
    Trace --> Guard["Guardrails"]
    Trace --> Query["Query Analysis"]
    Trace --> MQE["MQE"]
    Trace --> Retrieval["Retrieval"]
    Trace --> RRF["RRF"]
    Trace --> Rerank["Reranking"]
    Trace --> Context["Context"]
    Trace --> LLM["LLM"]
    Trace --> Output["Output Guard"]
    Trace --> Response["Response"]
```

Useful trace metadata includes:

-   Request ID
-   Conversation ID
-   Knowledge version
-   Document IDs
-   Chunk IDs
-   Retrieval scores
-   Reranker scores
-   Model name/version
-   Latency
-   Token usage where available
-   Guardrail decisions
-   Evaluation scores

------------------------------------------------------------------------

## 33. AI Provider Abstraction

The AI layer should abstract providers from business logic.

``` mermaid
flowchart TD
    Agent["Agent / RAG"] --> Provider["LLM Provider Interface"]
    Provider --> OpenAI["OpenAI Provider"]
    Provider --> Future["Future Provider"]

    Embedding["Embedding Interface"] --> Selected["Selected Embedding Provider"]
    Embedding --> FutureEmbed["Future Embedding Provider"]
```

Development uses OpenAI GPT-4o-mini as specified in the PRD. The
embedding model remains benchmark-driven.

------------------------------------------------------------------------

## 34. Failure Handling

The architecture should fail safely.

``` mermaid
flowchart TD
    Request["Chat Request"] --> Agent["Agent"]
    Agent --> Retrieval["Retrieval"]

    Retrieval --> Available{"Retrieval Available?"}
    Available -->|No| RetrievalFail["Safe Retrieval Failure"]
    Available -->|Yes| Generate["Generation"]

    Generate --> Generated{"Generation Successful?"}
    Generated -->|No| GenFail["Safe Generation Failure"]
    Generated -->|Yes| Guard["Output Guard"]

    Guard --> Valid{"Valid?"}
    Valid -->|No| GuardFail["Safe Validation Failure"]
    Valid -->|Yes| Response["Response"]

    RetrievalFail --> Safe["Safe Error / Retry / Unavailable"]
    GenFail --> Safe
    GuardFail --> Safe
```

Infrastructure failures must never be converted into fabricated answers.

------------------------------------------------------------------------

## 35. Security Architecture

``` mermaid
flowchart TB
    Client["Client"] --> Transport["HTTPS / Transport Security"]
    Transport --> Network["Trusted Host / CORS"]
    Network --> Auth["Authentication"]
    Auth --> Authorization["Authorization"]
    Authorization --> Rate["Rate Limiting"]
    Rate --> Input["Input Validation"]
    Input --> Guard["Semantic Guardrails"]
    Guard --> Retrieval["Controlled Retrieval"]
    Retrieval --> Context["Context Isolation"]
    Context --> LLM["LLM"]
    LLM --> Output["Output Validation"]
    Output --> Audit["Logging / Tracing"]
```

Retrieved content remains isolated from system-level control
instructions.

------------------------------------------------------------------------

## 36. Complete Data Flow

``` mermaid
flowchart LR
    Source["Source Documents"] --> Knowledge["Knowledge Engineering"]
    Knowledge --> Approved["Approved Knowledge"]

    Approved --> Index["Indexing"]
    Index --> Vector["Pinecone"]
    Index --> Lexical["BM25"]

    User["User"] --> Query["Query"]
    Query --> MQE["MQE"]

    MQE --> Vector
    MQE --> Lexical

    Vector --> Fusion["RRF"]
    Lexical --> Fusion
    Fusion --> Rerank["Reranker"]
    Rerank --> Context["Validated Context"]

    Context --> LLM["LLM"]
    LLM --> Output["Guarded Response"]
    Output --> User
```

------------------------------------------------------------------------

## 37. Latency Architecture

The system should measure latency at each stage:

``` text
Request
  ├── Input guard
  ├── Query analysis
  ├── MQE
  ├── Dense retrieval
  ├── BM25 retrieval
  ├── RRF
  ├── Reranking
  ├── Context validation
  ├── LLM generation
  └── Output guard
```

Fixed latency targets are not assumed at this stage. Targets should be
established through benchmarking after implementation.

------------------------------------------------------------------------

## 38. Cost Control

Potential cost controls include:

-   Limiting MQE query count
-   Limiting retrieval candidate counts
-   Configurable reranking depth
-   Context-size controls
-   Environment-specific model selection
-   Prompt optimization
-   Caching where appropriate
-   Avoiding unnecessary model calls
-   Separating evaluation workloads from production workloads

Evaluation models should not automatically run on every production
request unless explicitly required.

------------------------------------------------------------------------

## 39. Deployment Architecture

The application is designed for containerized deployment.

``` mermaid
flowchart TB
    Client["Client"] --> LB["Load Balancer / Reverse Proxy"]

    LB --> API1["FastAPI Instance"]
    LB --> API2["FastAPI Instance"]
    LB --> APIN["FastAPI Instance"]

    API1 --> Pinecone[("Pinecone")]
    API2 --> Pinecone
    APIN --> Pinecone

    API1 --> Elasticsearch[("Elasticsearch")]
    API2 --> Elasticsearch
    APIN --> Elasticsearch

    API1 --> LLM["OpenAI API"]
    API2 --> LLM
    APIN --> LLM

    API1 --> LangSmith["LangSmith"]
    API2 --> LangSmith
    APIN --> LangSmith
```

The exact production infrastructure is intentionally left open at this
architecture stage.

------------------------------------------------------------------------

## 40. Environment Separation

The architecture supports:

``` text
Development
Testing
Production
```

Development uses GPT-4o-mini and development infrastructure.

Testing uses isolated settings and controlled external dependencies
where appropriate.

Production requires secure credentials, debug disabled, restricted
hosts/origins, real authentication, production observability, and
production knowledge configuration.

------------------------------------------------------------------------

## 41. Module Responsibilities

| Module | Responsibility |
|---|---|
| `core` | Configuration, exceptions, middleware, and application lifecycle |
| `api` | API aggregation and versioning |
| `modules/chat` | Chat API and conversation-facing application logic |
| `modules/knowledge` | Knowledge management and application integration |
| `ai/embeddings` | Embedding abstraction and generation |
| `ai/providers` | LLM and external AI provider adapters |
| `ai/prompts` | Prompt templates and prompt management |
| `ai/rag` | Query processing, retrieval, hybrid search, MQE, RRF, reranking, and context processing |
| `ai/agents` | Agent state, state management, and agent-facing logic |
| `ai/graphs` | LangGraph workflow definitions and orchestration |
| `ai/guardrails` | Input, retrieval, grounding, and output guardrails |
| `db` | Database connections, persistence infrastructure, and data-access configuration |
| `models` | Shared persistence and domain data models |
| `shared` | Reusable utilities and cross-module helpers |

------------------------------------------------------------------------

## 42. Dependency Direction

``` mermaid
flowchart TD
    API["API / Domain Modules"]
    AI["AI Application Layer"]
    RAG["RAG Components"]
    Providers["Provider Adapters"]
    DB["Infrastructure / Persistence"]
    Shared["Shared Kernel"]

    API --> AI
    API --> Shared
    AI --> RAG
    AI --> Providers
    AI --> Shared
    RAG --> Providers
    RAG --> Shared
    Providers --> Shared
    DB --> Shared
```

Lower-level infrastructure should not depend on high-level application
modules.

------------------------------------------------------------------------

## 43. Configuration Strategy

AI configuration should be externalized rather than hard-coded.

Examples:

``` text
LLM model
Embedding model
Retrieval top-K
MQE query count
RRF configuration
Reranker configuration
Grounding thresholds
Guardrail thresholds
Agent timeout
Retry configuration
Knowledge version
```

These should be represented through the application's settings system.

------------------------------------------------------------------------

## 44. Testing Architecture

``` mermaid
flowchart TD
    Tests["Test Strategy"]

    Tests --> Unit["Unit Tests"]
    Tests --> Integration["Integration Tests"]
    Tests --> Retrieval["Retrieval Tests"]
    Tests --> Agent["Agent Workflow Tests"]
    Tests --> Guard["Guardrail Tests"]
    Tests --> Eval["Evaluation Regression Tests"]
    Tests --> Smoke["Smoke Tests"]
    Tests --> Security["Security / Adversarial Tests"]
```

Examples:

### Unit Tests

-   Chunking
-   Metadata
-   RRF
-   Response policies
-   Validation

### Integration Tests

-   Pinecone retrieval
-   BM25 retrieval
-   LLM provider integration
-   LangGraph workflow

### Guardrail Tests

-   Prompt injection
-   Jailbreak
-   Out-of-scope queries
-   Partial support
-   Unsupported information

### Regression Tests

-   Fixed evaluation dataset
-   Retrieval quality
-   Answer quality
-   Guardrail behavior

------------------------------------------------------------------------

## 45. Architectural Trade-offs

### Modular Monolith vs Microservices

The project chooses a modular monolith initially because it reduces
operational complexity while preserving domain boundaries for future
extraction.

### Hybrid Retrieval vs Dense-Only Retrieval

Hybrid retrieval combines semantic similarity with exact lexical
matching, which is useful for banking terminology and natural-language
questions.

### RRF vs Single Retrieval Ranking

RRF combines independently ranked dense and lexical result sets without
requiring their raw scores to be directly comparable.

### Agent Graph vs Free-Form Agent Loop

An explicit LangGraph workflow provides predictable control flow,
inspectability, testability, guardrail insertion points, and easier
evaluation.

------------------------------------------------------------------------

## 46. Architectural Invariants

The following rules should remain true throughout implementation:

1.  The knowledge base is the authoritative source for banking facts.
2.  Retrieved content cannot override system policies.
3.  Unsupported information must not be fabricated.
4.  Partial support must be handled explicitly.
5.  Ambiguity should result in clarification when necessary.
6.  Agentic behavior must remain bounded.
7.  Deterministic controls should be preferred where appropriate.
8.  Retrieval and generation must be independently evaluable.
9.  Important execution steps must be traceable.
10. Knowledge versions must be distinguishable.
11. Transaction execution is outside the initial scope.
12. Evaluation is part of the architecture, not a final add-on.

------------------------------------------------------------------------

## 47. Future Evolution

The architecture can later evolve toward:

``` mermaid
flowchart LR
    Current["Knowledge Chat Agent"]
    Current --> CustomerData["Authorized Customer Data"]
    Current --> Tools["Controlled Banking Tools"]
    Current --> Human["Human Escalation"]
    Current --> Multilingual["Multilingual Support"]
    Current --> Voice["Voice Interface"]
    Current --> KG["Knowledge Graph"]
    Current --> LTR["Learning-to-Rank"]
```

These extensions must preserve the separation between knowledge, agent
reasoning, transactional actions, security, and evaluation.

------------------------------------------------------------------------

## 48. Final Architecture Summary

``` text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │  FastAPI    │
                    └──────┬──────┘
                           │
                           ▼
                    Input Guardrails
                           │
                           ▼
                    ┌─────────────┐
                    │ LangGraph   │
                    │ Chat Agent  │
                    └──────┬──────┘
                           │
                     Query Analysis
                           │
                           ▼
                          MQE
                    ┌──────┴──────┐
                    ▼             ▼
               Pinecone         BM25
                Dense          Lexical
                    │             │
                    └──────┬──────┘
                           ▼
                          RRF
                           │
                           ▼
                    Semantic Reranker
                           │
                           ▼
                   Context Validation
                           │
                           ▼
                          LLM
                           │
                           ▼
                   Output Guardrails
                           │
                           ▼
                    Grounded Answer
                           │
                           ▼
                         USER
```

The architecture makes the retrieval path, agent decisions, guardrails,
knowledge governance, and evaluation system explicit. This provides the
foundation for implementing the remaining RAG and conversational-agent
phases without turning the system into an unrestricted autonomous agent.
