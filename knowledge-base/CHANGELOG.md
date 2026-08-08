# Changelog

All notable changes to this knowledge base will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.6.0] — 2026-08-08

### Added

- **Phase 6 — Deposits Domain Documentation**: Fully authored 7 customer-facing deposit product documents with complete structural content and Single Source of Truth (SSOT) markers.
  - Authored comprehensive product documentation for 7 deposit types (Fixed Deposit, Recurring Deposit, Tax Saver, Senior Citizen, Flexi/Sweep, NRE, NRO) incorporating accurate eligibility rules, features, benefits, and SSOT cross-references.
  - Updated the knowledge taxonomy and master knowledge map to formally register the new deposit products.
  - Conducted rigorous Phase 6C QA Audit confirming zero factual hallucinations, proper SSOT isolation for dynamic rates and penalties, and 100% RAG-readiness. Transitioned all 7 files to `status: "approved"`.

---

## [0.5.0] — 2026-08-08

### Added

- **Phase 5B — Accounts Domain Documentation**: Fully authored 12 customer-facing account product documents and 4 canonical reference documents with complete structural content and Single Source of Truth (SSOT) markers.
  - Authored canonical source documents (`docs/charges/account-charges.md`, `docs/interest-rates/deposit-interest-rates.md`, `docs/forms/account-opening-documents.md`, `docs/forms/kyc-documents.md`) with structural content and `<!-- BANK-SPECIFIC -->` markers to prevent hardcoding of dynamic facts.
  - Authored comprehensive product documentation for 12 account types (Savings, Current, Salary, BSBDA, Senior Citizen, Student, Minor, Joint, NRE, NRO, FCNR, PMJDY) incorporating accurate eligibility rules, features, benefits, and SSOT cross-references.
  - Resolved missing document skeletons by generating the necessary files and updating the taxonomy, knowledge map, and coverage matrix.

## [0.4.0] — 2026-08-03

### Added

- **Phase 4 — Knowledge Base Validation & AI Readiness Audit**: Added comprehensive master quality and AI preparedness audit report to governance documentation ([ai-readiness-audit.md](governance/ai-readiness-audit.md)).
  - **Repository Structure & Knowledge Coverage Reports**: Verified 100% adherence to lowercase kebab-case naming conventions, 100% README coverage across all 22 directory levels, and zero orphaned or duplicate document concepts across 96 document skeletons. Identified future growth gaps (wealth management, insurance, NRI banking).
  - **Metadata & Template Consistency Reports**: Confirmed 100% valid YAML syntax, required attribute declaration, H1-H2-H3 markdown heading hierarchy, and zero-content guardrail compliance. Identified 47 documents requiring explicit `related_documents` frontmatter population prior to RAG graph ingestion.
  - **Cross-Reference & Duplicate Content Risk Reports**: Verified 0 broken inline hyperlinks out of 240+ checked links. Established strict single-source canonical referencing rules for fees, rates, KYC checklists, and dispute escalation to prevent content divergence.
  - **AI Readiness & Future Expansion Assessment**: Confirmed modular chunk-friendly markdown formatting and hybrid search compatibility. Recommended RAG ingestion header preprocessing (`[Title | ID] - Section:`) to maintain context independence during vectorization.
  - **Risk Register & Final Readiness Scorecard**: Formulated 7 prioritized risk scenarios with specific mitigation plans. Awarded an overall repository Readiness Score of **94/100 (HIGH)**, formally certifying the repository for production content authoring.
- Registered audit report in `governance/README.md` under new Quality Assurance and Audits section.

---

## [0.3.0] — 2026-08-03

### Added

- Complete knowledge inventory: 96 document skeletons across 17 categories
  - Accounts: 5 products (Savings, Current, Salary, Student, Senior Citizen)
  - Deposits: 3 products (Fixed Deposit, Recurring Deposit, Tax Saver)
  - Loans: 7 products (Home, Personal, Education, Vehicle, Gold, Business, LAP)
  - Cards: 5 products (Credit, Debit, Prepaid, Virtual, Forex)
  - Digital Banking: 8 documents (5 services + 3 troubleshooting)
  - Payments: 7 documents (6 services + 1 troubleshooting)
  - Banking Services: 9 process/service documents
  - Policies: 8 customer-facing policies
  - Security: 5 security guidance documents
  - Customer Support: 4 support process documents
  - Charges: 5 fee schedule documents (dynamic content)
  - Interest Rates: 2 rate documents (dynamic content)
  - Forms: 4 document requirement checklists
  - FAQs: 8 category-specific FAQ collections
  - Scenarios: 10 customer journey walkthroughs
  - Decision Guides: 5 product comparison guides
  - Glossary: 1 banking terminology document
- Meta documents
  - Master knowledge map with architecture diagram and full document inventory
  - Coverage matrix with status, ownership, and priority tracking
  - Reusable components identification with canonical source mapping
  - Validation report (all checks passed)
- All skeleton documents include
  - Complete YAML frontmatter metadata
  - Standardized section headings from templates
  - TODO markers with owner, priority, phase, and dependencies
  - Cross-reference placeholders to related documents

### Changed

- Updated 18 category README indexes with document listings
- Updated docs/README.md with master documentation index
- Updated metadata/README.md with new meta documents

---

## [0.2.0] — 2026-08-02

### Added

- Knowledge architecture documentation
  - Knowledge taxonomy with 7 domains and all categories/subcategories
  - Metadata schema with 30+ fields, validation rules, and complete examples
  - Tagging system with 10 namespaces and controlled vocabulary
  - Knowledge relationships with graph patterns and Mermaid diagrams
- Document templates (11 templates)
  - Product template
  - Loan template
  - Service template
  - Process guide template
  - Policy template
  - FAQ template
  - Scenario template
  - Decision guide template
  - Glossary entry template
  - Troubleshooting template
  - Form / required documents template
- Governance additions
  - Cross-reference strategy
  - Chunking guidelines for RAG optimization
  - Citation strategy for AI-generated references
  - Search optimization guide for semantic retrieval
  - Duplicate prevention strategy
  - Multilingual strategy (future-proofing)
  - Document lifecycle (6 stages with transitions)
  - Information architecture guide

### Changed

- Updated governance/README.md with all new documents
- Updated metadata/README.md with architecture documentation
- Updated templates/README.md with all 11 templates

---

## [0.1.0] — 2026-08-02

### Added

- Initial repository structure and folder hierarchy
- Governance documentation
  - Style guide
  - Documentation standards
  - Naming conventions
  - Repository rules
  - Contribution guide
  - Review process
  - Maintenance strategy
  - Versioning policy
  - Terminology guidelines
- Placeholder README files for all documentation categories
- Root README with project overview and navigation
- CONTRIBUTING.md with contribution workflow
- .gitignore, LICENSE, and CODEOWNERS placeholders
- Metadata folder reserved for future schema definition
- Templates folder reserved for future document templates
