# Tagging System

This document defines the structured tagging strategy for the knowledge base. Tags enable faceted filtering, retrieval refinement, and content discovery across the RAG system.

---

## Tagging Principles

1. **Namespaced Tags** — Every tag belongs to a namespace that describes its type
2. **Controlled Vocabulary** — Tags come from an approved list; contributors cannot invent arbitrary tags
3. **Multi-Dimensional** — A document can have tags from multiple namespaces
4. **Lowercase and Hyphenated** — Tags use `namespace:value` format, all lowercase with hyphens
5. **Complementary to Keywords** — Tags are structured; keywords are freeform. Both serve retrieval.

---

## Tag Format

```
namespace:value
```

**Rules:**
- Namespace and value are separated by a colon (`:`)
- No spaces in tags
- All lowercase
- Hyphens separate words within values
- A document must have at least 2 tags

---

## Tag Namespaces

### `product` — Product Tags

Identify which banking products a document relates to.

| Tag | Applies To |
|---|---|
| `product:savings-account` | Savings Account content |
| `product:current-account` | Current Account content |
| `product:salary-account` | Salary Account content |
| `product:minors-account` | Minor's Account content |
| `product:fixed-deposit` | Fixed Deposit content |
| `product:recurring-deposit` | Recurring Deposit content |
| `product:tax-saver-deposit` | Tax Saver FD content |
| `product:home-loan` | Home Loan content |
| `product:personal-loan` | Personal Loan content |
| `product:education-loan` | Education Loan content |
| `product:vehicle-loan` | Vehicle Loan content |
| `product:gold-loan` | Gold Loan content |
| `product:business-loan` | Business Loan content |
| `product:credit-card` | Credit Card content |
| `product:debit-card` | Debit Card content |
| `product:prepaid-card` | Prepaid Card content |

---

### `segment` — Customer Segment Tags

Identify the target customer segment.

| Tag | Description |
|---|---|
| `segment:retail` | Individual retail customers |
| `segment:business` | Business and MSME customers |
| `segment:nri` | Non-Resident Indian customers |
| `segment:senior-citizen` | Senior citizen customers |
| `segment:minor` | Minor (below 18) customers |
| `segment:women` | Women-specific products or benefits |
| `segment:salaried` | Salaried employees |
| `segment:self-employed` | Self-employed professionals |

---

### `channel` — Banking Channel Tags

Identify which banking channels are relevant.

| Tag | Description |
|---|---|
| `channel:branch` | In-branch services |
| `channel:internet-banking` | Internet Banking (Net Banking) |
| `channel:mobile-banking` | Mobile Banking app |
| `channel:atm` | ATM services |
| `channel:phone-banking` | Phone banking / IVR |
| `channel:upi` | UPI payments |
| `channel:all` | Available across all channels |

---

### `process` — Process Tags

Identify which banking processes a document covers.

| Tag | Description |
|---|---|
| `process:account-opening` | Opening a new account |
| `process:account-closure` | Closing an account |
| `process:kyc` | KYC verification |
| `process:fund-transfer` | Transferring money |
| `process:loan-application` | Applying for a loan |
| `process:card-application` | Applying for a card |
| `process:card-replacement` | Replacing a lost/damaged card |
| `process:dispute-resolution` | Resolving a transaction dispute |
| `process:complaint` | Filing a complaint |
| `process:nomination` | Setting up or changing nomination |
| `process:statement-request` | Requesting account statements |
| `process:cheque-request` | Requesting a cheque book |

---

### `intent` — Customer Intent Tags

Map to common customer intents for retrieval matching.

| Tag | Description |
|---|---|
| `intent:open` | Customer wants to open/start something |
| `intent:close` | Customer wants to close/cancel something |
| `intent:compare` | Customer wants to compare options |
| `intent:apply` | Customer wants to apply for something |
| `intent:check-status` | Customer wants to check a status |
| `intent:report-issue` | Customer wants to report a problem |
| `intent:understand` | Customer wants to learn how something works |
| `intent:calculate` | Customer wants to calculate something (EMI, interest) |
| `intent:update` | Customer wants to update their details |
| `intent:block` | Customer wants to block a card or service |

---

### `feature` — Product Feature Tags

Identify specific product features covered in the document.

