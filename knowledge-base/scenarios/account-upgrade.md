---
id: "SCEN-UPGRD-001"
title: "Account Upgrade"
slug: "account-upgrade"
domain: "cross-cutting"
category: "scenarios"
sub_category: "account-upgrade"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["account upgrade", "upgrade account", "change account type", "better account"]
search_aliases: ["upgrade my account", "switch account type", "better account option"]
tags: ["intent:update", "process:account-opening"]
priority: "high"
related_documents: ["ACCT-SA-001", "CHG-ACCT-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Account Upgrade Scenario

## Situation
The customer holds a basic savings account and wishes to upgrade to a premium account variant (e.g., from Basic Savings to Wealth Management Account) to access better features or higher limits.

## Customer Intent
`upgrade_account`

## What the Customer May Say
- "I want to upgrade my savings account."
- "How do I change my account type to a premium one?"
- "Can I switch to a wealth account?"

## Relevant Information
Upgrading an account typically involves meeting a higher Minimum Average Balance (MAB) criteria and accepting revised schedule of charges.

## Recommended Response Path
Explain the eligibility criteria for the desired premium account. Inform the customer that they can initiate the upgrade via Internet Banking or by visiting their base branch.

## Immediate Action
None.

## Next Steps
Customer must check their eligibility and submit an upgrade request online or offline.

## Exceptions
- **Insufficient Balance**: If the customer does not meet the funding requirement, the upgrade cannot proceed.
- **Dormant Account**: If the current account is dormant, it must be activated first.

## When to Escalate
Escalate to branch support if the customer receives an error online regarding their KYC status preventing the upgrade.

## Dynamic Information Required
- Current Minimum Average Balance (MAB) requirements.
- Current account fees and debit card charges.

## Live Banking Data Required
- Customer's current account balance and active variant.

## Security Considerations
None.

## Compliance Considerations
Account upgrades may require Re-KYC depending on the risk profiling of the new account tier.

## Related FAQs
- [Accounts FAQ](../faqs/accounts-faq.md)

## Related Documents
- [Savings Account](../docs/accounts/savings-account.md)
- [Account Charges](../docs/charges/account-charges.md)
