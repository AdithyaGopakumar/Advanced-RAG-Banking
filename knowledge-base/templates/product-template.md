# Product Documentation Template

<!-- 
TEMPLATE INSTRUCTIONS:
1. Copy this template to the appropriate folder under docs/
2. Rename following naming conventions (e.g., savings-account.md)
3. Fill in all YAML frontmatter fields
4. Complete all Required sections
5. Complete applicable Conditional sections
6. Remove any sections marked [REMOVE IF NOT APPLICABLE]
7. Delete all template instruction comments before publishing
-->

---

<!-- YAML FRONTMATTER — Complete all fields -->

```yaml
---
id: ""                              # e.g., "ACCT-SA-001"
title: ""                           # Must match H1 heading below
slug: ""                            # Must match filename without .md

domain: "products"
category: ""                        # accounts, deposits, cards
sub_category: ""                    # e.g., savings-account
document_type: "product"

applicable_to: ""                   # individual, business, both
target_audience: "both"             # customer, prospective-customer, both
applicable_channels:                # List applicable channels
  - "branch"
  - "internet-banking"
  - "mobile-banking"

language: "en"
region: "IN"

keywords:                           # 3–15 customer-facing search terms
  - ""
tags:                               # Minimum: 1 product + 1 segment + 1 channel
  - "product:"
  - "segment:"
  - "channel:"
search_aliases:                     # Common abbreviations and alternate names
  - ""
priority: "medium"                  # critical, high, medium, low

related_documents:                  # Document IDs of related content
  - ""

version: "1.0"
status: "draft"
created_date: ""                    # YYYY-MM-DD
last_updated: ""                    # YYYY-MM-DD
last_reviewed: ""                   # YYYY-MM-DD

owner: ""                          # e.g., "Retail Banking SME"
reviewer: ""

compliance_classification: "informational"  # regulatory, advisory, informational
confidentiality: "public"

dynamic_content: false
---
```

---

# [Product Name]

<!-- H1: Use the official product name. Must match the title in frontmatter. -->

## Overview

<!-- 
REQUIRED. 2–4 sentences summarising:
- What this product is
- Who it is designed for
- Its primary benefit
-->

---

## Features and Benefits

<!-- 
REQUIRED. List the key features and benefits of this product.
Use bullet points. Group into sub-sections if there are many features.
-->

### Key features

- 

### Benefits

- 

---

## Eligibility

<!-- 
REQUIRED. List all eligibility criteria clearly.
Include: age, residency, income, documentation, and any restrictions.
-->

| Criterion | Requirement |
|---|---|
| Age | |
| Residency | |
| Documentation | |
| Other | |

---

## Required Documents

<!-- 
REQUIRED. Brief summary of required documents.
Link to the canonical documents list in docs/forms/.
-->

To open a [Product Name], you will need the following documents:

- 
- 

For the complete list, see [Account Opening Documents](../forms/account-opening-documents.md).

---

## Interest Rates

<!-- 
CONDITIONAL: Include only if the product earns or charges interest.
Provide a brief summary and link to the canonical rates document.
[REMOVE IF NOT APPLICABLE]
-->

| Tier | Interest Rate (p.a.) |
|---|---|
| | |

For the latest rates, see [Deposit Interest Rates](../interest-rates/deposit-interest-rates.md).

---

## Fees and Charges

<!-- 
REQUIRED. Brief summary of key charges.
Link to the canonical charges document.
-->

| Charge | Amount |
|---|---|
| | |

For the complete fee schedule, see [Account Charges](../charges/account-charges.md).

---

## Transaction Limits

<!-- 
CONDITIONAL: Include for products with transaction limits.
[REMOVE IF NOT APPLICABLE]
-->

| Transaction Type | Channel | Limit |
|---|---|---|
| | | |

---

## How to Apply

<!-- 
REQUIRED. Step-by-step process for applying/opening.
Include channels available (branch, online, mobile).
-->

### Apply online

1. 
2. 
3. 

### Apply at a branch

1. 
2. 
3. 

---

## Important Information

<!-- 
CONDITIONAL: Include any important notes, warnings, or regulatory information.
Use admonitions sparingly.
[REMOVE IF NOT APPLICABLE]
-->

> **Important:** 

---

## Related Documents

<!-- 
REQUIRED. Link to all related documents with brief descriptions.
Order by relevance.
-->

- [Document Title](relative/path) — Brief description
- 

---

*Last updated: YYYY-MM-DD*
