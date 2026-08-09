---
id: "DG-ACCT-001"
title: "Choose Right Account Decision Guide"
slug: "choose-right-account"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "choose-right-account"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["choose account", "which account", "compare accounts", "account type"]
search_aliases: ["help me pick an account", "what account should I open"]
tags: ["process:decision", "product:account"]
priority: "high"
related_documents: ["ACCT-SA-001", "ACCT-CA-001"]
related_faqs: ["accounts-faq.md"]
related_scenarios: ["new-customer-onboarding.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Choose Right Account Decision Guide

## Purpose
To help the AI assistant evaluate customer needs and map them to the appropriate savings or current account product without giving personalized financial advice.

## Applicable Intent
`open_account`

## Inputs
- `customer_type` (Individual, Business, Minor, NRI)
- `transaction_volume` (High, Low)
- `primary_need` (Savings, Daily Business, Salary)

## Missing Information
If `customer_type` or `primary_need` is missing, clarify:
"Are you looking to open an account for personal savings or for business purposes?"

## Decision Logic
IF `customer_type` = Business
    THEN Route to Current Account selection
    
IF `customer_type` = Minor
    THEN Route to Minor Savings Account rules
    
IF `customer_type` = Individual AND `primary_need` = Salary
    THEN Route to Salary Account
    
IF `customer_type` = Individual AND `primary_need` = Savings
    IF `transaction_volume` = High
        THEN Route to Premium Savings Account
    ELSE
        THEN Route to Basic Savings Account

## Outcomes
- Basic Savings Account
- Premium Savings Account
- Salary Account
- Current Account
- Minor Account

## Recommended Customer Action
Review the features of the recommended account and apply online or visit the nearest branch.

## Exceptions
- If the customer is an NRI, standard resident accounts cannot be opened. Route to NRI Account documentation.

## Escalation
If the customer has complex corporate requirements, route to Branch / Corporate Support.

## Dynamic Data
- Minimum Average Balance (MAB) requirements for the selected account (`account-charges.md`).

## Live Data
- None.

## Safety / Compliance
- Adherence to KYC policy for account opening.

## Related FAQs
- [Accounts FAQ](../faqs/accounts-faq.md)

## Related Scenarios
- [New Customer Onboarding](../scenarios/new-customer-onboarding.md)

## Canonical Documents
- [Savings Account](../docs/accounts/savings-account.md)
