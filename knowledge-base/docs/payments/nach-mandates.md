---
id: "PAY-NACH-001"
title: "NACH and E-Mandates"
slug: "nach-mandates"
domain: "services"
category: "payments"
sub_category: "nach"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["internet-banking", "branch"]
language: "en"
region: "IN"
keywords: ["NACH", "e-mandate", "auto debit", "recurring payment", "ECS", "SIP deduction"]
tags: ["process:fund-transfer", "process:mandate"]
search_aliases: ["auto deduct", "cancel SIP mandate", "stop auto debit", "NACH bounce"]
priority: "medium"
related_documents: ["PAY-TS-001", "CHG-PAY-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["NPCI NACH Procedural Guidelines"]
confidentiality: "public"
dynamic_content: false
---

# NACH and E-Mandates

## Overview

The National Automated Clearing House (NACH) is a centralized system operated by the National Payments Corporation of India (NPCI) for bulk, repetitive, and periodic transactions. It replaces the older ECS (Electronic Clearing Service). 

NACH is primarily used by institutions for:
- **Direct Debits:** Collecting utility bills, loan EMIs, mutual fund SIPs, and insurance premiums.
- **Direct Credits:** Distributing subsidies (DBT), dividends, interest, and salaries.

---

## How Mandates Work

A mandate is an authorization given by the customer to a corporate/biller allowing them to automatically debit a specified bank account for a certain amount at regular intervals.

1. **Registration:** The customer registers a mandate with the biller.
   - **Physical Mandate:** Signing a physical NACH form, which the biller sends to the bank for signature verification.
   - **E-Mandate (Digital):** Authenticating the mandate instantly on the biller's website using Internet Banking credentials or a Debit Card (via the NPCI API).
2. **Presentation:** The biller (via their sponsor bank) presents the NACH debit file to NPCI on the due date.
3. **Clearing:** NPCI routes the debit requests to the customer's bank.
4. **Debit:** The bank checks the account balance and the mandate limit. If sufficient funds are available, the account is debited.

---

## Limits and Constraints

- **Maximum Amount:** The mandate specifies a "Maximum Limit". The actual debit can be varying amounts (e.g., a postpaid mobile bill) as long as it does not exceed the maximum limit.
- **Validity:** Mandates can be set for a specific duration (e.g., 5 years) or "Until Cancelled".

---

## Failed Transactions (NACH Bounce)

If a NACH debit fails due to **Insufficient Funds**, the consequences are severe:
- The bank levies a **NACH Return Charge** (Bounce Fee) on the customer's account for failing to maintain the balance.
- The biller may also levy a late fee or penalty.
- Bouncing a loan EMI mandate can negatively impact the customer's credit score (CIBIL) and attract legal action under the Payment and Settlement Systems Act.

---

## Cancellation and Modification

- **Cancellation:** Customers can cancel an active NACH mandate by logging into Internet Banking and navigating to the 'Mandate Management' section, or by submitting a cancellation form at a branch. 
- *Note:* It is recommended to cancel the mandate at least 3-5 working days before the next due date to prevent the cycle from initiating.
- **Modification:** To change the maximum amount or the bank account, the existing mandate must usually be cancelled and a new one registered.

---

## Related Documents
- [Payment Troubleshooting](payment-troubleshooting.md)
- [Payment Charges](../charges/payment-charges.md)

---
