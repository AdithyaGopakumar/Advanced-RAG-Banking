---
id: "SCEN-KYC-001"
title: "Profile & KYC Update"
slug: "profile-update-kyc"
domain: "cross-cutting"
category: "scenarios"
sub_category: "profile-update-kyc"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["update KYC", "change mobile number", "update address", "Re-KYC", "profile update"]
search_aliases: ["how to change phone number", "update my address", "submit KYC documents"]
tags: ["intent:update_profile", "process:compliance"]
priority: "high"
related_documents: ["POL-KYC-001", "FORM-KYC-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Profile & KYC Update Scenario

## Situation
The customer needs to update their address, mobile number, email, or is responding to a bank request to perform Re-KYC to keep their account active.

## Customer Intent
`update_kyc_profile`

## What the Customer May Say
- "How do I change my registered mobile number?"
- "I shifted to a new house, how to update address?"
- "I got a message to do Re-KYC."

## Relevant Information
Mobile and email can usually be updated via ATMs or Internet Banking. Address changes and Re-KYC usually require submitting an Officially Valid Document (OVD).

## Recommended Response Path
Explain the specific channel for the requested update (e.g., ATM for mobile number). For address/Re-KYC, direct them to the Re-KYC section in the Mobile App to upload documents, or advise visiting the branch.

## Immediate Action
None.

## Next Steps
Customer submits the document online or visits an ATM/branch.

## Exceptions
- **Account Frozen**: If the account is already frozen due to KYC non-compliance, it requires manual verification at the branch.

## When to Escalate
None.

## Dynamic Information Required
None.

## Live Banking Data Required
None.

## Security Considerations
Address and mobile number changes are highly sensitive as they control OTPs and communications. 

## Compliance Considerations
Adherence to Prevention of Money Laundering Act (PMLA) and RBI KYC directives.

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Documents
- [KYC Policy](../docs/policies/kyc-policy.md)
- [KYC Documents](../docs/forms/kyc-documents.md)
