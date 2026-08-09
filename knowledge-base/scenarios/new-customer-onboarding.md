---
id: "SCEN-ONBOARD-001"
title: "New Customer Onboarding"
slug: "new-customer-onboarding"
domain: "cross-cutting"
category: "scenarios"
sub_category: "new-customer-onboarding"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["new customer", "open account", "video KYC", "join bank", "start banking"]
search_aliases: ["how to open account", "become a customer", "V-KYC account opening"]
tags: ["intent:open_account", "process:onboarding"]
priority: "high"
related_documents: ["ACCT-SA-001", "POL-KYC-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# New Customer Onboarding Scenario

## Situation
A non-customer is interested in banking with the institution and wants to open their first savings account.

## Customer Intent
`open_account`

## What the Customer May Say
- "I want to open a new bank account."
- "How do I become a customer?"
- "Can I open an account through Video KYC?"

## Relevant Information
The bank offers instant digital account opening using Aadhaar, PAN, and Video KYC (V-KYC).

## Recommended Response Path
Provide the direct link to download the Mobile Banking App or visit the web portal to start the digital journey. Explain they need their original PAN card and Aadhaar handy for the video call.

## Immediate Action
None.

## Next Steps
Customer initiates the V-KYC flow.

## Exceptions
- **NRI / Minors**: Cannot use the standard V-KYC flow; must visit a branch or use specific non-resident application flows.

## When to Escalate
None.

## Dynamic Information Required
- Minimum balance requirements for the chosen variant.

## Live Banking Data Required
None.

## Security Considerations
None.

## Compliance Considerations
Strict adherence to RBI KYC guidelines.

## Related FAQs
- [Accounts FAQ](../faqs/accounts-faq.md)

## Related Documents
- [Savings Account](../docs/accounts/savings-account.md)
- [KYC Policy](../docs/policies/kyc-policy.md)
