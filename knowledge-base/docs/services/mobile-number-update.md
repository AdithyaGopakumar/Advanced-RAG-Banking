---
id: "SVC-MOB-001"
title: "Mobile Number Update"
slug: "mobile-number-update"
domain: "services"
category: "banking-services"
sub_category: "mobile-number-update"
document_type: "process"
applicable_to: "both"
target_audience: "customer"
applicable_channels: ["branch", "atm"]
language: "en"
region: "IN"
keywords: ["mobile number update", "change mobile number", "register mobile", "update phone number"]
tags: ["process:kyc", "intent:update", "channel:branch"]
search_aliases: ["change phone number", "update mobile in bank", "register new mobile number"]
priority: "medium"
related_documents: ["SVC-ADDR-001", "POL-KYC-001", "FAQ-ACCT-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Operations SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: false
---

# Mobile Number Update

## Overview

The registered mobile number is the primary security key for an account, used to deliver OTPs, transaction alerts, and login approvals. Due to the high risk of SIM-swap fraud, changing a registered mobile number is treated as a highly sensitive operation and cannot usually be done solely via Internet Banking without secondary physical authentication.

---

## What You Need Before You Start

- You must have access to your active Debit Card and its PIN if you wish to change the number at an ATM.
- If you visit a branch, you must carry an original identity proof (like Aadhaar or PAN).
- *Note:* Ensure you have the new SIM card active and inserted in your phone, as you may receive a confirmation OTP.

---

## How to Submit a Request

### 1. Via ATM (Instant & Recommended)
If you have an active debit card, you can change your number at any of the bank's ATMs.
1. Visit the bank's ATM and insert your Debit Card.
2. Enter your ATM PIN.
3. Select `Services / Registration > Mobile Number Registration > Change Mobile Number`.
4. Enter your new mobile number and confirm it.
5. An OTP and a reference number will be sent to your new mobile number.
6. Send an SMS containing the OTP and reference number from your new mobile number to the bank's designated shortcode (e.g., `ACTIVATE <OTP> <REF>`).

### 2. At the Branch
1. Visit your Home Branch.
2. Fill out the **Customer Profile Update Form**.
3. Submit a self-attested photocopy of an ID proof and present the original to the bank official.
4. The bank official will process the request in the core banking system.

### *Why can't I do it on the Mobile App?*
Because the mobile app relies on the existing mobile number for device binding and SMS verification, changing the number from within the app creates a security loop vulnerability.

---

## Processing Time and Outcome

- **ATM Update:** Typically instant after the confirmation SMS is sent.
- **Branch Update:** Processed within 1 to 2 working days.
- **Cooling Period:** To protect against fraud, the bank enforces a <!-- BANK-SPECIFIC: 24-hour --> cooling period after a mobile number change, during which all outgoing digital fund transfers (IMPS/NEFT/RTGS/UPI) are blocked.

---

## Related Documents
- [Address Update](address-update.md)
- [Other Profile Updates](other-profile-updates.md)
- [Fraud Prevention](../security/fraud-prevention.md)
- [Accounts FAQ](../../faqs/accounts-faq.md)

---
