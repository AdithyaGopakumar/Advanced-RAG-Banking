---
id: "DG-CARD-001"
title: "Choose Right Card Decision Guide"
slug: "choose-right-card"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "choose-right-card"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["choose card", "which card", "compare cards", "credit card type"]
search_aliases: ["help me pick a credit card", "best credit card"]
tags: ["process:decision", "product:card"]
priority: "high"
related_documents: ["CARD-CC-001"]
related_faqs: ["cards-faq.md"]
related_scenarios: []
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Choose Right Card Decision Guide

## Purpose
To suggest the appropriate credit card variant based on the customer's primary spending habits and lifestyle needs.

## Applicable Intent
`apply_card`

## Inputs
- `primary_spend_category` (Travel, Shopping, Cashback, Basic)
- `income_bracket` (Standard, High Net Worth)

## Missing Information
If `primary_spend_category` is unknown, clarify:
"Are you looking for a card primarily for travel rewards, shopping cashback, or just a basic card with no annual fee?"

## Decision Logic
IF `income_bracket` = High Net Worth AND `primary_spend_category` = Travel
    THEN Route to Premium Travel Credit Card
    
IF `primary_spend_category` = Cashback OR Shopping
    THEN Route to Cashback/Rewards Credit Card
    
IF `primary_spend_category` = Basic
    THEN Route to Entry-level Zero Fee Card

## Outcomes
- Premium Card
- Rewards Card
- Basic Card

## Recommended Customer Action
Apply via the Cards section in Internet Banking.

## Exceptions
- Card issuance is subject to credit score checks.

## Escalation
None.

## Dynamic Data
- Annual fees and joining fees (`card-charges.md`).

## Live Data
- Pre-approved limit checks (`LIVE_API`).

## Safety / Compliance
- Do not promise specific credit limits.

## Related FAQs
- [Cards FAQ](../faqs/cards-faq.md)

## Related Scenarios
- None.

## Canonical Documents
- [Credit Card](../docs/cards/credit-card.md)
