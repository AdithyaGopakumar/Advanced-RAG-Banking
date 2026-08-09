---
id: "SCEN-PREP-001"
title: "Home Loan Prepayment"
slug: "home-loan-prepayment"
domain: "cross-cutting"
category: "scenarios"
sub_category: "home-loan-prepayment"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["home loan prepayment", "foreclose loan", "part payment", "loan closure", "pay off loan"]
search_aliases: ["prepay home loan", "foreclosure charges", "close loan early"]
tags: ["intent:prepayment", "product:home-loan"]
priority: "high"
related_documents: ["CHG-LOAN-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Home Loan Prepayment Scenario

## Situation
The customer has excess funds and wants to make a part-payment or fully foreclose their active home loan to save on interest.

## Customer Intent
`loan_prepayment`

## What the Customer May Say
- "I want to pay off a chunk of my home loan."
- "Are there charges if I foreclose my loan early?"
- "How do I make a part payment?"

## Relevant Information
RBI mandates that floating-rate home loans for individual borrowers carry NO prepayment or foreclosure penalties.

## Recommended Response Path
Confirm that floating-rate home loans can be prepaid without penalty. Advise the customer that part-payments can be made via Internet Banking, which will reduce their outstanding principal.

## Immediate Action
None.

## Next Steps
Customer transfers funds to the loan account via the portal.

## Exceptions
- **Fixed Rate Loans**: May attract a foreclosure penalty.
- **Non-Individual Borrowers**: Corporate/Business loans attract penalties.

## When to Escalate
None.

## Dynamic Information Required
- Foreclosure charges for other loan types.

## Live Banking Data Required
- Outstanding loan principal balance.

## Security Considerations
None.

## Compliance Considerations
RBI guidelines on zero prepayment penalty for floating rate individual housing loans.

## Related FAQs
- [Loans FAQ](../faqs/loans-faq.md)

## Related Documents
- [Loan Charges](../docs/charges/loan-charges.md)
