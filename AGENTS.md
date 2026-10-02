# AGENTS.md

## 1. Purpose

This file defines the engineering instructions for implementing the Advanced RAG Banking Chat Agent.

This repository is a production-oriented FastAPI modular monolith. The system is a banking question-answering agent whose primary responsibility is to answer user queries using only information supported by the governed banking knowledge base.

**Important:** Do not treat this file as the complete product or architecture specification. Before implementing or changing functionality, read and follow the relevant project documentation.

---

## 2. Source of Truth

The project documentation is the primary source for product, architecture, RAG, agent, guardrail, evaluation, security, and knowledge-engineering decisions.

At minimum, review:

- `PRD.md` — product requirements, scope, boundaries, workflows, capabilities, delivery phases, and definition of done.
- `ARCHITECTURE.md` — system architecture and architectural principles.
- `KNOWLEDGE_ENGINEERING.md` — governed knowledge lifecycle and knowledge-processing design.
- `RAG_DESIGN.md` — retrieval, query expansion, fusion, reranking, context construction, and grounding design.
- `AGENT_DESIGN.md` — chat-agent behavior, orchestration, state, and LangGraph workflow.
- `GUARDRAILS.md` — input, retrieval, grounding, and output safety controls.
- `EVALUATION.md` — evaluation architecture, datasets, metrics, RAGAS, custom evaluators, JEV, and implementation phases.
- `SECURITY.md` — security requirements, threat model, controls, and secure implementation requirements.

If a requirement appears inconsistent across documents:

1. Do not silently choose an interpretation.
2. Identify the conflict.
3. Prefer the most specific document for the component being implemented.
4. Ask for clarification when the conflict affects architecture, security, data integrity, or user-visible behavior.

Do not replace documented project decisions with personal preferences without explicit approval.

---

## 3. Existing Backend Foundation

The repository already contains a FastAPI boilerplate.

Existing foundation includes:

- FastAPI application factory.
- Modular-monolith structure.
- `/api/v1` API aggregation.
- Configuration through Pydantic Settings.
- Centralized exception hierarchy and handlers.
- Standard success/error response envelopes.
- Request ID propagation.
- Request logging.
- Security headers.
- CORS.
- Trusted-host middleware.
- GZip.
- Rate limiting through slowapi.
- Lifecycle hooks.
- Docker multi-stage build and Docker Compose.
- Pytest configuration and initial tests.
- A system health module.
- Scaffolded AI directories.

Do not unnecessarily rewrite or replace this foundation.

Extend it cleanly and preserve existing conventions unless the project documentation explicitly requires a change.

Authentication is currently scaffolded and must not be considered production-ready merely because the dependency exists.

---

## 4. Core System Goal

The system is a banking chat agent.

Its purpose is narrowly defined:

> Answer user banking questions using information supported by the governed banking knowledge base.

The agent is **not** initially a transaction-execution agent.

Do not add unrelated capabilities such as:

- money transfers,
- account modification,
- payment execution,
- loan application submission,
- customer-service actions,
- arbitrary external tool execution,
- autonomous operational workflows,

unless explicitly added to the project scope later.

---

## 5. Fundamental Knowledge Policy

The governed banking knowledge base is the authoritative source for banking information.

The LLM's pretrained knowledge is not an authoritative banking source.

The implementation must preserve this principle throughout the pipeline:

```text
User Query
    ↓
Input Guardrails
    ↓
Query Processing
    ↓
Retrieval
    ↓
Evidence Validation / Grounding
    ↓
Agent Response Generation
    ↓
Output Guardrails
    ↓
Final Response
```

The LLM must not be allowed to freely answer banking questions from its own general knowledge when the knowledge base does not support the answer.

---

## 6. Expected Answering Behavior

The system must support three important evidence outcomes.

### Fully supported

When the retrieved evidence supports the requested information:

- Answer the supported question.
- Stay within the retrieved evidence.
- Do not introduce unsupported banking facts.

### Partially supported

When only part of a compound request is supported:

- Answer the supported portion.
- Explicitly identify the unsupported portion.
- Do not invent an answer for the unsupported portion.
- Ask for clarification where appropriate.

