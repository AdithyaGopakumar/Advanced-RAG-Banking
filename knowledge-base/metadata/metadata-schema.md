# Metadata Schema

This document defines the YAML frontmatter metadata schema that every document in the knowledge base must follow. The schema enables consistent classification, semantic retrieval, metadata filtering, citation support, and lifecycle management.

---

## Schema Overview

Every Markdown document begins with a YAML frontmatter block enclosed in triple dashes (`---`). The schema defines three tiers of fields:

| Tier | Description | Enforcement |
|---|---|---|
| **Required** | Must be present in every document | Automated validation blocks merge |
| **Conditional** | Required for specific document types | Validated per template |
| **Optional** | Enhances retrieval but not mandatory | Best-effort |

---

## Complete Field Specification

### Identification Fields

#### `id` — Document Identifier
- **Type**: String
- **Required**: Yes
- **Format**: `<CATEGORY_PREFIX>-<SUBCATEGORY>-<NNN>`
- **Validation**: Must be unique across the entire repository
- **Example**: `"ACCT-SA-001"`, `"LOAN-HL-001"`, `"FAQ-ACCT-001"`
- **Purpose**: Stable reference for cross-referencing and citations. Must never change once assigned.

#### `title` — Document Title
- **Type**: String
- **Required**: Yes
- **Validation**: Must match the H1 heading in the document body
- **Example**: `"Savings Account"`
- **Purpose**: Human-readable title used in search results and citations.

#### `slug` — URL-Safe Identifier
- **Type**: String
- **Required**: Yes
- **Format**: Lowercase, hyphen-separated, matching the filename without extension
- **Validation**: Must match the filename
- **Example**: `"savings-account"`, `"home-loan"`
- **Purpose**: Stable URL-safe identifier for web publishing and API references.

---

### Classification Fields

#### `domain` — Top-Level Domain
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `products`, `services`, `policies-and-compliance`, `customer-support`, `reference-data`, `forms-and-documentation`, `cross-cutting`
- **Example**: `"products"`
- **Purpose**: Broadest classification level. See [Knowledge Taxonomy](knowledge-taxonomy.md).

#### `category` — Functional Category
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `accounts`, `deposits`, `loans`, `cards`, `digital-banking`, `payments`, `banking-services`, `policies`, `security`, `support`, `charges`, `interest-rates`, `forms`, `faqs`, `scenarios`, `decision-guides`, `glossary`
- **Example**: `"accounts"`
- **Purpose**: Groups documents within a domain.

#### `sub_category` — Specific Topic
- **Type**: String
- **Required**: Yes
- **Format**: Lowercase, hyphen-separated
- **Example**: `"savings-account"`, `"home-loan"`, `"kyc-policy"`
- **Purpose**: Most specific classification level.

#### `document_type` — Nature of the Document
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `product`, `service`, `policy`, `process`, `reference`, `faq`, `scenario`, `decision-guide`, `glossary`, `troubleshooting`, `form`
- **Example**: `"product"`
- **Purpose**: Determines which template was used and what sections to expect.

---

### Audience and Applicability Fields

#### `applicable_to` — Target Customer Segment
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `individual`, `business`, `both`
- **Example**: `"individual"`
- **Purpose**: Enables filtering by customer type.

#### `target_audience` — Primary Reader
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `customer`, `prospective-customer`, `both`
- **Default**: `"customer"`
- **Example**: `"both"`
- **Purpose**: Distinguishes between existing and prospective customer content.

#### `applicable_channels` — Relevant Banking Channels
- **Type**: List of strings (enum)
- **Required**: Conditional (required for products and services)
- **Allowed Values**: `branch`, `internet-banking`, `mobile-banking`, `atm`, `phone-banking`, `upi`, `all`
- **Example**: `["branch", "internet-banking", "mobile-banking"]`
- **Purpose**: Enables filtering by available channel.

---

### Regional Fields

#### `language` — Document Language
- **Type**: String
- **Required**: Yes
- **Format**: ISO 639-1 code
- **Default**: `"en"`
- **Example**: `"en"`
- **Purpose**: Supports future multilingual expansion.

