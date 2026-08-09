---
id: "DG-DIGIREC-001"
title: "Digital Access Recovery Decision Guide"
slug: "digital-access-recovery"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "digital-access-recovery"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["forgot password", "reset MPIN", "app locked", "unlock net banking"]
search_aliases: ["how to reset net banking password", "unblock mobile app"]
tags: ["process:recovery", "channel:digital"]
priority: "high"
related_documents: ["DIGI-IB-001", "DIGI-MB-001"]
related_faqs: ["digital-banking-faq.md"]
related_scenarios: ["digital-banking-lockout.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Digital Access Recovery Decision Guide

## Purpose
To determine the correct path for a customer to regain access to Mobile or Internet Banking when locked out.

## Applicable Intent
`digital_login_troubleshooting`

## Inputs
- `lock_reason` (Forgot Password/PIN, Exceeded Attempts, Device Changed)
- `has_active_debit_card` (Yes, No)

## Missing Information
If `has_active_debit_card` is unknown, clarify:
"Do you have an active debit card and its ATM PIN available with you?"

## Decision Logic
IF `lock_reason` = Device Changed
    THEN Route to SMS Binding / Device Verification process.
    
IF `lock_reason` = Forgot Password/PIN OR Exceeded Attempts
    IF `has_active_debit_card` = YES
        THEN Route to Online Self-Service Reset (using card details).
    ELSE
        THEN Route to Branch Reset (physical request required).

## Outcomes
- Self-Service Reset Online
- Branch Reset Request
- Device Re-binding

## Recommended Customer Action
Follow the "Forgot Password" link on the login screen if self-service is applicable.

## Exceptions
- **Fraud Lock**: If backend systems locked the profile due to suspicious activity, self-service is disabled. Must contact Customer Care.

## Escalation
Escalate to technical support if SMS delivery for device binding fails repeatedly.

## Dynamic Data
- None.

## Live Data
- None.

## Safety / Compliance
- Remind customer never to share OTPs during the reset process.

## Related FAQs
- [Digital Banking FAQ](../faqs/digital-banking-faq.md)

## Related Scenarios
- [Digital Banking Lockout](../scenarios/digital-banking-lockout.md)

## Canonical Documents
- [Internet Banking Troubleshooting](../docs/digital-banking/internet-banking-troubleshooting.md)