### Unsupported / insufficient evidence

When the knowledge base does not contain sufficient evidence:

- Do not fabricate an answer.
- Return an appropriate unavailable response or clarification request.
- Follow the documented guardrail and response policy.

The implementation must preserve claim-level grounding rather than relying only on a vague document-level similarity score.

---

## 7. Architecture

Use the documented modular-monolith architecture.

Expected high-level areas include:

```text
app/
├── core/
├── api/
├── modules/
│   ├── chat/
│   └── knowledge/
├── ai/
│   ├── embeddings/
│   ├── prompts/
│   ├── providers/
│   ├── rag/
│   ├── agents/
│   ├── graphs/
│   └── guardrails/
├── db/
├── models/
└── shared/
```

Keep domain/application concerns separated from AI infrastructure.

Avoid creating a large monolithic `agent.py`, `rag.py`, or `service.py` containing the entire system.

Prefer focused components with explicit responsibilities.

---

## 8. Agent Orchestration

The project uses LangGraph for agent orchestration.

Use LangGraph for explicit workflow/state transitions rather than hiding the entire application inside opaque agent abstractions.

The graph should make important control points visible, especially:

- input validation/classification,
- query processing,
- retrieval,
- evidence validation,
- response generation,
- output validation,
- safe termination paths.

Do not introduce autonomous tool-calling behavior unless explicitly required by the project documentation.

The agent's autonomy is intentionally constrained.

---

## 9. RAG Architecture

The documented retrieval architecture should be implemented as composable stages.

The current design includes:

- Dense retrieval through Pinecone.
- Lexical retrieval through Elasticsearch using native BM25.
- Multi-query expansion (MQE).
- Reciprocal Rank Fusion (RRF).
- Semantic reranking.
- Context construction.
- Evidence/grounding validation.

Do not collapse all retrieval behavior into one function.

Each stage should be independently testable.

Conceptually:

```text
User Query
   ↓
Query Analysis / MQE
   ↓
 ┌───────────────┐
 │               │
Dense           BM25
Retrieval       Retrieval
 │               │
 └───────┬───────┘
         ↓
       RRF
         ↓
Semantic Reranker
         ↓
Context Builder
         ↓
Evidence / Grounding Validation
```

The embedding model is subject to benchmarking/finalization according to the project plan. Do not hard-code an unapproved production embedding choice.

---

## 10. LLM Provider

Development LLM:

- OpenAI GPT-4o-mini.

The implementation should use a provider abstraction so the application is not tightly coupled to one vendor.

Provider-specific behavior belongs under:

```text
app/ai/providers/
```

Do not scatter direct OpenAI SDK calls throughout services, graph nodes, routes, or guardrails.

---

## 11. Guardrails

Guardrails are a first-class architectural concern.

The system uses:

- deterministic controls,
- NeMo Guardrails,
- evidence/grounding controls,
- output validation.

The guardrail architecture has four conceptual layers:

| Layer | Responsibility |
|---|---|
| Input Guardrails | Protect and classify the incoming request |
| Retrieval Guardrails | Validate retrieved material and prevent unsafe context propagation |
| Evidence / Grounding Guardrails | Determine whether evidence supports requested claims |
| Output Guardrails | Ensure generated responses comply with system policies |

Deterministic checks should be preferred where a deterministic rule is sufficient.

Do not use an LLM to perform a check that can reliably be implemented with a deterministic validation.

Retrieved documents must be treated as untrusted data, not as instructions.

The implementation must defend against indirect prompt injection contained inside retrieved documents.

---

## 12. Evaluation

Evaluation is a core product capability, not an afterthought.

The project uses:

- RAGAS,
- custom evaluation metrics,
- JEV / System One as the judge/evaluator model,
- LangSmith for tracing and evaluation observability.

Do not build evaluation only after the RAG pipeline is finished.

Evaluation hooks should be designed alongside retrieval and generation.

Where possible, capture:

