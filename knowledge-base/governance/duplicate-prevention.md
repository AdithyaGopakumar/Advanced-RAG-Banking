# Duplicate Prevention Strategy

This document defines when to duplicate information, when to cross-reference, and how to maintain a Single Source of Truth (SSOT) across the knowledge base.

---

## Core Principle

**Every piece of information should have exactly one canonical source.** All other documents that need that information should reference the canonical source rather than reproducing it.

---

## Document Roles

### Canonical Documents (Single Source of Truth)

A canonical document is the **authoritative source** for a specific piece of information.

| Information Type | Canonical Location |
|---|---|
| Product features and eligibility | `docs/<category>/<product>.md` |
| Interest rates | `docs/interest-rates/` |
| Fees and charges | `docs/charges/` |
| Required documents | `docs/forms/` |
| Policies | `docs/policies/` |
| Glossary definitions | `glossary/banking-glossary.md` |

**Rules for canonical documents:**
- Must be the most detailed and complete source for that information
- Must be kept up to date first when information changes
- Must be clearly identified through their metadata `document_type` and `category`

### Referencing Documents

Documents that mention information from a canonical source but are not the primary source.

**Rules for referencing documents:**
- Provide a **brief summary** (1–2 sentences) for context
- Link to the canonical document for full details
- Never reproduce full tables, sections, or detailed content

### Derived Documents

Documents that synthesise information from multiple canonical sources (e.g., decision guides, scenarios, FAQs).

**Rules for derived documents:**
- Link back to every canonical source they draw from
- Provide summarised or reframed content, not copied content
- Must be reviewed when any referenced canonical document changes

---

## When to Duplicate (Acceptable Duplication)

| Situation | What to Duplicate | Why |
|---|---|---|
| **Self-containment** | A one-sentence summary of a key fact | Documents must be understandable in isolation (chunking requirement) |
| **FAQ answers** | A brief restatement of a product feature | FAQ answers should directly answer the question without requiring navigation |
| **Scenario steps** | A brief mention of a requirement | Scenarios must read as complete journeys |
| **Safety-critical information** | Emergency contact numbers, fraud reporting steps | Critical information should be immediately available |

### Acceptable Duplication Format

```markdown
The minimum balance for a Savings Account is ₹5,000. For a complete list of 
account-related charges, see [Account Charges](../charges/account-charges.md).
```

- The duplicated fact is **brief** (one sentence)
- The **canonical source** is linked
- The reader can get full details from the link

---

## When NOT to Duplicate

| Situation | Why Not | What to Do Instead |
|---|---|---|
| Full interest rate tables | Creates maintenance nightmare; rates change frequently | Link to `docs/interest-rates/` |
| Full charge schedules | Same product may appear in multiple charge tables | Link to `docs/charges/` |
| Detailed eligibility criteria | May change independently of the product | Keep in the product document (canonical) and reference from elsewhere |
| Complete process steps | Steps may be updated; duplicates become inconsistent | Link to the process document |
| Policy text | Compliance-sensitive; must have one definitive version | Link to `docs/policies/` |

---

## Content Ownership

Every piece of information has a single owner:

| Content | Owner | Responsibility |
|---|---|---|
| Product features and eligibility | Product SME | Keep canonical document current |
| Interest rates | Finance SME | Update rate documents promptly |
| Charges and fees | Finance SME | Update charge documents promptly |
| Required documents | Operations SME | Maintain form requirements |
| Policies | Compliance Lead | Ensure regulatory accuracy |
| FAQs | Technical Writer | Ensure FAQ summaries align with canonical sources |
| Scenarios | Technical Writer | Ensure scenarios reference current canonical sources |
| Decision guides | Technical Writer | Ensure comparisons reflect current product details |

---

## Detecting and Resolving Duplication

### During Authoring

Before writing a section, check:

1. Does this information already exist in a canonical document?
2. If yes, can I summarise in one sentence and link instead?
3. If I must include more detail, is there a strong reason? (self-containment, safety)

### During Review

Reviewers should check:

1. Does this document reproduce content that exists elsewhere?
2. Are all reproduced facts brief summaries with links to the canonical source?
3. If two documents state the same fact, do they agree?

### Periodic Audit

The Technical Writing Lead should quarterly:

1. Identify documents with overlapping content
2. Verify that brief summaries in referencing documents match canonical sources
3. Flag any inconsistencies for resolution

---

## Handling Inconsistencies

When duplicate information is found to be inconsistent:

1. **Identify the canonical source** — which document is authoritative?
2. **Update the canonical source** if it is wrong
3. **Update all referencing documents** to match
4. **Add to the review checklist** to prevent recurrence

---

## Related Documents

- [Repository Rules](repository-rules.md) — Rule 1 (Never Duplicate) and Rule 2 (Cross-Reference)
- [Cross-Reference Strategy](cross-reference-strategy.md) — How to link between documents
- [Knowledge Relationships](../metadata/knowledge-relationships.md) — Document relationship model
- [Maintenance Strategy](maintenance-strategy.md) — Update processes that prevent drift

---

*Last updated: 2026-08-02*
