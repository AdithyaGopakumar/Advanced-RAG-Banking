---
id: "DIGI-QR-001"
title: "QR Payments"
slug: "qr-payments"
domain: "services"
category: "digital-banking"
sub_category: "qr-payments"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["mobile-banking", "upi"]
language: "en"
region: "IN"
keywords: ["QR payment", "scan and pay", "QR code", "merchant QR", "Bharat QR"]
tags: ["channel:upi", "channel:mobile-banking", "process:fund-transfer"]
search_aliases: ["scan to pay", "QR code payment", "Bharat QR", "scan and pay"]
priority: "medium"
related_documents: ["DIGI-UPI-001", "DIGI-MB-001", "FAQ-DIGI-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Digital Banking SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: false
---

# QR Payments

## Overview

QR (Quick Response) Payments allow customers to pay merchants instantly by scanning a physical or digital barcode using their Mobile Banking or UPI app. It eliminates the need to carry physical cards or enter long merchant details (like account numbers or IFSC codes).

---

## How It Works

The QR code contains embedded merchant information (UPI ID, Merchant Category Code, and sometimes the transaction amount). When the customer scans the code, the banking app decodes this information and initiates a secure pull/push request over the UPI or BharatQR payment network.

*Note: See [Payments Domain](../payments/README.md) for network-level mechanics.*

---

## How to Use

1. **Open the App:** Launch the bank's Mobile Banking app or any linked UPI app.
2. **Select Scan:** Tap the **Scan & Pay** or **Scan QR** button on the home screen.
3. **Scan Code:** Point your smartphone camera at the merchant's QR code (BharatQR or standard UPI QR). Alternatively, select a saved QR image from your phone's gallery.
4. **Enter Amount:** If the QR is static (does not contain an embedded amount), enter the bill amount. If dynamic, the amount will be pre-filled.
5. **Authenticate:** Authorize the payment using your UPI PIN (for UPI apps) or MPIN/TPIN (for direct Mobile Banking transactions).
6. **Confirmation:** Both you and the merchant will receive instant success notifications.

---

## Transaction Limits

- **Standard Limit:** Up to <!-- BANK-SPECIFIC: ₹1,00,000 --> per day (as per standard UPI guidelines).
- **Merchant Specific:** Specific categories (e.g., small roadside vendors) may have lower per-transaction caps enforced by the network to prevent fraud.

---

## Security Features

- **No Credential Sharing:** The merchant never sees your bank account number, card details, or mobile number.
- **Dynamic QR Verification:** The app verifies the authenticity of the merchant before prompting for a PIN. If the QR code is malformed or blacklisted, the app will block the transaction.
- **PIN Protection:** All payments require your secure PIN; scanning a QR code alone cannot deduct money from your account.

---

## Related Documents
- [UPI](upi.md)
- [Mobile Banking](mobile-banking.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
