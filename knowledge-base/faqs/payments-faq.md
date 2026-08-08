---
id: "FAQ-PAY-001"
title: "Payments FAQ"
slug: "payments-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "payments-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["payment questions", "NEFT help", "RTGS questions", "transfer help", "cheque clearance"]
tags: ["topic:faq", "process:fund-transfer"]
search_aliases: ["transfer FAQ", "payment help", "NEFT questions"]
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

# Payments — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about Payments.

---


# Payments FAQ

## 1. Fund Transfer Types and Limits
### Intent: `compare_transfers_limits`
**Variations**:
- What is the difference between NEFT and IMPS?
- What is the maximum amount I can transfer via RTGS?
- What is my daily UPI limit?

**Response Route**: `STATIC_RAG` / `DYNAMIC_KNOWLEDGE`
**Answer**: IMPS and UPI are for instant transfers, while NEFT settles in batches. RTGS is for high-value transfers (minimum ₹2 Lakhs). Transfer limits are governed by regulatory thresholds and your specific customer profile.
**Canonical Documents**: [NEFT](../docs/payments/neft.md), [IMPS](../docs/payments/imps.md), and [Regulatory Thresholds](../docs/policies/regulatory-thresholds.md)

## 2. Transfer Charges
### Intent: `check_transfer_charges`
**Variations**:
- Is there a fee for NEFT transfers online?
- How much does an IMPS transfer cost?
- Are RTGS transfers free?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: Digital transfers (via Mobile/Internet banking) are typically free for savings account customers, but branch-initiated transfers may attract charges.
**Canonical Document**: [Payment Charges](../docs/charges/payment-charges.md)

## 3. Transaction Status (Live Data)
### Intent: `check_payment_status`
**Variations**:
- Why hasn't my NEFT transfer reached the beneficiary?
- My UPI payment failed but money was deducted, what now?
- How do I check the status of my RTGS transfer?

**Response Route**: `LIVE_API` / `STATIC_RAG`
**Answer**: I cannot check live transaction statuses from static memory. Please check the 'Recent Transactions' or 'Payment History' section in the Mobile App. If a transaction fails and money is debited, it is usually auto-refunded within a specified timeframe.
**Canonical Document**: [Payment Troubleshooting](../docs/payments/payment-troubleshooting.md)
