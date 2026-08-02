# Cross-Reference Strategy

This document defines how documents in the knowledge base reference one another. Consistent cross-referencing ensures navigability, prevents duplication, and supports the future knowledge graph.

---

## Cross-Reference Principles

1. **Reference, do not duplicate** — If information exists elsewhere, link to it
2. **Bidirectional awareness** — When A references B, consider whether B should reference A
3. **Brief context** — Every link includes a short description of what the reader will find
4. **Stable identifiers** — Use document IDs for metadata references, relative paths for inline links
5. **Maintainability** — Minimise the number of references to keep maintenance manageable

---

## Types of Cross-References

### 1. Metadata References

In the YAML frontmatter `related_documents` field:

```yaml
related_documents:
  - "RATE-DEP-001"
  - "CHG-ACCT-001"
  - "FORM-ACCT-001"
```

**Use for:** All related documents, regardless of relationship type. This is the primary input for the future knowledge graph.

### 2. Inline References

Within the document body, using relative Markdown links:

```markdown
To complete the account opening process, you will need to submit KYC documents.
See [KYC Documents](../forms/kyc-documents.md) for the complete list.
```

**Use for:** Providing context within a section where the reader may need more detail.

### 3. Related Documents Section

A dedicated section at the end of every document:

```markdown
## Related Documents

- [Current Account](../accounts/current-account.md) — Alternative account type for business use
- [Account Charges](../charges/account-charges.md) — Fee schedule for account operations
- [Accounts FAQ](../../faqs/accounts-faq.md) — Common questions about bank accounts
```

**Use for:** Comprehensive list of all related documents with context descriptions.

---

## When to Cross-Reference

| Situation | Action |
|---|---|
| Document mentions a charge or fee | Link to the charges document |
| Document mentions an interest rate | Link to the interest rates document |
| Document describes a process requiring KYC | Link to the KYC documents list |
| Document mentions a related product | Link to that product's document |
| Document mentions a digital channel | Link to the digital banking document |
| Document mentions a policy | Link to the policy document |
| FAQ answer summarises a product feature | Link to the full product document |
| Scenario references a product or process | Link to both |

---

## When NOT to Cross-Reference

| Situation | Reason |
|---|---|
| Common banking terms (ATM, PIN, EMI) | Use the glossary only if the term is complex or unusual |
| Well-known processes that are self-evident | Do not over-link; readers should not feel overwhelmed |
| References to the same document | Never self-reference |
| More than 10 related documents | Prioritise the most relevant; excess links reduce signal |

---

## Bidirectional Reference Rules

Not all references need to be bidirectional:

| Reference Type | Bidirectional? | Example |
|---|---|---|
| Product → Charges | Yes | Savings Account ↔ Account Charges |
| Product → Interest Rates | Yes | Fixed Deposit ↔ Deposit Interest Rates |
| Product → FAQ | One-way (FAQ → Product) | FAQ references the product; product does not need to list every FAQ |
| Scenario → Product | One-way (Scenario → Product) | Scenario references products; products do not list every scenario |
| Decision Guide → Products | One-way (Guide → Products) | Guide references products; products do not list every guide |
| Policy → Products | One-way (Policy → affected products) | Products reference policies they require |

---

## Reference Limits

To keep documents maintainable:

| Field | Minimum | Maximum | Guideline |
|---|---|---|---|
| `related_documents` (metadata) | 1 | 10 | Include only directly related documents |
| Inline references (per section) | 0 | 3 | Link only when context demands it |
| Related Documents section | 2 | 8 | Prioritise the most useful connections |

---

## Link Format Standards

### Inline Links

```markdown
See the [Savings Account](../accounts/savings-account.md) documentation for details.
```

- Use **descriptive link text** (never "click here" or "see here")
- Use **relative paths** from the current document
- Keep the link text short but meaningful

### Related Documents Section

```markdown
## Related Documents

- [Document Title](relative/path/to/document.md) — One-line description of what the reader will find
```

- Always include a dash and description after the link
- Order by relevance (most important first)
- Group logically if there are many links

---

## Handling Broken References

When a document is deprecated or moved:

1. Update all documents that reference it (search for the old document ID and path)
2. If a replacement exists, update the reference to point to the replacement
3. If no replacement exists, remove the reference and add context if needed
4. Run automated link validation after bulk changes

---

## Related Documents

- [Knowledge Relationships](../metadata/knowledge-relationships.md) — Conceptual relationship model
- [Duplicate Prevention](duplicate-prevention.md) — When to reference vs. duplicate content
- [Repository Rules](repository-rules.md) — Rule 1 (Never Duplicate) and Rule 2 (Cross-Reference Instead)
- [Metadata Schema](../metadata/metadata-schema.md) — `related_documents` and `parent_document` fields

---

*Last updated: 2026-08-02*
