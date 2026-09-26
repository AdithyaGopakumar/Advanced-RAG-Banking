# Advanced RAG Banking Chat Agent --- Architecture

**Document Status:** Draft --- Architecture Baseline\
**Version:** 1.0\
**Related Document:** `PRD.md`

------------------------------------------------------------------------

## 1. Architecture Overview

The Advanced RAG Banking Chat Agent is a **modular monolith** built
around a governed knowledge base, hybrid retrieval, a constrained
conversational agent, layered guardrails, and a first-class evaluation
and observability system.

The system is an **information-answering agent**, not a transactional
banking agent.

``` mermaid
flowchart TB
    User["User"] --> API["FastAPI API"]
    API --> InputGuard["Input Guardrails"]
    InputGuard --> Agent["LangGraph Chat Agent"]

    Agent --> Query["Query Understanding"]
    Query --> MQE["Multi-Query Expansion"]

    MQE --> Dense["Dense Retrieval"]
    MQE --> Lexical["BM25 Lexical Retrieval"]

    Dense --> Pinecone[("Pinecone")]
    Lexical --> BM25[("BM25 Index")]

    Pinecone --> RRF["Reciprocal Rank Fusion"]
    BM25 --> RRF

    RRF --> Reranker["Semantic Reranker"]
    Reranker --> Context["Context Validation"]

    Context --> LLM["LLM"]
    LLM --> OutputGuard["Output Guardrails"]
    OutputGuard --> Response["Grounded Response"]
    Response --> User

    KB["Governed Banking Knowledge Base"] --> Indexing["Knowledge Indexing Pipeline"]
    Indexing --> Pinecone
    Indexing --> BM25

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
        Web["Web / Mobile Client"]
    end

    subgraph API["FastAPI Application"]
        Router["API Router"]
        Auth["Authentication / Authorization"]
        Chat["Chat Module"]
        Health["System Module"]
    end

    subgraph Guardrails["Guardrails"]
        Input["Input Guards"]
        RetrievalGuard["Retrieval Guards"]
        Output["Output Guards"]
    end

    subgraph Agent["Agent Orchestration"]
        Graph["LangGraph Workflow"]
        Query["Query Analysis"]
        MQE["MQE"]
        Generation["Answer Generation"]
    end

    subgraph Retrieval["Retrieval"]
        Dense["Dense Retrieval"]
        Lexical["BM25"]
        Fusion["RRF"]
        Rerank["Semantic Reranker"]
        Validation["Context Validation"]
    end

    subgraph Knowledge["Knowledge"]
        KB["Governed Knowledge Base"]
        Pipeline["Knowledge Engineering"]
        Versioning["Version / Metadata"]
    end

    subgraph Models["Models"]
        LLM["LLM"]
        Embed["Embedding Model"]
        Judge["JEV / System One"]
    end

    subgraph Storage["Storage"]
        Pinecone[("Pinecone")]
        BM25Index[("BM25 Index")]
        Memory[("Conversation State")]
    end

    subgraph Eval["Evaluation / Observability"]
        Ragas["Ragas"]
        Custom["Custom Evaluators"]
        LangSmith["LangSmith"]
    end

    Web --> Router
    Router --> Auth
    Auth --> Chat
    Chat --> Input
    Input --> Graph
    Graph --> Query
    Query --> MQE
    MQE --> Dense
    MQE --> Lexical
    Dense --> Pinecone
    Lexical --> BM25Index
    Pinecone --> Fusion
    BM25Index --> Fusion
    Fusion --> Rerank
    Rerank --> Validation
    Validation --> Generation
    Generation --> LLM
    LLM --> Output
    Output --> Response["Final Response"]

    Pipeline --> KB
    KB --> Versioning
    Versioning --> Pinecone
    Versioning --> BM25Index

    Graph <--> Memory
    Ragas -.-> Graph
    Custom -.-> Graph
    Judge -.-> Graph
    LangSmith -.-> Graph
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

``` text
Backend/
├── run.py
├── main.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── responses.py
│   │   ├── lifecycle.py
│   │   └── middleware/
│   │
│   ├── api/
│   │   └── v1/
│   │       └── router.py
│   │
│   ├── modules/
│   │   ├── system/
│   │   ├── chat/
│   │   └── knowledge/
│   │
│   ├── ai/
│   │   ├── embeddings/
│   │   ├── prompts/
│   │   ├── providers/
│   │   ├── rag/
│   │   ├── agents/
│   │   ├── graphs/
│   │   └── guardrails/
│   │
│   ├── db/
│   ├── models/
│   └── shared/
│
├── tests/
└── docs/
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

The initial chat boundary is intentionally small:

``` text
POST /api/v1/chat
```

Example request:

``` json
{
  "conversation_id": "optional-id",
  "message": "What are the eligibility requirements for BSBDA?"
}
```

Example response:

``` json
{
  "success": true,
  "data": {
    "conversation_id": "conversation-id",
    "answer": "Grounded answer...",
    "status": "answered"
  }
}
```

Possible statuses:

-   `answered`
-   `partially_answered`
-   `clarification_required`
-   `information_unavailable`
-   `out_of_scope`
-   `blocked`

The API contract should remain independent of internal agent
implementation details.

------------------------------------------------------------------------

## 9. Agent Architecture

The agent is an explicit graph rather than an unrestricted autonomous
loop.

``` mermaid
flowchart TD
    START((START)) --> Input["Input Guard"]
    Input --> Analyze["Query Analysis"]
    Analyze --> Scope{"In Scope?"}

    Scope -->|No| Out["Out-of-Scope Response"]
    Scope -->|Yes| MQE["Multi-Query Expansion"]

    MQE --> Retrieve["Hybrid Retrieval"]
    Retrieve --> RRF["RRF"]
    RRF --> Rerank["Semantic Reranking"]
    Rerank --> Context["Context Validation"]
    Context --> Evidence{"Sufficient Evidence?"}

    Evidence -->|Yes| Generate["Generate Answer"]
    Evidence -->|Ambiguous| Clarify["Ask Clarification"]
    Evidence -->|No Evidence| Unavailable["Information Unavailable"]

    Generate --> Validate["Output / Claim Validation"]
    Validate --> Result{"Response Valid?"}

    Result -->|Fully supported| Answer["Return Answer"]
    Result -->|Partially supported| Partial["Return Supported Portion"]
    Result -->|Needs clarification| Clarify

    Answer --> END((END))
    Partial --> END
    Clarify --> END
    Unavailable --> END
    Out --> END
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

BM25 provides lexical retrieval for exact and term-oriented matching.

``` mermaid
flowchart TD
    KB["Knowledge Chunks"] --> Tokenize["Tokenization / Indexing"]
    Tokenize --> BM25[("BM25 Index")]
    Query["Query"] --> BM25
    BM25 --> Results["Lexical Candidates"]
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
    Index --> BM25[("BM25")]
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

Memory may resolve conversational references such as "its" to a
previously discussed product, but the factual answer must still be
retrieved from the current governed knowledge base.

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

NeMo Guardrails is planned for semantic conversational controls such as:

-   Banking-domain scope
-   Prompt injection detection
-   Jailbreak detection
-   Input policy
-   Output policy
-   Conversational constraints

NeMo Guardrails does not replace application-level security controls.

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

    API1 --> BM25[("BM25 Index")]
    API2 --> BM25
    APIN --> BM25

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
