---
id: "DG-PAYEXC-001"
title: "Payment Exception Handling Decision Guide"
slug: "payment-exception-handling"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "payment-exception-handling"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["payment failed", "transfer stuck", "money debited not received", "payment dispute"]
search_aliases: ["what to do if payment fails", "UPI failed money deducted"]
tags: ["process:exception", "product:payments"]
priority: "high"
related_documents: ["PAY-TRB-001"]
related_faqs: ["payments-faq.md"]
related_scenarios: ["payment-failure-resolution.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Payment Exception Handling Decision Guide

## Purpose
To resolve situations where a payment is delayed, failed, or disputed, guiding the customer to wait, retry, or escalate.

## Applicable Intent
`check_payment_status`

## Inputs
- `payment_rail` (UPI, NEFT, IMPS, RTGS)
- `debit_status` (Debited, Not Debited)
- `time_elapsed` (Hours/Days since transaction)
- `wrong_beneficiary` (Yes, No)

## Missing Information
If `debit_status` or `time_elapsed` is unknown, clarify:
"Has the money been deducted from your account, and when exactly did you make the transaction?"

## Decision Logic
IF `wrong_beneficiary` = YES
    THEN Escalate to Branch for immediate reversal request.
    
IF `debit_status` = NO
    THEN Transaction failed. Instruct customer to retry.

IF `debit_status` = YES AND `wrong_beneficiary` = NO
    IF `payment_rail` = UPI OR IMPS
        IF `time_elapsed` < 3 days
            THEN Wait. Inform customer of auto-reversal TAT (T+1 to T+3 days).
        ELSE
            THEN Instruct customer to raise a formal dispute on the portal.
    IF `payment_rail` = NEFT OR RTGS
        IF `time_elapsed` < 1 day
            THEN Wait (NEFT batches / RTGS windows).
        ELSE
            THEN Raise dispute.

## Outcomes
- Retry Transaction
- Wait for Auto-Reversal
- Raise Dispute
- Request Branch Reversal

## Recommended Customer Action
Follow the specific outcome branch. Check live status via 'Transaction History'.

## Exceptions
- None.

## Escalation
If T+3 days have elapsed and dispute is unresolved, escalate to Grievance Officer.

## Dynamic Data
- None.

## Live Data
- `LIVE_API` required to check actual transaction status in the backend.

## Safety / Compliance
- RBI mandates auto-reversals within specific TATs, failing which compensation applies.

## Related FAQs
- [Payments FAQ](../faqs/payments-faq.md)

## Related Scenarios
- [Payment Failure Resolution](../scenarios/payment-failure-resolution.md)

## Canonical Documents
- [Payment Troubleshooting](../docs/payments/payment-troubleshooting.md)
