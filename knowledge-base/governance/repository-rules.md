# Repository Rules

This document defines the non-negotiable rules that all content in the knowledge base must follow. These rules ensure consistency, quality, and AI-readiness across the entire repository.

---

## Core Rules

### Rule 1 — Never Duplicate Information

Every piece of information must exist in **exactly one place**. If multiple documents need the same information, use cross-references.

**Do:**

```markdown
For current interest rates, see [Deposit Interest Rates](../interest-rates/deposit-interest-rates.md).
```

**Do not:**

Copy interest rate tables into the Fixed Deposit document, the Savings Account document, and the Recurring Deposit document.

**Rationale:** Duplication leads to inconsistency. When a rate changes, every copy must be updated. Missed copies create conflicting information, which is especially harmful for AI retrieval.

---

### Rule 2 — Cross-Reference Instead of Copying

When one document needs to mention information that lives in another document:

1. Provide a **brief summary** (1–2 sentences) for context
2. Link to the **source document** for full details
3. Never reproduce full tables, lists, or sections from other documents

**Example:**

```markdown
The Bank charges a processing fee for loan applications. Fees vary by loan type and amount.
For the complete fee schedule, see [Loan Charges](../charges/loan-charges.md).
```

---

### Rule 3 — Use Customer-Friendly Language

All documents are written for bank customers, not internal staff or technical teams.

- Use plain, simple English
- Explain banking terms on first use
- Avoid internal jargon, process codes, or system names
- Write at a reading level accessible to a wide audience

See the [Style Guide](style-guide.md) for detailed language standards.

---

### Rule 4 — Keep Documents Modular

Each document must cover **one topic** completely. Do not combine multiple products, services, or processes into a single document.

**Do:**

- `savings-account.md` — covers only the Savings Account
- `current-account.md` — covers only the Current Account

**Do not:**

- `bank-accounts.md` — covers Savings, Current, Salary, and Minor accounts in one file

**Rationale:** Modular documents chunk better for AI retrieval. A customer asking about Savings Accounts should not receive a chunk that mixes in Current Account information.

---

### Rule 5 — Every Document Must Be Self-Contained

Each document must be **fully understandable on its own**, without requiring the reader to consult other documents for basic context.

This means every document must:

- Define its scope in the Overview section
- Explain any banking terms used (or link to the glossary)
- Provide enough context for a reader who arrived via search
- Not rely on "see the previous section" references to other documents

**Rationale:** In a RAG system, documents are retrieved independently. A document that opens with "As described above..." or "Continuing from the previous section..." is useless when retrieved in isolation.

---

### Rule 6 — Include Complete Metadata

Every document must have:

- Complete YAML frontmatter (as defined by the metadata schema)
- A unique document ID
- Accurate category and sub-category tags
- Relevant keywords for semantic search
- Cross-references to related documents
- A `last_updated` date

---

### Rule 7 — Separate Static from Dynamic Information

Information that changes frequently (interest rates, charges, branch listings) should be:

1. Maintained in **dedicated reference documents** (in `charges/`, `interest-rates/`)
2. **Cross-referenced** from product documents
3. Marked in metadata as `dynamic_content: true` (future field)

Product documents should contain **static information** (features, eligibility, processes) that changes infrequently.

**Rationale:** In the future RAG system, dynamic data may come from APIs or databases instead of static documents. Separating concerns now makes that transition easier.

---

### Rule 8 — Follow the Template

Every document type has a designated template. When creating a new document:

1. Start from the correct template
2. Fill in all required sections
3. Remove optional sections that do not apply
4. Do not invent new sections unless approved by the Knowledge Base Owner

See [templates/README.md](../templates/README.md) for available templates.

---

### Rule 9 — Never Include Out-of-Scope Content

The knowledge base contains **only** customer-facing information. Never include:

- Internal employee procedures or workflows
- HR policies or internal memos
- Core banking system documentation
- Internal approval workflows or escalation matrices
- Infrastructure or deployment documentation
- Customer-specific data or personally identifiable information (PII)
- Confidential or restricted-access information

---

### Rule 10 — Maintain Consistent Terminology

Use the same term for the same concept throughout the entire knowledge base.

- If the repository calls it "Savings Account", never call it "savings a/c" or "SA" without first establishing the abbreviation
- Follow the [Terminology Guidelines](terminology-guidelines.md) for the approved vocabulary
- If a new term is needed, propose it through the review process

---

### Rule 11 — Design for AI Retrieval

When writing content, consider how it will be retrieved by an AI system:

- Use **descriptive headings** that match customer queries (e.g., "How to Open a Savings Account" not "Process")
- Include **keywords** naturally in the text
- Write **complete sentences** that make sense without surrounding context
- Avoid **ambiguous references** (use specific nouns instead of "this", "that", "it")
- Structure content so that any individual section can be a useful retrieval result

---

### Rule 12 — Version Everything

- Every content change must be committed to Git with a descriptive commit message
- Document-level versioning is tracked in YAML frontmatter
- Repository-level changes are tracked in [CHANGELOG.md](../CHANGELOG.md)
- Never make changes without documenting what changed and why

---

## Rule Enforcement

These rules are enforced through:

1. **Author self-review** — Authors check their work against these rules before submitting
2. **Peer review** — Reviewers verify compliance during the review process (see [Review Process](review-process.md))
3. **Automated checks** — Linting and validation tools verify metadata, links, and formatting
4. **Periodic audits** — The Knowledge Base Owner conducts quarterly audits for compliance

---

## Exceptions

If a situation requires deviating from these rules:

1. Document the exception and the rationale
2. Get approval from the Knowledge Base Owner
3. Add a comment in the document explaining why the rule was not followed

---

## Related Documents

- [Style Guide](style-guide.md) — Writing and language standards
- [Documentation Standards](documentation-standards.md) — Formatting and structural rules
- [Naming Conventions](naming-conventions.md) — File and folder naming rules
- [Review Process](review-process.md) — How compliance is verified during review
- [Terminology Guidelines](terminology-guidelines.md) — Approved banking vocabulary

---

*Last updated: 2026-08-02*
