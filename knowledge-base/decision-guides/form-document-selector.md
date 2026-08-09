---
id: "DG-FORM-001"
title: "Form & Document Selector Decision Guide"
slug: "form-document-selector"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "form-document-selector"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["which form", "download form", "certificate", "service request"]
search_aliases: ["what form do I need", "how to get certificate"]
tags: ["process:decision", "category:forms"]
priority: "high"
related_documents: ["FORM-SR-001", "FORM-CERT-001"]
related_faqs: ["general-faq.md"]
related_scenarios: ["form-document-assistance.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Form & Document Selector Decision Guide

## Purpose
To route a customer to the correct physical form or digital certificate based on their service request.

## Applicable Intent
`request_certificate_form`

## Inputs
- `request_type` (Nomination, KYC, Claim, Interest Cert, Balance Cert)

## Missing Information
"Which specific certificate or service form are you looking for?"

## Decision Logic
IF `request_type` = Interest Cert OR Balance Cert OR TDS Cert
    THEN Route to Digital Download (Internet Banking > Services > Certificates).
    
IF `request_type` = Nomination
    THEN Route to Form DA1 (Addition) or DA2/DA3 (Modification/Cancellation).
    
IF `request_type` = Claim (Deceased)
    THEN Route to Deceased Claim Form.
    
IF `request_type` = KYC
    THEN Route to Re-KYC Form.

## Outcomes
- Digital Certificate Download
- Form DA1/DA2/DA3
- Deceased Claim Form
- Re-KYC Form

## Recommended Customer Action
Download the relevant form, fill it, and submit it at the home branch, or download the certificate digitally.

## Exceptions
- None.

## Escalation
None.

## Dynamic Data
- Ensure the agent provides the link to the *current* version of the form (Phase 15 dynamic checking).

## Live Data
- Certificates generated via `LIVE_API` for specific financial years.

## Safety / Compliance
- Ensure KYC forms mention the requirement for self-attested Officially Valid Documents (OVDs).

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Scenarios
- [Form & Document Assistance](../scenarios/form-document-assistance.md)

## Canonical Documents
- [Service Request Forms](../docs/forms/service-request-forms.md)
- [Certificates](../docs/forms/certificates.md)