- input query,
- query transformations,
- retrieved candidates,
- fused rankings,
- reranked evidence,
- selected context,
- generated answer,
- grounding decisions,
- guardrail outcomes,
- latency,
- token usage,
- evaluator results,
- trace identifiers.

Judge-based evaluation must itself be validated against curated evaluation datasets.

Do not treat a judge score as unquestionable ground truth.

---

## 13. Testing Requirements

Every meaningful feature must have tests.

At minimum, add appropriate:

### Unit tests

Test individual:

- parsers,
- chunkers,
- metadata builders,
- embedding adapters,
- retrieval adapters,
- BM25 logic,
- MQE logic,
- RRF,
- reranking,
- context construction,
- grounding checks,
- guardrails,
- prompt builders,
- graph nodes,
- response formatting,
- evaluation metrics.

### Integration tests

Test interactions between major components, such as:

- retrieval pipeline,
- RAG pipeline,
- graph execution,
- guardrail pipeline,
- provider adapters,
- persistence boundaries.

### API tests

Test:

- success responses,
- validation failures,
- authentication failures,
- rate limits,
- unsupported questions,
- partially supported questions,
- grounded answers,
- request IDs,
- error envelopes.

### Evaluation tests

Maintain curated examples for:

- supported questions,
- unsupported questions,
- partially supported questions,
- ambiguous questions,
- multi-intent questions,
- adversarial prompts,
- prompt injection attempts,
- indirect document injection,
- retrieval failures,
- grounding failures.

Do not write tests that merely reproduce implementation details. Prefer behavior-oriented assertions.

---

## 14. Clean Code Rules

Write code that is:

- readable,
- explicit,
- testable,
- maintainable,
- cohesive,
- loosely coupled.

Follow SOLID principles where they improve the design.

In particular:

### Single Responsibility

A module/class/function should have one clear reason to change.

### Open/Closed

Prefer interfaces and adapters where providers or implementations are expected to change.

### Dependency Inversion

Core application logic should depend on abstractions rather than concrete external services where practical.

### Interface Segregation

Do not create giant interfaces containing unrelated functionality.

### Liskov Substitution

Implementations of an abstraction should honor the abstraction's behavioral contract.

Do not apply SOLID mechanically when it makes simple code unnecessarily complex.

---

## 15. Dependency Injection

Use dependency injection for external dependencies where appropriate.

Examples:

- LLM provider,
- embedding provider,
- vector store,
- lexical retriever,
- reranker,
- evaluation provider,
- configuration,
- persistence repositories.

Avoid hidden global state.

Existing settings use `@lru_cache`; preserve that established configuration pattern.

---

## 16. Configuration

Do not hard-code:

- API keys,
- provider credentials,
- model names that should be configurable,
- Pinecone configuration,
- environment-specific URLs,
- evaluation configuration,
- production limits.

Use Pydantic Settings and environment variables.

Update `.env.example` whenever introducing a new required environment variable.

Never commit real secrets.

---

## 17. Error Handling

Use the existing centralized exception system.

Do not casually return inconsistent error shapes from individual endpoints.

Prefer domain-specific exceptions where they improve clarity.

Do not leak:

- API keys,
- credentials,
- internal stack traces,
- provider secrets,
- sensitive retrieved content,
- internal implementation details

to production clients.

Preserve request IDs in errors where supported by the existing middleware.

---

## 18. Logging and Observability

Use the existing logging infrastructure.

Logs should be:

- structured where appropriate,
- useful for debugging,
- free of secrets,
- free of unnecessary sensitive banking information.

Use request IDs and trace identifiers to correlate operations.

For AI operations, capture useful metadata without logging raw sensitive content unnecessarily.

Prefer identifiers, counts, timings, and decision metadata over unrestricted prompt/context logging.

---

## 19. Async and Performance

FastAPI handlers should remain asynchronous where appropriate.

Do not block the event loop with synchronous network or CPU-heavy operations.

If a dependency is synchronous and expensive, use an appropriate execution strategy rather than blocking the async request path.

Measure before optimizing.

Important performance areas include:

- embedding latency,
- Pinecone latency,
- BM25 retrieval,
- MQE generation,
- RRF,
- reranking,
- LLM generation,
- guardrails,
- evaluation.

