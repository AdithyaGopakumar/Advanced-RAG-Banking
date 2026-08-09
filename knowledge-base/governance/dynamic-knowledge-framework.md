# Dynamic Knowledge Framework

This document outlines the framework for handling dynamic, time-sensitive, and real-time knowledge within the Banking Customer Support RAG system.

---

## 1. Static vs Dynamic Classification

The knowledge base classifies information based on its material volatility:

| Classification | Definition | Examples |
|---|---|---|
| **STATIC** | Core concepts and mechanics that rarely change. | Definition of a Savings Account, NEFT mechanics. |
| **SLOWLY_DYNAMIC** | Features and policies that change occasionally (yearly+). | Loan eligibility criteria, general account closure policy. |
| **PERIODICALLY_DYNAMIC** | Values that change on a known schedule or predictable trigger. | Deposit interest rates, schedule of charges, form versions. |
| **FREQUENTLY_DYNAMIC** | Information that changes daily, weekly, or ad-hoc. | Exchange rates, active promotional offers, branch availability. |
| **REAL_TIME** | Live customer-specific or system-specific states. | Account balances, transaction statuses, live credit limits. |

---

## 2. Dynamic Knowledge Inventory & Models

### Interest Rate Dynamic Model
- **Data Type**: `PERIODICALLY_DYNAMIC`
- **Scope**: Savings rates, FD rates, RD rates, Loan rates (repo-linked, base rates), Senior Citizen premiums, Penal rates.
- **Source Authority**: ALCO (Asset Liability Committee) Circulars, Treasury.
- **Refresh Frequency**: On-change (ALCO meeting triggers) or Regulatory-triggered.
- **Retrieval Strategy**: Track `effective_from` and `effective_until`. Retain historical rates for temporal questions ("What was the FD rate last month?").
- **Risk Level**: HIGH

### Fees & Charges Dynamic Model
- **Data Type**: `PERIODICALLY_DYNAMIC`
- **Scope**: Account maintenance fees, ATM charges, Transfer charges, Loan processing/foreclosure fees, Card fees.
- **Source Authority**: Official Schedule of Charges / Finance Pricing Team.
- **Refresh Frequency**: On-change (typically annual or bi-annual reviews).
- **Retrieval Strategy**: Canonical `reference-data` documents. No fee values duplicated in static product pages.
- **Risk Level**: HIGH

### FX & Exchange Rate Dynamic Model
- **Data Type**: `FREQUENTLY_DYNAMIC`
- **Scope**: FX buying/selling rates, Remittance rates, Card conversion markup.
- **Source Authority**: Treasury / Card Networks (Visa/Mastercard) / RBI reference rates.
- **Refresh Frequency**: Daily or Hourly (depending on currency volatility).
- **Retrieval Strategy**: The RAG should *not* answer with a hardcoded static value. It must route to a Dynamic Store or Live API for today's rate. 
- **Risk Level**: HIGH

### Regulatory Dynamic Model
- **Data Type**: `PERIODICALLY_DYNAMIC`
- **Scope**: KYC thresholds, Deposit insurance limits, Transaction limits, Tax rates (TDS).
- **Source Authority**: RBI Master Directions, Income Tax Department, NPCI, DICGC.
- **Refresh Frequency**: Regulatory-triggered (Union Budget, RBI Monetary Policy).
- **Retrieval Strategy**: Strict temporal versioning. Track `superseded_date` and `authority`.
- **Risk Level**: CRITICAL

### Product Availability Model
- **Data Type**: `SLOWLY_DYNAMIC`
- **Scope**: Current product lineup, newly launched variants, discontinued/grandfathered products.
- **Source Authority**: Product Management.
- **Refresh Frequency**: On-change.
- **Retrieval Strategy**: Maintain status flags (`active`, `discontinued`). Historical products remain for existing customers but are not recommended to new prospects.
- **Risk Level**: MEDIUM

### Branch & Channel Dynamic Model
- **Data Type**: `FREQUENTLY_DYNAMIC`
- **Scope**: Branch hours, Holiday schedules, ATM cash availability, Service outages.
- **Source Authority**: Operations / IT Incident Management / RBI Holiday list.
- **Refresh Frequency**: Daily (for operational status) or Annually (for holiday lists).
- **Retrieval Strategy**: Route live outages to API. Holiday lists can be stored in the Dynamic Store.
- **Risk Level**: MEDIUM

