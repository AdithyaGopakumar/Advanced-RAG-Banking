---
id: "DEP-FLX-001"
title: "Flexi Deposit"
slug: "flexi-deposit"
domain: "products"
category: "deposits"
sub_category: "flexi-deposit"
document_type: "product"
applicable_to: "individual"
target_audience: "both"
applicable_channels:
  - "branch"
  - "internet-banking"
  - "mobile-banking"
language: "en"
region: "IN"
keywords:
  - "flexi deposit"
  - "sweep in sweep out"
  - "auto sweep"
  - "flexi FD"
tags:
  - "product:flexi-deposit"
  - "segment:retail"
  - "channel:all"
  - "feature:sweep-in"
search_aliases:
  - "flexi FD"
  - "sweep FD"
  - "auto sweep facility"
priority: "medium"
related_documents:
  - "DEP-FD-001"
  - "ACCT-SA-001"
  - "RATE-DEP-001"
  - "CHG-ACCT-001"
version: "1.0"
status: "approved"
created_date: "2026-08-08"
last_updated: "2026-08-08"
last_reviewed: "2026-08-08"
owner: "Retail Banking SME"
compliance_classification: "regulatory"
regulatory_references: []
confidentiality: "public"
dynamic_content: false
---

# Flexi Deposit

## Overview

The Flexi Deposit (also known as a Sweep-in / Sweep-out deposit) combines the liquidity of a Savings or Current account with the higher returns of a Fixed Deposit. Surplus funds in the linked account are automatically swept into an FD, and funds are automatically swept back to cover shortfalls.

---

## Features and Benefits

### Key features

- Auto sweep-out from the linked operational account when the balance crosses a predefined threshold
- Auto sweep-in to the linked account when funds are required to honor a debit/cheque
- Sweep-in happens on a Last-In-First-Out (LIFO) basis
- No manual intervention required for creating or breaking the FD

### Benefits

- **Maximized Returns**: Idle funds automatically earn higher FD interest rates.
- **Complete Liquidity**: Never bounce a cheque due to insufficient operational balance.
- **Convenience**: Fully automated fund management.

---

## Eligibility

| Criterion | Requirement |
|---|---|
| Linked Account | Must have an active Savings or Current account with the Bank. |
| Sweep-out Threshold | The minimum balance that must remain in the linked account before a sweep-out occurs (e.g., ₹25,000). |
| Sweep-in Multiple | Funds are swept back in specific multiples (e.g., ₹1,000) to ensure the rest of the deposit continues earning FD interest. |

---

## Interest Rates

The swept-out funds earn interest at the standard Fixed Deposit rate for the default tenure selected at the time of enrollment. See [Deposit Interest Rates](../interest-rates/deposit-interest-rates.md).

---

## Sweep-In / Sweep-Out Mechanics

- **Sweep-Out**: When the operational account balance exceeds the threshold, the excess is automatically converted into an FD.
- **Sweep-In**: If a transaction (ATM, cheque, UPI) causes the operational balance to drop below zero (or the minimum balance), the exact shortfall amount (in multiples of the sweep-in multiple) is instantly broken from the FD and credited to the operational account.

---

## Premature Withdrawal

When funds are swept back (premature withdrawal), the broken amount earns interest applicable for the period it remained with the bank, often subject to a premature penalty. The unbroken portion continues to earn the original interest rate. See [Account Charges](../charges/account-charges.md).

---

## Tax Implications

Interest earned on the swept-out FD portion is fully taxable. TDS applies if the total interest earned across all deposits exceeds the regulatory threshold in a financial year, unless a valid Form 15G/15H is submitted.

---

## How to Apply

Customers can activate the Flexi Deposit facility on their existing Savings or Current accounts by logging into Internet Banking or submitting a request form at the branch.

---

## Related Documents

- [Fixed Deposit](fixed-deposit.md) — Standard standalone term deposits
- [Savings Account](../accounts/savings-account.md) — Accounts eligible for linking
- [Deposit Interest Rates](../interest-rates/deposit-interest-rates.md) — Current FD interest rates
- [Account Charges](../charges/account-charges.md) — Premature withdrawal penalties

---

*Last updated: 2026-08-08*
