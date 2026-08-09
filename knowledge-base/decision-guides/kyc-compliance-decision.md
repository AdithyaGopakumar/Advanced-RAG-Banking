---
id: "DG-KYC-001"
title: "KYC Compliance Decision Guide"
slug: "kyc-compliance-decision"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "kyc-compliance-decision"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["KYC", "Re-KYC", "update PAN", "update Aadhaar", "account frozen"]
search_aliases: ["how to do KYC", "why is my account blocked for KYC"]
tags: ["process:compliance", "category:kyc"]
priority: "high"
related_documents: ["POL-KYC-001"]
related_faqs: ["general-faq.md"]
related_scenarios: ["profile-update-kyc.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# KYC Compliance Decision Guide

## Purpose
To guide customers on the correct channel to submit KYC/Re-KYC documents based on their account state.

## Applicable Intent
`update_kyc_profile`

## Inputs
- `account_state` (Active, Frozen)
- `update_type` (Routine Address Change, Mandated Re-KYC, PAN Update)

## Missing Information
If `account_state` is unknown:
"Are you able to make transactions currently, or has your account been restricted?"

## Decision Logic
IF `account_state` = Frozen
    THEN Branch visit is MANDATORY. Online Re-KYC is disabled for frozen accounts.
    
IF `account_state` = Active AND `update_type` = Mandated Re-KYC
    THEN Route to V-KYC (Video KYC) or App-based Re-KYC upload.
    
IF `account_state` = Active AND `update_type` = PAN Update
    THEN Route to Internet Banking Profile section.

## Outcomes
- Branch Visit (Mandatory)
- Video KYC / App Upload
- Internet Banking Self-Service

## Recommended Customer Action
Follow the required channel. Remind them to carry original OVDs (Officially Valid Documents) if visiting a branch or doing V-KYC.

## Exceptions
- **NRI Customers**: Must use specific NRI email channels or send attested copies; cannot use standard V-KYC.

## Escalation
None.

## Dynamic Data
- None.

## Live Data
- None.

## Safety / Compliance
- Re-KYC is an RBI mandate based on risk categorization (High risk = 2 yrs, Medium = 8 yrs, Low = 10 yrs).

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Scenarios
- [Profile Update KYC](../scenarios/profile-update-kyc.md)

## Canonical Documents
- [KYC Policy](../docs/policies/kyc-policy.md)
