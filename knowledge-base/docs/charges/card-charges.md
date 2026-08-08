---
id: "CHG-CARD-001"
title: "Card Charges"
slug: "card-charges"
domain: "reference-data"
category: "charges"
sub_category: "card-charges"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["card charges", "annual fee", "late payment fee", "cash advance fee", "card renewal"]
tags: ["reference:charges", "product:credit-card", "product:debit-card"]
search_aliases: ["credit card fees", "debit card charges", "card annual fee"]
priority: "high"
related_documents: ["CARD-CC-001", "CARD-DC-001"]
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

# Card Charges

This document serves as the Single Source of Truth (SSOT) for all fees and charges related to Debit, Credit, Prepaid, Virtual, and Forex cards.

## 1. Credit Card Fees

| Charge Type | Amount / Details |
|---|---|
| Joining Fee | <!-- BANK-SPECIFIC: ₹500 to ₹10,000 --> (Depends on card variant). |
| Annual Fee | <!-- BANK-SPECIFIC: ₹500 to ₹10,000 --> (May be waived upon reaching spend milestones). |
| Add-on Card Fee | <!-- BANK-SPECIFIC: Nil for first 2 cards, ₹500 thereafter -->. |
| Cash Advance Fee | <!-- BANK-SPECIFIC: 2.5% of withdrawal amount (Min ₹500) -->. |
| Foreign Currency Markup | <!-- BANK-SPECIFIC: 1.5% to 3.5% --> of the transaction value. |
| Late Payment Fee | <!-- BANK-SPECIFIC: ₹100 to ₹1,300 --> depending on the Total Amount Due. |
| Over-limit Fee | <!-- BANK-SPECIFIC: 2.5% of the over-limit amount (Min ₹500) -->. |
| Reward Redemption Fee | <!-- BANK-SPECIFIC: ₹99 per redemption request -->. |
| EMI Processing Fee | <!-- BANK-SPECIFIC: 1% of the transaction amount (Min ₹99) -->. |
| Card Replacement Fee | <!-- BANK-SPECIFIC: ₹100 --> (Waived for premium cards). |

## 2. Debit Card Fees

| Charge Type | Amount / Details |
|---|---|
| Issuance Fee | <!-- BANK-SPECIFIC: ₹150 to ₹1,000 --> (Depends on variant). |
| Annual Maintenance Charge (AMC) | <!-- BANK-SPECIFIC: ₹150 to ₹1,000 -->. |
| ATM Withdrawal beyond free limits | <!-- BANK-SPECIFIC: ₹21 per transaction --> (Financial); <!-- BANK-SPECIFIC: ₹11 per transaction --> (Non-financial). |
| International ATM Withdrawal | <!-- BANK-SPECIFIC: ₹125 per transaction --> + Forex Markup of <!-- BANK-SPECIFIC: 3.5% -->. |
| Card Replacement Fee | <!-- BANK-SPECIFIC: ₹200 -->. |
| PIN Regeneration (Physical) | <!-- BANK-SPECIFIC: ₹50 --> (Digital PIN regeneration is free). |

## 3. Forex and Prepaid Card Fees

| Charge Type | Amount / Details |
|---|---|
| Issuance Fee | <!-- BANK-SPECIFIC: ₹300 -->. |
| Reload Fee | <!-- BANK-SPECIFIC: ₹75 per reload --> (Branch); Free via Internet Banking. |
| Cross-currency Markup | <!-- BANK-SPECIFIC: 3.5% --> (Applicable if used in a currency not loaded on the card). |
| Cash Withdrawal (International ATM) | <!-- BANK-SPECIFIC: USD 2 or equivalent --> per withdrawal. |
| Inactivity Fee | <!-- BANK-SPECIFIC: $5 per month --> (Applicable after 12 months of inactivity). |

## 4. Virtual Card Fees

Virtual debit and credit cards generated via Mobile/Internet Banking are generally issued **Free of Charge** with zero annual maintenance fees. Standard transaction charges apply based on the underlying account/card.

---

> [!NOTE] 
> All charges mentioned above are exclusive of applicable GST (currently 18%). Fees are subject to periodic review by the bank.

---

## Related Documents
- [Credit Card](../cards/credit-card.md)
- [Debit Card](../cards/debit-card.md)
- [Card Interest Rates](../interest-rates/card-interest-rates.md)

---

*Effective from: <!-- BANK-SPECIFIC: 01-Jan-2026 --> | Last updated: 2026-08-08*
