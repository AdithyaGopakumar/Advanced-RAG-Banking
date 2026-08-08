# Knowledge Taxonomy

This document defines the complete classification hierarchy for the Banking Customer Support Knowledge Base. Every document must be placed within this taxonomy.

---

## Taxonomy Principles

1. **Mutual Exclusivity** — Each document belongs to exactly one category and subcategory
2. **Collective Exhaustiveness** — The taxonomy covers all customer-facing banking knowledge
3. **Consistent Depth** — All branches reach a similar level of specificity
4. **Extensibility** — New products, services, or categories can be added without restructuring
5. **Customer-Centric** — Categories reflect how customers think about banking, not internal organisational structure

---

## Taxonomy Structure

The taxonomy has four levels:

```
Domain → Category → Subcategory → Document Type
```

| Level | Purpose | Example |
|---|---|---|
| Domain | Broadest classification | Products, Services, Policies |
| Category | Functional grouping within a domain | Accounts, Loans, Cards |
| Subcategory | Specific product or topic | Savings Account, Home Loan |
| Document Type | Nature of the document | Product doc, FAQ, Scenario |

---

## Complete Taxonomy

### Domain 1 — Products

Banking products that customers can open, hold, or subscribe to.

| Category | Subcategory | Document Location |
|---|---|---|
| **Accounts** | Savings Account | `docs/accounts/` |
| | Current Account | `docs/accounts/` |
| | Salary Account | `docs/accounts/` |
| | Minor Account | `docs/accounts/` |
| | Basic Savings Bank Deposit Account (BSBDA) | `docs/accounts/` |
| | Joint Account | `docs/accounts/` |
| | NRE Account | `docs/accounts/` |
| | NRO Account | `docs/accounts/` |
| | FCNR Account | `docs/accounts/` |
| | PMJDY Account | `docs/accounts/` |
| **Deposits** | Fixed Deposit | `docs/deposits/` |
| | Recurring Deposit | `docs/deposits/` |
| | Tax Saver Fixed Deposit | `docs/deposits/` |
| | Senior Citizen Fixed Deposit | `docs/deposits/` |
| | Flexi / Sweep Deposit | `docs/deposits/` |
| | NRE Fixed Deposit | `docs/deposits/` |
| | NRO Fixed Deposit | `docs/deposits/` |
| **Loans** | Home Loan | `docs/loans/` |
| | Personal Loan | `docs/loans/` |
| | Education Loan | `docs/loans/` |
| | Vehicle Loan | `docs/loans/` |
| | Gold Loan | `docs/loans/` |
| | Business Loan | `docs/loans/` |
| | Loan Against Property | `docs/loans/` |
| | Loan Against Fixed Deposit | `docs/loans/` |
| **Cards** | Credit Card | `docs/cards/` |
| | Debit Card | `docs/cards/` |
| | Prepaid Card | `docs/cards/` |

---

### Domain 2 — Services

Banking services and channels that customers use to interact with the Bank.

| Category | Subcategory | Document Location |
|---|---|---|
| **Digital Banking** | Mobile Banking | `docs/digital-banking/` |
| | Internet Banking | `docs/digital-banking/` |
| | UPI | `docs/digital-banking/` |
| **Payments** | NEFT | `docs/payments/` |
| | RTGS | `docs/payments/` |
| | IMPS | `docs/payments/` |
| | Cheque Services | `docs/payments/` |
| | Demand Draft | `docs/payments/` |
| **Banking Services** | ATM Services | `docs/services/` |
| | Locker Facility | `docs/services/` |
| | Nomination | `docs/services/` |

---

### Domain 3 — Policies and Compliance

Customer-facing rules, regulations, and compliance requirements.

| Category | Subcategory | Document Location |
|---|---|---|
| **Policies** | KYC Policy | `docs/policies/` |
| | Account Closure Policy | `docs/policies/` |
| | Dormant Account Policy | `docs/policies/` |
| | Grievance Redressal Policy | `docs/policies/` |
| | Fair Practice Code | `docs/policies/` |
| **Security** | Security Guidelines | `docs/security/` |
| | Fraud Prevention | `docs/security/` |
| | Safe Banking Tips | `docs/security/` |

---

### Domain 4 — Customer Support

Processes for resolving customer issues and getting help.

| Category | Subcategory | Document Location |
|---|---|---|
| **Support** | Complaint Process | `docs/customer-support/` |
| | Escalation Matrix | `docs/customer-support/` |
| | Contact Channels | `docs/customer-support/` |

---

### Domain 5 — Reference Data

Frequently changing reference information.

| Category | Subcategory | Document Location |
|---|---|---|
| **Charges** | Account Charges | `docs/charges/` |
| | Loan Charges | `docs/charges/` |
| | Card Charges | `docs/charges/` |
| | Payment Charges | `docs/charges/` |
| **Interest Rates** | Deposit Interest Rates | `docs/interest-rates/` |
| | Loan Interest Rates | `docs/interest-rates/` |
| | Card Interest Rates | `docs/interest-rates/` |

