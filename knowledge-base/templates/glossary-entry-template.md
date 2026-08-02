# Glossary Entry Template

<!-- 
TEMPLATE INSTRUCTIONS:
This template defines the format for entries in the banking glossary
(glossary/banking-glossary.md). 

Unlike other templates, this is NOT copied as a standalone file.
Instead, use this format when adding entries to the glossary document.

Each entry is an H3 section that serves as a standalone retrieval chunk.
-->

---

## Entry Format

Each glossary entry follows this structure:

```markdown
### [Term Name]

**Also known as**: [Alternative names, abbreviations, or acronyms]

[Clear, customer-friendly definition in 1–3 sentences. Define what the term 
means in the context of Indian banking. Use simple language.]

**Example**: [Optional. A concrete example showing how the term is used.]

**Related terms**: [Link to related glossary entries]
```

---

## Example Entries

### EMI

**Also known as**: Equated Monthly Instalment

EMI is the fixed monthly payment made by a borrower to the Bank to repay a loan. Each EMI consists of two parts: the principal amount and the interest. The EMI amount remains the same throughout the loan tenure (for fixed-rate loans), making it easy to plan monthly expenses.

**Example**: If you take a Home Loan of ₹50,00,000 at 8.50% p.a. for 20 years, your monthly EMI would be approximately ₹43,391.

**Related terms**: [Tenure](#tenure), [Interest Rate](#interest-rate), [Prepayment](#prepayment)

---

### CIBIL Score

**Also known as**: Credit Score, Credit Information Bureau Score

A CIBIL Score is a three-digit number (ranging from 300 to 900) that represents your creditworthiness. It is calculated by the Credit Information Bureau (India) Limited based on your credit history, including loan repayments, credit card usage, and other credit activities. A higher score (typically 750 and above) improves your chances of loan approval.

**Related terms**: [Credit History](#credit-history), [Loan Eligibility](#loan-eligibility)

---

## Writing Rules for Glossary Entries

1. **Define from the customer's perspective** — explain what it means to them, not to the Bank
2. **Use simple language** — avoid circular definitions ("EMI is an instalment")
3. **Include context** — explain why the term matters
4. **Add examples** — especially for numerical or process-related terms
5. **Link related terms** — help customers build understanding
6. **Keep it brief** — 1–3 sentences for the definition, plus optional example
7. **Alphabetical order** — entries are arranged alphabetically within the glossary

---

## Glossary Document Metadata

```yaml
---
id: "GLOSS-001"
title: "Banking Glossary"
slug: "banking-glossary"

domain: "cross-cutting"
category: "glossary"
sub_category: "banking-glossary"
document_type: "glossary"

applicable_to: "both"
target_audience: "both"

language: "en"
region: "IN"

keywords:
  - "banking terms"
  - "financial glossary"
  - "banking definitions"
  - "what does X mean"
tags:
  - "topic:glossary"
  - "segment:retail"
priority: "medium"

related_documents: []

version: "1.0"
status: "draft"
created_date: ""
last_updated: ""
last_reviewed: ""

owner: "Technical Writing Lead"

compliance_classification: "informational"
confidentiality: "public"

dynamic_content: false
---
```

---

*Last updated: YYYY-MM-DD*
