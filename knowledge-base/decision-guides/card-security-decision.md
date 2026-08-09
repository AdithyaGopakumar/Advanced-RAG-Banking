---
id: "DG-CARDSEC-001"
title: "Card Security Decision Guide"
slug: "card-security-decision"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "card-security-decision"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["card lost", "card stolen", "block card", "unauthorized transaction"]
search_aliases: ["what to do if card is stolen", "suspect fraud on card"]
tags: ["process:security", "product:card"]
priority: "high"
related_documents: ["SEC-CARD-001"]
related_faqs: ["cards-faq.md", "security-faq.md"]
related_scenarios: ["lost-card-replacement.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Card Security Decision Guide

## Purpose
To provide emergency routing when a card is compromised, lost, or experiencing unauthorized usage.

## Applicable Intent
`block_card` / `report_fraud`

## Inputs
- `issue_type` (Lost/Stolen, Misplaced temporarily, Unauthorized Transaction)

## Missing Information
If `issue_type` is vague ("my card is gone"), clarify:
"Do you think it is permanently lost/stolen, or just temporarily misplaced? Are there any transactions on it that you didn't make?"

## Decision Logic
IF `issue_type` = Unauthorized Transaction
    THEN **URGENT**: Route to Permanent Block AND Fraud Reporting pipeline.
    
IF `issue_type` = Lost/Stolen
    THEN Route to Permanent Block AND Issue Replacement.
    
IF `issue_type` = Misplaced temporarily
    THEN Route to Temporary Card Lock (can be unlocked later).

## Outcomes
- Permanent Block + Fraud Dispute
- Permanent Block + Card Replacement
- Temporary Lock

## Recommended Customer Action
Execute the block via the Mobile App or emergency helpline immediately.

## Exceptions
- None.

## Escalation
If customer cannot log in to block, invoke `LIVE_API` block via human agent instantly.

## Dynamic Data
- None.

## Live Data
- `LIVE_API` to execute the block command on the customer's card.

## Safety / Compliance
- **CRITICAL**: Customer liability depends on reporting speed. Zero liability applies if reported within 3 days of unauthorized debit.

## Related FAQs
- [Cards FAQ](../faqs/cards-faq.md)
- [Security FAQ](../faqs/security-faq.md)

## Related Scenarios
- [Lost Card Replacement](../scenarios/lost-card-replacement.md)

## Canonical Documents
- [Card Security Guidelines](../docs/security/card-security.md)
