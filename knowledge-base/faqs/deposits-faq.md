---
id: "FAQ-DEP-001"
title: "Deposits FAQ"
slug: "deposits-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "deposits-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["fixed deposit questions", "FD help", "RD questions", "deposit interest", "premature withdrawal"]
tags: ["topic:faq", "product:fixed-deposit", "product:recurring-deposit"]
search_aliases: ["FD FAQ", "deposit help", "FD questions"]
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

# Deposits — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about Deposits.

---


# Deposits — Frequently Asked Questions

## 1. Current Interest Rates
### Intent: `check_fd_rate`
**Variations**:
- What is the current FD interest rate?
- How much interest do I get on a 1-year FD?
- Do senior citizens get higher interest?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: Interest rates vary by deposit tenure and customer category (senior citizens typically receive a premium). Rates are periodically updated by the bank.
**Canonical Document**: [Deposit Interest Rates](../docs/interest-rates/deposit-interest-rates.md)

## 2. Premature Withdrawal
### Intent: `premature_fd_closure`
**Variations**:
- Can I close my FD early?
- Is there a penalty for breaking an FD before maturity?
- How do I withdraw my fixed deposit prematurely?

**Response Route**: `STATIC_RAG` / `DYNAMIC_KNOWLEDGE`
**Answer**: Yes, FDs can generally be closed before maturity (except for specific Tax-Saver FDs). However, a premature withdrawal penalty usually applies, and interest will be paid at the rate applicable for the period the deposit actually remained with the bank.
**Canonical Document**: [Fixed Deposit](../docs/deposits/fixed-deposit.md) and [Account Charges](../docs/charges/account-charges.md)

## 3. Maturity Status (Live Data)
### Intent: `check_fd_maturity`
**Variations**:
- When will my FD mature?
- What is the maturity amount of my FD?
- Has my recurring deposit matured yet?

**Response Route**: `LIVE_API`
**Answer**: I cannot access your specific deposit details from static memory. To view your exact maturity date and maturity amount, please check the 'Deposits' section in Internet Banking or your Mobile App.
**Canonical Document**: None (Live routing)

## 4. Tax Deduction at Source (TDS)
### Intent: `check_fd_tds`
**Variations**:
- How much tax is deducted on FD interest?
- What is the TDS limit for fixed deposits?
- How do I submit Form 15G/15H?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: TDS is deducted if the total interest earned across all branches exceeds the regulatory threshold in a financial year. You can submit Form 15G or Form 15H (for senior citizens) to request non-deduction of TDS if your total income is below the taxable limit.
**Canonical Document**: [Regulatory Thresholds](../docs/policies/regulatory-thresholds.md)
