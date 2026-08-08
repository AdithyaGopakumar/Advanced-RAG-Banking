---
id: "DIGI-IB-TS-001"
title: "Internet Banking Troubleshooting"
slug: "internet-banking-troubleshooting"
domain: "services"
category: "digital-banking"
sub_category: "internet-banking"
document_type: "troubleshooting"
applicable_to: "both"
target_audience: "customer"
applicable_channels: ["internet-banking"]
language: "en"
region: "IN"
keywords: ["internet banking not working", "login problem", "password reset", "net banking error", "session expired"]
tags: ["topic:troubleshooting", "intent:report-issue", "channel:internet-banking"]
search_aliases: ["net banking not working", "online banking problem", "cannot login net banking"]
priority: "high"
related_documents: ["DIGI-IB-001", "SUP-CONT-001"]
parent_document: "DIGI-IB-001"
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

# Internet Banking — Troubleshooting

## Overview

This guide assists customers in resolving common issues encountered on the Internet Banking web portal, primarily related to login access, passwords, and transaction states.

---

## Common Issues

### Unable to log in

- **Problem:** "Invalid User ID or Password" error, or the account is locked.
- **Possible Causes:** Entering incorrect credentials (case sensitivity), or exceeding the maximum number of failed login attempts (usually 3 to 5).
- **What the Customer Can Check:** Ensure CAPS lock is off. Verify the User ID (CIF) is correct.
- **Recommended Action:** If the account is locked due to failed attempts, use the **Forgot Password / Unlock Account** link on the login page. Authentication via Debit Card and OTP is required.

---

### Password reset issues

- **Problem:** Unable to reset the Login Password or Transaction Password digitally.
- **Possible Causes:** Customer does not have an active Debit Card, or the registered mobile number is inactive.
- **Recommended Action:** If digital reset fails, the customer must submit a physical request form at the home branch to receive a physical PIN mailer.

---

### Transaction failed or pending

- **Problem:** An NEFT/RTGS/IMPS transfer shows as "Pending" or "Failed" but funds were debited.
- **Possible Causes:** NEFT batch delays, beneficiary bank server downtime, or invalid beneficiary details.
- **Recommended Action:** 
  - **Pending:** Wait for the transaction to clear. (NEFT operates in half-hourly batches; RTGS/IMPS is real-time).
  - **Failed:** Funds are auto-reversed. Do not re-initiate until the status is confirmed as Failed.
- **Escalation:** If funds are not reversed within <!-- BANK-SPECIFIC: T+1 days -->, raise a service request via the portal.

---

### Session expired unexpectedly

- **Problem:** Customer is logged out while navigating or entering transaction details.
- **Possible Causes:** Idle timeout for security purposes (typically <!-- BANK-SPECIFIC: 5 minutes -->), or the browser's cookies/cache are corrupted.
- **Recommended Action:** Log in again. If the issue persists immediately upon login, clear the browser's cache and cookies, or try using an "Incognito/Private" browsing window.

---

### Beneficiary addition failed

- **Problem:** Unable to add a new payee or initiate a transfer to a newly added payee.
- **Possible Causes:** Incorrect IFSC code, or attempting a high-value transfer during the cooling period.
- **What the Customer Can Check:** Verify the IFSC code matches the payee's branch.
- **Recommended Action:** Wait for the mandatory cooling period (e.g., <!-- BANK-SPECIFIC: 30 minutes -->) to elapse before initiating a transfer. Adhere to the new payee security limit (e.g., <!-- BANK-SPECIFIC: ₹50,000 -->) for the first 24 hours.

---

## When to Contact Support

Contact the 24/7 customer support helpline or visit the branch if:
- You observe unauthorized transactions or unfamiliar payees added to your account.
- You are unable to reset your password digitally and require manual intervention.
- The portal displays persistent backend errors over multiple days.

---

## Related Documents
- [Internet Banking](internet-banking.md)
- [Contact Channels](../customer-support/contact-channels.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
