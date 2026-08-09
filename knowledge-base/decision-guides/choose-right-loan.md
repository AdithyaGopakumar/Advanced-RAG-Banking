---
id: "DG-LOAN-001"
title: "Choose Right Loan Decision Guide"
slug: "choose-right-loan"
domain: "cross-cutting"
category: "decision-guides"
sub_category: "choose-right-loan"
document_type: "decision-guide"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["choose loan", "which loan", "compare loans", "loan type"]
search_aliases: ["help me pick a loan", "what kind of loan do I need"]
tags: ["process:decision", "product:loan"]
priority: "high"
related_documents: ["LOAN-HL-001", "LOAN-PL-001"]
related_faqs: ["loans-faq.md"]
related_scenarios: ["loan-application-journey.md"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Choose Right Loan Decision Guide

## Purpose
To map a customer's borrowing need and collateral availability to the correct loan product category.

## Applicable Intent
`apply_loan`

## Inputs
- `purpose` (Home, Auto, Education, General)
- `collateral_available` (Yes, No)

## Missing Information
If `purpose` is general/missing, clarify:
"Are you looking for a loan for a specific purpose like buying a home or car, or a general personal loan?"

## Decision Logic
IF `purpose` = Home OR `purpose` = Property
    THEN Route to Home Loan / LAP
    
IF `purpose` = Auto
    THEN Route to Auto Loan
    
IF `purpose` = General OR `collateral_available` = NO
    THEN Route to Personal Loan

## Outcomes
- Home Loan
- Auto Loan
- Personal Loan

## Recommended Customer Action
Check eligibility using the online calculator and submit an application lead.

## Exceptions
- None.

## Escalation
Complex or high-value business loans route to Corporate Banking.

## Dynamic Data
- Current Loan Interest Rates (`loan-interest-rates.md`).

## Live Data
- Checking if customer has a pre-approved offer (`LIVE_API`).

## Safety / Compliance
- Do not guarantee loan approval. Approval is subject to credit underwriting.

## Related FAQs
- [Loans FAQ](../faqs/loans-faq.md)

## Related Scenarios
- [Loan Application Journey](../scenarios/loan-application-journey.md)

## Canonical Documents
- [Personal Loan](../docs/loans/personal-loan.md)
- [Home Loan](../docs/loans/home-loan.md)
