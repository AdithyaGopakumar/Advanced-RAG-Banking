---
id: "SCEN-CARD-001"
title: "Lost Card & Replacement"
slug: "lost-card-replacement"
domain: "cross-cutting"
category: "scenarios"
sub_category: "lost-card-replacement"
document_type: "scenario"
applicable_to: "individual"
target_audience: "customer"
language: "en"
region: "IN"
keywords: ["lost card", "stolen card", "replace card", "block card", "new debit card"]
search_aliases: ["lost my debit card", "credit card stolen", "get a replacement card"]
tags: ["intent:block_card", "security:high"]
priority: "high"
related_documents: ["SEC-CARD-001", "CHG-CARD-001"]
version: "1.0"
status: "current"
owner: "Technical Writing Lead"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
---

# Lost Card & Replacement Scenario

## Situation
The customer has physically lost their debit or credit card, or it has been stolen, and they need to secure their account and get a new card.

## Customer Intent
`block_card` / `replace_card`

## What the Customer May Say
- "I dropped my wallet and lost my debit card."
- "My credit card was stolen."
- "I can't find my card, please block it and send a new one."

## Relevant Information
A blocked card cannot be unblocked. Replacement cards are mailed to the registered address and usually incur a replacement fee.

## Recommended Response Path
Treat as high priority. Guide the customer to permanently block the card immediately via the Mobile App 'Manage Cards' section or the emergency toll-free number. Explain that they can request a replacement card simultaneously during the block process.

## Immediate Action
Route to LIVE API to block card if channel supports it.

## Next Steps
Customer blocks card and verifies mailing address for replacement.

## Exceptions
- **Unauthorized Transactions**: If the card was used after being lost, pivot to the `fraud-reporting` scenario immediately.
- **Card Temporarily Misplaced**: Customer can choose to 'Temporarily Lock' the card instead of a permanent block if they think they might find it.

## When to Escalate
If the customer is unable to authenticate to block the card, route immediately to human support.

## Dynamic Information Required
- Card replacement fees.

## Live Banking Data Required
- Customer's active cards list.

## Security Considerations
**HIGH**. Ensure the card is blocked immediately.

## Compliance Considerations
None.

## Related FAQs
- [Cards FAQ](../faqs/cards-faq.md)

## Related Documents
- [Card Security Guidelines](../docs/security/card-security.md)
- [Card Charges](../docs/charges/card-charges.md)
