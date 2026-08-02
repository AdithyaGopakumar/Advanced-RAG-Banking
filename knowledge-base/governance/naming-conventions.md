# Naming Conventions

This document defines the naming rules for all files, folders, images, metadata, and other resources in the knowledge base.

---

## General Principles

1. **Lowercase only** — all file and folder names must be lowercase
2. **Hyphens as separators** — use hyphens (`-`) to separate words (not underscores or spaces)
3. **Descriptive names** — names should clearly indicate the content
4. **Short but meaningful** — avoid abbreviations unless they are standard banking terms (KYC, UPI, NEFT)
5. **No special characters** — only use letters, numbers, and hyphens
6. **English only** — all names must be in English

---

## Folder Naming

### Rules

- Use lowercase with hyphens
- Use plural nouns for collections (e.g., `accounts/`, `loans/`)
- Use singular nouns for concepts (e.g., `glossary/`, `governance/`)
- Keep folder names to 1–3 words
- Do not use version numbers in folder names

### Examples

| Correct | Incorrect | Reason |
|---|---|---|
| `accounts/` | `Accounts/` | Must be lowercase |
| `digital-banking/` | `digital_banking/` | Use hyphens, not underscores |
| `customer-support/` | `cust-support/` | Do not abbreviate |
| `interest-rates/` | `interest rates/` | No spaces allowed |
| `loans/` | `loan/` | Use plural for collections |

---

## File Naming

### Markdown Documents

**Pattern**: `<descriptive-name>.md`

| Correct | Incorrect | Reason |
|---|---|---|
| `savings-account.md` | `SavingsAccount.md` | Must be lowercase with hyphens |
| `home-loan.md` | `home_loan.md` | Use hyphens, not underscores |
| `kyc-policy.md` | `KYC-Policy.md` | Must be lowercase |
| `credit-card.md` | `cc.md` | Must be descriptive |
| `neft.md` | `NEFT.md` | Must be lowercase |

### README Files

- Always named `README.md` (uppercase is the standard exception)
- Every folder must contain a `README.md`

### Governance Documents

**Pattern**: `<topic-name>.md`

Examples: `style-guide.md`, `review-process.md`, `naming-conventions.md`

### FAQ Documents

**Pattern**: `<category>-faq.md`

Examples: `accounts-faq.md`, `loans-faq.md`, `digital-banking-faq.md`

### Scenario Documents

**Pattern**: `<scenario-description>.md`

Examples: `lost-card-replacement.md`, `new-customer-onboarding.md`

### Decision Guides

**Pattern**: `choose-right-<product-type>.md`

Examples: `choose-right-account.md`, `choose-right-loan.md`

---

## Image Naming

**Pattern**: `<category>-<subject>-<descriptor>.<ext>`

### Rules

- Use the documentation category as a prefix
- Describe the content, not the file type
- Use hyphens to separate words
- Use lowercase only

### Examples

| Filename | Description |
|---|---|
| `accounts-savings-opening-process.png` | Savings account opening process flow |
| `loans-home-loan-eligibility-flow.svg` | Home loan eligibility decision flow |
| `payments-neft-transfer-steps.png` | NEFT transfer step-by-step illustration |
| `cards-credit-card-tiers.svg` | Credit card tier comparison chart |
| `security-phishing-warning-signs.png` | Phishing awareness illustration |

---

## Table Naming

When documents contain multiple tables, use descriptive captions:

**Pattern**: *Table: \<Description\>*

### Examples

```markdown
*Table: Savings Account Interest Rates by Balance Tier*

| Balance Range | Interest Rate |
|---|---|
| Up to ₹1,00,000 | 3.00% p.a. |
| ₹1,00,001 – ₹10,00,000 | 3.50% p.a. |
```

---

## Metadata and Data Files

### YAML Files

**Pattern**: `<descriptive-name>.yaml`

- Use `.yaml` extension (not `.yml`)
- Lowercase with hyphens

### JSON Files

**Pattern**: `<descriptive-name>.json`

- Lowercase with hyphens

### Examples

| Correct | Incorrect |
|---|---|
| `metadata-schema.yaml` | `MetadataSchema.yml` |
| `document-index.json` | `doc_index.JSON` |
| `category-taxonomy.yaml` | `categories.yml` |

---

## Document IDs

Every document has a unique ID in its YAML frontmatter. IDs follow this pattern:

**Pattern**: `<CATEGORY>-<SUBCATEGORY>-<NNN>`

### Category Prefixes

| Category | Prefix |
|---|---|
| Accounts | `ACCT` |
| Deposits | `DEP` |
| Loans | `LOAN` |
| Cards | `CARD` |
| Digital Banking | `DIGI` |
| Payments | `PAY` |
| Services | `SVC` |
| Policies | `POL` |
| Security | `SEC` |
| Customer Support | `SUP` |
| Charges | `CHG` |
| Interest Rates | `RATE` |
| Forms | `FORM` |
| FAQs | `FAQ` |
| Scenarios | `SCEN` |
| Decision Guides | `GUIDE` |
| Glossary | `GLOSS` |

### Examples

| Document | ID |
|---|---|
| Savings Account | `ACCT-SA-001` |
| Home Loan | `LOAN-HL-001` |
| Credit Card | `CARD-CC-001` |
| KYC Policy | `POL-KYC-001` |
| Accounts FAQ | `FAQ-ACCT-001` |
| Lost Card Scenario | `SCEN-CARD-001` |
| Deposit Interest Rates | `RATE-DEP-001` |

---

## Branch Naming (Git)

**Pattern**: `docs/<category>/<action>-<description>`

### Actions

| Action | Use Case |
|---|---|
| `add` | New document |
| `update` | Content update |
| `fix` | Correction or bug fix |
| `remove` | Document removal |
| `restructure` | Folder or structure change |

### Examples

```
docs/accounts/add-savings-account
docs/loans/update-home-loan-rates
docs/governance/fix-style-guide-typo
docs/faqs/add-upi-questions
```

---

## Versioning in Filenames

- **Do not** include version numbers in filenames
- Version tracking is handled through YAML frontmatter metadata and Git history
- If a document is deprecated, update its metadata `status` field to `deprecated` rather than renaming the file

---

## Summary Table

| Resource Type | Pattern | Example |
|---|---|---|
| Folder | `lowercase-with-hyphens/` | `digital-banking/` |
| Markdown file | `descriptive-name.md` | `savings-account.md` |
| Image | `category-subject-descriptor.ext` | `loans-home-loan-flow.svg` |
| YAML file | `descriptive-name.yaml` | `metadata-schema.yaml` |
| JSON file | `descriptive-name.json` | `document-index.json` |
| Document ID | `CATEGORY-SUBCATEGORY-NNN` | `ACCT-SA-001` |
| Git branch | `docs/category/action-description` | `docs/loans/add-gold-loan` |

---

## Related Documents

- [Documentation Standards](documentation-standards.md) — Structural and formatting rules
- [Style Guide](style-guide.md) — Writing and language standards
- [Repository Rules](repository-rules.md) — Core content rules

---

*Last updated: 2026-08-02*
