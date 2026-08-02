# Chunking Guidelines

This document defines authoring rules that ensure documents can be effectively chunked by a future RAG system. These are writing guidelines — the actual chunking logic will be implemented in the RAG pipeline.

---

## Why Chunking Matters

In a RAG system, documents are split into smaller pieces (chunks) for indexing and retrieval. The quality of retrieval depends heavily on how well the source content aligns with chunk boundaries. Poorly structured documents produce poor chunks.

**Goal:** Write documents so that any section, when extracted as a chunk, provides a complete, useful, and self-contained answer.

---

## Document Size Guidelines

| Guideline | Target | Rationale |
|---|---|---|
| **Total document length** | 300–1,500 words | Documents over 1,500 words should be evaluated for splitting |
| **H2 section length** | 100–400 words | Each H2 section should be a viable standalone chunk |
| **H3 section length** | 50–200 words | H3 sections provide finer-grained chunks |
| **Paragraph length** | 2–4 sentences | Keeps chunks readable and focused |
| **Maximum section depth** | H4 | Deeper nesting indicates content should be restructured |

> **Note:** These are guidelines, not hard limits. Charge schedules and interest rate tables may naturally be shorter. Loan documentation with complex eligibility criteria may be longer.

---

## Section-Level Authoring Rules

### Rule 1 — Every Section Must Be Self-Contained

Each H2 section should make sense when read alone, without requiring the reader to have read previous sections.

**Do:**

```markdown
## Eligibility for Savings Account

To open a Savings Account with the Bank, you must meet the following criteria:

- Be an Indian resident aged 18 years or above
- Have a valid KYC document (Aadhaar, PAN, Passport, or Voter ID)
- Provide a recent passport-size photograph
```

**Do not:**

```markdown
## Eligibility

As mentioned in the overview above, this product has the following criteria:

- Same as listed in the table
- See the previous section for details
```

---

### Rule 2 — Headings Must Be Descriptive

Headings should describe the content clearly enough that a retrieval system can match them to customer queries.

| Good Heading | Bad Heading |
|---|---|
| "Eligibility for Home Loan" | "Eligibility" |
| "How to Apply for a Credit Card" | "Application" |
| "Interest Rates for Fixed Deposit" | "Rates" |
| "Required Documents for Account Opening" | "Documents" |
| "Charges for NEFT Transfer" | "Fees" |

**Rationale:** When a section is extracted as a chunk, the heading becomes the primary context signal. A heading that says "Eligibility" without context is ambiguous across dozens of products.

---

### Rule 3 — Front-Load Key Information

Put the most important information at the beginning of each section. If a chunk is truncated, the critical information should survive.

**Do:**

```markdown
## Minimum Balance for Savings Account

The minimum average quarterly balance requirement for a Savings Account is ₹5,000.
Failure to maintain this balance results in a monthly charge of ₹500 plus GST.
```

**Do not:**

```markdown
## Minimum Balance

There are many factors that determine account maintenance. The Bank has carefully 
designed its balance requirements to serve customers well. After considering various 
aspects, the minimum balance was set at ₹5,000.
```

---

### Rule 4 — One Topic Per Section

Each section should cover exactly one topic. Do not mix unrelated information.

**Do:**

```markdown
## Interest Rates

[Only interest rate information]

## Charges and Fees

[Only fee information]
```

**Do not:**

```markdown
## Interest Rates and Charges

[Mix of rate and fee information]
```

---

### Rule 5 — Include Context in Every Section

Because sections may be retrieved independently, include enough context to orient the reader.

**Do:**

```markdown
## Prepayment Charges for Home Loan

Home Loan borrowers can prepay part or all of their outstanding loan amount. 
The Bank charges a prepayment fee based on the loan type:

| Loan Type | Prepayment Charge |
|---|---|
| Floating Rate Home Loan | Nil |
| Fixed Rate Home Loan | 2% of prepaid amount |
```

**Do not:**

```markdown
## Prepayment Charges

| Type | Charge |
|---|---|
| Floating | Nil |
| Fixed | 2% |
```

---

### Rule 6 — Tables Must Have Context

Never start a section with a bare table. Always provide at least one sentence of context before the table.

**Rationale:** When a chunk contains only a table with no context, the retrieval system cannot determine what the table represents.

---

### Rule 7 — Avoid Cross-Section Dependencies

Sections should not depend on content from other sections within the same document.

**Do not:**

- "As shown in the table above..."
- "Using the formula from the previous section..."
- "Continuing from the eligibility criteria..."

**Instead:** Repeat the minimum necessary context or link to the relevant section explicitly.

---

### Rule 8 — Keep Lists Bounded

Long lists should be broken into categorised sub-sections:

**Instead of:**

```markdown
## Features
- Feature 1
- Feature 2
- ... (20 features)
```

**Use:**

```markdown
## Account Features

### Transaction features
- Feature 1
- Feature 2

### Digital banking features
- Feature 3
- Feature 4
```

---

## Chunk Boundary Indicators

The following elements serve as natural chunk boundaries for the future RAG system:

| Boundary | Chunking Behaviour |
|---|---|
| `---` (horizontal rule) | Major section break |
| H2 heading | Primary chunk boundary |
| H3 heading | Secondary chunk boundary |
| Metadata block (YAML) | Separate metadata chunk |

**Implication for authors:** Be deliberate about where you place H2 and H3 headings. Each heading potentially starts a new chunk.

---

## FAQ Chunking Considerations

FAQ documents have a unique structure. Each Q&A pair should be a viable chunk:

```markdown
### Q: What is the minimum balance for a Savings Account?

The minimum average quarterly balance for a Savings Account is ₹5,000.
If the balance falls below this amount, a monthly charge of ₹500 plus GST is applied.

**Related**: [Savings Account](../docs/accounts/savings-account.md)
```

- Each Q&A pair uses an H3 heading
- The question is phrased in natural language (matching customer queries)
- The answer is self-contained
- A related link provides deeper information

---

## Glossary Chunking Considerations

Each glossary entry should be a self-contained chunk:

```markdown
### Fixed Deposit

**Also known as**: FD, Term Deposit

A Fixed Deposit is a savings instrument where a lump sum amount is deposited 
with the Bank for a fixed tenure at a predetermined interest rate. The interest 
rate is typically higher than a Savings Account. The deposit can be withdrawn 
prematurely, subject to a penalty.

**Related terms**: [Recurring Deposit](#recurring-deposit), [Interest Rate](#interest-rate)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Very long sections (500+ words) | Chunks become too large, reducing retrieval precision | Split into H3 sub-sections |
| Very short sections (under 30 words) | Chunks lack context for meaningful retrieval | Merge with related section or add context |
| Sections with only a link | "See [document]" has no retrievable content | Add a summary before the link |
| Sections that reference "above" or "below" | Breaks self-containment when chunked | Use explicit section names or repeat context |
| Tables without surrounding context | Retrieval cannot identify the table's purpose | Always precede tables with explanatory text |
| Nested lists deeper than 2 levels | Complex structure chunks poorly | Flatten or convert to sub-sections |

---

## Related Documents

- [Documentation Standards](documentation-standards.md) — Heading hierarchy and formatting rules
- [Citation Strategy](citation-strategy.md) — How section identifiers support citations
- [Repository Rules](repository-rules.md) — Rule 5 (Self-Contained Documents)
- [Search Optimization Guide](search-optimization-guide.md) — How content structure supports retrieval

---

*Last updated: 2026-08-02*
