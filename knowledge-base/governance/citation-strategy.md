# Citation Strategy

This document defines how documents should be authored to support reliable citations in AI-generated responses. When the future RAG system retrieves information, it must be able to cite the exact source with precision.

---

## Citation Goals

1. **Traceability** — Every piece of information can be traced to a specific document and section
2. **Stability** — Citation identifiers do not change when content is updated
3. **Precision** — Citations point to the specific section, not just the document
4. **Verifiability** — A human can follow a citation and find the referenced information
5. **Machine-Readable** — The RAG system can generate citations automatically

---

## Citation Format

The standard citation format for this knowledge base:

```
[Document Title] > [Section Heading] (Document ID, Version X.Y, Updated YYYY-MM-DD)
```

### Examples

```
Savings Account > Eligibility (ACCT-SA-001, v1.2, Updated 2026-08-02)
Home Loan > Interest Rates (LOAN-HL-001, v2.0, Updated 2026-09-15)
Accounts FAQ > Q: What is the minimum balance for a Savings Account? (FAQ-ACCT-001, v1.1, Updated 2026-08-10)
```

---

## Stable Section Identifiers

### Heading-Based Identifiers

Every H2 and H3 heading automatically becomes a citable section. Markdown generates anchor IDs from headings:

| Heading | Anchor ID |
|---|---|
| `## Eligibility` | `#eligibility` |
| `## Features and Benefits` | `#features-and-benefits` |
| `### Interest rate structure` | `#interest-rate-structure` |
| `## Required Documents` | `#required-documents` |

### Stability Rules

To keep citations stable:

1. **Do not rename H2 headings** unless absolutely necessary — it breaks existing citations
2. If a heading must be renamed, document the change in the CHANGELOG
3. **Adding new sections** between existing ones is safe (anchors are based on text, not position)
4. **Removing a section** requires checking for existing citations and references

---

## Authoring for Citability

### Rule 1 — Use Descriptive, Unique Headings

Headings must be unique within a document and descriptive enough to serve as citation context.

**Good:**
```markdown
## Eligibility for Savings Account
## Interest Rates for Savings Account
## Charges for Savings Account
```

**Bad:**
```markdown
## Eligibility
## Rates
## Charges
```

While the bad examples are unique within a single document, they are ambiguous when cited across the knowledge base.

### Rule 2 — Keep Key Facts Under Clear Headings

Information that is likely to be cited should appear under a clear, descriptive heading — not buried in a paragraph under a generic section.

**Good:**
```markdown
## Minimum Balance Requirement

The minimum average quarterly balance for a Savings Account is ₹5,000.
```

**Bad:**
```markdown
## Overview

...The Savings Account requires a minimum quarterly balance of ₹5,000, 
which is among many other features of this versatile product...
```

### Rule 3 — State Facts Definitively

Citable content should use definitive statements, not hedging language.

**Good:** "The processing fee for a Home Loan is 0.50% of the loan amount."

**Bad:** "The processing fee is usually around 0.50% or so."

### Rule 4 — Include Source Attribution

When content is derived from an external source (RBI circular, NPCI guideline), include the reference:

```markdown
As per RBI circular RBI/2022-23/123 dated 01 April 2023, banks must...
```

This enables the AI system to provide authoritative citations.

---

## Citation Metadata

The following metadata fields support citations:

| Field | Citation Role |
|---|---|
| `id` | Stable document identifier |
| `title` | Human-readable document name |
| `version` | Specific version being cited |
| `last_updated` | Date of the cited content |
| `effective_date` | When the information became effective |
| `regulatory_references` | External authoritative sources |
| `owner` | Who is responsible for the content |

---

## Regulatory Citation Format

When citing RBI or other regulatory guidelines:

```markdown
As per [RBI Master Direction on KYC](https://rbi.org.in/...) (RBI/2016-17/81, updated 2023):
```

### Regulatory Reference Table

Include regulatory references in the metadata:

```yaml
regulatory_references:
  - "RBI/2022-23/123 — Master Direction on KYC"
  - "RBI/2021-22/45 — Circular on Savings Account Interest"
```

And in the document body, use inline citations:

```markdown
> **Regulatory Basis:** This policy is based on RBI Master Direction RBI/2016-17/81 
> on Know Your Customer (KYC) norms, as amended from time to time.
```

---

## Citation in FAQ Documents

FAQ answers should be citable individually. The question itself serves as the citation heading:

```
Accounts FAQ > Q: Can I have two Savings Accounts? (FAQ-ACCT-001, v1.0)
```

### FAQ Citation Best Practices

- Phrase questions exactly as customers would ask them
- Include the full answer in a self-contained block
- Link to the source document for deeper information

---

## Version-Specific Citations

When information changes across versions, the citation system preserves history:

```
Savings Account > Interest Rates (ACCT-SA-001, v1.0, Updated 2026-08-02)  → 3.00% p.a.
Savings Account > Interest Rates (ACCT-SA-001, v1.1, Updated 2026-09-01)  → 3.50% p.a.
```

Git history maintains previous versions. The `version` field in metadata tracks the current version.

---

## External Link Citations

When linking to external sources:

```markdown
For more details, visit the [RBI website](https://www.rbi.org.in/) or contact the 
[Banking Ombudsman](https://cms.rbi.org.in/).
```

### Rules for External Links

- Only link to **authoritative sources** (RBI, NPCI, government websites)
- Do not link to news articles, blog posts, or third-party comparison sites
- Include the external link in both the document body and the metadata `regulatory_references` field
- Note that external links may break over time — provide enough context that the citation is useful even without the link

---

## Related Documents

- [Documentation Standards](documentation-standards.md) — Heading conventions that support citations
- [Chunking Guidelines](chunking-guidelines.md) — How section structure enables chunk-level citations
- [Versioning Policy](versioning-policy.md) — Version tracking for citation precision
- [Metadata Schema](../metadata/metadata-schema.md) — Citation-relevant metadata fields

---

*Last updated: 2026-08-02*