| Tag | Description |
|---|---|
| `feature:interest-rate` | Interest rate information |
| `feature:eligibility` | Eligibility criteria |
| `feature:charges` | Fees and charges |
| `feature:limits` | Transaction or balance limits |
| `feature:rewards` | Reward points or cashback |
| `feature:insurance` | Insurance coverage |
| `feature:tax-benefit` | Tax-saving benefits (80C, 24, 80E) |
| `feature:overdraft` | Overdraft facility |
| `feature:auto-renewal` | Auto-renewal option |
| `feature:premature-withdrawal` | Premature withdrawal rules |
| `feature:prepayment` | Loan prepayment or foreclosure |
| `feature:emi` | EMI details |
| `feature:collateral` | Collateral or security requirements |

---

### `compliance` — Compliance Tags

Identify regulatory or compliance aspects.

| Tag | Description |
|---|---|
| `compliance:rbi` | RBI-regulated content |
| `compliance:kyc` | KYC-related requirements |
| `compliance:tds` | Tax Deducted at Source applicability |
| `compliance:fema` | FEMA-related (for NRI products) |
| `compliance:pmla` | Prevention of Money Laundering Act |
| `compliance:dicgc` | Deposit insurance coverage |
| `compliance:ombudsman` | Banking Ombudsman related |

---

### `security` — Security Tags

Identify security-related content.

| Tag | Description |
|---|---|
| `security:fraud-prevention` | Fraud awareness and prevention |
| `security:phishing` | Phishing-specific guidance |
| `security:card-security` | Card security (chip, PIN, CVV) |
| `security:online-security` | Internet and mobile banking security |
| `security:password` | Password and PIN management |
| `security:otp` | OTP-related security |

---

### `topic` — General Topic Tags

Broad topic tags for general classification.

| Tag | Description |
|---|---|
| `topic:getting-started` | Content for new customers |
| `topic:troubleshooting` | Problem resolution content |
| `topic:how-to` | Step-by-step guides |
| `topic:comparison` | Product comparisons |
| `topic:glossary` | Terminology definitions |
| `topic:faq` | Frequently asked questions |
| `topic:rates-and-charges` | Interest rates and fee information |
| `topic:documents-required` | Required document lists |

---

### `reference` — Reference Data Tags

Identify reference data documents.

| Tag | Description |
|---|---|
| `reference:interest-rates` | Interest rate tables |
| `reference:charges` | Fee and charge schedules |
| `reference:limits` | Transaction limit tables |
| `reference:forms` | Forms and document requirements |

---

## Tagging Rules

### Minimum Requirements

| Document Type | Minimum Tags |
|---|---|
| Product | 1 `product` + 1 `segment` + 1 `channel` |
| Service | 1 `channel` + 1 `process` |
| Policy | 1 `compliance` + 1 `process` |
| FAQ | 1 `product` or `topic` + `topic:faq` |
| Scenario | 1 `intent` + 1 `process` |
| Decision Guide | `intent:compare` + 1 `product` |
| Reference | 1 `reference` + 1 `product` |

### Do Not

- Do not create tags outside the approved namespaces without approval
- Do not use tags that duplicate the `category` or `sub_category` metadata fields
- Do not use more than 12 tags per document
- Do not use multi-word values without hyphens

---

## Requesting New Tags

1. Identify the namespace the new tag belongs to
2. Submit a pull request updating this document
3. Include a justification for why existing tags are insufficient
4. Get approval from the Knowledge Base Owner
5. Update any existing documents that should use the new tag

---

## Tags vs. Keywords vs. Search Aliases

| Feature | Tags | Keywords | Search Aliases |
|---|---|---|---|
| Format | `namespace:value` | Freeform phrases | Freeform phrases |
| Purpose | Structured faceted filtering | Semantic search matching | Alternative name matching |
| Vocabulary | Controlled | Open | Open |
| Example | `product:savings-account` | `"savings account opening"` | `"SB account"` |
| Used For | Filtering, categorisation | Embedding similarity | Query expansion |

All three serve retrieval but through different mechanisms. A well-tagged document with good keywords and search aliases will have the highest retrieval quality.

---

## Related Documents

- [Metadata Schema](metadata-schema.md) — Where tags appear in document frontmatter
- [Search Optimization Guide](../governance/search-optimization-guide.md) — How tags work with keywords for retrieval
- [Knowledge Taxonomy](knowledge-taxonomy.md) — How tags align with the classification hierarchy

---

*Last updated: 2026-08-02*
