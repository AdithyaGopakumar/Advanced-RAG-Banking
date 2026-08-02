# Maintenance Strategy

This document defines how the knowledge base is maintained over time, including update schedules, ownership, audits, and the deprecation process.

---

## Maintenance Objectives

1. **Currency** — All documents reflect the latest banking products, rates, policies, and regulations
2. **Quality** — Content quality does not degrade as the repository grows
3. **Accuracy** — Outdated or incorrect information is identified and corrected promptly
4. **Scalability** — Maintenance processes scale as the document count grows

---

## Document Ownership

Every document has an **owner** who is responsible for its accuracy and currency.

| Category | Owner Role | Backup Owner |
|---|---|---|
| Accounts | Retail Banking SME | Technical Writer |
| Deposits | Retail Banking SME | Technical Writer |
| Loans | Lending SME | Technical Writer |
| Cards | Cards SME | Technical Writer |
| Digital Banking | Digital Banking SME | Technical Writer |
| Payments | Payments SME | Technical Writer |
| Services | Operations SME | Technical Writer |
| Policies | Compliance Lead | Technical Writer |
| Security | Security Lead | Technical Writer |
| Customer Support | Customer Support Lead | Technical Writer |
| Charges | Finance SME | Technical Writer |
| Interest Rates | Finance SME | Technical Writer |
| Forms | Operations SME | Technical Writer |
| FAQs | Technical Writer | Knowledge Base Owner |
| Scenarios | Technical Writer | Knowledge Base Owner |
| Decision Guides | Technical Writer | Knowledge Base Owner |
| Glossary | Technical Writer | Knowledge Base Owner |
| Governance | Knowledge Base Owner | Technical Writing Lead |

---

## Update Schedule

### Frequency Tiers

| Tier | Update Frequency | Document Types |
|---|---|---|
| **Tier 1 — High Frequency** | Within 2 working days of change | Interest rates, charges, transaction limits |
| **Tier 2 — Medium Frequency** | Monthly review | Product features, eligibility, processes, FAQs |
| **Tier 3 — Low Frequency** | Quarterly review | Policies, security guidelines, governance, glossary |
| **Tier 4 — Event-Driven** | When triggered | Regulatory changes, new products, product discontinuation |

### Trigger-Based Updates

Some updates cannot wait for the scheduled review:

| Trigger | Action | SLA |
|---|---|---|
| RBI regulatory change | Update all affected documents | 5 working days |
| Product launch or discontinuation | Create or deprecate documents | On launch/discontinuation date |
| Interest rate revision | Update rate documents | 1 working day |
| Fee revision | Update charge documents | 2 working days |
| Security incident (e.g., new scam type) | Update security documents | 2 working days |
| Customer complaint trend | Review and update relevant documents | 5 working days |

---

## Review Schedule

### Monthly Review

The Technical Writing Lead conducts a monthly review:

1. Check all Tier 1 and Tier 2 documents for currency
2. Review any documents flagged by customer feedback or support teams
3. Verify all internal links are valid
4. Report findings to the Knowledge Base Owner

### Quarterly Audit

The Knowledge Base Owner conducts a quarterly audit:

1. Full compliance check against governance standards
2. Review of document ownership assignments
3. Identification of missing or outdated content
4. Assessment of FAQ library completeness
5. Review of metadata quality and consistency
6. Publish audit findings and action items

### Annual Review

Once per year, the entire knowledge base undergoes:

1. Full content review by all SME owners
2. Governance standards review and update
3. Template review and update
4. Metadata schema review
5. Alignment check with current RBI guidelines
6. Assessment of AI retrieval quality (with AI Engineering team)

---

## Staleness Detection

Documents are considered **stale** when:

| Condition | Action |
|---|---|
| `last_reviewed` > 90 days ago (Tier 1/2) | Flag for immediate review |
| `last_reviewed` > 180 days ago (Tier 3) | Flag for immediate review |
| Referenced regulation has been superseded | Flag for compliance review |
| Product or service has been modified | Flag for SME review |
| Multiple customer complaints reference the document | Flag for urgent review |

### Staleness Reporting

A monthly report lists:

- All documents past their review date
- Documents with broken internal links
- Documents flagged by automated quality checks
- Documents with high customer query volume but low retrieval accuracy (future, with RAG system)

---

## Deprecation Process

When a document is no longer relevant:

### Step 1 — Flag for Deprecation

The document owner or reviewer identifies the document as needing deprecation and creates a deprecation request.

### Step 2 — Verify No Active Dependencies

Check:

- No other active documents reference this document
- The FAQ library does not reference this document
- No scenarios depend on this document

### Step 3 — Update the Document

1. Set metadata `status` to `deprecated`
2. Add a deprecation notice at the top:

```markdown
> **Warning:** This document was deprecated on [date].
> For current information, see [Replacement Document](path/to/replacement.md).
```

3. Update `last_updated` date

### Step 4 — Update References

1. Update all documents that referenced the deprecated document
2. Update the FAQ library if needed
3. Update the CHANGELOG

### Step 5 — Archive (Optional)

After 6 months in `deprecated` status:

- Move to an `_archive/` folder (if the repository grows large)
- Or retain in place with `status: archived`

---

## Quality Metrics

Track the following metrics to measure knowledge base health:

| Metric | Target | Measurement |
|---|---|---|
| Document currency | < 5% stale documents | Monthly |
| Link validity | 100% valid internal links | Weekly (automated) |
| Metadata completeness | 100% documents with complete metadata | Monthly (automated) |
| Review SLA compliance | > 90% reviews within SLA | Monthly |
| Customer feedback score | > 4.0/5.0 (future) | Quarterly |
| RAG retrieval accuracy | > 85% relevant results (future) | Quarterly |

---

## Roles and Responsibilities

| Role | Maintenance Responsibilities |
|---|---|
| **Document Owner (SME)** | Keep content accurate and current |
| **Technical Writer** | Maintain formatting, style, and cross-references |
| **Technical Writing Lead** | Monthly reviews, staleness reporting |
| **Knowledge Base Owner** | Quarterly audits, governance updates, strategic direction |
| **AI Engineering Lead** | Metadata quality, retrieval performance monitoring |

---

## Related Documents

- [Versioning Policy](versioning-policy.md) — How changes are versioned
- [Review Process](review-process.md) — Review workflow and checklist
- [Contribution Guide](contribution-guide.md) — How to submit updates
- [Repository Rules](repository-rules.md) — Core content rules

---

*Last updated: 2026-08-02*
