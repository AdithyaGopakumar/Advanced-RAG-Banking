# Contribution Guide

This document provides detailed guidance for contributing documentation to the knowledge base. It supplements the repository-level [CONTRIBUTING.md](../CONTRIBUTING.md) with in-depth procedures.

---

## Who Can Contribute

| Role | Can Create | Can Update | Can Review | Can Approve |
|---|---|---|---|---|
| Technical Writer | Yes | Yes | Yes | No |
| Banking SME | Yes (with writer support) | Yes | Yes | Yes (content accuracy) |
| Compliance Reviewer | No | Suggest changes | Yes | Yes (compliance) |
| Knowledge Base Owner | Yes | Yes | Yes | Yes (all) |
| AI Engineer | No | Metadata only | Yes (metadata) | Yes (metadata) |

---

## Creating a New Document

### Step 1 — Determine the Document Type

Identify which category and template to use:

| Content Type | Template | Target Folder |
|---|---|---|
| Bank account product | `product-template.md` | `docs/accounts/` |
| Deposit product | `product-template.md` | `docs/deposits/` |
| Loan product | `loan-template.md` | `docs/loans/` |
| Card product | `card-template.md` | `docs/cards/` |
| Digital banking service | `service-template.md` | `docs/digital-banking/` |
| Payment service | `service-template.md` | `docs/payments/` |
| Banking service | `service-template.md` | `docs/services/` |
| Customer-facing policy | `policy-template.md` | `docs/policies/` |
| Security guide | `policy-template.md` | `docs/security/` |
| Support process | `process-template.md` | `docs/customer-support/` |
| Fee schedule | `product-template.md` | `docs/charges/` |
| Interest rate schedule | `product-template.md` | `docs/interest-rates/` |
| Required documents list | `process-template.md` | `docs/forms/` |
| FAQ collection | `faq-template.md` | `faqs/` |
| Customer scenario | `scenario-template.md` | `scenarios/` |
| Decision guide | `scenario-template.md` | `decision-guides/` |
| Glossary | N/A (append to existing) | `glossary/` |

### Step 2 — Copy the Template

```bash
cp templates/<template-name>.md docs/<category>/<new-document-name>.md
```

### Step 3 — Assign a Document ID

Follow the [Naming Conventions](naming-conventions.md) to assign a unique document ID:

1. Use the correct category prefix
2. Use the correct sub-category abbreviation
3. Use the next available number (check existing documents)

### Step 4 — Complete the Metadata

Fill in all YAML frontmatter fields. Required fields vary by document type but always include:

- `id`
- `title`
- `category`
- `document_type`
- `keywords`
- `version`
- `status` (set to `draft`)
- `last_updated`

### Step 5 — Write the Content

- Follow the [Style Guide](style-guide.md) for language and tone
- Follow the [Documentation Standards](documentation-standards.md) for formatting
- Follow the [Terminology Guidelines](terminology-guidelines.md) for banking terms
- Ensure the document is self-contained (see [Repository Rules](repository-rules.md), Rule 5)

### Step 6 — Add Cross-References

- Add a **Related Documents** section at the end
- Add the new document's ID to the `related_documents` field of any document that should reference it

### Step 7 — Self-Review

Run through the complete self-review checklist:

- [ ] Follows the correct template structure
- [ ] All metadata fields are complete and accurate
- [ ] Content is accurate (verified with SME if needed)
- [ ] Language follows the style guide
- [ ] Formatting follows documentation standards
- [ ] All internal links are valid
- [ ] Document is self-contained
- [ ] No duplicated information
- [ ] Customer-friendly language throughout
- [ ] Spelling and grammar are correct

### Step 8 — Submit for Review

1. Commit with a descriptive message: `docs(<category>): add <document-name>`
2. Create a pull request with:
   - Summary of the document's purpose
   - List of related documents updated
   - Any decisions or assumptions made
3. Tag the appropriate reviewers per [CODEOWNERS](../CODEOWNERS)

---

## Updating an Existing Document

### Minor Updates (Corrections, Typos)

1. Make the change directly
2. Do **not** change the document `version`
3. Update the `last_updated` date
4. Commit: `docs(<category>): fix <brief description>`

### Content Updates (Rates, Processes, Eligibility)

1. Make the content changes
2. Increment the **patch version** (e.g., 1.0 → 1.1)
3. Update `last_updated` and `last_reviewed`
4. Submit for SME review
5. Commit: `docs(<category>): update <brief description>`

### Structural Changes (New Sections, Reorganisation)

1. Make the structural changes
2. Increment the **minor version** (e.g., 1.1 → 2.0)
3. Update metadata
4. Submit for Knowledge Base Owner review
5. Commit: `docs(<category>): restructure <brief description>`

---

## Deprecating a Document

When a document is no longer relevant:

1. Update the metadata `status` field to `deprecated`
2. Add a deprecation notice at the top of the document:

```markdown
> **Warning:** This document has been deprecated as of [date]. 
> For current information, see [Replacement Document](path/to/replacement.md).
```

3. Do **not** delete the file — it may be referenced by the AI system or other documents
4. Remove it from the active document index
5. Commit: `docs(<category>): deprecate <document-name>`

---

## Conflict Resolution

When contributors disagree on content:

1. **Factual disputes** — Defer to the Banking SME or official RBI guidelines
2. **Style disputes** — Defer to the Style Guide; if ambiguous, defer to the Knowledge Base Owner
3. **Structural disputes** — Defer to the Knowledge Base Owner
4. **Metadata disputes** — Defer to the AI Engineering Lead

---

## Related Documents

- [CONTRIBUTING.md](../CONTRIBUTING.md) — Quick-start contribution workflow
- [Review Process](review-process.md) — What happens after you submit
- [Style Guide](style-guide.md) — Writing standards
- [Documentation Standards](documentation-standards.md) — Formatting standards
- [Naming Conventions](naming-conventions.md) — Naming rules

---

*Last updated: 2026-08-02*
