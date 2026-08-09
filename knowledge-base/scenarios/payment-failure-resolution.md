---
id: "SCEN-PAYFAIL-001"
title: "Payment Failure Resolution"
slug: "payment-failure-resolution"
domain: "cross-cutting"
category: "scenarios"
sub_category: "payment-failure-resolution"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["payment failed", "UPI pending", "NEFT delayed", "money debited", "IMPS failure"]
search_aliases: ["money deducted but transfer failed", "UPI transaction pending", "where is my NEFT"]
tags: ["intent:payment_status", "product:payments"]
priority: "high"
related_documents: ["PAY-NEFT-001", "PAY-IMPS-001", "PAY-TRB-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Payment Failure Resolution Scenario

## Situation
A customer initiated a fund transfer (UPI, NEFT, IMPS) which either failed or is pending, and money has been debited from their account.

## Customer Intent
`check_payment_status`

## What the Customer May Say
- "My UPI payment failed but money was deducted."
- "I sent money via NEFT 2 hours ago and it hasn't reached."
- "Why is my IMPS transfer pending?"

## Relevant Information
Most failed digital transactions with debited funds are automatically reconciled and refunded by the payment gateway/NPCI within T+1 to T+3 working days.

## Recommended Response Path
Reassure the customer. Explain that pending or failed transactions are usually auto-refunded within 48 hours. Direct them to check the live status in the 'Transaction History' tab.

## Immediate Action
None.

## Next Steps
Customer checks live status or waits for the auto-refund window.

## Exceptions
- **Wrong Beneficiary**: If the payment was SUCCESSFUL but sent to the wrong person, auto-refund does not apply. Requires branch escalation immediately.
- **NEFT Batches**: Remind them NEFT operates in batches; a slight delay is normal.

## When to Escalate
Escalate to grievance portal if the refund timeline (e.g., T+3 days) has elapsed and funds are still missing.

## Dynamic Information Required
None.

## Live Banking Data Required
- Live status of the specific transaction ID.

## Security Considerations
None.

## Compliance Considerations
RBI turnaround time (TAT) guidelines for failed transactions and compensation.

## Related FAQs
- [Payments FAQ](../faqs/payments-faq.md)

## Related Documents
- [Payment Troubleshooting](../docs/payments/payment-troubleshooting.md)
