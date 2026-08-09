---
id: "SCEN-DEC-001"
title: "Deceased Account Handling"
slug: "deceased-account-handling"
domain: "cross-cutting"
category: "scenarios"
sub_category: "deceased-account-handling"
document_type: "scenario"
applicable_to: "both"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["deceased account", "death claim", "nominee claim", "legal heir", "settlement"]
search_aliases: ["claim deceased funds", "report account holder death", "nomination claim"]
tags: ["intent:claim", "process:deceased-claim"]
priority: "high"
related_documents: ["FORM-SR-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Deceased Account Handling Scenario

## Situation
A relative or legal heir contacts the bank to report the death of an account holder and wishes to claim the funds or close the account.

## Customer Intent
`deceased_claim`

## What the Customer May Say
- "My father passed away, how do I access his account?"
- "How do I file a death claim?"
- "The account holder is deceased, what is the procedure?"

## Relevant Information
Settlement depends heavily on whether a nominee was registered, or if it was a joint account with "Survivor" clause.

## Recommended Response Path
Offer condolences. Explain that the claimant needs to submit a Death Certificate along with the Deceased Claim Form at the home branch.

## Immediate Action
Mark the account to prevent unauthorized debit transactions (if authorized to do so).

## Next Steps
Claimant must visit the home branch with the original death certificate and claimant's KYC.

## Exceptions
- **Nominee Exists**: Simple settlement process directly to the registered nominee.
- **No Nominee**: Requires a Legal Heir Certificate or Succession Certificate, which takes longer.
- **Joint Account**: Surviving holder can continue operating or claim the funds easily.

## When to Escalate
If there is a dispute among legal heirs, escalate to the Legal/Nodal Officer immediately.

## Dynamic Information Required
None.

## Live Banking Data Required
- Verification of registered nominee.

## Security Considerations
Preventing unauthorized access post-demise is critical.

## Compliance Considerations
Strict adherence to RBI guidelines on timely settlement of deceased claims.

## Related FAQs
- [General FAQ](../faqs/general-faq.md)

## Related Documents
- [Service Request Forms](../docs/forms/service-request-forms.md)
