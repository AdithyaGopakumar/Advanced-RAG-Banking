---
id: "DIGI-MB-TS-001"
title: "Mobile Banking Troubleshooting"
slug: "mobile-banking-troubleshooting"
domain: "services"
category: "digital-banking"
sub_category: "mobile-banking"
document_type: "troubleshooting"
applicable_to: "both"
target_audience: "customer"
applicable_channels: ["mobile-banking"]
language: "en"
region: "IN"
keywords: ["mobile banking not working", "app crash", "login failed", "app error", "cannot login"]
tags: ["topic:troubleshooting", "intent:report-issue", "channel:mobile-banking"]
search_aliases: ["app not working", "bank app problem", "mobile banking error"]
priority: "high"
related_documents: ["DIGI-MB-001", "SUP-CONT-001"]
parent_document: "DIGI-MB-001"
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

# Mobile Banking — Troubleshooting

## Overview

This guide assists customers in resolving common issues encountered while using the Mobile Banking app. Most issues relate to authentication, connectivity, or device binding and can be resolved through self-service options within the app.

---

## Common Issues

### Unable to log in to the app

- **Problem:** The app rejects the MPIN or biometric authentication, or the account is locked.
- **Possible Causes:** Entering the wrong MPIN multiple times (usually 3 attempts), biometric mismatch, or the app was reinstalled.
- **What the Customer Can Check:** Ensure the phone's internet connection is active. Verify that CAPS lock or specific keyboard settings aren't causing typos.
- **Recommended Action:** Tap on the **Forgot MPIN / Unlock** option on the login screen. Re-authenticate using the registered Debit Card details or Internet Banking credentials to generate a new MPIN.
- **When to Contact the Bank:** If the customer does not have an active debit card or net banking access to perform the reset.

---

### App crashes on launch

- **Problem:** The app opens and immediately closes, or freezes on the loading screen.
- **Possible Causes:** Outdated app version, incompatible OS version, or corrupted app cache.
- **What the Customer Can Check:** Check the App Store / Play Store for available updates. Ensure the device OS is supported (iOS <!-- BANK-SPECIFIC: 14+ -->, Android <!-- BANK-SPECIFIC: 9+ -->).
- **Recommended Action:** 
  1. Update the app. 
  2. If the issue persists, clear the app cache (Android) or reinstall the app. *Note: Reinstalling will require going through the SIM binding registration process again.*

---

### Transaction failed but money debited

- **Problem:** An IMPS or NEFT transfer initiated via the app failed, but the amount was deducted from the account.
- **Possible Causes:** Network timeout between the bank and the beneficiary bank's servers.
- **Recommended Action:** Do not re-initiate the transaction immediately. Wait for the auto-reversal process. Funds are typically credited back to the source account within <!-- BANK-SPECIFIC: T+1 working days -->.
- **When to Contact the Bank:** If the funds are not refunded within the specified TAT (Turn Around Time).

---

### OTP not received

- **Problem:** Customer is trying to register or perform a transaction but the SMS OTP does not arrive.
- **Possible Causes:** Poor cellular network, carrier SMS delays, DND (Do Not Disturb) settings, or full SMS inbox.
- **What the Customer Can Check:** Verify network signal strength. Check if promotional/transactional SMS are blocked at the OS level. Restart the phone.
- **Recommended Action:** Tap **Resend OTP** after the cooldown timer expires.

---

### Unable to register for mobile banking

- **Problem:** The SIM binding process fails during initial setup.
- **Possible Causes:** The mobile number on the device does not match the bank's records, dual-SIM mismatch, or insufficient SMS balance to send the binding text.
- **What the Customer Can Check:** Ensure the registered SIM is inserted in **Slot 1** (for older Android devices) and has an active SMS pack to send outbound texts.
- **Recommended Action:** Retry the binding process over a strong cellular data connection (turn off Wi-Fi during registration).

---

### Changed Phone or Lost Phone

- **Problem:** Customer bought a new phone or lost the old one.
- **Recommended Action (New Phone):** Simply download the app on the new phone and follow the registration process. This will automatically deregister the old device.
- **Recommended Action (Lost Phone):** Immediately call customer care or use Internet Banking to block Mobile Banking access and prevent unauthorized transactions.

---

## When to Contact Support

Contact the 24/7 customer support helpline if:
- You suspect unauthorized access or fraudulent transactions.
- You are locked out and cannot reset the MPIN digitally.
- A failed transaction has crossed the auto-reversal timeline.

---

## Related Documents
- [Mobile Banking](mobile-banking.md)
- [Contact Channels](../customer-support/contact-channels.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
