---
id: "DIGI-MB-001"
title: "Mobile Banking"
slug: "mobile-banking"
domain: "services"
category: "digital-banking"
sub_category: "mobile-banking"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["mobile-banking"]
language: "en"
region: "IN"
keywords: ["mobile banking", "banking app", "mobile app", "phone banking app", "bank app"]
tags: ["channel:mobile-banking", "process:fund-transfer", "process:statement-request", "security:online-security"]
search_aliases: ["bank app", "mobile app", "phone banking", "app banking"]
priority: "high"
related_documents: ["DIGI-IB-001", "DIGI-UPI-001", "DIGI-MB-TS-001", "FAQ-DIGI-001", "SEC-GUIDE-001"]
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

# Mobile Banking

## Overview

Mobile Banking is a secure, smartphone-based application that allows customers to access their accounts, perform transactions, and manage banking services 24/7 on the go. It acts as a comprehensive digital branch in the customer's pocket.

---

## Features

- **Account Management:** View balances, download statements, and track linked deposits or loans.
- **Fund Transfers:** Instant transfers via NEFT, RTGS, IMPS, and UPI.
- **Bill Payments & Recharge:** Pay utility bills, credit card bills, and recharge mobile/DTH connections.
- **Card Controls:** Block/unblock cards, set transaction limits, generate PINs, and apply for new cards.
- **Service Requests:** Request cheque books, update email ID, and manage nominees.
- **Investments:** Open Fixed/Recurring Deposits or apply for instant loans.

---

## Eligibility and Prerequisites

- **Eligibility:** Available to all active Savings and Current Account holders (individual or sole proprietor).
- **Prerequisites:**
  - A smartphone running a supported OS version (iOS <!-- BANK-SPECIFIC: 14+ --> or Android <!-- BANK-SPECIFIC: 9+ -->).
  - The mobile number registered with the bank must be active on the device (for SIM binding).
  - An active Debit Card or Internet Banking credentials (for initial registration).

---

## Registration and Setup

1. **Download App:** Download the official banking app from the Apple App Store or Google Play Store.
2. **SIM Binding:** Open the app and allow it to send a verification SMS from the registered mobile number to securely bind the device.
3. **Authentication:** Enter Debit Card details (Card Number, Expiry, ATM PIN) OR Internet Banking credentials to verify identity.
4. **Set MPIN:** Create a secure 4 or 6-digit MPIN for future logins.
5. **Biometric Setup:** (Optional) Enable Face ID or Fingerprint login for faster access.

---

## Authentication and Security

- **Login:** Handled via MPIN or Biometrics.
- **Transaction Authentication:** Financial transactions require an OTP sent to the registered mobile number or a separate Transaction PIN (TPIN).
- **Device Binding:** The app is cryptographically bound to the physical device. If the customer changes their phone, they must repeat the Registration process.
- **Auto-Logout:** The app automatically logs out after a brief period of inactivity.

---

## Supported Operations

### Fund Transfers
Initiate transfers to saved beneficiaries or make quick transfers without adding a beneficiary (subject to lower limits). 
- *See [Payments Domain](../payments/README.md) for rail details.*

### Bill Payments
Access the Bharat Bill Payment System (BBPS) to fetch and pay utility bills. Set up AutoPay for recurring bills.

### Account Management
Manage all relationships (Savings, Current, FD, RD, Loans, Cards) from a single consolidated dashboard.

---

## Transaction Limits

Limits are set to balance convenience and security. Customers can reduce these limits within the app settings.

- **Daily Transfer Limit:** Up to <!-- BANK-SPECIFIC: ₹10,00,000 --> (combined across IMPS/NEFT/RTGS).
- **Quick Transfer (Without Beneficiary):** Up to <!-- BANK-SPECIFIC: ₹50,000 --> per day.
- **New Beneficiary Cooling Period:** Transfers to newly added beneficiaries are restricted to <!-- BANK-SPECIFIC: ₹50,000 --> for the first <!-- BANK-SPECIFIC: 24 hours -->.

*Note: UPI limits are separate and governed by NPCI guidelines.*

---

## Fees and Charges

- The Mobile Banking app is free to download and use.
- Standard charges apply for IMPS/NEFT transfers, SMS alerts, or specific bill payments.
- See [Account Charges](../charges/account-charges.md) and [Service Charges](../charges/service-charges.md).

---

## Troubleshooting

For login issues, device changes, MPIN resets, and transaction failures, please refer to the dedicated troubleshooting guide:
**[Mobile Banking Troubleshooting](mobile-banking-troubleshooting.md)**

---

## Related Documents
- [Internet Banking](internet-banking.md)
- [UPI](upi.md)
- [Mobile Banking Troubleshooting](mobile-banking-troubleshooting.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)
- [Security Guidelines](../security/security-guidelines.md)

---
