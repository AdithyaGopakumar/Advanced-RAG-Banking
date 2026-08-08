---
id: "PAY-CHQ-001"
title: "Cheque Services"
slug: "cheque-services"
domain: "services"
category: "payments"
sub_category: "cheque-services"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["branch"]
language: "en"
region: "IN"
keywords: ["cheque", "cheque book", "cheque deposit", "cheque clearance", "CTS", "cheque truncation"]
tags: ["channel:branch", "process:fund-transfer", "process:cheque-request"]
search_aliases: ["check", "cheque book request", "cheque deposit", "cheque clearance time"]
priority: "medium"
related_documents: ["PAY-DD-001", "CHG-PAY-001", "FAQ-PAY-001", "POL-CHQ-001"]
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

# Cheque Services

## Overview

A cheque is a negotiable physical instrument used to instruct the bank to pay a specific amount from the drawer's (issuer's) account to a designated person or entity. Cheque clearing in India is largely governed by the Cheque Truncation System (CTS), operated by the National Payments Corporation of India (NPCI).

---

## Types of Cheques

- **Account Payee Cheque:** Has two parallel lines crossed on the top left. The funds can only be credited to the bank account of the payee. It is highly secure.
- **Bearer Cheque:** Payable to whoever presents the cheque at the bank counter. It is risky and can be cashed by anyone holding it.
- **Order Cheque:** Payable to a specific person. The payee must endorse it to transfer it to someone else.
- **Post-Dated Cheque (PDC):** Bears a future date. It cannot be cleared before that date.
- **Stale Cheque:** A cheque presented after 3 months from the date of issue is considered "stale" and will be rejected.

---

## Cheque Truncation System (CTS) and Clearing

CTS eliminates the physical movement of cheques from the presenting bank to the paying bank.
1. The customer deposits the cheque at their bank (Presenting Bank).
2. The bank scans the cheque and sends the electronic image along with MICR data to the NPCI Clearing House.
3. The clearing house routes the image to the issuer's bank (Drawee Bank).
4. The Drawee Bank verifies the signature and account balance.
5. If valid, funds are settled and credited to the depositor.

**Clearing Timelines:**
- **Local/CTS Cheques:** Usually cleared within `T+1` or `T+2` working days.
- **Outstation Cheques:** May take `T+3` to `T+5` days depending on the location.

---

## Positive Pay System (PPS)

To prevent fraud, RBI mandates the Positive Pay mechanism.
- For cheques issued for high values (usually <!-- BANK-SPECIFIC: ₹50,000 --> and above), the issuer must pre-inform the bank regarding the cheque details (Cheque Number, Date, Amount, Payee Name) via NetBanking, Mobile Banking, or SMS.
- If the details presented in CTS do not match the Positive Pay instructions, the cheque will be returned unpaid.

---

## Cheque Return (Bouncing) and Stop Payment

- **Bouncing:** If a cheque is returned unpaid due to insufficient funds, signature mismatch, or being stale, a **Cheque Return Memo** is issued specifying the reason. Returning a cheque due to insufficient funds is a criminal offense under Section 138 of the Negotiable Instruments Act.
- **Stop Payment:** An issuer can request the bank to stop the payment of a cheque before it is cleared. This can be done instantly via Internet/Mobile Banking. A fee applies for stopping a cheque.

---

## Charges

- Issuance of cheque books beyond the free limit incurs a per-leaf charge.
- Cheque return (bouncing) incurs substantial penal charges for both the drawer and the depositor.
- Refer to [Payment Charges](../charges/payment-charges.md) and the [Cheque Return Policy](../policies/cheque-return-policy.md) for specifics.

---

## Related Documents
- [Demand Draft](demand-draft.md)
- [Payment Charges](../charges/payment-charges.md)
- [Cheque Return Policy](../policies/cheque-return-policy.md)
- [Payments FAQ](../../faqs/payments-faq.md)

---
