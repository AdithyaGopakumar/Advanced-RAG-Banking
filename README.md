# Banking RAG System & Knowledge Base

This repository is a monorepo containing both the production-grade banking customer support knowledge base and the future Retrieval-Augmented Generation (RAG) software components and backend code.

---

## Repository Structure

```
├── knowledge-base/       ← AI-friendly banking documentation, standards, taxonomy, and templates
├── Backend/              ← FastAPI service and knowledge ingestion
├── .gitignore            ← Repository-wide Git exclusions
├── LICENSE               ← Proprietary licence
└── README.md             ← Root repository overview
```

### 1. Knowledge Base (`knowledge-base/`)
The documentation repository serving as the single source of truth for the RAG system. It is structured, modular, self-contained, and pre-configured for semantic retrieval in the Indian banking context.
- **[View Knowledge Base Documentation](knowledge-base/README.md)**
- **[Governance & Standards](knowledge-base/governance/README.md)**
- **[Metadata & Taxonomy](knowledge-base/metadata/README.md)**
- **[Document Templates](knowledge-base/templates/README.md)**

### 2. Backend (`Backend/`)
FastAPI service and the knowledge ingestion pipeline. Setup, configuration, and the terminal ingest command are in [Backend/README.md](Backend/README.md).

From `Backend`, with the virtual environment active:

```powershell
.\.venv\Scripts\Activate.ps1
python ingest.py
```

`ingest.py` validates the knowledge base and indexes eligible chunks. With Pinecone unset, the dense index stays in memory for that process. Set `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` to write vectors to an existing 384-dimension cosine index.

---

## License

See [LICENSE](LICENSE) for terms and restrictions. Copyright (c) 2026 The Bank. All rights reserved.
