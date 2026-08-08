---
id: "PAY-SWIFT-001"
title: "SWIFT Transfer"
slug: "swift"
domain: "services"
category: "payments"
sub_category: "swift"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["branch", "internet-banking"]
language: "en"
region: "IN"
keywords: ["SWIFT", "international transfer", "foreign remittance", "wire transfer", "overseas transfer"]
tags: ["channel:branch", "channel:internet-banking", "process:fund-transfer", "compliance:fema"]
search_aliases: ["wire transfer", "international money transfer", "foreign transfer", "overseas remittance"]
priority: "medium"
related_documents: ["PAY-NEFT-001", "CHG-PAY-001", "FAQ-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["FEMA Regulations on Foreign Remittance", "RBI Liberalised Remittance Scheme"]
confidentiality: "public"
dynamic_content: false
---

# SWIFT Transfer (International Remittance)

## Overview

A SWIFT (Society for Worldwide Interbank Financial Telecommunication) transfer is the global standard for international wire transfers. It is used to securely transmit funds and messaging between banks across borders. 

In India, outward international remittances for resident individuals are heavily regulated under the **Liberalised Remittance Scheme (LRS)** administered by the Reserve Bank of India (RBI) and the Foreign Exchange Management Act (FEMA).

---

## Transaction Flow

1. **Initiation:** The customer initiates an outward remittance via the branch or Internet Banking, providing the beneficiary's details, IBAN/Account Number, and the receiving bank's SWIFT/BIC code.
2. **Purpose Declaration:** The customer must declare the specific "Purpose Code" (e.g., S0305 for Travel, S1301 for Family Maintenance).
3. **FX Conversion:** The bank converts INR to the destination currency based on the prevailing Foreign Exchange (FX) rate.
4. **Routing:** The bank sends a SWIFT message (usually MT103). If there is no direct relationship between the remitting and receiving banks, the funds are routed through an Intermediary (Correspondent) Bank.
5. **Credit:** The receiving bank credits the beneficiary's account.

---

## LRS Limits (Regulatory Requirements)

Under the RBI's Liberalised Remittance Scheme:
- **Maximum Limit:** Resident individuals can freely remit up to **USD 250,000** (or its equivalent in other currencies) per financial year (April to March) for permissible current or capital account transactions.
- **TCS (Tax Collected at Source):** A TCS is applicable on remittances exceeding certain thresholds (e.g., above ₹7 Lakhs) depending on the purpose of remittance (education, travel, etc.). 
- *Note: Limits and TCS rates are defined by the government and are subject to change in the annual Union Budget.*

---

## Beneficiary Requirements

To send a SWIFT transfer, you need:
- Beneficiary Name and Address
- Beneficiary Account Number or IBAN (International Bank Account Number)
- Receiving Bank's SWIFT / BIC Code
- Receiving Bank's Name and Address
- Sort Code / Routing Number (varies by destination country, e.g., ABA Routing Number for the US, BSB for Australia)

---

## Charges and Fees

International transfers involve multiple fee layers:
1. **Remitter Bank Commission:** A flat or percentage-based fee charged by the originating bank.
2. **FX Markup:** A margin applied to the currency conversion rate.
3. **Correspondent/Intermediary Bank Charges:** If an intermediary bank is used, they may deduct a fee from the principal amount before it reaches the beneficiary (unless the remitter opts to bear all charges via the `OUR` billing code).
4. **TCS:** Withheld tax (which can be claimed back during income tax filing, if applicable).

*Refer to the [Payment Charges](../charges/payment-charges.md) and Forex branch desk for current fees and real-time exchange rates.*

---

## Timings and Settlement

- SWIFT transfers are not real-time.
- **Credit Timeline:** Funds typically reach the beneficiary within `T+2` to `T+5` working days, depending on the destination country, time zone differences, and the number of intermediary banks involved.
- **Compliance Hold:** Transactions may be delayed if they are flagged by international Anti-Money Laundering (AML) filters for manual review.

---

## Related Documents
- [NEFT](neft.md)
- [Payment Charges](../charges/payment-charges.md)
- [Payments FAQ](../../faqs/payments-faq.md)

---
