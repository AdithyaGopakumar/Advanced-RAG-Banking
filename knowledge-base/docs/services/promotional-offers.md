---
id: "SVC-PROMO-001"
title: "Promotional Offers and Campaigns"
slug: "promotional-offers"
domain: "services"
category: "services"
sub_category: "promotions"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["offers", "promotions", "cashback", "discounts", "campaign"]
tags: ["reference:promotions"]
search_aliases: ["current offers", "card discounts"]
priority: "medium"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-08"
last_updated: "2026-08-08"
effective_from: "2026-08-08"
effective_until: ""
source: "Marketing Campaigns"
authority: "Marketing"
owner: "Marketing SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
dynamic_classification: "FREQUENTLY_DYNAMIC"
data_source: "offers-api"
---

# Promotional Offers and Campaigns

## Overview

> [!WARNING]
> Promotional offers are strictly time-bound and subject to eligibility. According to the bank's current campaign list, the following offers apply. Always refer to the live offers API for real-time validity and expiry dates. Expired promotions are marked as `EXPIRED` or `WITHDRAWN`.

This document aggregates currently active promotional campaigns for credit cards, debit cards, loans, and other banking services. 

---

## Active Campaigns

<!-- BANK-SPECIFIC: List of current campaigns retrieved from API -->

- *Currently, there are no static promotional campaigns indexed. Please refer to the live offers portal for active cashback, discounts, and fee waivers.*

## Real-Time Knowledge Boundary

To check if an offer is still active or if a customer is eligible:
- **Do not answer from static memory if the current date is past the `effective_until` date.**
- **Required System:** Offers API / Customer CRM.
- **Fallback (if unavailable):** "Offers are subject to change and specific eligibility criteria. Please check the 'Offers' section in your mobile banking app."
