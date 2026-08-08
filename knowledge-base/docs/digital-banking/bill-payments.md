---
id: "DIGI-BP-001"
title: "Bill Payments"
slug: "bill-payments"
domain: "services"
category: "digital-banking"
sub_category: "bill-payments"
document_type: "service"
applicable_to: "individual"
target_audience: "both"
applicable_channels: ["internet-banking", "mobile-banking"]
language: "en"
region: "IN"
keywords: ["bill payment", "utility payment", "BBPS", "electricity bill", "mobile recharge", "autopay"]
tags: ["channel:internet-banking", "channel:mobile-banking", "process:fund-transfer"]
search_aliases: ["pay bills", "utility bills", "BBPS", "autopay", "bill pay online"]
priority: "medium"
related_documents: ["DIGI-MB-001", "DIGI-IB-001", "FAQ-DIGI-001", "CHG-PAY-001"]
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

# Bill Payments

## Overview

The digital Bill Payments service allows customers to pay utility bills, recharge mobile connections, and settle credit card dues directly from their bank accounts. It is integrated directly with the Bharat Bill Payment System (BBPS), ensuring instant confirmation and high reliability across thousands of registered billers in India.

---

## Supported Billers

The service supports payments for:
- Electricity, Water, and Piped Gas.
- Mobile Postpaid and Prepaid recharges.
- DTH and Broadband connections.
- FASTag recharges.
- Credit Card bills, Loan EMIs, and Insurance Premiums.
- Municipal Taxes and Housing Society maintenance.

---

## How to Pay Bills

1. **Login:** Access your account via Internet Banking or the Mobile Banking app.
2. **Navigate:** Go to the **Bill Pay & Recharge** section.
3. **Select Biller:** Choose the category (e.g., Electricity) and select your specific provider (e.g., BESCOM).
4. **Enter Details:** Input your Consumer Number or Customer ID. The system will automatically fetch the pending bill amount via BBPS.
5. **Pay:** Select the debit account and authorize the transaction using an OTP, MPIN, or TPIN.
6. **Confirmation:** The payment is executed instantly, and a BBPS receipt is generated.

---

## Auto-Pay / Standing Instructions

Customers can automate their recurring bill payments using the Auto-Pay feature (E-Mandates).
1. While paying a bill, check the **Set up Auto-Pay** option.
2. Define a maximum limit (e.g., up to ₹5,000). If the fetched bill exceeds this amount, the auto-pay will require manual authorization.
3. The bank will automatically debit the account on the due date.
4. Auto-Pay mandates can be cancelled or modified at any time via the "Manage Mandates" section.

---

## Charges

- Paying utility bills through BBPS via Mobile/Internet banking is typically **Free of Charge** for retail savings accounts.
- **Credit Card Bill Payments:** May attract a nominal fee if paying a third-party bank's credit card bill (refer to [Payment Charges](../charges/payment-charges.md)).

---

## Related Documents
- [Mobile Banking](mobile-banking.md)
- [Internet Banking](internet-banking.md)
- [Digital Banking FAQ](../../faqs/digital-banking-faq.md)

---