#### `region` — Applicable Region
- **Type**: String
- **Required**: Yes
- **Format**: ISO 3166-1 alpha-2 code
- **Default**: `"IN"`
- **Example**: `"IN"`
- **Purpose**: Enables regional filtering in future multi-region expansion.

---

### Retrieval Fields

#### `keywords` — Semantic Search Keywords
- **Type**: List of strings
- **Required**: Yes
- **Validation**: Minimum 3 keywords, maximum 15
- **Example**: `["savings account", "interest rate", "minimum balance", "passbook", "zero balance"]`
- **Purpose**: Primary keywords for semantic search matching. Use terms customers are likely to search for.

#### `tags` — Classification Tags
- **Type**: List of strings
- **Required**: Yes
- **Validation**: Minimum 2 tags, must follow the [Tagging System](tagging-system.md) conventions
- **Example**: `["product:savings-account", "segment:retail", "channel:all"]`
- **Purpose**: Structured classification for faceted filtering. See [Tagging System](tagging-system.md).

#### `search_aliases` — Alternative Search Terms
- **Type**: List of strings
- **Required**: Optional
- **Example**: `["SB account", "savings bank", "bank account", "basic account"]`
- **Purpose**: Common alternative names, abbreviations, or customer phrasings that should match this document.

#### `priority` — Retrieval Priority Hint
- **Type**: String (enum)
- **Required**: Optional
- **Allowed Values**: `critical`, `high`, `medium`, `low`
- **Default**: `"medium"`
- **Example**: `"high"`
- **Purpose**: Hints to the RAG system about retrieval ranking. Use `critical` for security alerts, `high` for core products, `medium` for standard docs, `low` for supplementary content.

---

### Relationship Fields

#### `related_documents` — Cross-References
- **Type**: List of strings
- **Required**: Yes
- **Format**: Document IDs
- **Validation**: Every ID must reference an existing document
- **Example**: `["RATE-DEP-001", "CHG-ACCT-001", "FORM-ACCT-001"]`
- **Purpose**: Enables graph-based navigation and "See Also" functionality. See [Cross-Reference Strategy](../governance/cross-reference-strategy.md).

#### `parent_document` — Hierarchical Parent
- **Type**: String
- **Required**: Optional
- **Format**: Document ID
- **Example**: `"ACCT-SA-001"`
- **Purpose**: Establishes parent-child relationships (e.g., a troubleshooting guide for a specific product).

#### `supersedes` — Replaced Document
- **Type**: String
- **Required**: Optional
- **Format**: Document ID
- **Example**: `"ACCT-SA-OLD-001"`
- **Purpose**: Links to a deprecated document that this document replaces.

---

### Lifecycle Fields

#### `version` — Document Version
- **Type**: String
- **Required**: Yes
- **Format**: `MAJOR.MINOR`
- **Example**: `"1.0"`
- **Purpose**: Tracks individual document version. See [Versioning Policy](../governance/versioning-policy.md).

#### `status` — Document Lifecycle Status
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `draft`, `in-review`, `approved`, `published`, `deprecated`, `archived`
- **Default**: `"draft"`
- **Example**: `"published"`
- **Purpose**: Tracks document lifecycle stage. See [Document Lifecycle](../governance/document-lifecycle.md).

#### `created_date` — Creation Date
- **Type**: String
- **Required**: Yes
- **Format**: `YYYY-MM-DD`
- **Example**: `"2026-08-02"`

#### `last_updated` — Last Modification Date
- **Type**: String
- **Required**: Yes
- **Format**: `YYYY-MM-DD`
- **Example**: `"2026-08-02"`

#### `last_reviewed` — Last Review Date
- **Type**: String
- **Required**: Yes
- **Format**: `YYYY-MM-DD`
- **Example**: `"2026-08-02"`
- **Purpose**: Used for staleness detection. See [Maintenance Strategy](../governance/maintenance-strategy.md).

#### `next_review_date` — Scheduled Review Date
- **Type**: String
- **Required**: Optional
- **Format**: `YYYY-MM-DD`
- **Example**: `"2026-11-02"`
- **Purpose**: Proactive review scheduling.

