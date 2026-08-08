---
id: "DIGI-UPI-001"
title: "UPI"
slug: "upi"
domain: "services"
category: "digital-banking"
sub_category: "upi"
document_type: "service"
applicable_to: "individual"
target_audience: "both"
applicable_channels: ["mobile-banking", "upi"]
language: "en"
region: "IN"
keywords: ["UPI", "unified payments interface", "UPI payment", "UPI transfer", "UPI PIN", "VPA"]
tags: ["channel:upi", "channel:mobile-banking", "process:fund-transfer", "security:otp"]
search_aliases: ["UPI payment", "BHIM UPI", "UPI transfer", "pay by UPI"]
priority: "high"
related_documents: ["DIGI-MB-001", "DIGI-QR-001", "DIGI-UPI-TS-001", "PAY-IMPS-001", "FAQ-DIGI-001", "CHG-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Digital Banking SME"
compliance_classification: "regulatory"
regulatory_references: ["NPCI UPI Procedural Guidelines"]
confidentiality: "public"
dynamic_content: false
---

# UPI

## Overview

Unified Payments Interface (UPI) is a real-time payment system developed by the National Payments Corporation of India (NPCI). It facilitates inter-bank peer-to-peer (P2P) and person-to-merchant (P2M) transactions instantly using a mobile device, without requiring the sharing of actual bank account details.

- *See [Payments Domain](../payments/README.md) for the underlying settlement mechanics.*

---

## Features

- **Instant Transfers:** Funds are transferred and credited in real-time, 24/7, 365 days a year.
- **Virtual Payment Address (VPA):** Users create a unique UPI ID (e.g., `mobilenumber@bankname`) to send and receive money.
- **Multiple Accounts:** Link multiple bank accounts from different banks within a single UPI app.
- **Collect Requests:** Request money from others using their UPI ID.
- **UPI AutoPay:** Set up recurring e-mandates for subscriptions and EMI payments.
- **UPI Lite:** An on-device wallet for pin-less, low-value transactions up to <!-- BANK-SPECIFIC: ₹500 -->.

---

## How to Register

1. Download the bank's official Mobile Banking app or any third-party UPI app (e.g., Google Pay, PhonePe, BHIM).
2. Verify your mobile number. (The number must be active on the device and linked to your bank account).
3. Select your bank from the list. The app will fetch your associated accounts via SMS binding.
4. Select the account you wish to link.
5. Create your Virtual Payment Address (UPI ID).

---

## UPI PIN Management

The UPI PIN is a 4 or 6-digit passcode required to authorize all outgoing financial transactions.

- **Creating a PIN:** You must verify your identity using the last 6 digits of your linked Debit Card and its Expiry Date (or via Aadhaar OTP, if supported).
- **Resetting a PIN:** Can be done securely within the UPI app using the Debit Card or Aadhaar method.
- **Important Security Rule:** A UPI PIN is **ONLY** required for sending money. It is never required to receive money.

---

## Supported Operations

### Send Money
You can send money using:
- The beneficiary's UPI ID (VPA).
- The beneficiary's mobile number (if registered on UPI).
- Traditional Account Number + IFSC.

### Receive Money
Share your UPI ID or Mobile Number to receive funds. You can also generate a QR code for the payer to scan.

### Pay Merchants
Scan any interoperable BharatQR or UPI QR code at retail outlets or enter the merchant's UPI ID. 
- *See [QR Payments](qr-payments.md).*

### Collect Requests
You can send a request for money to another UPI ID. The recipient receives a notification, reviews the request, and enters their UPI PIN to authorize the payment.

---

## Transaction Limits

Limits are governed by NPCI guidelines but banks may impose stricter caps.

- **Standard P2P Transfer Limit:** Up to <!-- BANK-SPECIFIC: ₹1,00,000 --> per day, per linked bank account.
- **Special Category Limit:** Up to <!-- BANK-SPECIFIC: ₹5,00,000 --> for specific merchant categories like Capital Markets, Collections, Insurance, Medical, and Education.
- **New User Limit:** For the first 24 hours after registering or resetting the UPI PIN, outgoing transactions are capped at <!-- BANK-SPECIFIC: ₹5,000 -->.

---

## Charges

- UPI transactions (P2P and standard P2M) are generally **Free of Charge** for retail customers.
- Refer to the canonical [Payment Charges](../charges/payment-charges.md) document for any specific limits on free transactions.

---

## Security Features

- **Device Binding:** Transactions can only be initiated from the device containing the registered SIM card.
- **PIN Authorization:** Every outgoing transaction is authenticated via the secure UPI PIN.
- **Fraud Warning:** Apps display prominent warnings when authorizing "Collect Requests" to prevent social engineering fraud.

---

## Troubleshooting

For pending transactions, declined payments, refunds, and dispute resolution via the UPI Help feature, refer to the dedicated troubleshooting guide:
**[UPI Troubleshooting](upi-troubleshooting.md)**

---

## Related Documents
- [Mobile Banking](mobile-banking.md)
- [QR Payments](qr-payments.md)
- [UPI Troubleshooting](upi-troubleshooting.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