---

### Domain 6 — Forms and Documentation

Required documents and forms for banking processes.

| Category | Subcategory | Document Location |
|---|---|---|
| **Forms** | Account Opening Documents | `docs/forms/` |
| | Loan Application Documents | `docs/forms/` |
| | KYC Documents | `docs/forms/` |

---

### Domain 7 — Cross-Cutting Knowledge

Knowledge that spans multiple domains and products.

| Category | Subcategory | Document Location |
|---|---|---|
| **FAQs** | Accounts FAQ | `faqs/` |
| | Deposits FAQ | `faqs/` |
| | Loans FAQ | `faqs/` |
| | Cards FAQ | `faqs/` |
| | Digital Banking FAQ | `faqs/` |
| | Payments FAQ | `faqs/` |
| | Security FAQ | `faqs/` |
| | General FAQ | `faqs/` |
| **Scenarios** | New Customer Onboarding | `scenarios/` |
| | Lost Card Replacement | `scenarios/` |
| | Loan Application Journey | `scenarios/` |
| | Dispute Resolution | `scenarios/` |
| | Account Upgrade | `scenarios/` |
| | Deceased Account Handling | `scenarios/` |
| **Decision Guides** | Choose Right Account | `decision-guides/` |
| | Choose Right Loan | `decision-guides/` |
| | Choose Right Card | `decision-guides/` |
| | Choose Right Deposit | `decision-guides/` |
| **Glossary** | Banking Glossary | `glossary/` |

---

## Document Types

Every document is classified by its **document type**, independent of its category:

| Document Type | Purpose | Typical Location |
|---|---|---|
| `product` | Describes a banking product's features, eligibility, and usage | `docs/accounts/`, `docs/deposits/`, `docs/loans/`, `docs/cards/` |
| `service` | Describes a banking service or channel | `docs/digital-banking/`, `docs/payments/`, `docs/services/` |
| `policy` | Describes a customer-facing policy or regulation | `docs/policies/`, `docs/security/` |
| `process` | Step-by-step guide for a specific procedure | `docs/customer-support/`, `docs/forms/` |
| `reference` | Tabular reference data (rates, charges) | `docs/charges/`, `docs/interest-rates/` |
| `faq` | Frequently asked questions for a category | `faqs/` |
| `scenario` | End-to-end customer journey walkthrough | `scenarios/` |
| `decision-guide` | Product comparison and selection guide | `decision-guides/` |
| `glossary` | Banking terminology definitions | `glossary/` |
| `troubleshooting` | Problem diagnosis and resolution steps | Any folder (as needed) |
| `form` | Required documents and form descriptions | `docs/forms/` |

---

## Taxonomy Metadata Mapping

When creating a document, map it to the taxonomy using these metadata fields:

```yaml
domain: "products"                    # Level 1
category: "accounts"                  # Level 2
sub_category: "savings-account"       # Level 3
document_type: "product"              # Document type
```

---

## Extending the Taxonomy

### Adding a New Subcategory

Example: The Bank launches a "Senior Citizen Savings Account".

1. Add it under **Domain: Products → Category: Accounts → Subcategory: Senior Citizen Savings Account**
2. Create the document in `docs/accounts/senior-citizen-savings-account.md`
3. Update this taxonomy document
4. No structural changes needed

### Adding a New Category

Example: The Bank launches an "Insurance" product line.

1. Add it under **Domain: Products → Category: Insurance**
2. Create a new folder: `docs/insurance/`
3. Add a `README.md` to the new folder
4. Update this taxonomy document
5. Create a document ID prefix (e.g., `INS`)
6. Update the [Naming Conventions](../governance/naming-conventions.md)

### Adding a New Domain

Example: The Bank wants to add "Business Banking" as a separate domain.

1. Create the new domain in this taxonomy
2. Create appropriate categories and folders
3. Consider whether existing documents need reclassification
4. Update the [Information Architecture Guide](../governance/information-architecture-guide.md)
5. Get approval from the Knowledge Base Owner

---

## Taxonomy Governance

| Action | Approval Required |
|---|---|
| Add a subcategory | Technical Writing Lead |
| Add a category | Knowledge Base Owner |
| Add a domain | Knowledge Base Owner + all SME leads |
| Rename or restructure | Knowledge Base Owner + migration plan |
| Deprecate a category | Knowledge Base Owner + impact assessment |

---

## Related Documents

- [Metadata Schema](metadata-schema.md) — How taxonomy fields appear in document metadata
- [Naming Conventions](../governance/naming-conventions.md) — File and folder naming rules
- [Information Architecture Guide](../governance/information-architecture-guide.md) — How to extend the knowledge base
- [Knowledge Relationships](knowledge-relationships.md) — How documents connect across the taxonomy

---

*Last updated: 2026-08-02*