#### `effective_date` — Content Effective Date
- **Type**: String
- **Required**: Conditional (required for reference data: charges, interest rates)
- **Format**: `YYYY-MM-DD`
- **Example**: `"2026-08-01"`
- **Purpose**: When the documented information takes effect. Critical for rates and charges.

---

### Ownership Fields

#### `owner` — Document Owner
- **Type**: String
- **Required**: Yes
- **Example**: `"Retail Banking SME"`
- **Purpose**: Primary person or team responsible for content accuracy.

#### `reviewer` — Assigned Reviewer
- **Type**: String
- **Required**: Optional
- **Example**: `"Compliance Lead"`

#### `author` — Original Author
- **Type**: String
- **Required**: Optional
- **Example**: `"Knowledge Management Team"`

---

### Compliance Fields

#### `compliance_classification` — Regulatory Sensitivity
- **Type**: String (enum)
- **Required**: Optional
- **Allowed Values**: `regulatory`, `advisory`, `informational`
- **Default**: `"informational"`
- **Example**: `"regulatory"`
- **Purpose**: `regulatory` — content driven by RBI guidelines, `advisory` — Bank's recommended practices, `informational` — general information.

#### `regulatory_references` — Applicable Regulations
- **Type**: List of strings
- **Required**: Conditional (required when `compliance_classification` is `regulatory`)
- **Example**: `["RBI/2022-23/123", "KYC Master Direction 2016"]`
- **Purpose**: Enables traceability to specific regulatory requirements.

#### `confidentiality` — Access Level
- **Type**: String (enum)
- **Required**: Yes
- **Allowed Values**: `public`, `customer-only`, `restricted`
- **Default**: `"public"`
- **Example**: `"public"`
- **Purpose**: All documents in this knowledge base should be `public` or `customer-only`. `restricted` exists for future use.

---

### Dynamic Content Fields

#### `dynamic_content` — Contains Frequently Changing Data
- **Type**: Boolean
- **Required**: Optional
- **Default**: `false`
- **Example**: `true`
- **Purpose**: Flags documents that may become dynamic data sources in the future RAG system. Typically `true` for interest rates and charges.

#### `data_source` — External Data Source Reference
- **Type**: String
- **Required**: Optional
- **Example**: `"interest-rate-api"`
- **Purpose**: Future field. Identifies the API or database that will eventually replace static content.

---

## Complete Example — Product Document

```yaml
---
id: "ACCT-SA-001"
title: "Savings Account"
slug: "savings-account"

domain: "products"
category: "accounts"
sub_category: "savings-account"
document_type: "product"

applicable_to: "individual"
target_audience: "both"
applicable_channels:
  - "branch"
  - "internet-banking"
  - "mobile-banking"
  - "atm"

language: "en"
region: "IN"

keywords:
  - "savings account"
  - "interest rate"
  - "minimum balance"
  - "passbook"
  - "account opening"
  - "zero balance"
  - "savings bank"
tags:
  - "product:savings-account"
  - "segment:retail"
  - "channel:all"
  - "process:account-opening"
search_aliases:
  - "SB account"
  - "savings bank account"
  - "basic savings account"
priority: "high"

related_documents:
  - "RATE-DEP-001"
  - "CHG-ACCT-001"
  - "FORM-ACCT-001"
  - "DIGI-MB-001"
  - "FAQ-ACCT-001"

version: "1.0"
status: "published"
created_date: "2026-08-02"
last_updated: "2026-08-02"
last_reviewed: "2026-08-02"
next_review_date: "2026-11-02"

owner: "Retail Banking SME"
reviewer: "Technical Writing Lead"

compliance_classification: "regulatory"
regulatory_references:
  - "RBI Master Direction on SB Accounts"
confidentiality: "public"

dynamic_content: false
---
```

---

## Complete Example — Reference Data Document