### Contact Information Model
- **Data Type**: `SLOWLY_DYNAMIC` (Standard contacts) / `FREQUENTLY_DYNAMIC` (Nodal officers)
- **Scope**: Customer care numbers, Fraud-reporting hotlines, Grievance officers, Official URLs.
- **Source Authority**: Customer Service / Compliance.
- **Refresh Frequency**: On-change.
- **Retrieval Strategy**: Canonical contacts reference. 
- **Risk Level**: CRITICAL (Fraud/Phishing risk if wrong).

### Form Versioning Model
- **Data Type**: `PERIODICALLY_DYNAMIC`
- **Scope**: KYC forms, Account opening documents, Dispute forms.
- **Source Authority**: Compliance / Operations.
- **Refresh Frequency**: On-change.
- **Retrieval Strategy**: Strict versioning (v1, v2). Track `effective_until`. Obsolete forms must be marked `superseded`.
- **Risk Level**: HIGH

### Promotional Knowledge Model
- **Data Type**: `FREQUENTLY_DYNAMIC`
- **Scope**: Cashback offers, fee waivers, limited-time benefits.
- **Source Authority**: Marketing / Partnerships.
- **Refresh Frequency**: On-change (campaign launches).
- **Retrieval Strategy**: Strict `effective_from` and `effective_until`. Expired promotions must not be visible to prospects.
- **Risk Level**: MEDIUM

---

## 3. Real-Time Knowledge Boundary

The RAG system must recognize when to stop searching static/dynamic text and route to a live banking tool.

| Customer Query / Data | Required System | Fallback (if unavailable) |
|---|---|---|
| Account Balance | Core Banking System API | "I cannot access your live balance right now. Please check the Mobile Banking App." |
| Transaction Status | Payment Gateway / UPI Switch API | "To check transaction status, please navigate to 'Recent Transactions' in Internet Banking." |
| Card Status (Active/Blocked) | Card Management System API | "Please verify your card status in the 'Manage Cards' section of the Mobile App." |
| Loan Outstanding Amount | Loan Management System API | "You can view your exact outstanding principal in the 'Loans' tab online." |
| Current Live FX Rate | Treasury API | "Live FX rates fluctuate. Please check the live rate calculator on the banking portal." |

---

## 4. Source Authority Model & Conflict Resolution

If sources conflict, the system evaluates precedence using the following hierarchy:

1. **PRIMARY SOURCE**: Regulator / Canonical Official Circular (e.g., RBI Master Direction, ALCO pricing circular).
2. **SECONDARY SOURCE**: Internal Bank Policy Document.
3. **FALLBACK SOURCE**: General FAQ or legacy product document.

**Conflict Resolution Rules:**
1. **Authority**: RBI overrules internal policy; ALCO overrules Marketing.
2. **Effective Date**: The document with the most recent `effective_from` date in the *past* wins. Future effective dates are held in reserve.
3. **Currentness**: A document marked `status: published` or `status: current` outranks `status: archived`.

---

## 5. Refresh Strategy & Staleness Policy

### Staleness States
- **CURRENT**: Information is within its effective dates and verified recently.
- **STALE**: Information has passed its expected refresh frequency without verification, but no newer version exists. (Proceed with caution).
- **EXPIRED**: Information has passed its `effective_until` date. (Do not serve as active).
- **SUPERSEDED**: A newer version exists. (Serve new version).
- **UNVERIFIED**: Source authority cannot be confirmed.

### Refresh Matrix
- **Regulatory Thresholds**: Manual verification quarterly.
- **Interest Rates / Fees**: On-change trigger (API webhook) or manual verification monthly.
- **Branch Holidays**: Annual batch load.
- **Promotions**: System-automated deprecation upon `effective_until` date.

---

## 6. RAG vs Dynamic Store vs Live API Matrix

| Information Type | Storage Layer | Rationale |
|---|---|---|
| General Product Policies | **Static RAG** | Rarely changes; text-heavy; semantically rich. |
| Fees, Rates, Thresholds | **Dynamic Store (Canonical Docs)** | Changes periodically; needs versioning; must be canonical to avoid RAG conflicts. |
| Exchange Rates, Offers | **Dynamic Store / API** | High volatility; requires strict expiry handling. |
| Account Balances, Statuses | **Live API / Tool** | Unique per customer; instantaneous; impossible to index. |

---

## 7. Customer Intent Inventory

The RAG intent router must identify these specific dynamic intents to trigger the correct data source:

- `intent:get_current_interest_rate`
- `intent:get_current_fee`
- `intent:get_current_exchange_rate`
- `intent:check_product_availability`
- `intent:find_branch_hours`
- `intent:get_contact_details`
- `intent:get_latest_form`
- `intent:check_active_offers`
- `intent:check_transaction_status` (Routes to API)
- `intent:check_account_balance` (Routes to API)

---

*Last updated: 2026-08-08*
