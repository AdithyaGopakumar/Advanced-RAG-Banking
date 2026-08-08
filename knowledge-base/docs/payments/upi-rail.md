---
id: "PAY-UPI-001"
title: "UPI Payment Mechanism"
slug: "upi-rail"
domain: "services"
category: "payments"
sub_category: "upi"
document_type: "service"
applicable_to: "both"
target_audience: "both"
applicable_channels: ["mobile-banking", "upi"]
language: "en"
region: "IN"
keywords: ["UPI backend", "UPI rail", "UDIR", "VPA translation", "UPI clearing"]
tags: ["process:fund-transfer", "channel:upi"]
search_aliases: ["how upi works", "upi backend", "upi clearing"]
priority: "high"
related_documents: ["PAY-IMPS-001", "DIGI-UPI-001", "PAY-TS-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Payments SME"
compliance_classification: "regulatory"
regulatory_references: ["NPCI UPI Procedural Guidelines"]
confidentiality: "public"
dynamic_content: false
---

# UPI Payment Mechanism

## Overview

The Unified Payments Interface (UPI) is a robust payment rail operated by the National Payments Corporation of India (NPCI). While the *digital experience* (how customers send money via apps) is covered in the [Digital Banking Domain](../digital-banking/upi.md), this document explains the underlying payment mechanism, network participants, and settlement architecture.

---

## Network Participants

A standard UPI transaction involves multiple entities:
1. **Remitter:** The customer sending the money.
2. **Payer PSP (Payment Service Provider):** The app used by the remitter (e.g., Google Pay, Bank App).
3. **Remitter Bank (Issuer):** The bank holding the remitter's account.
4. **NPCI Switch:** The central clearing house that routes messages between banks.
5. **Beneficiary Bank (Acquirer):** The bank holding the receiver's account.
6. **Payee PSP:** The app/system used by the receiver.
7. **Beneficiary:** The person or merchant receiving the funds.

---

## The Transaction Flow (Backend)

1. **Initiation:** The Payer PSP captures the transaction details and sends a request to the Remitter Bank.
2. **VPA Translation:** If the payment is sent to a UPI ID (VPA), the NPCI switch performs a real-time lookup to translate the `name@bank` into an Account Number + IFSC.
3. **Authorization:** The Remitter Bank verifies the UPI PIN and debits the account.
4. **Routing:** The Remitter Bank sends a success message to NPCI.
5. **Credit:** NPCI routes the message to the Beneficiary Bank, which instantly credits the receiver's account.
6. **Confirmation:** Success messages are sent back down the chain to both PSP apps.
7. **Settlement:** The actual funds are settled between the Remitter and Beneficiary banks during deferred, multi-lateral settlement cycles conducted by RBI.

---

## UDIR (Unified Dispute and Issue Resolution)

NPCI provides an automated, API-driven dispute management system called UDIR.
- If a transaction is "Pending", UDIR automatically triggers a status check across all participants.
- If the Beneficiary Bank confirms they did not credit the user, UDIR instructs the Remitter Bank to automatically reverse the debit.
- **Timeline:** This automated reconciliation handles almost all pending transactions within `T+2` days, eliminating the need for manual chargebacks.

---

## UPI AutoPay (E-Mandates)

UPI AutoPay uses the same rail but introduces an **electronic mandate** flow.
1. The merchant sends a mandate creation request.
2. The user authorizes it once using their UPI PIN.
3. For subsequent billing cycles, the merchant's bank sends a pull request. As long as the amount is within the mandated limit (e.g., < ₹5,000), the Remitter Bank debits the account automatically without requiring the UPI PIN again.

---

## Related Documents
- [UPI Digital Experience](../digital-banking/upi.md)
- [IMPS](imps.md)
- [Payment Troubleshooting](payment-troubleshooting.md)

---
