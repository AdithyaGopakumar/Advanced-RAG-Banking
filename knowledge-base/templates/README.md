# Document Templates

This folder contains reusable templates for creating new documents in the knowledge base. Every new document must start from the appropriate template.

---

## Available Templates

| Template | Purpose | Use For |
|---|---|---|
| [product-template.md](product-template.md) | Banking product documentation | Accounts, deposits, cards |
| [loan-template.md](loan-template.md) | Loan product documentation | All loan types |
| [service-template.md](service-template.md) | Banking service documentation | Digital banking, payments, operational services |
| [process-template.md](process-template.md) | Step-by-step process guides | Complaint process, document submission, account operations |
| [policy-template.md](policy-template.md) | Customer-facing policy documentation | KYC, account closure, grievance, fair practice |
| [faq-template.md](faq-template.md) | FAQ collections by category | All FAQ documents |
| [scenario-template.md](scenario-template.md) | End-to-end customer journey walkthroughs | Lost card, loan application, onboarding |
| [decision-guide-template.md](decision-guide-template.md) | Product comparison and selection guides | Choose right account, loan, card, deposit |
| [glossary-entry-template.md](glossary-entry-template.md) | Banking terminology entry format | Glossary entries (appended to glossary document) |
| [troubleshooting-template.md](troubleshooting-template.md) | Problem-resolution guides | Product/service troubleshooting |
| [form-template.md](form-template.md) | Required documents and forms | Account opening docs, loan docs, KYC docs |

---

## How to Use Templates

1. **Identify the document type** using the [Knowledge Taxonomy](../metadata/knowledge-taxonomy.md)
2. **Copy the appropriate template** to the target folder
3. **Rename the file** following the [Naming Conventions](../governance/naming-conventions.md)
4. **Fill in the YAML frontmatter** completely per the [Metadata Schema](../metadata/metadata-schema.md)
5. **Write the content** following the [Style Guide](../governance/style-guide.md) and [Documentation Standards](../governance/documentation-standards.md)
6. **Apply retrieval optimisation** per the [Search Optimization Guide](../governance/search-optimization-guide.md) and [Chunking Guidelines](../governance/chunking-guidelines.md)
7. **Add tags** per the [Tagging System](../metadata/tagging-system.md)
8. **Establish cross-references** per the [Cross-Reference Strategy](../governance/cross-reference-strategy.md)
9. **Remove inapplicable sections** marked `[REMOVE IF NOT APPLICABLE]`
10. **Delete all template instruction comments** (HTML comments starting with `<!--`)
11. **Submit for review** per the [Contribution Guide](../governance/contribution-guide.md)

---

## Template Structure

Every template includes:

- **YAML frontmatter scaffold** — All required metadata fields with placeholder values
- **Required sections** — Sections that must appear in every document of that type
- **Conditional sections** — Sections included only when applicable (marked with `[REMOVE IF NOT APPLICABLE]`)
- **Inline instructions** — HTML comments guiding the author on what to write (delete before publishing)

---

## Which Template Should I Use?

| I want to document... | Use This Template |
|---|---|
| A bank account product | `product-template.md` |
| A deposit product | `product-template.md` |
| A loan product | `loan-template.md` |
| A credit/debit/prepaid card | `product-template.md` |
| Mobile/internet banking | `service-template.md` |
| A payment method (NEFT, RTGS, IMPS) | `service-template.md` |
| A customer-facing policy | `policy-template.md` |
| A step-by-step how-to process | `process-template.md` |
| Frequently asked questions | `faq-template.md` |
| A customer journey scenario | `scenario-template.md` |
| A product comparison guide | `decision-guide-template.md` |
| Banking term definitions | `glossary-entry-template.md` |
| Troubleshooting a product issue | `troubleshooting-template.md` |
| Required documents for a process | `form-template.md` |
| Fee and charge schedules | `product-template.md` (adapted) |
| Interest rate tables | `product-template.md` (adapted) |

---

## Related Resources

- [metadata/metadata-schema.md](../metadata/metadata-schema.md) — Complete frontmatter field specification
- [metadata/knowledge-taxonomy.md](../metadata/knowledge-taxonomy.md) — How to classify documents
- [governance/documentation-standards.md](../governance/documentation-standards.md) — Formatting rules
- [governance/style-guide.md](../governance/style-guide.md) — Writing standards

---

*Last updated: 2026-08-02*
