---
id: "FAQ-ACCT-001"
title: "Accounts FAQ"
slug: "accounts-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "accounts-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["savings account questions", "account opening help", "minimum balance", "account closure", "passbook"]
tags: ["topic:faq", "product:savings-account", "product:current-account"]
search_aliases: ["account help", "account FAQ", "bank account questions"]
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

# Accounts — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about Accounts.

---


# Accounts — Frequently Asked Questions

## 1. Opening an Account
### Intent: `open_account`
**Variations**:
- How do I open a savings account?
- What is the process to open a new account?
- Can I open a bank account online?

**Response Route**: `STATIC_RAG`
**Answer**: To open an account, you can apply online via the website or visit your nearest branch. You will need your PAN, Aadhaar, and a photograph. For specific account features and eligibility, please refer to the relevant product page.
**Canonical Document**: [Savings Account](../docs/accounts/savings-account.md)

## 2. Minimum Balance Requirements
### Intent: `check_minimum_balance`
**Variations**:
- How much is the minimum balance for my account?
- What is the MAB for a savings account?
- Is there a penalty for not maintaining a minimum balance?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: Minimum Average Balance (MAB) requirements depend on your specific account variant and branch location (Metro, Urban, Semi-Urban, or Rural). 
**Canonical Document**: [Account Charges](../docs/charges/account-charges.md)

## 3. Joint Accounts
### Intent: `open_joint_account`
**Variations**:
- Can I open a joint account?
- How do I add my spouse to my account?
- What are the rules for joint accounts?

**Response Route**: `STATIC_RAG`
**Answer**: Yes, most savings and current accounts can be opened jointly. Both applicants must complete full KYC. The mode of operation can be "Either or Survivor", "Anyone or Survivor", or "Jointly".
**Canonical Document**: [Savings Account](../docs/accounts/savings-account.md)

## 4. Adding a Nominee
### Intent: `add_nominee`
**Variations**:
- How do I add a nominee to my bank account?
- Can I change my nominee later?
- Is nomination mandatory?

**Response Route**: `STATIC_RAG`
**Answer**: You can add or modify a nominee anytime through Internet Banking, Mobile Banking, or by submitting a nomination form at your base branch. Nomination is highly recommended to ensure smooth claim settlement.
**Canonical Document**: [Service Request Forms](../docs/forms/service-request-forms.md)

## 5. Account Closure
### Intent: `close_account`
**Variations**:
- How do I close my bank account?
- Can I close my account online?
- Are there charges for closing an account?

**Response Route**: `STATIC_RAG` / `DYNAMIC_KNOWLEDGE`
**Answer**: Account closure requests must typically be submitted in writing at your home branch along with your unused cheque book and debit card. Early closure (within a specific timeframe of opening) may attract charges.
**Canonical Document**: [Account Closure Policy](../docs/policies/account-closure-policy.md) and [Account Charges](../docs/charges/account-charges.md)
