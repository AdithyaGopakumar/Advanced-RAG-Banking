---
id: "SCEN-FRAUD-001"
title: "Fraud Reporting & Mitigation"
slug: "fraud-reporting"
domain: "cross-cutting"
category: "scenarios"
sub_category: "fraud-reporting"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["fraud", "scam", "unauthorized transaction", "hacked", "stolen money"]
search_aliases: ["report fraud", "money deducted without permission", "block compromised account"]
tags: ["intent:report_fraud", "security:critical"]
priority: "high"
related_documents: ["SEC-FRAUD-001", "CUST-CHAN-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Fraud Reporting Scenario

## Situation
The customer realizes unauthorized funds have left their account or someone has gained unauthorized access to their banking channels.

## Customer Intent
`report_fraud`

## What the Customer May Say
- "Money was deducted from my account without my permission!"
- "I think my account got hacked."
- "I lost 50,000 rupees to a scammer."

## Relevant Information
Time is critical. The liability of the customer depends on how quickly they report the unauthorized transaction.

## Recommended Response Path
This is an EMERGENCY. Immediately instruct the customer to freeze their account or block their card via the mobile app, OR provide the 24x7 emergency toll-free number to do it instantly. 

## Immediate Action
Route to LIVE API to block card/account if channel supports it.

## Next Steps
Customer must call the fraud helpline, register a formal dispute, and potentially file a cyber police complaint.

## Exceptions
- **Transaction Pending**: If it's a pending UPI collect request, instruct them to simply decline it.

## When to Escalate
IMMEDIATELY escalate to human support if the bot cannot facilitate the block.

## Dynamic Information Required
None.

## Live Banking Data Required
- Customer's active cards and channels to execute the block.

## Security Considerations
**CRITICAL**. Do not ask for full card numbers, CVVs, or PINs in the chat.

## Compliance Considerations
Zero Liability Policy applies if reported within 3 working days.

## Related FAQs
- [Security FAQ](../faqs/security-faq.md)

## Related Documents
- [Fraud Prevention](../docs/security/fraud-prevention.md)
- [Contact Channels](../docs/customer-support/contact-channels.md)
