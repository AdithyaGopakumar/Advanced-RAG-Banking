---
id: "RATE-LOAN-001"
title: "Loan Interest Rates"
slug: "loan-interest-rates"
domain: "reference-data"
category: "interest-rates"
sub_category: "loan-interest-rates"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["loan interest rate", "home loan rate", "personal loan rate", "EBLR", "MCLR"]
tags: ["reference:interest-rates", "product:home-loan", "product:personal-loan"]
search_aliases: ["loan rates", "home loan EMI rate", "current loan rate", "EBLR rate"]
priority: "critical"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
effective_from: "2026-08-01"
effective_until: ""
source: "ALCO Circular 2026-08"
authority: "ALCO"
owner: "Finance SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
dynamic_classification: "PERIODICALLY_DYNAMIC"
data_source: "interest-rate-api"
---

# Loan Interest Rates

## Overview

> [!WARNING]
> Rates are subject to change. According to the bank's current published tariff, the following information applies. Always refer to the current rate schedule or live API for real-time information.

This document serves as the Single Source of Truth (SSOT) for all retail loan interest rates. It outlines the current reference rates (EBLR/Repo) and the applicable spread for each loan product. All product-specific documentation must link to this document for pricing information.

---

## Rate Table

> [!NOTE]
> All floating rates are linked to the External Benchmark Lending Rate (EBLR), which is currently pegged to the RBI Repo Rate.

| Loan Product | Rate Type | Base Rate (EBLR) | Applicable Spread | Final Interest Rate (p.a.) |
|---|---|---|---|---|
| Home Loan | Floating | <!-- BANK-SPECIFIC: Repo Rate --> | <!-- BANK-SPECIFIC: Spread % --> | <!-- BANK-SPECIFIC: Final % --> |
| Personal Loan | Fixed | N/A | N/A | <!-- BANK-SPECIFIC: Fixed % --> |
| Education Loan | Floating | <!-- BANK-SPECIFIC: Repo Rate --> | <!-- BANK-SPECIFIC: Spread % --> | <!-- BANK-SPECIFIC: Final % --> |
| Vehicle Loan | Fixed/Floating | <!-- BANK-SPECIFIC: Repo Rate --> | <!-- BANK-SPECIFIC: Spread % --> | <!-- BANK-SPECIFIC: Final % --> |
| Gold Loan | Fixed | N/A | N/A | <!-- BANK-SPECIFIC: Fixed % --> |
| Loan Against Property | Floating | <!-- BANK-SPECIFIC: Repo Rate --> | <!-- BANK-SPECIFIC: Spread % --> | <!-- BANK-SPECIFIC: Final % --> |
| Loan Against FD | Fixed | N/A | N/A | FD Rate + <!-- BANK-SPECIFIC: Spread % --> |

---

## Concessional Rates

| Category | Applicable Concession |
|---|---|
| Female Co-applicant (Home Loan) | <!-- BANK-SPECIFIC: -0.05% --> |
| Bank Salary Account Holders | <!-- BANK-SPECIFIC: -0.25% --> |
| Priority Sector (Education Loan) | As per RBI guidelines |

---

## Rate Change History

Historical rate changes are managed by the internal treasury department and updated in the core banking system. The rates in this document reflect the currently effective EBLR.

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
