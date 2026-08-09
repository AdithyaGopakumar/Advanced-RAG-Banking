---
id: "SCEN-DOC-001"
title: "Form & Document Assistance"
slug: "form-document-assistance"
domain: "cross-cutting"
category: "scenarios"
sub_category: "form-document-assistance"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["bank forms", "interest certificate", "TDS certificate", "download form", "service request"]
search_aliases: ["how to get interest certificate", "where to find forms", "download Form 16A"]
tags: ["intent:request_form", "process:service"]
priority: "high"
related_documents: ["FORM-SR-001", "FORM-CERT-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Form & Document Assistance Scenario

## Situation
The customer needs a specific certificate (Interest, TDS, Balance) or a physical form for a service request (e.g., adding a nominee, closing an account).

## Customer Intent
`request_certificate_form`

## What the Customer May Say
- "I need an interest certificate for filing ITR."
- "Where can I download the account closure form?"
- "How do I get my Form 16A?"

## Relevant Information
Most certificates can be downloaded instantly from the digital portal. Physical forms are available on the website's download center.

## Recommended Response Path
Direct the customer to the 'Services' > 'Certificates' section in Internet Banking for instant digital downloads. For physical forms, provide the link to the forms repository.

## Immediate Action
None.

## Next Steps
Customer downloads the required document.

## Exceptions
- **Physical Stamping**: If the customer requires a physically stamped balance certificate for visa purposes, they must visit the branch.

## When to Escalate
None.

## Dynamic Information Required
- Current version of the requested form (must be pulled dynamically from Phase 15 logic to avoid serving stale forms).

## Live Banking Data Required
- Customer's actual financial data to generate the certificate.

## Security Considerations
None.

## Compliance Considerations
Ensuring TDS certificates (Form 16A) are issued accurately.

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Documents
- [Certificates](../docs/forms/certificates.md)
- [Service Request Forms](../docs/forms/service-request-forms.md)
