---
id: "CARD-VC-001"
title: "Virtual Card"
slug: "virtual-card"
domain: "products"
category: "cards"
sub_category: "virtual-card"
document_type: "product"
applicable_to: "individual"
target_audience: "both"
applicable_channels: ["internet-banking", "mobile-banking"]
language: "en"
region: "IN"
keywords: ["virtual card", "online shopping card", "temporary card", "digital card", "e-card"]
tags: ["product:debit-card", "segment:retail", "channel:internet-banking", "channel:mobile-banking", "security:online-security"]
search_aliases: ["digital card", "e-card", "online card", "temporary card number"]
priority: "medium"
related_documents: ["CARD-DC-001", "CARD-CC-001", "CHG-CARD-001", "FAQ-CARD-001", "SEC-CARD-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Cards SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: false
---

# Virtual Card

## Overview

A Virtual Card is a digital-only representation of a debit or credit card. It exists purely within the Mobile Banking or Internet Banking app and has no physical plastic form. It provides an instant, highly secure way to make online and in-app payments.

---

## Features and Benefits

- **Instant Issuance:** Generated immediately upon request; no waiting for postal delivery.
- **Enhanced Security:** Perfect for online shopping. Customers can generate disposable or single-use virtual cards to protect their primary account details.
- **E-commerce Ready:** Supports all standard online transactions requiring a 16-digit card number, Expiry Date, and CVV.
- **Wallet Integration:** Easily provisioned into digital wallets like Apple Pay or Google Pay for contactless NFC payments at physical POS terminals.
- **Zero Physical Risk:** Cannot be lost or stolen in the physical sense.

---

## How to Generate

1. Log in to Mobile Banking or Internet Banking.
2. Navigate to the **Cards** section and select **Generate Virtual Card**.
3. Choose the funding source (Savings/Current account or an existing Credit Card limit).
4. Set the card limits and validity.
5. The 16-digit card number, CVV, and expiry date are instantly displayed on screen.

---

## Transaction Limits

- **Maximum Limit:** The user can define the maximum limit for the virtual card at the time of creation (up to the available balance in the linked account or credit limit).
- **Usage Scope:** Exclusively for Online (E-commerce) transactions and mobile wallet tokenization. Not valid for ATM withdrawals.

---

## Validity and Expiry

- **Single-Use Cards:** Automatically expire immediately after the first successful transaction.
- **Multi-Use Virtual Cards:** Can be set to expire after a specific duration (e.g., 24 hours, 30 days, or up to 5 years).
- **Manual Deactivation:** Customers can instantly delete or deactivate a virtual card at any time via the app.

---

## Fees and Charges

Virtual Cards are generally issued completely **free of charge** and carry no issuance or annual maintenance fees. Standard transaction fees apply to the underlying funding account.
See [Card Charges](../charges/card-charges.md).

---

## Security Features

- **Dynamic CVV:** Some virtual cards offer a dynamic CVV that changes every few minutes for added security.
- **OTP Authentication:** All domestic online transactions require standard OTP authentication.
- **Isolation:** If the virtual card details are compromised on a merchant site, the customer's primary physical card and core bank account remain entirely safe.

---

## Related Documents
- [Debit Card](debit-card.md)
- [Credit Card](credit-card.md)
- [Card Charges](../charges/card-charges.md)

---
