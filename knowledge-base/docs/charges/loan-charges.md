---
id: "CHG-LOAN-001"
title: "Loan Charges"
slug: "loan-charges"
domain: "reference-data"
category: "charges"
sub_category: "loan-charges"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["loan charges", "processing fee", "prepayment charge", "foreclosure charge", "late payment penalty"]
tags: ["reference:charges", "product:home-loan", "product:personal-loan"]
search_aliases: ["loan fees", "loan processing fee", "EMI late fee"]
priority: "high"
related_documents: ["LOAN-HL-001", "LOAN-PL-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
effective_date: "2026-08-01"
owner: "Finance SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
data_source: "charges-api"
---

# Loan Charges

## Overview

This document is the Single Source of Truth (SSOT) for all fees and charges associated with retail lending products. It covers processing fees, late payment penalties, and foreclosure charges.

---

## Charge Schedule

### Processing Fees

| Loan Product | Processing Fee |
|---|---|
| Home Loan | <!-- BANK-SPECIFIC: % of loan amount (Min ₹ / Max ₹) --> |
| Personal Loan | <!-- BANK-SPECIFIC: % of loan amount --> |
| Education Loan | <!-- BANK-SPECIFIC: Nil up to ₹X lakhs, else ₹Y --> |
| Vehicle Loan | <!-- BANK-SPECIFIC: ₹ amount --> |
| Gold Loan | <!-- BANK-SPECIFIC: ₹ amount based on slab --> |
| Loan Against Property | <!-- BANK-SPECIFIC: % of loan amount --> |
| Loan Against FD | <!-- BANK-SPECIFIC: Nil or ₹ amount --> |

### Late Payment / Penal Interest

| Charge Type | Applicable Rate |
|---|---|
| Late EMI Payment | <!-- BANK-SPECIFIC: 24% p.a. / 2% per month --> on overdue amount |
| Cheque / Mandate Bounce | <!-- BANK-SPECIFIC: ₹500 --> per instance |

### Prepayment and Foreclosure Charges

> [!IMPORTANT]
> As per RBI guidelines, **NO foreclosure charges or pre-payment penalties** are applicable on any floating-rate term loan sanctioned to individual borrowers.

| Loan Product (Rate Type) | Foreclosure Penalty | Part-Payment Penalty |
|---|---|---|
| Home Loan (Floating) | Nil | Nil |
| Loan Against Property (Floating) | Nil | Nil |
| Personal Loan (Fixed) | <!-- BANK-SPECIFIC: 2% to 4% --> on principal outstanding | <!-- BANK-SPECIFIC: % on amount --> |
| Vehicle Loan (Fixed) | <!-- BANK-SPECIFIC: % on principal outstanding --> | <!-- BANK-SPECIFIC: % on amount --> |

---

## GST Applicability

All fees and charges (except penal interest) are exclusive of Goods and Services Tax (GST). GST at the prevailing rate (currently 18%) is applicable on all processing fees, valuation charges, and mandate bounce charges.

---

## Related Documents

- [Home Loan](../loans/home-loan.md)
- [Personal Loan](../loans/personal-loan.md)
- [Education Loan](../loans/education-loan.md)
- [Vehicle Loan](../loans/vehicle-loan.md)
- [Gold Loan](../loans/gold-loan.md)
- [Business Loan](../loans/business-loan.md)
- [Loan Against Property](../loans/loan-against-property.md)
- [Loan Against Fixed Deposit](../loans/loan-against-fd.md)

---

*Effective from: <!-- BANK-SPECIFIC: Date --> | Last updated: 2026-08-08*
