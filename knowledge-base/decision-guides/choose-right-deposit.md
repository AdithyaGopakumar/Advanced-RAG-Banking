---
id: "DG-DEP-001"
title: "Choose Right Deposit Decision Guide"
slug: "choose-right-deposit"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "choose-right-deposit"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["choose FD", "which FD", "compare deposits", "deposit type"]
search_aliases: ["help me pick an FD", "should I open an FD or RD"]
tags: ["process:decision", "product:deposit"]
priority: "high"
related_documents: ["DEP-FD-001", "DEP-RD-001"]
related_faqs: ["deposits-faq.md"]
related_scenarios: ["fixed-deposit-maturity.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Choose Right Deposit Decision Guide

## Purpose
To evaluate a customer's investment horizon, liquidity needs, and tax-saving goals to suggest the appropriate deposit product type.

## Applicable Intent
`open_deposit` / `check_fd_rate`

## Inputs
- `tenure_preference` (Short, Medium, Long)
- `tax_saving_required` (Yes, No)
- `liquidity_required` (Yes, No)

## Missing Information
If `liquidity_required` or `tax_saving_required` is missing, clarify:
"Are you looking to save tax under Section 80C, and do you need the option to break the deposit early?"

## Decision Logic
IF `tax_saving_required` = YES
    THEN Route to Tax Saver FD (Note: 5-year lock-in applies)
    
IF `tax_saving_required` = NO AND `liquidity_required` = YES
    THEN Route to Flexi/Sweep-in Deposit
    
IF `tax_saving_required` = NO AND `liquidity_required` = NO
    IF deposit method is monthly recurring
        THEN Route to Recurring Deposit (RD)
    ELSE
        THEN Route to Standard Fixed Deposit (FD)

## Outcomes
- Standard Fixed Deposit
- Tax Saver FD
- Recurring Deposit
- Flexi Deposit

## Recommended Customer Action
Review the current interest rates and initiate the deposit opening via Internet/Mobile Banking.

## Exceptions
- Senior citizens typically receive a premium rate.

## Escalation
If deposit amount is exceptionally large (e.g., bulk deposits over Rs 2 Crore), escalate to Branch for negotiated rates.

## Dynamic Data
- Current Deposit Interest Rates (`deposit-interest-rates.md`).

## Live Data
- None.

## Safety / Compliance
- Tax Saver FDs cannot be broken prematurely under any circumstance except the death of the depositor.

## Related FAQs
- [Deposits FAQ](../faqs/deposits-faq.md)

## Related Scenarios
- [Fixed Deposit Maturity](../scenarios/fixed-deposit-maturity.md)

## Canonical Documents
- [Fixed Deposit](../docs/deposits/fixed-deposit.md)
