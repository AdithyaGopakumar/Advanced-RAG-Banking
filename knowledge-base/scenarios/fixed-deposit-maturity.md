---
id: "SCEN-DEP-001"
title: "Fixed Deposit Maturity"
slug: "fixed-deposit-maturity"
domain: "cross-cutting"
category: "scenarios"
sub_category: "fixed-deposit-maturity"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["FD maturity", "deposit maturity", "renew FD", "break FD", "maturity instructions"]
search_aliases: ["check FD status", "when will FD mature", "change auto renewal"]
tags: ["intent:maturity", "product:fixed-deposit"]
priority: "high"
related_documents: ["DEP-FD-001", "DEP-RATES-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Fixed Deposit Maturity Scenario

## Situation
The customer wants to know what happens when their FD matures, or wants to change the maturity instructions before the date.

## Customer Intent
`check_fd_maturity` / `modify_fd_instructions`

## What the Customer May Say
- "My FD matures next week, what should I do?"
- "I want the money credited to my savings account instead of renewing."
- "Has my deposit matured?"

## Relevant Information
By default, most FDs auto-renew for the same tenure at the prevailing interest rate unless instructed otherwise.

## Recommended Response Path
Explain that the customer can view and modify their maturity instructions (e.g., auto-renew principal, pay out interest) via Internet Banking under the 'Deposits' section prior to the maturity date.

## Immediate Action
None.

## Next Steps
Customer logs in and updates maturity instructions.

## Exceptions
- **Tax Saver FD**: Cannot be broken prematurely; matures strictly after 5 years.
- **Already Matured**: If maturity date has passed, instructions cannot be changed; the deposit has already renewed or paid out.

## When to Escalate
None.

## Dynamic Information Required
- Current FD Interest Rates (if customer asks what the renewal rate will be).

## Live Banking Data Required
- The exact maturity date and current instructions of the specific FD.

## Security Considerations
None.

## Compliance Considerations
TDS implications on the renewed interest.

## Related FAQs
- [Deposits FAQ](../faqs/deposits-faq.md)

## Related Documents
- [Fixed Deposit](../docs/deposits/fixed-deposit.md)
- [Deposit Interest Rates](../docs/interest-rates/deposit-interest-rates.md)
