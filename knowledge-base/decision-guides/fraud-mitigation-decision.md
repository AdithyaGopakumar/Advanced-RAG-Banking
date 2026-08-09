---
id: "DG-FRAUD-001"
title: "Fraud Mitigation Decision Guide"
slug: "fraud-mitigation-decision"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "fraud-mitigation-decision"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["fraud", "scam", "phishing", "OTP shared", "hacked"]
search_aliases: ["I was scammed", "someone took my money"]
tags: ["process:security", "category:fraud"]
priority: "high"
related_documents: ["SEC-FRAUD-001", "SEC-PHISH-001"]
related_faqs: ["security-faq.md"]
related_scenarios: ["fraud-reporting.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Fraud Mitigation Decision Guide

## Purpose
To assess a security threat (e.g., phishing link clicked vs. OTP shared) and execute the appropriate lockdown protocol.

## Applicable Intent
`report_fraud` / `verify_communication`

## Inputs
- `threat_vector` (Suspicious SMS, Link Clicked, Credentials/OTP Shared, Unauthorized Debit Occurred)

## Missing Information
"Did you click any links, share any OTP/passwords, or notice money actually leaving your account?"

## Decision Logic
IF `threat_vector` = Suspicious SMS (Ignored)
    THEN Route to Awareness (No action needed, do not engage).
    
IF `threat_vector` = Link Clicked (But no credentials entered)
    THEN Route to Precautionary (Run antivirus, change passwords).
    
IF `threat_vector` = Credentials/OTP Shared OR Unauthorized Debit Occurred
    THEN **CRITICAL EMERGENCY**. Route to Total Lockdown (Block net banking, freeze account, block cards).

## Outcomes
- Awareness / Ignore
- Precautionary Password Reset
- CRITICAL Lockdown + Fraud Dispute

## Recommended Customer Action
For CRITICAL: Block all channels immediately via App or Phone.

## Exceptions
- None.

## Escalation
For CRITICAL, invoke `LIVE_API` to freeze account immediately or route to highest-priority human queue.

## Dynamic Data
- None.

## Live Data
- None.

## Safety / Compliance
- **Zero Tolerance**. Never ask the customer for the compromised credentials.
- Adherence to RBI circular on customer liability in unauthorized electronic banking transactions.

## Related FAQs
- [Security FAQ](../faqs/security-faq.md)

## Related Scenarios
- [Fraud Reporting](../scenarios/fraud-reporting.md)

## Canonical Documents
- [Fraud Prevention](../docs/security/fraud-prevention.md)
- [Phishing Awareness](../docs/security/phishing-awareness.md)
