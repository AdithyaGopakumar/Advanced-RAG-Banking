---
id: "PAY-IMPS-001"
title: "IMPS"
slug: "imps"
domain: "services"
category: "payments"
sub_category: "imps"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["internet-banking", "mobile-banking", "atm"]
language: "en"
region: "IN"
keywords: ["IMPS", "immediate payment service", "instant transfer", "24x7 transfer", "real time transfer"]
tags: ["channel:internet-banking", "channel:mobile-banking", "process:fund-transfer"]
search_aliases: ["immediate payment service", "instant bank transfer", "IMPS transfer"]
priority: "high"
related_documents: ["PAY-NEFT-001", "PAY-RTGS-001", "DIGI-UPI-001", "CHG-PAY-001", "FAQ-PAY-001", "GUIDE-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["NPCI IMPS Procedural Guidelines"]
confidentiality: "public"
dynamic_content: false
---

# IMPS

## Overview

Immediate Payment Service (IMPS) is an instant, interbank electronic fund transfer system managed by the National Payments Corporation of India (NPCI). It offers a robust, real-time platform for transferring funds up to ₹5,00,000 using mobile phones, internet banking, or ATMs.

---

## Features

- **Instant Credit:** Funds are credited to the beneficiary's account within seconds.
- **24x7x365 Availability:** Operates round the clock, including Sundays and public holidays.
- **Multiple Identifiers:** Funds can be sent using traditional Account+IFSC or via Mobile Number+MMID (Mobile Money Identifier).

---

## How It Works (Transaction Flow)

1. **Initiation:** Remitter initiates the transfer via the bank's digital channels.
2. **Authorization:** The remitter authenticates using MPIN or TPIN.
3. **Routing:** The remitter's bank sends the transaction to the NPCI switch.
4. **Validation:** NPCI forwards the request to the beneficiary bank.
5. **Credit & Settlement:** The beneficiary bank instantly credits the account and sends a success response back through NPCI to the remitter's bank. (Actual net settlement between the banks happens in deferred cycles).
6. **Notification:** Both sender and receiver receive instant SMS alerts.

---

## Required Information

To initiate an IMPS transfer, the remitter can use one of two methods:
1. **P2A (Person to Account):** Beneficiary Account Number + IFSC.
2. **P2P (Person to Person):** Beneficiary Mobile Number + MMID (a 7-digit code provided by the bank).

---

## Transaction Limits

- **Maximum Limit:** The maximum limit per IMPS transaction is **₹5,00,000** (mandated by NPCI).
- **Default Daily Limit:** The bank imposes a daily cumulative digital limit of <!-- BANK-SPECIFIC: ₹10,00,000 --> across all IMPS transfers.
- **SMS/USSD Limits:** Transfers initiated via basic SMS or USSD (*99#) have a lower limit of ₹5,000 per transaction.

---

## Charges

- Inward IMPS is **Free of Charge**.
- Outward IMPS charges depend on the transfer amount and the customer's account variant (e.g., Salary and Premium accounts usually enjoy free IMPS).
- See [Payment Charges](../charges/payment-charges.md) for the exact fee slabs.

---

## Failed and Pending Transactions

Because IMPS requires instantaneous handshakes across multiple networks, intermittent failures can occur:
- **Failed:** If the beneficiary details are invalid, the transaction fails instantly and no money is deducted.
- **Pending (Timeout):** If the remitter's bank does not receive a response from the beneficiary bank within the timeout window, the status becomes "Pending". 
- **Reconciliation:** According to NPCI guidelines, pending IMPS transactions are reconciled by the banks internally. The remitter's account is usually credited back (reversed) within `T+1` business days if the beneficiary was not credited.

---

## Related Documents
- [NEFT](neft.md)
- [RTGS](rtgs.md)
- [UPI Mechanism](upi-rail.md)
- [Payment Troubleshooting](payment-troubleshooting.md)
- [Payment Charges](../charges/payment-charges.md)
- [Payments FAQ](../../faqs/payments-faq.md)

---
