# FAQ Library

This folder contains Frequently Asked Questions (FAQs) organised by banking category.

---

## Planned Documents

| Document | Description | Status |
|---|---|---|
| accounts-faq.md | FAQs about savings, current, salary, and minor accounts | Planned |
| deposits-faq.md | FAQs about fixed, recurring, and tax saver deposits | Planned |
| loans-faq.md | FAQs about all loan products | Planned |
| cards-faq.md | FAQs about credit, debit, and prepaid cards | Planned |
| digital-banking-faq.md | FAQs about mobile banking, internet banking, and UPI | Planned |
| payments-faq.md | FAQs about NEFT, RTGS, IMPS, cheques, and demand drafts | Planned |
| security-faq.md | FAQs about banking security and fraud prevention | Planned |
| general-faq.md | General banking FAQs not specific to a single category | Planned |

---

## Design Rationale

FAQs are maintained in a separate top-level folder (rather than embedded in product documents) because:

1. **Retrieval Efficiency** — FAQ documents are high-value targets for RAG retrieval and can be queried as a distinct collection
2. **No Duplication** — A single FAQ may span multiple products or services; a central location avoids content duplication
3. **Independent Maintenance** — FAQs can be updated on a different cadence than product documentation
4. **Scalability** — The FAQ library can grow independently to thousands of entries

Each FAQ document links back to its source product or service documentation for deeper information.

---

## FAQ Format

Each FAQ entry follows this structure:

```markdown
### Q: [Customer question in natural language]

[Clear, concise answer]

**Related**: [Link to relevant product/policy document]
```

---

## Related Folders

- [docs/](../docs/) — Source product and service documentation referenced by FAQs
- [scenarios/](../scenarios/) — End-to-end customer journey guides for complex multi-step questions

---

*Last updated: 2026-08-02*
