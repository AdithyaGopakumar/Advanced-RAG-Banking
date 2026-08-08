---
id: "FAQ-LOAN-001"
title: "Loans FAQ"
slug: "loans-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "loans-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["loan questions", "EMI help", "loan eligibility", "prepayment", "foreclosure"]
tags: ["topic:faq", "product:home-loan", "product:personal-loan"]
search_aliases: ["loan help", "EMI FAQ", "loan questions"]
priority: "high"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Loans — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about Loans.

---


# Loans — Frequently Asked Questions

## 1. Loan Interest Rates
### Intent: `check_loan_rate`
**Variations**:
- What is the current home loan interest rate?
- How much is the personal loan interest?
- What is the current EBLR/Repo rate?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: Loan interest rates are typically linked to an external benchmark like the RBI Repo Rate (EBLR) plus a spread. The spread may depend on your credit score and loan amount.
**Canonical Document**: [Loan Interest Rates](../docs/interest-rates/loan-interest-rates.md)

## 2. Loan Prepayment and Foreclosure
### Intent: `loan_prepayment`
**Variations**:
- Can I prepay my home loan?
- Are there charges for foreclosing a personal loan?
- Can I make a part-payment on my loan?

**Response Route**: `STATIC_RAG` / `DYNAMIC_KNOWLEDGE`
**Answer**: Yes, loans can be prepaid or foreclosed. While floating-rate home loans for individuals typically do not have prepayment penalties, other loans like personal loans often attract foreclosure charges if closed before a certain period.
**Canonical Document**: [Loan Charges](../docs/charges/loan-charges.md)

## 3. Outstanding Loan Amount (Live Data)
### Intent: `check_loan_outstanding`
**Variations**:
- What is my current outstanding loan amount?
- How many EMIs are left on my loan?
- Did my last EMI get credited?

**Response Route**: `LIVE_API`
**Answer**: I cannot access your individual loan account details from static memory. To check your outstanding principal, remaining tenure, or EMI status, please log in to the 'Loans' section in Internet Banking or your Mobile App.
**Canonical Document**: None (Live routing)

## 4. Obtaining an NOC (No Objection Certificate)
### Intent: `get_loan_noc`
**Variations**:
- How do I get an NOC after closing my loan?
- Will the bank send the NOC automatically?
- My loan is closed, where are my original property documents?

**Response Route**: `STATIC_RAG`
**Answer**: Upon full repayment and closure of your loan, the bank issues a No Objection Certificate (NOC). For home loans, the original property documents are returned to the owner. This process typically takes a few working days after final settlement.
**Canonical Document**: [Service Request Forms](../docs/forms/service-request-forms.md)
