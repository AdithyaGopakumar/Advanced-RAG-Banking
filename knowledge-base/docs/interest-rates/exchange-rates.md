---
id: "RATE-FX-001"
title: "Foreign Exchange Rates"
slug: "exchange-rates"
domain: "reference-data"
category: "interest-rates"
sub_category: "exchange-rates"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["exchange rate", "FX rate", "forex", "conversion rate"]
tags: ["reference:exchange-rates"]
search_aliases: ["currency conversion", "forex rates"]
priority: "high"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-08"
last_updated: "2026-08-08"
effective_from: "2026-08-08"
effective_until: ""
source: "Treasury Live Rates API"
authority: "Treasury"
owner: "Finance SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
dynamic_classification: "FREQUENTLY_DYNAMIC"
data_source: "fx-rate-api"
---

# Foreign Exchange Rates

## Overview

> [!CAUTION]
> Exchange rates are **FREQUENTLY DYNAMIC** and change multiple times a day. Do NOT rely on static knowledge for live FX conversions. You MUST check the live treasury API for the current buy/sell rate.

This document serves as a pointer to the live FX systems. The bank offers dynamic currency conversion for remittances, card transactions, and cash withdrawals.

---

## Real-Time Knowledge Boundary

If a customer asks for the current exchange rate (e.g., "What is the USD to INR rate today?"):

- **Do not answer from static memory.** 
- **Required System:** Treasury API / Live FX Calculator.
- **Fallback (if unavailable):** "Live FX rates fluctuate constantly. Please check the live rate calculator on the internet banking portal or call customer support."