```yaml
---
id: "RATE-DEP-001"
title: "Deposit Interest Rates"
slug: "deposit-interest-rates"

domain: "reference-data"
category: "interest-rates"
sub_category: "deposit-interest-rates"
document_type: "reference"

applicable_to: "both"
target_audience: "both"

language: "en"
region: "IN"

keywords:
  - "interest rate"
  - "fixed deposit rate"
  - "savings account interest"
  - "recurring deposit rate"
  - "senior citizen rate"
  - "FD rate"
tags:
  - "reference:interest-rates"
  - "product:fixed-deposit"
  - "product:savings-account"
  - "product:recurring-deposit"
  - "segment:retail"
search_aliases:
  - "FD rates"
  - "deposit rates"
  - "bank interest rates"
  - "current FD rate"
priority: "critical"

related_documents:
  - "ACCT-SA-001"
  - "DEP-FD-001"
  - "DEP-RD-001"
  - "DEP-TS-001"

version: "1.0"
status: "published"
created_date: "2026-08-02"
last_updated: "2026-08-02"
last_reviewed: "2026-08-02"
effective_date: "2026-08-01"

owner: "Finance SME"
reviewer: "Retail Banking SME"

compliance_classification: "informational"
confidentiality: "public"

dynamic_content: true
data_source: "interest-rate-api"
---
```

---

## Complete Example — FAQ Document

```yaml
---
id: "FAQ-ACCT-001"
title: "Accounts FAQ"
slug: "accounts-faq"

domain: "cross-cutting"
category: "faqs"
sub_category: "accounts-faq"
document_type: "faq"

applicable_to: "both"
target_audience: "both"

language: "en"
region: "IN"

keywords:
  - "savings account questions"
  - "how to open account"
  - "minimum balance"
  - "account closure"
  - "passbook"
  - "cheque book"
tags:
  - "faq:accounts"
  - "product:savings-account"
  - "product:current-account"
  - "segment:retail"
search_aliases:
  - "account help"
  - "account FAQ"
  - "bank account questions"
priority: "high"

related_documents:
  - "ACCT-SA-001"
  - "ACCT-CA-001"
  - "FORM-ACCT-001"

version: "1.0"
status: "published"
created_date: "2026-08-02"
last_updated: "2026-08-02"
last_reviewed: "2026-08-02"

owner: "Technical Writing Lead"

compliance_classification: "informational"
confidentiality: "public"

dynamic_content: false
---
```

---

## Validation Rules Summary

| Field | Rule |
|---|---|
| `id` | Unique across the repository |
| `title` | Matches H1 heading in document body |
| `slug` | Matches filename without `.md` extension |
| `domain` | Must be a valid enum value |
| `category` | Must be a valid enum value |
| `keywords` | 3–15 entries |
| `tags` | 2+ entries, following tagging system format |
| `related_documents` | All IDs must reference existing documents |
| `parent_document` | Must reference an existing document |
| `version` | Format `MAJOR.MINOR` |
| `status` | Must be a valid enum value |
| Date fields | Format `YYYY-MM-DD` |
| `regulatory_references` | Required when `compliance_classification` is `regulatory` |
| `applicable_channels` | Required for `product` and `service` document types |
| `effective_date` | Required for `reference` document type |

---

## Schema Evolution

When modifying this schema:

1. New **optional** fields can be added without a major version bump
2. New **required** fields require updating all existing documents (migration)
3. Removing or renaming fields requires a major version bump and migration plan
4. Changes must be approved by the Knowledge Base Owner and AI Engineering Lead
5. Update the [CHANGELOG](../CHANGELOG.md) with schema changes

---

## Related Documents

- [Knowledge Taxonomy](knowledge-taxonomy.md) — Classification hierarchy this schema references
- [Tagging System](tagging-system.md) — Tag naming conventions and categories
- [Knowledge Relationships](knowledge-relationships.md) — How `related_documents` connects the graph
- [Naming Conventions](../governance/naming-conventions.md) — Document ID format
- [Document Lifecycle](../governance/document-lifecycle.md) — Status field values and transitions
- [Versioning Policy](../governance/versioning-policy.md) — Version field rules

---

*Last updated: 2026-08-02*
