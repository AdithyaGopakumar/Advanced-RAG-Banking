# Information Architecture Guide

This document provides step-by-step guidance for extending the knowledge base. It explains how to add new documents, create new categories, introduce new banking products, and maintain consistency as the repository grows.

---

## Adding a New Document

### Step 1 — Classify the Document

Use the [Knowledge Taxonomy](../metadata/knowledge-taxonomy.md) to determine:

1. **Domain**: Products, Services, Policies, etc.
2. **Category**: Accounts, Loans, Cards, etc.
3. **Subcategory**: Savings Account, Home Loan, etc.
4. **Document Type**: Product, Service, FAQ, Scenario, etc.

If the document does not fit any existing category, see [Adding a New Category](#adding-a-new-category).

### Step 2 — Choose the Right Template

Select the template from `templates/` that matches the document type:

| Document Type | Template |
|---|---|
| Product | `product-template.md` |
| Loan | `loan-template.md` |
| Service | `service-template.md` |
| Process | `process-template.md` |
| Policy | `policy-template.md` |
| FAQ | `faq-template.md` |
| Scenario | `scenario-template.md` |
| Decision Guide | `decision-guide-template.md` |
| Glossary Entry | `glossary-entry-template.md` |
| Troubleshooting | `troubleshooting-template.md` |
| Form/Documents | `form-template.md` |

### Step 3 — Assign a Document ID

Follow the [Naming Conventions](naming-conventions.md) to assign a unique ID:

1. Look up the category prefix
2. Determine the subcategory abbreviation
3. Find the next available number

### Step 4 — Create the Document

1. Copy the template to the correct folder
2. Rename following the naming conventions
3. Fill in the YAML frontmatter completely
4. Write the content following the [Style Guide](style-guide.md) and [Documentation Standards](documentation-standards.md)
5. Apply the [Chunking Guidelines](chunking-guidelines.md) and [Search Optimization Guide](search-optimization-guide.md)
6. Add tags per the [Tagging System](../metadata/tagging-system.md)

### Step 5 — Establish Relationships

1. Identify related documents
2. Add them to the `related_documents` metadata field
3. Add a Related Documents section at the end
4. Update the related documents to reference the new document (bidirectional, where appropriate)
5. Follow the [Cross-Reference Strategy](cross-reference-strategy.md)

### Step 6 — Submit for Review

Follow the [Contribution Guide](contribution-guide.md) and [Review Process](review-process.md).

---

## Adding a New Banking Product

When the Bank launches a new product:

### Before You Start

1. Identify the product's **domain** and **category** in the taxonomy
2. Determine if this is a variant of an existing product or a completely new product type
3. Check if a new subcategory is needed

### Checklist of Documents to Create

For a new banking product, you typically need:

- [ ] **Product document** — Core features, eligibility, process
- [ ] **Charges entry** — Add the product's charges to the relevant charges document
- [ ] **Interest rate entry** — Add rates to the relevant rates document (if applicable)
- [ ] **Required documents entry** — Add to the relevant forms document
- [ ] **FAQ entries** — Add Q&A pairs to the relevant FAQ document
- [ ] **Decision guide update** — Update the relevant comparison guide to include the new product
- [ ] **Glossary entry** — Add any new terms to the glossary

### Example: Launching a "Green Savings Account"

1. **Category**: Products → Accounts → Green Savings Account
2. **Document ID**: `ACCT-GS-001`
3. **File**: `docs/accounts/green-savings-account.md`
4. **Template**: `product-template.md`
5. **Updates needed**:
   - Add charges to `docs/charges/account-charges.md`
   - Add interest rates to `docs/interest-rates/deposit-interest-rates.md`
   - Add to `docs/forms/account-opening-documents.md` (if different requirements)
   - Add FAQ entries to `faqs/accounts-faq.md`
   - Update `decision-guides/choose-right-account.md`
   - Update `metadata/knowledge-taxonomy.md`

---

## Adding a New Category

When a new category is needed (e.g., "Insurance"):

### Step 1 — Propose the Category

1. Define the new category's scope and boundaries
2. Explain how it relates to existing categories
3. Identify the initial subcategories
4. Get approval from the Knowledge Base Owner

### Step 2 — Create the Structure

1. Create the folder: `docs/<new-category>/`
2. Add a `README.md` explaining the category's purpose
3. Update the [Knowledge Taxonomy](../metadata/knowledge-taxonomy.md)
4. Create a document ID prefix and update the [Naming Conventions](naming-conventions.md)
5. Add the category to the metadata schema's `category` enum
6. Create or identify a template for documents in this category

### Step 3 — Create Initial Documents

1. Create the first document(s) in the new category
2. Establish cross-references with existing documents
3. Add FAQ entries if applicable
4. Update relevant decision guides

### Step 4 — Update Repository Documentation

1. Update `docs/README.md` to list the new category
2. Update `CODEOWNERS` to assign ownership
3. Update `CHANGELOG.md`

---

## Adding a New Domain

Adding a new top-level domain (e.g., "Wealth Management") is a major change:

1. **Proposal**: Document the new domain's scope, categories, and estimated document count
2. **Impact Assessment**: Analyse how it affects existing navigation, taxonomy, and retrieval
3. **Approval**: Requires Knowledge Base Owner and all SME leads
4. **Implementation**: Create folders, update taxonomy, update repository README
5. **Verification**: Ensure existing documents and cross-references are not broken

---

## Avoiding Consistency Breaks

### Common Mistakes

| Mistake | Prevention |
|---|---|
| Using a non-standard template | Always start from `templates/` |
| Inventing new metadata fields | Follow the schema; propose changes through review |
| Creating folders outside the structure | Check the taxonomy before creating folders |
| Using different terminology | Follow the [Terminology Guidelines](terminology-guidelines.md) |
| Duplicating content | Follow the [Duplicate Prevention Strategy](duplicate-prevention.md) |
| Using inconsistent headings | Follow the [Documentation Standards](documentation-standards.md) |
| Forgetting cross-references | Use the relationship checklist in this document |

### Consistency Checklist for New Documents

- [ ] Template: Used the correct template
- [ ] Metadata: All required fields filled, valid values
- [ ] ID: Follows naming convention, is unique
- [ ] Taxonomy: Document fits existing taxonomy or taxonomy was updated
- [ ] Tags: Follow the tagging system
- [ ] Cross-references: Related documents identified and bidirectional links created
- [ ] Style: Follows style guide and documentation standards
- [ ] Chunking: Sections are self-contained and appropriately sized
- [ ] Search: Keywords, aliases, and headings optimised for retrieval
- [ ] Lifecycle: Status set to `draft`, dates populated

---

## Scaling Considerations

### When the Repository Reaches 100+ Documents

- Consider creating an automated document index
- Implement link validation as a CI/CD check
- Establish quarterly taxonomy reviews
- Assign category-level ownership more granularly

### When the Repository Reaches 500+ Documents

- Consider splitting the FAQ library into sub-folders by category
- Evaluate whether reference data should move to a database
- Implement automated staleness detection
- Consider a documentation search portal for contributors

### When the Repository Reaches 1,000+ Documents

- Evaluate category boundaries — some may need splitting
- Consider language-specific sub-teams for translation
- Implement automated metadata quality scoring
- Consider graph database for relationship management

---

## Related Documents

- [Knowledge Taxonomy](../metadata/knowledge-taxonomy.md) — Classification hierarchy
- [Metadata Schema](../metadata/metadata-schema.md) — Required and optional fields
- [Naming Conventions](naming-conventions.md) — File, folder, and ID naming rules
- [Tagging System](../metadata/tagging-system.md) — Tag namespaces and values
- [Cross-Reference Strategy](cross-reference-strategy.md) — How documents link together
- [Contribution Guide](contribution-guide.md) — Submission workflow
- [Duplicate Prevention](duplicate-prevention.md) — Single source of truth rules

---

*Last updated: 2026-08-02*
