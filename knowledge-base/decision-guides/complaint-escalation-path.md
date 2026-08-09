---
id: "DG-ESC-001"
title: "Complaint Escalation Decision Guide"
slug: "complaint-escalation-path"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "complaint-escalation-path"
document_type: "decision-guide"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["complaint", "escalate", "grievance", "ombudsman", "nodal officer"]
search_aliases: ["how to escalate issue", "where to complain"]
tags: ["process:escalation", "category:service"]
priority: "high"
related_documents: ["CUST-COMP-001", "CUST-ESC-001"]
related_faqs: ["general-faq.md"]
related_scenarios: ["dispute-resolution.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Complaint Escalation Decision Guide

## Purpose
To determine the correct grievance redressal level for a dissatisfied customer based on their current ticket status.

## Applicable Intent
`file_complaint`

## Inputs
- `existing_ticket` (Yes, No)
- `ticket_age` (Under 30 days, Over 30 days)
- `current_level` (None, Level 1, Level 2, Level 3)

## Missing Information
If `existing_ticket` is YES, ask:
"Do you have a reference number, and has it been more than 30 days since you raised it?"

## Decision Logic
IF `existing_ticket` = NO
    THEN Route to Level 1 (Branch / Customer Care).
    
IF `existing_ticket` = YES AND `current_level` = Level 1
    THEN Route to Level 2 (Nodal Officer).
    
IF `existing_ticket` = YES AND `current_level` = Level 2
    THEN Route to Level 3 (Principal Nodal Officer).
    
IF `ticket_age` > 30 days AND unresolved
    THEN Route to Banking Ombudsman (RBI).

## Outcomes
- Log Level 1 Ticket
- Escalate to Level 2
- Escalate to Level 3
- File with Banking Ombudsman

## Recommended Customer Action
Use the online grievance portal with the previous ticket reference number to escalate.

## Exceptions
- None.

## Escalation
This guide *is* the escalation matrix.

## Dynamic Data
- Current contact details for Nodal/Principal Officers.

## Live Data
- Check status of existing ticket ID.

## Safety / Compliance
- The bank is legally obligated to resolve complaints within 30 days under the RBI Integrated Ombudsman Scheme.

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Scenarios
- [Dispute Resolution](../scenarios/dispute-resolution.md)

## Canonical Documents
- [Complaint Process](../docs/customer-support/complaint-process.md)
- [Escalation Matrix](../docs/customer-support/escalation-matrix.md)
