---
id: "SVC-KYC-001"
title: "KYC and Re-KYC Services"
slug: "kyc-services"
domain: "services"
category: "banking-services"
sub_category: "kyc"
document_type: "process"
applicable_to: "both"
target_audience: "customer"
applicable_channels: ["branch", "internet-banking", "mobile-banking", "video"]
language: "en"
region: "IN"
keywords: ["Re-KYC", "KYC update", "video KYC", "V-CIP", "freeze account", "CKYC"]
tags: ["process:kyc", "intent:update", "channel:all"]
search_aliases: ["update kyc online", "unfreeze kyc", "video kyc process"]
priority: "high"
related_documents: ["POL-KYC-001", "FORM-KYC-001", "SVC-REACT-001"]
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Operations SME"
compliance_classification: "regulatory"
regulatory_references: ["RBI Master Direction on KYC"]
confidentiality: "public"
dynamic_content: false
---

# KYC and Re-KYC Services

## Overview

Know Your Customer (KYC) is a mandatory regulatory process governed by the RBI. While initial KYC is done during account opening, the RBI mandates **Periodic Updation of KYC (Re-KYC)** to ensure customer records remain current.

---

## When is Re-KYC Required?

The frequency of Re-KYC depends on the risk categorization of the account:
- **High-Risk Customers:** Every 2 years.
- **Medium-Risk Customers:** Every 8 years.
- **Low-Risk Customers:** Every 10 years.

The bank will notify you via SMS, Email, and NetBanking alerts when your Re-KYC is due.

### Consequences of Not Doing Re-KYC
If Re-KYC is not completed within the stipulated notice period, the bank is legally required to restrict the account. Typically, a **"Debit Freeze"** is applied first (stopping all outgoing payments), followed eventually by a **"Total Freeze"** (stopping incoming funds as well).

---

## How to Complete Re-KYC

### 1. Digital Re-KYC (No changes to details)
If there is **no change** in your KYC information (Address, Name, etc.), you do not need to visit a branch or upload new documents.
- Log in to Internet or Mobile Banking.
- Navigate to `Services > Re-KYC`.
- Read the declaration stating your details are unchanged and submit. The Re-KYC date is instantly updated.

### 2. Video KYC (V-CIP)
If your details have changed, or if you need to upgrade a limited-KYC digital account to a full-KYC account, you can use Video KYC (Video Customer Identification Process).
1. Go to the bank's website or Mobile App and select **Video KYC**.
2. **Requirements:** You must be physically present in India, have a stable internet connection, original PAN Card, and Aadhaar number (for XML fetch).
3. Connect with the bank agent via video call.
4. The agent will capture your live photo, capture a snapshot of your PAN card, and verify your location via geotagging.
5. **Timeline:** The KYC is usually approved within 1 working day after the call.

### 3. Branch Re-KYC
1. Visit any branch.
2. Submit the **Re-KYC form**.
3. Provide self-attested photocopies of your current OVDs (e.g., Aadhaar and PAN) and present the originals for verification.
4. **Timeline:** Processed within 1 to 3 working days.

---

## CKYC (Central KYC)

CKYC is a centralized registry of KYC records in India. If you have already completed CKYC with another financial institution (like a mutual fund), you have a 14-digit CKYC number. 
- You can provide this CKYC number to the bank.
- The bank will fetch your KYC records directly from the central registry, meaning you do not have to submit physical documents again.

---

## Related Documents
- [KYC Policy](../policies/kyc-policy.md)
- [KYC Documents](../forms/kyc-documents.md)
- [Account Reactivation](account-reactivation.md)
- [Address Update](address-update.md)

---
