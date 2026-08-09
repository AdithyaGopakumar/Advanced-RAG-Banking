---
id: "GLOS-PAY-001"
title: "Payments Glossary"
slug: "payments-glossary"
domain: "payments"
category: "glossary"
sub_category: "payments-glossary"
document_type: "glossary"
language: "en"
region: "IN"
keywords: ["payment terms", "NEFT", "RTGS", "IMPS", "payment failed"]
tags: ["domain:payments", "layer:semantic"]
priority: "high"
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
---

# Payments Glossary

## Debited but Not Credited
**Short Definition**: Money left your account but hasn't reached the receiver.

**Standard Definition**: A transaction state where the remitter's account is debited, but due to network or beneficiary bank downtime, the funds are held in a suspense account and not credited.

**Customer May Say**: "money went out but receiver didn't get it", "transfer stuck", "payment deducted but failed"

**Synonyms**: Transaction Pending, Amount Deducted

**Acronyms / Abbreviations**: None

**Common Misspellings**: money cut from account

**Related Terms**: Auto-Reversal, Transaction Status

**Confusable Terms**: Reversed Payment (where the money has already returned to the sender)

**Canonical Documents**: [Payment Troubleshooting](../docs/payments/payment-troubleshooting.md)

**Related FAQs**: [Payments FAQ](../faqs/payments-faq.md)

**Related Scenarios**: [Payment Failure Resolution](../scenarios/payment-failure-resolution.md)

**Related Decision Guides**: [Payment Exception Handling](../decision-guides/payment-exception-handling.md)

**Source / Authority**: NPCI/RBI Guidelines

---

## Payment
**Short Definition**: A generic term for transferring money (ambiguous).

**Standard Definition**: AMBIGUOUS TERM. Can refer to UPI, NEFT, IMPS, RTGS, Bill Payment, or Card Swipes. Requires clarification: 'Which method did you use for this payment?'

**Customer May Say**: "make a payment", "my payment failed"

**Synonyms**: Transfer, Remittance

**Acronyms / Abbreviations**: None

**Common Misspellings**: paymant, transfar

**Related Terms**: UPI, NEFT, RTGS

**Confusable Terms**: None

**Canonical Documents**: [NEFT](../docs/payments/neft.md)

**Related FAQs**: [Payments FAQ](../faqs/payments-faq.md)

**Related Scenarios**: None

**Related Decision Guides**: [Choose Right Payment Method](../decision-guides/choose-right-payment-method.md)

**Source / Authority**: General Terminology

---
