---
id: "PAY-RTGS-001"
title: "RTGS"
slug: "rtgs"
domain: "services"
category: "payments"
sub_category: "rtgs"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["branch", "internet-banking"]
language: "en"
region: "IN"
keywords: ["RTGS", "real time gross settlement", "high value transfer", "large fund transfer"]
tags: ["channel:internet-banking", "channel:branch", "process:fund-transfer"]
search_aliases: ["real time gross settlement", "RTGS transfer", "large amount transfer"]
priority: "high"
related_documents: ["PAY-NEFT-001", "PAY-IMPS-001", "CHG-PAY-001", "FAQ-PAY-001", "GUIDE-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["RBI RTGS System Regulations"]
confidentiality: "public"
dynamic_content: false
---

# RTGS

## Overview

Real-Time Gross Settlement (RTGS) is an electronic fund transfer system operated by the Reserve Bank of India (RBI). Unlike NEFT, which operates in batches, RTGS processes transactions continuously and settles them on a one-to-one, gross basis. It is primarily designed for high-value transactions that require immediate clearing.

---

## Features

- **Real-Time Settlement:** Funds are settled instantly at the RBI level.
- **Finality:** Once processed, RTGS payments are final and irrevocable.
- **High Value:** Exclusively used for transfers of ₹2,00,000 or more.

---

## How It Works (Transaction Flow)

1. **Initiation:** The remitter submits a transfer request via Internet Banking, Corporate Banking portals, or a physical branch.
2. **Validation:** The bank verifies the minimum amount (₹2 Lakhs) and account balance.
3. **Transmission:** The request is sent immediately to the RBI's RTGS system.
4. **Settlement:** RBI debits the remitter bank's settlement account and credits the beneficiary bank's account instantly.
5. **Credit:** The beneficiary bank receives the RTGS message and credits the beneficiary's account.

---

## Required Information

To initiate an RTGS transfer, the remitter must provide:
- Beneficiary Name
- Beneficiary Account Number
- Beneficiary Bank Name
- Beneficiary Branch IFSC
- Amount to be transferred (must be ≥ ₹2,00,000)

---

## Transaction Limits

- **Minimum Limit:** ₹2,00,000 (Mandated by RBI). The system will automatically reject any RTGS request below this amount.
- **Maximum Limit:** No upper limit mandated by RBI. However, the bank imposes a default daily digital limit of <!-- BANK-SPECIFIC: ₹25,00,000 --> for retail customers. Corporate accounts have customizable limits.

---

## Charges

- Inward RTGS (receiving money) is completely **Free of Charge**.
- Outward RTGS initiated via digital channels for Savings Accounts is **Free of Charge** (as mandated by RBI).
- Outward RTGS initiated at a branch is chargeable based on the time of transaction and amount. See [Payment Charges](../charges/payment-charges.md) for details.

---

## Timings and Settlement

- **Availability:** RTGS operates 24x7, 365 days a year.
- **Credit Timeline:** The beneficiary bank is expected to credit the beneficiary's account within 30 minutes of receiving the funds transfer message from RBI.

## Failed Transactions and Reversals

If the funds cannot be credited to the beneficiary (e.g., account frozen or invalid account number):
- The beneficiary bank must return the funds to the originating bank within **1 hour** or before the end of the RTGS business day, whichever is earlier.
- Once returned by the beneficiary bank, the remitter's account is credited immediately.

---

## Related Documents
- [NEFT](neft.md)
- [IMPS](imps.md)
- [Payment Troubleshooting](payment-troubleshooting.md)
- [Payment Charges](../charges/payment-charges.md)
- [Payments FAQ](../../faqs/payments-faq.md)

---
