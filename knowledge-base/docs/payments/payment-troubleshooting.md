---
id: "PAY-TS-001"
title: "Payment Troubleshooting"
slug: "payment-troubleshooting"
domain: "services"
category: "payments"
sub_category: "payment-troubleshooting"
document_type: "troubleshooting"
applicable_to: "both"
target_audience: "customer"
applicable_channels: ["branch", "internet-banking", "mobile-banking"]
language: "en"
region: "IN"
keywords: ["payment failed", "transfer failed", "money not received", "wrong transfer", "NEFT pending"]
tags: ["topic:troubleshooting", "intent:report-issue", "process:fund-transfer"]
search_aliases: ["transfer not received", "payment stuck", "wrong account transfer"]
priority: "high"
related_documents: ["PAY-NEFT-001", "PAY-RTGS-001", "PAY-IMPS-001", "SUP-CONT-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: false
---

# Payment Troubleshooting

## Overview

This guide assists customers in diagnosing and resolving common issues encountered during electronic funds transfers (NEFT, RTGS, IMPS), cheque clearing, and mandate deductions. For UPI-specific troubleshooting, refer to [UPI Troubleshooting](../digital-banking/upi-troubleshooting.md).

---

## Common Issues

### NEFT/RTGS transfer not received

- **Problem:** The remitter has successfully sent funds, but the beneficiary has not received the credit.
- **Possible Causes:**
  - The transaction is still in the RBI batch queue (NEFT only).
  - The beneficiary bank is experiencing a technical delay in crediting the account.
  - The transaction occurred on a bank holiday (while NEFT/RTGS is 24x7, some cooperative banks may delay credit).
- **What to Check:** Ensure at least 2 hours have passed since the NEFT was initiated, or 30 minutes for RTGS.
- **Recommended Action:** Obtain the **UTR (Unique Transaction Reference)** number from the remitter's bank statement. The beneficiary should provide this UTR to their bank to trace the funds.

---

### Money debited but transfer shows failed

- **Problem:** The transfer attempt failed, but the amount was deducted from the customer's account.
- **Possible Causes:** The remitter's bank debited the funds but the connection to the central payment switch (RBI/NPCI) timed out before the transfer could be completed.
- **What to Check:** Check the transaction status in the mobile/internet banking app.
- **Recommended Action:** Wait. As per RBI guidelines, the remitter's bank will automatically reconcile the transaction and reverse the debited amount. For IMPS, this reversal typically happens within `T+1` business days.

---

### Wrong account number entered

- **Problem:** Funds were successfully transferred, but the customer entered the wrong beneficiary account number.
- **Possible Causes:** Manual entry error during beneficiary registration.
- **What to Check:** Check if the IFSC matched the wrong account number. (If the IFSC was correct but the account number does not exist, the destination bank will automatically reject and return the funds within `T+1` day).
- **Recommended Action:** 
  - **If the money was credited to an unintended third party:** The customer must immediately contact their home branch and file a written complaint. 
  - **Reversal process:** The remitter bank will contact the beneficiary bank. However, the beneficiary bank cannot reverse the funds without the explicit consent of the unintended receiver. This process can take significant time.

---

### Transfer amount limit exceeded

- **Problem:** The customer cannot initiate a transfer because the app shows "Limit Exceeded".
- **Possible Causes:**
  - Attempting to send more than the daily digital transfer limit (e.g., > <!-- BANK-SPECIFIC: ₹25,00,000 -->).
  - Attempting to send funds to a newly added beneficiary within the 24-hour cooling period (capped at <!-- BANK-SPECIFIC: ₹50,000 -->).
- **What to Check:** Check the 'Manage Limits' section in the NetBanking portal.
- **Recommended Action:** Reduce the transfer amount, wait for the cooling period to expire, or visit a branch to perform the transfer without digital limits.

---

## When to Contact Support

If a failed NEFT/IMPS transaction is not automatically reversed within the stipulated RBI Turn Around Time (`T+1` business day), the customer should escalate the issue.

- Contact the 24x7 helpline.
- File a complaint via the [Contact Channels](../customer-support/contact-channels.md).
- Keep the UTR or Reference Number ready.

---

## Related Documents
- [NEFT](neft.md)
- [RTGS](rtgs.md)
- [IMPS](imps.md)
- [Contact Channels](../customer-support/contact-channels.md)

---
