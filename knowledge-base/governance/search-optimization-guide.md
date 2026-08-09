# Search Optimization Guide

This document provides guidance for authors to make documents highly discoverable through semantic retrieval. The goal is not SEO — it is optimising for a vector search and hybrid retrieval system.

---

## How Retrieval Works (Author's Perspective)

When a customer asks a question, the RAG system:

1. **Converts the question into a vector** (embedding) that captures its meaning
2. **Searches for document chunks** with similar meaning (semantic search)
3. **Optionally filters by metadata** (category, tags, product type)
4. **Optionally matches keywords** (hybrid search combining semantic and keyword matching)
5. **Returns the most relevant chunks** as context for generating an answer

**Your job as an author:** Write content that a machine can match to the way customers phrase questions.

---

## Keyword Strategy

### Primary Keywords

The `keywords` field in metadata should contain 3–15 terms that:

- Represent the core topics of the document
- Match how customers search and ask questions
- Include both formal and informal phrasings

**Example for a Savings Account document:**

```yaml
keywords:
  - "savings account"
  - "interest rate"
  - "minimum balance"
  - "account opening"
  - "zero balance account"
  - "passbook"
  - "savings bank"
```

### Keyword Selection Rules

| Do | Do Not |
|---|---|
| Use customer-facing language | Use internal system terms |
| Include both full terms and common abbreviations | Use only abbreviations |
| Think about what customers would type or say | Use only banking jargon |
| Include action phrases ("open account", "check balance") | List only nouns |
| Include related concepts | List unrelated terms for broader matching |

---

## Search Aliases

The `search_aliases` field captures alternative names, abbreviations, and common customer phrasings:

```yaml
search_aliases:
  - "SB account"
  - "savings bank account"
  - "basic account"
  - "bank account for savings"
```

### When to Use Search Aliases

| Use Case | Example |
|---|---|
| Common abbreviations | "FD" for Fixed Deposit, "RD" for Recurring Deposit |
| Colloquial terms | "bank account" for Savings Account |
| Regional variations | "cheque" and "check" |
| Common misspellings | "Aadhar" for "Aadhaar" |
| Older product names | Previous names for products that were renamed |
| Customer phrasings | "how to send money" for NEFT/RTGS/IMPS |

---

## Natural Language Phrasing

Customers ask questions in natural language. Authors should ensure their content naturally contains phrases that match customer queries.

### Matching Customer Questions to Content

| Customer Query | Content That Should Match |
|---|---|
| "How do I open a savings account?" | Section: "How to Open a Savings Account" |
| "What documents do I need for a home loan?" | Section: "Required Documents for Home Loan" |
| "What is the interest rate on FD?" | Section: "Interest Rates for Fixed Deposit" |
| "I lost my debit card, what do I do?" | Scenario: "Lost Card Replacement" |
| "Which account should I choose?" | Decision Guide: "Choose the Right Account" |
| "What are the charges for NEFT?" | Section: "Charges for NEFT Transfer" |

### Authoring Tips

1. **Use question-style headings** where appropriate: "How to Open a Savings Account" instead of "Account Opening Procedure"
2. **Include the product name in headings**: "Eligibility for Home Loan" not just "Eligibility"
3. **Write introductory sentences that mirror customer queries**: "To transfer money using NEFT, follow these steps..."
4. **Use common synonyms naturally** in the text: "The minimum balance (also called minimum average quarterly balance) is ₹5,000."

---

## Banking Terminology vs. Customer Language

Customers often use different terms than banking professionals. Content should bridge this gap:

| Banking Term | Customer Language | Author Action |
|---|---|---|
| EMI | Monthly payment | Use both in the content |
| Disbursement | Getting the loan money | Define and use both |
| Foreclosure | Paying off the loan early | Define and use both |
| Beneficiary | Person receiving money | Define and use both |
| Debit Card | ATM card | Note the common confusion |
| Internet Banking | Internet Banking, Online Banking | Use the approved term, add aliases |
| CIBIL Score | Credit score | Use both in the content |
| Account statement | Bank statement | Use the approved term, add alias |

### How to Bridge

```markdown
## Prepayment and Foreclosure of Home Loan

You can pay off your Home Loan before the scheduled end date. This is called 
**prepayment** (paying part of the outstanding amount early) or **foreclosure** 
(paying the entire remaining amount to close the loan).
```

---

## Intent Matching

Customers have specific intents when they search. Tag and write content to match these intents:

| Intent | Typical Query Pattern | Content Pattern |
|---|---|---|
| **Learn** | "What is...", "How does..." | Overview section, introductory paragraphs |
| **Apply** | "How to open...", "How to apply..." | Step-by-step process sections |
| **Compare** | "Which is better...", "Difference between..." | Decision guides, comparison tables |
| **Troubleshoot** | "Not working...", "Failed...", "Error..." | Troubleshooting guides, FAQ entries |
| **Calculate** | "How much...", "What will be..." | Rate tables, formula explanations, examples |
| **Report** | "Lost...", "Stolen...", "Fraud..." | Emergency procedures, complaint process |
| **Verify** | "What documents...", "Am I eligible..." | Eligibility sections, document requirement lists |

---

## Structural Optimization

### Heading Optimization

Headings are the strongest retrieval signals. Optimise them:

```markdown
## How to Open a Savings Account                    ← Matches "open savings account"
## Minimum Balance for Savings Account               ← Matches "minimum balance savings"
## Interest Rates for Savings Account                ← Matches "savings account interest rate"
## Documents Required to Open a Savings Account      ← Matches "documents for savings account"
```

### First Paragraph Optimization

The first paragraph of each section should summarise the key information:

```markdown
## Minimum Balance for Savings Account

A Savings Account with the Bank requires a minimum average quarterly balance of 
₹5,000. If the balance falls below this amount, a charge of ₹500 plus GST is 
applied each month.
```

This ensures the chunk contains the answer even if the rest of the section is not retrieved.

### Table Optimization

Tables should include context that aids retrieval:

```markdown
## Home Loan Interest Rates

The Bank offers Home Loans at competitive interest rates. Rates are linked to the 
External Benchmark Lending Rate (EBLR) and vary by loan amount and tenure.

*Table: Home Loan Interest Rates (Effective from 01 August 2026)*

| Loan Amount | Interest Rate (p.a.) |
|---|---|
| Up to ₹30,00,000 | 8.50% |
| ₹30,00,001 – ₹75,00,000 | 8.70% |
| Above ₹75,00,000 | 8.90% |
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Generic headings ("Overview", "Features") | Low retrieval precision | Include the product name |
| No keywords in first paragraph | Chunk misses keyword matching | Front-load key terms |
| Using only formal banking terms | Customers use informal terms | Bridge both terminologies |
| Very long sections without sub-headings | Chunks are too large and unfocused | Add H3 sub-sections |
| Empty sections ("To be updated") | Waste of retrieval resources | Remove or fill in |
| Duplicate content across documents | Conflicting retrieval results | Use cross-references |

---

## Related Documents

- [Tagging System](../metadata/tagging-system.md) — Structured tags for faceted filtering
- [Metadata Schema](../metadata/metadata-schema.md) — `keywords`, `search_aliases`, and `tags` fields
- [Chunking Guidelines](chunking-guidelines.md) — How content structure affects chunk quality
- [Terminology Guidelines](terminology-guidelines.md) — Approved terms and their alternatives
- [Style Guide](style-guide.md) — Language standards for customer-facing content

---

*Last updated: 2026-08-02*
