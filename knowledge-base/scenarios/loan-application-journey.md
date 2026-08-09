---
id: "SCEN-LOAN-001"
title: "Loan Application Journey"
slug: "loan-application-journey"
domain: "cross-cutting"
category: "scenarios"
sub_category: "loan-application-journey"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["loan application", "apply for loan", "loan eligibility", "get a loan", "new loan"]
search_aliases: ["how to apply for loan", "am I eligible for loan", "loan process"]
tags: ["intent:apply_loan", "process:origination"]
priority: "high"
related_documents: ["LOAN-HL-001", "LOAN-PL-001", "RATES-LOAN-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Loan Application Journey Scenario

## Situation
A prospective or existing customer wants to apply for a new loan (Home, Personal, Auto) and wants to know the process, rates, or eligibility.

## Customer Intent
`apply_loan`

## What the Customer May Say
- "I need a personal loan of 5 lakhs."
- "How do I apply for a home loan?"
- "What is your current car loan interest rate?"

## Relevant Information
Loan approval is subject to credit score, income, and existing liabilities.

## Recommended Response Path
Guide the customer to the online eligibility calculator. Explain that they can apply entirely digitally (for personal loans) or schedule a call with a loan officer (for home loans). Provide the link to current rates.

## Immediate Action
None.

## Next Steps
Customer submits the initial lead form or completes the digital journey.

## Exceptions
- **Pre-approved Loans**: Existing customers might have instant disbursement offers available in their mobile app.

## When to Escalate
Escalate to sales team/human agent if the customer needs specialized advice on large loan amounts.

## Dynamic Information Required
- Current loan interest rates (EBLR + Spread).
- Processing fees.

## Live Banking Data Required
- Checking for pre-approved offers (if authenticated).

## Security Considerations
None.

## Compliance Considerations
Fair Practices Code in lending.

## Related FAQs
- [Loans FAQ](../faqs/loans-faq.md)

## Related Documents
- [Home Loan](../docs/loans/home-loan.md)
- [Personal Loan](../docs/loans/personal-loan.md)
- [Loan Interest Rates](../docs/interest-rates/loan-interest-rates.md)
