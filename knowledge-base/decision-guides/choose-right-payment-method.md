---
id: "DG-PAY-001"
title: "Choose Right Payment Method Decision Guide"
slug: "choose-right-payment-method"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "choose-right-payment-method"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["choose payment method", "NEFT vs RTGS", "UPI limit", "transfer type"]
search_aliases: ["how should I transfer money", "best way to send large amount"]
tags: ["process:decision", "product:payments"]
priority: "high"
related_documents: ["PAY-NEFT-001", "PAY-IMPS-001", "PAY-RTGS-001"]
related_faqs: ["payments-faq.md"]
related_scenarios: ["payment-failure-resolution.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Choose Right Payment Method Decision Guide

## Purpose
To evaluate a customer's transfer amount and urgency to recommend the correct payment rail (UPI, NEFT, RTGS, IMPS).

## Applicable Intent
`compare_transfers_limits`

## Inputs
- `amount` (Below 1 Lakh, 1-2 Lakhs, Above 2 Lakhs)
- `urgency` (Instant, Same Day)

## Missing Information
If `amount` is unknown, clarify:
"Approximately how much are you trying to transfer? Some methods like RTGS have a minimum limit."

## Decision Logic
IF `amount` < 1 Lakh AND `urgency` = Instant
    THEN Route to UPI or IMPS
    
IF `amount` >= 2 Lakhs AND `urgency` = Instant
    THEN Route to RTGS
    
IF `urgency` = Same Day (Not Instant)
    THEN Route to NEFT

## Outcomes
- UPI
- IMPS
- NEFT
- RTGS

## Recommended Customer Action
Initiate the chosen transfer type via Mobile Banking or Internet Banking.

## Exceptions
- If the payee is not added as a beneficiary, a cooling-off period (usually 24 hours with a reduced limit) applies to NEFT/RTGS/IMPS.

## Escalation
None.

## Dynamic Data
- Transfer charges for the specific rail (`payment-charges.md`).

## Live Data
- None.

## Safety / Compliance
- Limits are bound by RBI regulations and the customer's profile limits.

## Related FAQs
- [Payments FAQ](../faqs/payments-faq.md)

## Related Scenarios
- [Payment Failure Resolution](../scenarios/payment-failure-resolution.md)

## Canonical Documents
- [NEFT](../docs/payments/neft.md)
- [RTGS](../docs/payments/rtgs.md)