Do not prematurely optimize at the cost of correctness or readability.

---

## 20. Database and Persistence

Persistence infrastructure belongs under:

```text
app/db/
```

Shared persistence/data models belong under:

```text
app/models/
```

Do not place database access directly inside API route handlers.

Use repository/service boundaries where the complexity justifies them.

Database connections and other long-lived resources should be managed through the application lifecycle.

---

## 21. Knowledge Engineering

Knowledge engineering is a governed pipeline.

The knowledge base is not merely a folder of documents.

Preserve the documented lifecycle:

```text
Create / Receive Source
        ↓
      Review
        ↓
     Validate
     ↙      ↘
   Fail      Pass
    ↓         ↓
  Review    Approve
              ↓
           Publish
              ↓
           Monitor
           ↙     ↘
       Update    Retire
          ↓
        Review
```

Do not bypass validation/governance for convenience.

Knowledge versioning, effective dates, provenance, and document metadata must remain available to downstream retrieval and evaluation where required by the documentation.

---

## 22. Context and Chunking

Follow the documented knowledge-engineering decisions for:

- section parsing,
- chunk generation,
- metadata,
- contextual breadcrumbs,
- scenario/decision-guide handling.

Do not independently redesign chunking while implementing retrieval unless the documentation is explicitly changed.

Chunking must preserve enough context for downstream semantic retrieval.

---

## 23. Prompts

Store reusable prompts under:

```text
app/ai/prompts/
```

Do not embed large prompt strings inside route handlers or business services.

Prompts should be:

- versionable,
- readable,
- testable,
- explicit about evidence boundaries,
- resistant to prompt injection,
- consistent with the system's KB-only policy.

The model should be explicitly instructed to treat retrieved content as evidence/data, not executable instructions.

---

## 24. Provider Abstractions

External services must be isolated behind adapters where practical.

Examples:

```text
LLMProvider
EmbeddingProvider
VectorStore
LexicalRetriever
Reranker
JudgeProvider
```

A provider adapter should not leak vendor-specific types throughout the application.

This allows:

- model benchmarking,
- provider replacement,
- testing with mocks/fakes,
- local development,
- future production model changes.

---

## 25. Retrieval Contracts

Retrieval components should return structured results rather than loosely formatted dictionaries.

A retrieval result should contain enough information for downstream processing, such as:

- document/chunk identifier,
- score,
- retrieval source,
- rank,
- metadata,
- content/reference,
- provenance/version information where applicable.

Do not discard provenance before grounding/evaluation.

---

## 26. Grounding and Claims

Treat grounding as a first-class operation.

A response should be decomposable into claims where needed for evaluation and validation.

The system should be able to determine whether claims are:

- supported,
- partially supported,
- unsupported.

Do not rely only on the fact that "some relevant documents were retrieved."

Relevant retrieval does not automatically mean sufficient evidence.

---

## 27. Security Rules

Follow `SECURITY.md` closely.

At minimum:

- never commit secrets,
- validate external input,
- treat retrieved content as untrusted,
- defend against prompt injection,
- isolate system instructions from retrieved content,
- validate generated output,
- apply authentication/authorization where required,
- apply rate limits,
- avoid sensitive logging,
- use secure configuration,
- preserve security headers,
- maintain dependency hygiene.

Security controls should be implemented as layered defenses rather than a single check.

---

## 28. API Design

Follow the existing API conventions.

Routes should be thin.

Prefer:

```text
Router
  ↓
Application/Service
  ↓
Domain / AI components
  ↓
Infrastructure adapters
```

Avoid putting retrieval, prompt construction, LLM calls, or database logic directly into FastAPI route functions.

Maintain:

- API versioning,
- consistent response envelopes,
- validation,
- documented status codes,
- predictable error behavior.

---

## 29. Comments and Documentation

Write comments to explain **why**, not obvious **what**.

Good:

```python
# Preserve the original rank because RRF requires rank position,
# not the raw similarity score.
```

Avoid:

