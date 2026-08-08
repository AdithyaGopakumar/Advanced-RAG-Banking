---
id: "DIGI-IB-001"
title: "Internet Banking"
slug: "internet-banking"
domain: "services"
category: "digital-banking"
sub_category: "internet-banking"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["internet-banking"]
language: "en"
region: "IN"
keywords: ["internet banking", "net banking", "online banking", "web banking", "bank login"]
tags: ["channel:internet-banking", "process:fund-transfer", "process:statement-request", "security:online-security"]
search_aliases: ["net banking", "online banking", "web banking", "e-banking"]
priority: "high"
related_documents: ["DIGI-MB-001", "DIGI-IB-TS-001", "FAQ-DIGI-001", "SEC-GUIDE-001", "SCEN-DIGI-001"]
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

# Internet Banking

## Overview

Internet Banking (or Net Banking) is a secure web-based portal that allows customers to manage their accounts, conduct complex financial transactions, and request banking services from any internet-connected computer. It is optimized for comprehensive account management and bulk transactions.

---

## Features

- **Comprehensive Dashboard:** View all linked accounts, cards, loans, and deposits in a single unified view.
- **Advanced Fund Transfers:** Support for NEFT, RTGS, and IMPS, including bulk uploads for corporate/business accounts.
- **Beneficiary Management:** Add, modify, and delete payees securely.
- **Tax and Utility Payments:** Direct integration with income tax portals and the Bharat Bill Payment System (BBPS).
- **Extensive Service Requests:** Request cheque books, block/replace cards, update address/email, and manage standing instructions.

---

## Eligibility and Prerequisites

- **Eligibility:** Available to all Savings, Current, and Corporate account holders.
- **Prerequisites:**
  - An active Customer ID (CIF).
  - The registered mobile number must be active to receive OTPs for 2FA.
  - A secure web browser.

---

## Registration and Setup

1. **Visit the Portal:** Go to the official bank website and click on "Net Banking Login", then select "Register for New User".
2. **Online Registration:**
   - Enter your Customer ID and Registered Mobile Number.
   - Enter the OTP received on your mobile.
   - Verify identity using an active Debit Card (Card Number, Expiry, ATM PIN).
3. **Branch Registration:** Alternatively, customers without a debit card can submit a physical form at the branch to receive a physical PIN mailer.
4. **Set Passwords:**
   - Create a strong **Login Password** (for accessing the dashboard).
   - Create a distinct **Transaction Password** (required for initiating financial transfers).

---

## Supported Operations

### Fund Transfers
Initiate secure NEFT, RTGS, or IMPS transfers.
1. Navigate to **Transfers** > **Send to Saved Beneficiary**.
2. Select the payee and enter the amount.
3. Authenticate the transaction using your Transaction Password and the OTP sent to your mobile.
- *See [Payments Domain](../payments/README.md) for detailed rail mechanics.*

### Beneficiary Management
To add a new payee:
1. Navigate to **Manage Payees** > **Add New**.
2. Enter the payee's Account Number, IFSC, and Name.
3. Authenticate with OTP.
4. **Cooling Period:** A standard cooling period of <!-- BANK-SPECIFIC: 30 minutes --> applies before the beneficiary is activated. During the first <!-- BANK-SPECIFIC: 24 hours -->, transfers to this new beneficiary are capped at a security limit (e.g., <!-- BANK-SPECIFIC: ₹50,000 -->).

---

## Transaction Limits

Internet Banking offers the highest transaction limits among all digital channels.

- **Daily Overall Limit:** Up to <!-- BANK-SPECIFIC: ₹25,00,000 --> per day for retail customers (customizable).
- **RTGS Minimum:** ₹2,00,000 per transaction (as per RBI guidelines).
- **IMPS Maximum:** <!-- BANK-SPECIFIC: ₹5,00,000 --> per transaction.

---

## Authentication and Security Features

- **Two-Factor Authentication (2FA):** All logins require a password and an OTP (or Captcha). All financial transactions require a Transaction Password + OTP.
- **Virtual Keyboard:** Protects against keyloggers when entering passwords.
- **Security Questions:** Used for password resets or unusual login attempts.
- **Last Login Stamp:** The dashboard displays the date, time, and IP address of the last successful login.
- **Auto-Logout:** The session expires automatically after <!-- BANK-SPECIFIC: 5 minutes --> of inactivity.

---

## Fees and Charges

- Internet Banking registration and usage are free.
- Transfer fees (NEFT/RTGS) may apply depending on the account variant.
- See [Service Charges](../charges/service-charges.md) for details.

---

## Troubleshooting

For issues such as locked accounts, forgotten passwords, or transaction state inquiries, please see:
**[Internet Banking Troubleshooting](internet-banking-troubleshooting.md)**

---

## Related Documents
- [Mobile Banking](mobile-banking.md)
- [Internet Banking Troubleshooting](internet-banking-troubleshooting.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)
- [Security Guidelines](../security/security-guidelines.md)

---
