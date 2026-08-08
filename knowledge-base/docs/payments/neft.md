---
id: "PAY-NEFT-001"
title: "NEFT"
slug: "neft"
domain: "services"
category: "payments"
sub_category: "neft"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["branch", "internet-banking", "mobile-banking"]
language: "en"
region: "IN"
keywords: ["NEFT", "national electronic fund transfer", "fund transfer", "bank transfer", "interbank transfer"]
tags: ["channel:internet-banking", "channel:mobile-banking", "channel:branch", "process:fund-transfer"]
search_aliases: ["national electronic fund transfer", "NEFT transfer", "bank to bank transfer"]
priority: "high"
related_documents: ["PAY-RTGS-001", "PAY-IMPS-001", "CHG-PAY-001", "FAQ-PAY-001", "GUIDE-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["RBI NEFT Procedural Guidelines"]
confidentiality: "public"
dynamic_content: false
---

# NEFT

## Overview

National Electronic Funds Transfer (NEFT) is a nation-wide centralized payment system owned and operated by the Reserve Bank of India (RBI). It enables the electronic transfer of funds from any bank branch to any individual, firm, or corporate having an account with any other bank branch in the country participating in the Scheme.

---

## Features

- **Pan-India Coverage:** Can be used to send money to any NEFT-enabled bank in India.
- **No Minimum Limit:** Suitable for transferring small to medium amounts.
- **Batch Processing:** Transactions are not settled instantly; they are cleared in half-hourly batches.

---

## How It Works (Transaction Flow)

1. **Initiation:** The remitter (customer) initiates the transfer via Internet Banking, Mobile Banking, or by visiting a branch.
2. **Validation:** The remitter's bank verifies the account balance and debits the amount.
3. **Pooling:** The remitter's bank pools all NEFT requests and sends them to the NEFT Service Centre (operated by RBI).
4. **Clearing & Settlement:** RBI processes these requests in batches and settles the funds with the beneficiary's bank.
5. **Credit:** The beneficiary's bank receives the funds and credits the beneficiary's account.

---

## Required Information

To initiate an NEFT transfer, the remitter must provide:
- Beneficiary Name
- Beneficiary Account Number
- Beneficiary Bank Name
- Beneficiary Branch IFSC (Indian Financial System Code)
- Amount to be transferred

---

## Transaction Limits

- **Minimum Limit:** ₹1 (No minimum limit stipulated by RBI).
- **Maximum Limit:** No upper limit mandated by RBI for standard transfers. However, the bank imposes a default daily limit of <!-- BANK-SPECIFIC: ₹10,00,000 --> for retail digital channels to prevent fraud.
- **Cash Remittances:** For walk-in customers depositing cash at a branch, the maximum limit is ₹50,000 per transaction (as per RBI rules).

---

## Charges

- Inward NEFT (receiving money) is completely **Free of Charge**.
- Outward NEFT initiated via digital channels (Internet/Mobile Banking) for Savings Account holders is **Free of Charge** (as mandated by RBI).
- Outward NEFT initiated at a branch may attract nominal fees. See [Payment Charges](../charges/payment-charges.md) for details.

---

## Timings and Settlement

- **Availability:** NEFT operates 24x7, 365 days a year (including holidays and weekends).
- **Settlement Batches:** RBI operates NEFT in half-hourly batches starting from 00:30 hrs to 00:00 hrs.
- **Credit Timeline:** The beneficiary bank must credit the funds to the beneficiary's account within 2 business hours of receiving the batch settlement from RBI.

## Failed Transactions and Reversals

If a transaction fails at the beneficiary bank (e.g., due to an invalid account number):
- The beneficiary bank must return the funds to the originating bank on the same day or the next working day.
- **Reversal Timeline:** The originating bank will credit the remitter's account immediately upon receiving the return from RBI (typically `T+1` business day maximum).

---

## Related Documents
- [RTGS](rtgs.md)
- [IMPS](imps.md)
- [Payment Troubleshooting](payment-troubleshooting.md)
- [Payment Charges](../charges/payment-charges.md)
- [Payments FAQ](../../faqs/payments-faq.md)

---
