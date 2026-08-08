---
id: "SCEN-FRAUD-001"
title: "Fraud Reporting"
slug: "fraud-reporting"
domain: "cross-cutting"
category: "scenarios"
sub_category: "fraud-reporting"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["report fraud", "fraud complaint", "unauthorised transaction", "phishing report", "cyber fraud"]
tags: ["intent:report-issue", "security:fraud-prevention", "process:complaint"]
search_aliases: ["report bank fraud", "stolen money", "cyber crime banking"]
priority: "high"
related_documents: []
version: "1.0"
status: "draft"
created_date: "2026-08-03"
last_updated: "2026-08-03"
last_reviewed: "2026-08-03"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: false
---

# Fraud Reporting & Response

## What Is It?
An unauthorized transaction or account takeover occurs when a fraudster gains access to your banking credentials (via phishing, skimming, or malware) and moves money without your consent. Time is of the essence. Reporting unauthorized transactions immediately (within 3 days) ensures zero liability under RBI guidelines.

---

## Common Warning Signs
- You receive an SMS or email alert for a transaction you did not make.
- You receive an OTP for a transaction you did not initiate.
- Your mobile banking password or MPIN is suddenly rejected as "incorrect."
- Your phone loses cellular network unexpectedly (potential SIM-swap).

---

## What You Should Never Do
- **Never panic and search Google for "Customer Care Number."** Fraudsters buy ads to place fake helpline numbers at the top of search results.
- **Never share an OTP.** Even if the person on the phone claims they are "reversing the fraudulent transaction" and need the OTP to cancel it. The bank NEVER needs an OTP to reverse a transaction.
- **Never install remote-access apps** (like AnyDesk or TeamViewer) if a "support agent" tells you it will help them fix the fraud.

---

## If It Happens to You (Immediate Actions)

If you detect fraud, use the **Detect → Protect → Block → Contact** model:

### Step 1: Protect and Block
Immediately disable the compromised channel. You can do this from the Mobile Banking app (if you still have access):
- **Card Fraud:** Go to "Cards" and select "Hotlist / Block Card".
- **UPI Fraud:** Go to "UPI" and select "Deregister UPI Profile".
- **Account Takeover:** If you cannot log in, proceed immediately to Step 2.

### Step 2: Contact the Bank
Call the official 24x7 emergency fraud helpline: `<!-- BANK-SPECIFIC: 1800-XXX-XXXX -->`.
Request the agent to completely freeze your digital channels (NetBanking and Mobile Banking) and block all associated debit/credit cards.

### Step 3: Secure Credentials
Once the bleeding is stopped, work with the bank to reset your Internet Banking password and MPIN.

---

## How to Report It

To formally dispute the transaction and initiate an investigation:
1. **Bank Reporting:** File a formal dispute by submitting the "Dispute Form" via email to `<!-- BANK-SPECIFIC: fraud.report@bank.com -->` or visiting your home branch.
2. **National Cyber Crime Portal:** Register a police complaint immediately by dialing **1930** or visiting **https://cybercrime.gov.in**. Keep the Acknowledgement Number safe.

---

## What Happens Next
1. **Investigation:** The bank will investigate the transaction trail.
2. **Shadow Credit:** As per the [Customer Liability Policy](../docs/policies/customer-liability-policy.md), if the fraud is reported within 3 working days, the bank will credit the disputed amount back to your account within 10 working days while the investigation continues.
3. **Resolution:** The final resolution (whether the shadow credit is made permanent or reversed) will be communicated within 90 days.

---

## Related Information
- [Customer Liability Policy](../docs/policies/customer-liability-policy.md)
- [Fraud Prevention](../docs/security/fraud-prevention.md)
- [Lost Card Replacement](lost-card-replacement.md)

---

*Last updated: 2026-08-08*
