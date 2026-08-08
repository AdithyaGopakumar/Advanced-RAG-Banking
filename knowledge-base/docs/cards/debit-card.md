---
id: "CARD-DC-001"
title: "Debit Card"
slug: "debit-card"
domain: "products"
category: "cards"
sub_category: "debit-card"
document_type: "product"
applicable_to: "individual"
target_audience: "both"
applicable_channels: ["branch", "internet-banking", "mobile-banking", "atm"]
language: "en"
region: "IN"
keywords: ["debit card", "ATM card", "shopping card", "online payment", "contactless payment", "PIN"]
tags: ["product:debit-card", "segment:retail", "channel:all", "process:card-application", "feature:limits"]
search_aliases: ["ATM card", "bank card", "shopping card", "rupay debit card"]
priority: "high"
related_documents: ["CARD-CC-001", "CHG-CARD-001", "FORM-CARD-001", "FAQ-CARD-001", "GUIDE-CARD-001", "SEC-CARD-001", "SCEN-CARD-001"]
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

# Debit Card

## Overview

A Debit Card is a payment card linked directly to a customer's Savings or Current Account. It allows customers to access their own funds for cash withdrawals at ATMs and cashless purchases at merchant outlets or online. Unlike a credit card, transactions are immediately deducted from the linked account balance.

---

## Features and Benefits

### Usage Channels
Debit cards provide 24/7 access to account funds through:
- **ATMs:** Cash withdrawals, balance inquiries, and PIN changes.
- **Point of Sale (POS):** Swiping or inserting the chip at retail stores.
- **Online (E-commerce):** Secure online shopping authenticated via OTP.
- **Contactless (Tap-to-Pay):** Fast checkout for transactions up to <!-- BANK-SPECIFIC: ₹5000 --> without requiring a PIN (NFC enabled).

### International Usage
Premium and Platinum debit cards can be enabled for international usage, allowing ATM withdrawals and POS transactions abroad (subject to forex markup charges).

### Value-Added Benefits
Depending on the variant, debit cards may offer:
- Complimentary airport lounge access.
- Reward points on specific merchant categories.
- Personal accident or purchase protection insurance cover.

---

## Eligibility

Debit cards are issued to customers holding an active banking relationship.

| Account Type | Eligibility |
|---|---|
| Savings Account | Issued to primary and joint account holders (Operating instructions must allow card issuance). |
| Current Account | Issued to Proprietors or authorized signatories. |
| Minors | Issued for specific minor accounts (e.g., above 10 years of age) with restricted limits. |

*Note: Fully compliant KYC is mandatory for debit card issuance.*

---

## Transaction Limits

Debit card limits are set to protect customer funds and manage risk.
- **Daily ATM Withdrawal Limit:** Ranges from <!-- BANK-SPECIFIC: ₹25,000 to ₹1,00,000 --> based on the card variant.
- **Daily POS/Online Limit:** Ranges from <!-- BANK-SPECIFIC: ₹50,000 to ₹5,00,000 -->.
- **Limit Customization:** Customers can reduce these limits or disable specific channels (e.g., online, international) via Mobile Banking to enhance security.

---

## Fees and Charges

Debit cards typically attract an Annual Maintenance Charge (AMC) and fees for transactions beyond the free limit.
Please refer to the [Card Charges](../charges/card-charges.md) schedule for detailed pricing.

---

## Security Features

- **EMV Chip & PIN:** Ensures secure physical transactions.
- **Tokenization:** Supports secure mobile wallet additions (Apple Pay, Google Pay).
- **Transaction Alerts:** SMS and email alerts are sent instantly for every transaction.
- **Instant Controls:** Customers can permanently block or temporarily freeze their debit card via the banking app.

---

## PIN Generation and Management

A Personal Identification Number (PIN) is required for ATM and POS transactions.
- **Green PIN (Paperless):** Customers can generate or reset their PIN instantly using Mobile Banking, Internet Banking, or at the bank's ATM.
- For security reasons, the bank will never call or email asking for the card PIN.

---

## Lost or Stolen Card and Replacement

If a debit card is lost, stolen, or compromised, the customer must act immediately:
1. **Block the Card:** Use the Mobile App, Internet Banking, or call the 24/7 toll-free number to hotlist the card.
2. **Request Replacement:** A replacement card can be requested digitally or at the branch.
3. **Card Dispatch:** The new card is delivered to the registered communication address within <!-- BANK-SPECIFIC: 7 working days -->.
4. **Unauthorized Transactions:** Must be reported immediately to avail zero liability protection under RBI guidelines.

---

## Transaction Problems and Disputes

- **ATM Cash Not Dispensed:** If an account is debited but cash is not dispensed, the bank usually auto-reverses the transaction within <!-- BANK-SPECIFIC: T+5 days -->. If not, the customer must log a formal dispute.
- **POS/Online Failures:** If a transaction fails but funds are deducted, the auto-reversal timeline is similar.
- **Chargebacks:** For unauthorized merchant charges or goods not received, chargebacks must be raised within <!-- BANK-SPECIFIC: 30 days -->.

---

## How to Apply

- **New Accounts:** A debit card is automatically issued as part of the Welcome Kit during account opening.
- **Existing Accounts:** Customers can request a new or upgraded debit card via Internet Banking or by submitting a request at the home branch.

---

## Related Documents
- [Credit Card](credit-card.md)
- [Card Charges](../charges/card-charges.md)
- [Card Application Documents](../forms/card-application-documents.md)
- [Savings Account](../accounts/savings-account.md)

---