```python
# Add one to rank
rank += 1
```

Document non-obvious:

- algorithms,
- safety decisions,
- provider constraints,
- architectural tradeoffs,
- security assumptions,
- evaluation methodology.

Do not fill the code with redundant comments.

Public interfaces and complex components should have useful docstrings.

---

## 30. Type Safety

Use Python type hints consistently.

Prefer:

- explicit return types,
- typed configuration,
- Pydantic models for structured boundaries,
- enums/literals where appropriate,
- protocols/abstract interfaces where appropriate.

Avoid unnecessary `Any`.

If `Any` is unavoidable at an external boundary, isolate it and validate/convert immediately.

---

## 31. Data Models

Use Pydantic models for API and structured application boundaries.

Keep models cohesive.

Do not pass arbitrary dictionaries through the entire system when a stable domain model would make the contract clearer.

However, do not create excessive models for trivial internal values.

---

## 32. Git and Change Discipline

Keep changes focused.

A change should ideally represent one coherent capability or fix.

Do not:

- reformat unrelated files,
- rename unrelated modules,
- change architecture casually,
- introduce unrelated dependencies,
- modify existing behavior without documenting why.

Before completing a task:

1. Review the diff.
2. Remove dead code.
3. Remove debug prints.
4. Check for accidental secrets.
5. Run relevant tests.
6. Run the full test suite when practical.

---

## 33. Dependencies

Add dependencies only when justified.

Before introducing a library:

1. Check whether the existing project already provides the capability.
2. Check whether the architecture requires the dependency.
3. Prefer mature, maintained libraries.
4. Keep provider-specific dependencies isolated where practical.
5. Update dependency files consistently.
6. Add tests for integration behavior.

Do not add heavyweight dependencies merely to avoid writing a small deterministic utility.

---

## 34. Testing External Services

Do not make normal unit tests depend on:

- live OpenAI calls,
- live Pinecone calls,
- live reranker APIs,
- live JEV calls,
- live LangSmith services.

Use:

- mocks,
- fakes,
- fixtures,
- deterministic test doubles.

Separate live/provider evaluation suites from ordinary CI unit tests.

---

## 35. Determinism

Where possible, core decision logic should be deterministic.

Examples:

- validation,
- metadata checks,
- rank fusion,
- filtering,
- threshold logic,
- policy decisions,
- response envelope formatting.

LLMs should be used where language reasoning is actually required.

Do not delegate simple deterministic decisions to an LLM.

---

## 36. Agent State

Keep agent state explicit and minimal.

Do not store unnecessary raw data in graph state.

State should contain only information required by downstream nodes.

Be deliberate about:

- query,
- transformed queries,
- retrieved evidence,
- grounding decisions,
- response draft,
- guardrail decisions,
- errors,
- metadata,
- trace identifiers.

Conversation memory is context, not the authoritative banking source.

---

## 37. Conversation Memory

The project uses conversation context as memory.

Memory must not become an independent source of banking truth.

When answering banking questions:

```text
Knowledge Base Evidence
        >
Conversation Memory
        >
LLM Pretrained Knowledge
```

Conversation history can help resolve references and context, but factual banking claims must remain grounded in governed knowledge.

---

## 38. Evaluation-First Development

When implementing a major AI component, define how it will be evaluated before considering the component complete.

For example:

### Retrieval

Measure:

- recall,
- precision-related retrieval metrics,
- ranking quality,
- MQE impact,
- RRF impact,
- reranker impact.

### Generation

Measure:

- faithfulness/groundedness,
- answer relevance,
- context relevance,
- completeness where applicable.

### Safety

Measure:

- prompt injection resistance,
- unsupported-answer rejection,
- partial-support behavior,
- indirect injection resistance.

### End-to-end

Measure:

- task success,
- grounded answer quality,
- latency,
- failure modes,
- guardrail outcomes.

Use RAGAS and custom evaluation as specified by `EVALUATION.md`.

---

## 39. Definition of Done for Code

A feature is not done merely because it works manually.

Before marking implementation complete, verify:

