---
id: "SUP-BRN-001"
title: "Branch and Channel Information"
slug: "branch-information"
domain: "customer-support"
category: "support"
sub_category: "branch-information"
document_type: "reference"
applicable_to: "both"
target_audience: "both"
language: "en"
region: "IN"
keywords: ["branch hours", "ATM availability", "holidays", "branch locator"]
tags: ["reference:branch-info"]
search_aliases: ["bank timings", "working days", "is the bank open"]
priority: "medium"
related_documents: []
version: "1.0"
status: "current"
created_date: "2026-08-08"
last_updated: "2026-08-08"
effective_from: "2026-08-01"
effective_until: ""
source: "Operations Branch Network"
authority: "Operations"
owner: "Operations SME"
compliance_classification: "informational"
confidentiality: "public"
dynamic_content: true
dynamic_classification: "FREQUENTLY_DYNAMIC"
data_source: "branch-locator-api"
---

# Branch and Channel Information

## Overview

> [!WARNING]
> Branch hours and availability are subject to change due to local holidays or operational issues. According to the bank's current published network list, the standard hours apply. Always refer to the live branch locator API for real-time status.

This document outlines standard branch working hours and the schedule for national and regional banking holidays.

---

## Standard Working Hours

- **Weekdays**: 10:00 AM to 4:00 PM
- **Saturdays**: 10:00 AM to 4:00 PM (Open on 1st, 3rd, and 5th Saturdays only).
- **Sundays & 2nd/4th Saturdays**: Closed

*Note: Cash counters typically close 30 minutes before branch closing time.*

## Holiday Schedule

The bank observes all holidays mandated by the Reserve Bank of India (RBI) under the Negotiable Instruments Act. 
Since holidays vary by state, always route specific date queries to the live `branch-locator-api`.
