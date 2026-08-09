---
id: "SCEN-LOCKOUT-001"
title: "Digital Banking Lockout"
slug: "digital-banking-lockout"
domain: "cross-cutting"
category: "scenarios"
sub_category: "digital-banking-lockout"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["app locked", "forgot password", "forgot MPIN", "account blocked", "unlock access"]
search_aliases: ["can't login to app", "reset internet banking password", "unblock mobile banking"]
tags: ["intent:login_issue", "channel:digital"]
priority: "high"
related_documents: ["DIGI-IB-001", "DIGI-MB-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Digital Banking Lockout Scenario

## Situation
The customer has forgotten their password, entered the wrong MPIN too many times, or has had their digital access locked for security reasons.

## Customer Intent
`digital_login_troubleshooting`

## What the Customer May Say
- "I am locked out of my mobile app."
- "I forgot my net banking password."
- "My account is blocked due to wrong MPIN."

## Relevant Information
Access can be reset using an active Debit Card (Number, Expiry, ATM PIN) or by answering security questions/profile passwords.

## Recommended Response Path
Direct the customer to the "Forgot Password / Unlock Access" link on the login screen. Instruct them to use their debit card details to reset their credentials instantly.

## Immediate Action
None.

## Next Steps
Customer completes the self-service reset flow.

## Exceptions
- **No Active Debit Card**: Must reset via branch using a physical form.
- **Fraud Lock**: If locked by the backend fraud engine, the customer must call Customer Care to verify identity.

## When to Escalate
Escalate to human support if self-service reset fails multiple times.

## Dynamic Information Required
None.

## Live Banking Data Required
None.

## Security Considerations
Never ask the customer to share their OTP or new password.

## Compliance Considerations
None.

## Related FAQs
- [Digital Banking FAQ](../faqs/digital-banking-faq.md)

## Related Documents
- [Internet Banking Troubleshooting](../docs/digital-banking/internet-banking-troubleshooting.md)
- [Mobile Banking Troubleshooting](../docs/digital-banking/mobile-banking-troubleshooting.md)
