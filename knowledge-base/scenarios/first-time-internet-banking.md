---
id: "SCEN-DIGI-001"
title: "First Time Internet Banking Registration"
slug: "first-time-internet-banking"
domain: "cross-cutting"
category: "scenarios"
sub_category: "first-time-internet-banking"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["internet banking registration", "net banking signup", "first time login", "generate password"]
search_aliases: ["register for net banking", "how to login online", "get online access"]
tags: ["intent:register", "channel:internet-banking"]
priority: "high"
related_documents: ["DIGI-IB-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# First Time Internet Banking Registration Scenario

## Situation
A new or existing customer wants to access their bank account online for the first time via a web browser.

## Customer Intent
`register_digital_banking`

## What the Customer May Say
- "How do I register for internet banking?"
- "I want to check my account online."
- "How do I get my login password?"

## Relevant Information
Registration requires the customer's Customer ID (CIF), registered mobile number, and active Debit Card details for self-registration.

## Recommended Response Path
Guide the customer to the bank's website, click on 'New User Registration', and keep their Debit Card and mobile phone handy for OTP validation.

## Immediate Action
None.

## Next Steps
Customer completes the online flow to generate their login and profile passwords.

## Exceptions
- **No Debit Card**: Customer must visit the branch to request physical PIN mailers.
- **Corporate Account**: Self-registration is usually disabled; requires branch submission.

## When to Escalate
Escalate to technical support if the portal throws an unexpected error despite correct details.

## Dynamic Information Required
None.

## Live Banking Data Required
None.

## Security Considerations
Ensure the customer is on the official bank URL. Warn them not to share the registration OTPs with anyone.

## Compliance Considerations
None.

## Related FAQs
- [Digital Banking FAQ](../faqs/digital-banking-faq.md)

## Related Documents
- [Internet Banking Troubleshooting](../docs/digital-banking/internet-banking-troubleshooting.md)
