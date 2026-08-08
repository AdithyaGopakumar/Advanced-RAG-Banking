---
id: "FAQ-CARD-001"
title: "Cards FAQ"
slug: "cards-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "cards-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["credit card questions", "debit card help", "card block", "card limit", "card PIN"]
tags: ["topic:faq", "product:credit-card", "product:debit-card"]
search_aliases: ["card help", "credit card FAQ", "debit card questions"]
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

# Cards — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about Cards.

---


# Cards — Frequently Asked Questions

## 1. Card Blocking (Security Critical)
### Intent: `block_card`
**Variations**:
- I lost my credit card, how do I block it?
- My debit card is stolen, what should I do?
- How to block my card immediately?

**Response Route**: `STATIC_RAG` (Security Priority)
**Answer**: If your card is lost or stolen, block it immediately to prevent unauthorized usage. You can block it via Mobile Banking, Internet Banking, or by calling the 24x7 Customer Care helpline.
**Canonical Documents**: [Card Security Guidelines](../docs/security/card-security.md) and [Contact Channels](../docs/customer-support/contact-channels.md)

## 2. PIN Generation
### Intent: `generate_card_pin`
**Variations**:
- How do I generate a PIN for my new card?
- I forgot my ATM PIN, how do I reset it?
- Can I change my credit card PIN online?

**Response Route**: `STATIC_RAG`
**Answer**: You can generate or change your card PIN instantly through Mobile Banking, Internet Banking, or at any bank ATM using the OTP sent to your registered mobile number.
**Canonical Document**: [Credit Card](../docs/cards/credit-card.md) or [Debit Card](../docs/cards/debit-card.md)

## 3. Card Limits and International Usage
### Intent: `manage_card_limits`
**Variations**:
- How do I increase my credit card limit?
- Can I use my debit card internationally?
- How do I enable e-commerce transactions on my card?

**Response Route**: `STATIC_RAG` / `LIVE_API`
**Answer**: As per RBI guidelines, cards are disabled for international, online (e-commerce), and contactless transactions by default. You can enable these and manage your transaction limits instantly via the 'Manage Cards' section in the Mobile App.
**Canonical Document**: [Card Security Guidelines](../docs/security/card-security.md)

## 4. Fees and Interest Rates
### Intent: `check_card_fees`
**Variations**:
- What is the annual fee for my credit card?
- How much interest is charged on credit card cash advances?
- What is the markup fee for international transactions?

**Response Route**: `DYNAMIC_KNOWLEDGE`
**Answer**: Card fees (such as annual fees, replacement fees, and forex markup) and interest rates (APR) vary by card variant. Please refer to the official rate schedules.
**Canonical Documents**: [Card Charges](../docs/charges/card-charges.md) and [Card Interest Rates](../docs/interest-rates/card-interest-rates.md)
