---
id: "DIGI-UPI-TS-001"
title: "UPI Troubleshooting"
slug: "upi-troubleshooting"
domain: "services"
category: "digital-banking"
sub_category: "upi"
document_type: "troubleshooting"
applicable_to: "individual"
target_audience: "customer"
applicable_channels: ["upi", "mobile-banking"]
language: "en"
region: "IN"
keywords: ["UPI failed", "UPI not working", "UPI pending", "money debited not credited", "wrong UPI transfer"]
tags: ["topic:troubleshooting", "intent:report-issue", "channel:upi"]
search_aliases: ["UPI payment failed", "UPI transaction pending", "money not received UPI"]
priority: "high"
related_documents: ["DIGI-UPI-001", "SUP-CONT-001"]
parent_document: "DIGI-UPI-001"
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

# UPI — Troubleshooting

## Overview

UPI is designed for real-time transactions, but network congestion or banking server downtime can occasionally cause issues. This guide helps customers interpret transaction states and resolve common UPI-related errors.

---

## Common Issues

### UPI payment failed

- **Problem:** The transaction instantly fails and the UPI app shows a red cross.
- **Possible Causes:** Incorrect UPI PIN, insufficient funds in the linked account, daily transaction limit exceeded, or the receiver's bank server is down.
- **Recommended Action:** The customer should check their account balance and verify they haven't exceeded the daily limit of <!-- BANK-SPECIFIC: ₹1,00,000 -->. Try the transaction again after a few minutes, or use an alternate payment method if the receiver's bank is facing an outage.

---

### Money debited but not credited to receiver (Pending)

- **Problem:** The transaction status is "Pending". Money is deducted from the sender's account, but the receiver hasn't received it.
- **Possible Causes:** Intermittent network issue between the remitter bank, NPCI switch, and the beneficiary bank.
- **What the Customer Can Check:** Check the transaction history in the UPI app.
- **Recommended Action:** Wait. According to NPCI guidelines, pending transactions are automatically reconciled. Funds will either be credited to the receiver or reversed to the sender within <!-- BANK-SPECIFIC: T+2 days --> (usually within a few hours). 
- **DO NOT** initiate the payment again immediately to the same merchant to avoid double debit.

---

### Unable to set or reset UPI PIN

- **Problem:** Attempting to set the PIN fails with an error.
- **Possible Causes:** Entering incorrect Debit Card details (wrong expiry/number), entering the wrong ATM PIN, or the mobile number linked to the Aadhaar (if using Aadhaar verification) doesn't match.
- **Recommended Action:** Ensure the physical debit card is active (not blocked). Verify that the correct OTP received from the bank is being entered before setting the new PIN.

---

### VPA not found / Invalid UPI ID

- **Problem:** Error states the receiver's UPI ID does not exist.
- **Possible Causes:** Typo in the UPI ID, or the receiver has deregistered their UPI handle.
- **Recommended Action:** Carefully verify the spelling of the UPI ID with the receiver. Remember that UPI IDs are not case-sensitive, but exact character matching is required.

---

### Transaction limit exceeded

- **Problem:** Error states the daily limit or transaction count is exhausted.
- **Possible Causes:** Attempting a transfer > ₹1,00,000, or exceeding the maximum number of allowed daily UPI transactions (usually 10 to 20 depending on the bank). Also applies to the new user 24-hour limit (e.g., ₹5,000).
- **Recommended Action:** The customer must wait until the next calendar day (midnight) for the limits to reset. Use NEFT/IMPS via Mobile Banking for immediate, higher-value transfers.

---

## Dispute Resolution (UPI Help)

If a pending transaction is not reversed within the specified turnaround time, or if money was sent to the wrong person:
1. Open the UPI app and navigate to **Transaction History**.
2. Select the disputed transaction.
3. Tap on **Raise Dispute** or **Contact Support**.
4. The complaint is routed through the NPCI Dispute Management System (UDIR).

## When to Contact Support

Contact the bank's 24/7 support line immediately if:
- You receive an SMS for a UPI transaction you did not authorize.
- A "Collect Request" you declined still resulted in a debit.

---

## Related Documents
- [UPI](upi.md)
- [Contact Channels](../customer-support/contact-channels.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
