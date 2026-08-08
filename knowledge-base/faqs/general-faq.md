---
id: "FAQ-GEN-001"
title: "General FAQ"
slug: "general-faq"
domain: "cross-cutting"
category: "faqs"
sub_category: "general-faq"
document_type: "faq"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["general questions", "banking help", "bank hours", "branch locator", "customer care"]
tags: ["topic:faq", "segment:retail"]
search_aliases: ["general help", "banking basics", "new customer questions"]
priority: "high"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# General — Frequently Asked Questions

## Overview

This document answers the most commonly asked questions about general banking topics.

---


# General & Service FAQs

## 1. Updating KYC and Profile Details
### Intent: `update_kyc_profile`
**Variations**:
- How do I update my mobile number?
- Can I change my address online?
- Why is the bank asking me to do Re-KYC?

**Response Route**: `STATIC_RAG` / `DYNAMIC_KNOWLEDGE`
**Answer**: You can update your mobile number and email via Internet Banking or at an ATM. Address changes and Re-KYC usually require submitting an officially valid document (OVD) via the app or at a branch. Re-KYC is a mandatory RBI requirement to keep your account active.
**Canonical Documents**: [KYC Policy](../docs/policies/kyc-policy.md) and [KYC Documents](../docs/forms/kyc-documents.md)

## 2. Forms and Certificates
### Intent: `request_certificate_form`
**Variations**:
- How do I get an interest certificate?
- Which form do I fill to add a nominee?
- Can I get a TDS certificate online?

**Response Route**: `STATIC_RAG`
**Answer**: Most certificates (Interest, TDS, Balance) can be downloaded directly from Internet Banking. For physical requests or specific account modification forms, please check our documentation list or visit a branch.
**Canonical Documents**: [Certificates](../docs/forms/certificates.md) and [Service Request Forms](../docs/forms/service-request-forms.md)

## 3. Filing Complaints
### Intent: `file_complaint`
**Variations**:
- How do I file a complaint against a branch manager?
- Where can I escalate my unresolved issue?
- What is the email ID for the grievance officer?

**Response Route**: `STATIC_RAG` / `HUMAN_ESCALATION`
**Answer**: If you have a grievance, you should first contact Customer Care or your Branch Manager. If unresolved, you can escalate to the Nodal Officer, followed by the Principal Nodal Officer, and finally the Banking Ombudsman.
**Canonical Documents**: [Complaint Process](../docs/customer-support/complaint-process.md) and [Escalation Matrix](../docs/customer-support/escalation-matrix.md)

---

# Dynamic & Live Data Fallback Routing

> [!CAUTION]
> This section explicitly defines the negative and fallback intents for the RAG system. The system MUST NOT hallucinate answers to these questions from static memory.

## 4. Live Customer Data (Negative Intent)
### Intent: `check_live_balance_status`
**Variations**:
- What is my account balance?
- Did my salary get credited today?
- Is my debit card active right now?

**Response Route**: `LIVE_API`
**Answer Model**: 
"I cannot access your personal, live account data from this knowledge base for security reasons. To check your balance, transaction status, or card status, please log in to the Mobile Banking app or Internet Banking portal."

## 5. Highly Regulated / Out-of-Scope Advice
### Intent: `out_of_scope_advice`
**Variations**:
- Which mutual fund should I invest in?
- How can I save tax legally?
- Is Bank X better than your bank?

**Response Route**: `HUMAN_ESCALATION` / `DECLINE`
**Answer Model**: 
"I can provide information about our banking products and services, but I cannot offer personalized investment, tax, or legal advice, nor can I compare specific competitor products. Please consult a certified financial advisor."
