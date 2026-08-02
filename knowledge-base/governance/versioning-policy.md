# Versioning Policy

This document defines how versions are tracked for individual documents and for the knowledge base repository as a whole.

---

## Why Versioning Matters

Versioning enables:

1. **Traceability** — Know what changed, when, and why
2. **Currency** — Identify outdated documents quickly
3. **Citations** — AI systems can reference specific document versions
4. **Rollback** — Revert to a previous version if errors are introduced
5. **Audit Trail** — Demonstrate regulatory compliance over time

---

## Two-Level Versioning

The knowledge base uses two independent versioning layers:

| Level | What It Tracks | Where It Lives |
|---|---|---|
| **Repository Version** | Major releases of the entire knowledge base | [CHANGELOG.md](../CHANGELOG.md) |
| **Document Version** | Individual document changes | YAML frontmatter `version` field |

---

## Repository Versioning

The repository follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

**Format**: `MAJOR.MINOR.PATCH`

| Component | When to Increment | Example |
|---|---|---|
| **MAJOR** | Significant structural changes, major content overhauls, or breaking changes to metadata schema | 1.0.0 → 2.0.0 |
| **MINOR** | New document categories, new templates, governance updates, or batches of new documents | 1.0.0 → 1.1.0 |
| **PATCH** | Individual document additions, corrections, or minor updates | 1.0.0 → 1.0.1 |

### Repository Version History

All repository version changes are recorded in [CHANGELOG.md](../CHANGELOG.md) following the [Keep a Changelog](https://keepachangelog.com/) format.

---

## Document Versioning

Individual documents track their own version in YAML frontmatter:

```yaml
version: "1.2"
```

**Format**: `MAJOR.MINOR`

| Component | When to Increment | Example |
|---|---|---|
| **MAJOR** | Significant content restructuring, major section additions/removals, or fundamental information changes | 1.2 → 2.0 |
| **MINOR** | Content updates (rate changes, process updates, new entries), corrections, or clarifications | 1.2 → 1.3 |

### Rules

- New documents start at version `1.0`
- The `last_updated` date must be updated with every version change
- The `last_reviewed` date must be updated whenever the document is reviewed, even if no changes are made
- Version history is tracked through Git commit history (not within the document itself)

---

## Date Tracking Fields

Every document tracks these dates in its YAML frontmatter:

| Field | Description | Format | Updated When |
|---|---|---|---|
| `last_updated` | Date of last content modification | YYYY-MM-DD | Any content change |
| `last_reviewed` | Date of last review (even if no changes) | YYYY-MM-DD | Any review, including "no changes needed" |

---

## What Counts as a Version Change

### Increment the Version

- Changing interest rates, fees, or charges
- Updating eligibility criteria
- Adding or removing process steps
- Correcting factual errors
- Adding new sections
- Removing deprecated sections
- Updating regulatory references

### Do NOT Increment the Version

- Fixing typos or spelling errors
- Adjusting formatting without changing content
- Updating internal links
- Adding or adjusting metadata keywords
- Rewording sentences without changing meaning

Even when the version does not change, `last_updated` must still be updated.

---

## Version Tracking in Practice

### Example: Savings Account Document

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-15 | Initial document created |
| 1.1 | 2026-09-01 | Updated interest rates for Q3 |
| 1.2 | 2026-10-15 | Added senior citizen special rate tier |
| 2.0 | 2026-12-01 | Restructured to separate digital and branch processes |

---

## Git Tags

Repository milestones are marked with Git tags:

```bash
git tag -a v1.0.0 -m "Phase 1: Foundation and Standards"
git tag -a v1.1.0 -m "Phase 2: Core Products and Templates"
```

---

## Related Documents

- [CHANGELOG.md](../CHANGELOG.md) — Repository-level version history
- [Maintenance Strategy](maintenance-strategy.md) — Update schedules and review cadence
- [Contribution Guide](contribution-guide.md) — How to submit versioned changes

---

*Last updated: 2026-08-02*