- [ ] Relevant project docs were reviewed.
- [ ] Existing architecture/conventions were preserved.
- [ ] Code has clear responsibilities.
- [ ] Types are present and meaningful.
- [ ] External dependencies are abstracted appropriately.
- [ ] Errors are handled consistently.
- [ ] Security implications were considered.
- [ ] Unit tests were added.
- [ ] Integration/API tests were added where applicable.
- [ ] Edge cases were tested.
- [ ] No secrets were introduced.
- [ ] Logging is appropriate.
- [ ] Documentation was updated if behavior/architecture changed.
- [ ] Relevant test suite passes.
- [ ] Diff was reviewed for unnecessary changes.

For AI functionality additionally verify:

- [ ] Evidence boundaries are explicit.
- [ ] Unsupported claims are not silently generated.
- [ ] Guardrails are applied at the correct layer.
- [ ] Retrieval provenance is preserved.
- [ ] Evaluation instrumentation exists.
- [ ] Tracing metadata is captured appropriately.

---

## 40. Implementation Workflow

For every implementation task, follow this sequence:

### Step 1 — Understand

Read the relevant documentation.

Identify:

- requirements,
- constraints,
- interfaces,
- dependencies,
- expected behavior,
- evaluation requirements.

### Step 2 — Inspect

Inspect the existing code before creating files.

Look for:

- existing abstractions,
- naming conventions,
- configuration patterns,
- exception handling,
- tests,
- reusable utilities.

Do not duplicate existing functionality.

### Step 3 — Plan

Before making a significant change, identify:

- files to create,
- files to modify,
- interfaces,
- test strategy,
- dependency changes,
- migration implications.

### Step 4 — Implement

Implement the smallest coherent change that satisfies the documented requirement.

Prefer simple, explicit code.

### Step 5 — Test

Run focused tests first.

Then run the broader suite.

For AI functionality, include deterministic test fixtures and evaluation cases.

### Step 6 — Review

Review:

- correctness,
- readability,
- security,
- performance,
- test coverage,
- architecture alignment,
- unintended side effects.

### Step 7 — Report

When reporting completion, summarize:

- what changed,
- tests executed,
- important design decisions,
- any remaining limitation or question.

Do not claim a feature is production-ready if required production controls remain unimplemented.

---

## 41. Do Not Guess

When the documentation or existing code does not provide enough information for a consequential architectural decision:

- stop before making the decision,
- explain the ambiguity,
- present the relevant options,
- ask for a decision.

Do not silently introduce a new architecture, provider, database, model, security policy, or user-visible behavior.

For small implementation details, use established project conventions and reasonable engineering judgment.

---

## 42. Avoid Overengineering

The goal is a serious production-oriented system, not maximum abstraction.

Avoid:

- unnecessary factories,
- unnecessary interfaces,
- excessive inheritance,
- speculative microservices,
- premature distributed systems,
- generic frameworks built before a need exists,
- abstractions with only one trivial implementation.

Use abstractions where they provide a real benefit:

- provider substitution,
- testability,
- clear boundaries,
- independent evaluation,
- security isolation,
- domain separation.

---

## 43. No Silent Scope Expansion

Do not add capabilities simply because they seem useful.

Examples:

- transaction tools,
- autonomous banking actions,
- web search,
- unrestricted browsing,
- external knowledge sources,
- unrelated recommendation systems,
- notification workflows.

If a capability is not in the documented scope, ask before implementing it.

---

## 44. Production Mindset

Treat the project as a production-oriented banking AI system.

That means prioritizing:

1. Correctness
2. Grounding
3. Security
4. Deterministic safety controls
5. Observability
6. Testability
7. Maintainability
8. Performance
9. Extensibility

Do not optimize for "demo behavior" at the expense of these properties.

---

## 45. Final Instruction

Before implementing anything substantial:

> Read the relevant documentation first, inspect the existing implementation second, plan the change third, implement it fourth, test it fifth, and review the resulting diff before declaring it complete.

When in doubt, preserve the documented architecture and ask rather than guessing.

The coding agent is responsible for implementing the project faithfully; the project documentation is responsible for defining what the project is.
