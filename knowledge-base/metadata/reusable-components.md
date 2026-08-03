# Reusable Components

This document identifies sections and content patterns that appear across multiple documents. These are candidates for future partial templates or shared content blocks to prevent duplication.

---

## Principle

When the same information appears in multiple documents, it should be:

1. **Authored once** in a canonical document
2. **Summarised briefly** in referencing documents (1–2 sentences)
3. **Linked** to the canonical source for full details

See [Duplicate Prevention Strategy](../governance/duplicate-prevention.md) for detailed rules.

---

## Identified Reusable Components

### 1. Eligibility Criteria

| Component | Canonical Location | Referenced By |
|---|---|---|
| Account eligibility | Each product document | FAQs, Scenarios, Decision Guides |
| Loan eligibility (salaried) | Each loan document | FAQs, Scenarios, Decision Guides |
| Loan eligibility (self-employed) | Each loan document | FAQs, Scenarios, Decision Guides |
| Card eligibility | Each card document | FAQs, Decision Guides |

**Reuse Strategy**: Eligibility stays in the product document (canonical). FAQs summarise in one sentence and link. Decision guides compare eligibility across products.

---

### 2. Charges and Fees

| Component | Canonical Location | Referenced By |
|---|---|---|
| Account charges | `docs/charges/account-charges.md` | All account product documents |
| Loan charges | `docs/charges/loan-charges.md` | All loan product documents |
| Card charges | `docs/charges/card-charges.md` | All card product documents |
| Payment charges | `docs/charges/payment-charges.md` | All payment service documents |
| Service charges | `docs/charges/service-charges.md` | ATM, locker, statement, passbook documents |

**Reuse Strategy**: Charges live exclusively in the charges documents. Product documents link to the charges document; they do not reproduce the charge table.

---

### 3. Interest Rates

| Component | Canonical Location | Referenced By |
|---|---|---|
| Deposit interest rates | `docs/interest-rates/deposit-interest-rates.md` | All deposit product documents, FAQs |
| Loan interest rates | `docs/interest-rates/loan-interest-rates.md` | All loan product documents, FAQs |

**Reuse Strategy**: Rates are canonical in the rate documents. Product documents provide a brief summary and link.

---

### 4. Required Documents / KYC

| Component | Canonical Location | Referenced By |
|---|---|---|
| Account opening documents | `docs/forms/account-opening-documents.md` | All account product documents |
| Loan application documents | `docs/forms/loan-application-documents.md` | All loan product documents |
| KYC documents | `docs/forms/kyc-documents.md` | Account, loan, card, services documents |
| Card application documents | `docs/forms/card-application-documents.md` | All card product documents |

**Reuse Strategy**: Document requirement lists are canonical in the forms folder. Product documents summarise ("You will need valid KYC documents") and link.

---

### 5. Contact and Support Information

| Component | Canonical Location | Referenced By |
|---|---|---|
| Contact channels | `docs/customer-support/contact-channels.md` | All troubleshooting guides, scenarios |
| Complaint process | `docs/customer-support/complaint-process.md` | All policy documents, escalation paths |
| Escalation matrix | `docs/customer-support/escalation-matrix.md` | Grievance policy, complaint process |

**Reuse Strategy**: Contact information appears only in the contact channels document. All other documents use: "Contact the Bank through any of the [support channels](path)."

---

### 6. Security Warnings

| Component | Canonical Location | Referenced By |
|---|---|---|
| Fraud prevention tips | `docs/security/fraud-prevention.md` | Digital banking, card, payment documents |
| Phishing awareness | `docs/security/phishing-awareness.md` | Digital banking, email-related documents |
| Card security | `docs/security/card-security.md` | Credit card, debit card documents |

**Reuse Strategy**: Security content lives in dedicated security documents. Product/service documents include a brief warning with a link. Example: "> **Important:** Never share your OTP, PIN, or password. See [Safe Banking Tips](path)."

---

### 7. Tax Information

| Component | Canonical Location | Referenced By |
|---|---|---|
| Section 80C benefits | Tax Saver Deposit, Home Loan | FAQs, Decision Guides |
| Section 24 benefits | Home Loan | FAQs |
| Section 80E benefits | Education Loan | FAQs |
| TDS on deposits | FD, RD documents | FAQs, Deposit product documents |

**Reuse Strategy**: Tax information is canonical in the relevant product document. FAQs summarise and link.

---

### 8. Common Process Patterns

These patterns recur across multiple process documents:

| Pattern | Appears In |
|---|---|
| "Before You Start" prerequisites | All process documents |
| Multi-channel step-by-step instructions | Address update, mobile update, fund transfers |
| "Expected Timeline" section | All process and scenario documents |
| "What to Do If Something Goes Wrong" | All troubleshooting and scenario documents |
| "Related Documents" section | Every document in the knowledge base |

**Reuse Strategy**: These are structural patterns ensured by templates, not content to be deduplicated.

---

## Future Consideration: Content Includes

If the documentation system is later enhanced with a static site generator (e.g., Hugo, Docusaurus), the reusable components above could become **partial templates** or **shortcodes** that are included at build time. This would enable true single-source authoring.

Until then, the cross-reference strategy ensures consistency.

---

## Related Documents

- [Duplicate Prevention Strategy](../governance/duplicate-prevention.md) — Full rules on when to duplicate vs. reference
- [Cross-Reference Strategy](../governance/cross-reference-strategy.md) — How to link between documents
- [Master Knowledge Map](master-knowledge-map.md) — Complete document inventory

---

*Last updated: 2026-08-03*
