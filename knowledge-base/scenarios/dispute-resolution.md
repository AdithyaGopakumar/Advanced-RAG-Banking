---
id: "SCEN-DISP-001"
title: "Dispute Resolution"
slug: "dispute-resolution"
domain: "cross-cutting"
category: "scenarios"
sub_category: "dispute-resolution"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["dispute", "complaint", "escalation", "grievance", "ombudsman"]
search_aliases: ["file a complaint", "escalate issue", "raise a dispute"]
tags: ["intent:complain", "process:dispute"]
priority: "high"
related_documents: ["CUST-COMP-001", "CUST-ESC-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Dispute Resolution Scenario

## Situation
The customer is dissatisfied with a bank charge, service failure, or previous complaint outcome, and wishes to raise a formal dispute.

## Customer Intent
`file_complaint`

## What the Customer May Say
- "I want to file a complaint against the branch."
- "You charged me a fee unfairly, I want a refund."
- "My issue wasn't resolved, who can I escalate to?"

## Relevant Information
The bank has a multi-tiered grievance redressal mechanism mandated by RBI.

## Recommended Response Path
Acknowledge the frustration. Provide the link to log a formal grievance via the grievance portal or provide the Customer Care email. If they have an existing ticket, provide the escalation path.

## Immediate Action
None.

## Next Steps
Customer must log a formal ticket to receive a reference number.

## Exceptions
- **Fraud Dispute**: Belongs in the Fraud Reporting scenario, not general dispute.

## When to Escalate
If the customer has already passed Level 1 (Branch/Customer Care), escalate to the Principal Nodal Officer (PNO).

## Dynamic Information Required
None.

## Live Banking Data Required
- Current status of the complaint ticket.

## Security Considerations
None.

## Compliance Considerations
Complaints must be acknowledged and resolved within the RBI-stipulated timeframe (typically 30 days before Ombudsman escalation).

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Documents
- [Complaint Process](../docs/customer-support/complaint-process.md)
- [Escalation Matrix](../docs/customer-support/escalation-matrix.md)
