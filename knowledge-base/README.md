# Banking Customer Support Knowledge Base

## Purpose

This repository contains the official customer-facing knowledge base for the Bank. It serves as the single source of truth for all banking product documentation, policies, procedures, and customer support information.

The knowledge base is designed to be consumed by:

- **Customers** — through the Bank's website, mobile app, and support channels
- **AI Systems** — as the retrieval source for a Retrieval-Augmented Generation (RAG) powered customer support assistant
- **Technical Writers** — for maintaining and extending banking documentation
- **Subject Matter Experts** — for reviewing and validating content accuracy
- **Compliance Reviewers** — for ensuring regulatory alignment

---

## Documentation Philosophy

Every document in this repository follows these principles:

1. **Accuracy** — All information must be verified and current
2. **Clarity** — Use plain, customer-friendly English
3. **Self-Containment** — Each document must be understandable on its own, even when retrieved independently by an AI system
4. **Modularity** — Documents are atomic units that can be composed, linked, and retrieved individually
5. **Consistency** — All documents follow the same structure, style, and formatting standards
6. **Maintainability** — Content is organised for long-term upkeep by multiple contributors
7. **AI-Readiness** — Documents are optimised for semantic retrieval, chunking, metadata filtering, and citation

---

## Repository Layout

```
├── docs/                      # All customer-facing banking documentation
│   ├── accounts/              # Savings, Current, Salary, Minor accounts
│   ├── deposits/              # Fixed Deposits, Recurring Deposits, Tax Saver
│   ├── loans/                 # Home, Personal, Education, Vehicle, Gold, Business
│   ├── cards/                 # Credit Cards, Debit Cards, Prepaid Cards
│   ├── digital-banking/       # Mobile Banking, Internet Banking, UPI
│   ├── payments/              # NEFT, RTGS, IMPS, Cheque, Demand Draft
│   ├── services/              # ATM, Locker, Nomination
│   ├── policies/              # KYC, Account Closure, Dormant Accounts, Grievance
│   ├── security/              # Security Guidelines, Fraud Prevention, Safe Banking
│   ├── customer-support/      # Complaints, Escalation, Contact Channels
│   ├── charges/               # Fee schedules by category
│   ├── interest-rates/        # Deposit and loan interest rate schedules
│   └── forms/                 # Required documents and forms by process
│
├── faqs/                      # Frequently Asked Questions library
├── scenarios/                 # End-to-end customer journey walkthroughs
├── decision-guides/           # Product comparison and selection guides
├── glossary/                  # Banking terminology definitions
│
├── governance/                # Documentation standards and maintenance rules
├── templates/                 # Reusable document templates
├── metadata/                  # Metadata schema and AI optimisation specifications
├── assets/                    # Images, diagrams, and static resources
│
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution workflow
├── CHANGELOG.md               # Documentation version history
├── LICENSE                    # Licence information
└── CODEOWNERS                 # Ownership assignments
```

---

## Project Goals

1. **Comprehensive Coverage** — Document every customer-facing banking product, service, policy, and process
2. **RAG Optimisation** — Structure all content for high-quality retrieval by AI systems
3. **Regulatory Alignment** — Reflect RBI guidelines and Indian banking regulations
4. **Scalability** — Support hundreds of documents, thousands of FAQs, and multiple languages
5. **Production Quality** — Every document is ready for customer-facing deployment

---

## Intended Audience

| Audience | Use Case |
|---|---|
| Bank Customers | Understanding products, services, and processes |
| AI/RAG System | Retrieving accurate answers to customer queries |
| Technical Writers | Creating and maintaining documentation |
| Banking SMEs | Reviewing content for accuracy |
| Compliance Team | Ensuring regulatory correctness |
| Engineering Team | Integrating documentation into AI pipelines |

---

## Regional Context

This knowledge base is written for **Indian banking** customers. It assumes:

- Reserve Bank of India (RBI) regulatory framework
- Indian Rupee (INR) as the currency
- India-specific payment systems (UPI, NEFT, RTGS, IMPS)
- Aadhaar and PAN-based KYC requirements
- Indian tax regulations where applicable

---

## Getting Started

### For Contributors

1. Read the [Governance Documentation](governance/README.md) before making any changes
2. Follow the [Style Guide](governance/style-guide.md) for writing standards
3. Use the [Templates](templates/README.md) for creating new documents
4. Follow the [Contribution Guide](CONTRIBUTING.md) for the submission workflow
5. Review the [Naming Conventions](governance/naming-conventions.md) for file and folder naming

### For AI Engineers

1. Review the [Metadata Documentation](metadata/README.md) for schema specifications
2. See the [Repository Rules](governance/repository-rules.md) for content guarantees
3. Refer to individual document frontmatter for metadata filtering

---

## Key Standards

- **Language**: Clear, customer-friendly English
- **Format**: Markdown with YAML frontmatter
- **Structure**: Standardised sections per document type
- **Linking**: Cross-references via document IDs and relative paths
- **Versioning**: Semantic versioning for the repository; per-document version tracking via metadata

---

## Related Resources

| Resource | Location |
|---|---|
| Documentation Standards | [governance/documentation-standards.md](governance/documentation-standards.md) |
| Style Guide | [governance/style-guide.md](governance/style-guide.md) |
| Naming Conventions | [governance/naming-conventions.md](governance/naming-conventions.md) |
| Repository Rules | [governance/repository-rules.md](governance/repository-rules.md) |
| Review Process | [governance/review-process.md](governance/review-process.md) |
| Maintenance Strategy | [governance/maintenance-strategy.md](governance/maintenance-strategy.md) |
| Versioning Policy | [governance/versioning-policy.md](governance/versioning-policy.md) |
| Terminology Guidelines | [governance/terminology-guidelines.md](governance/terminology-guidelines.md) |

---

## Licence

See [LICENSE](LICENSE) for details.

---

*Last updated: 2026-08-02*
