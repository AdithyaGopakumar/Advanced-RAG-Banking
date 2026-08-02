# Contributing to the Banking Knowledge Base

Thank you for contributing to the Bank's customer support knowledge base. This guide explains how to add, update, or review documentation in this repository.

---

## Before You Start

1. Read the [Style Guide](governance/style-guide.md) to understand writing standards
2. Review the [Documentation Standards](governance/documentation-standards.md) for formatting rules
3. Familiarise yourself with the [Naming Conventions](governance/naming-conventions.md)
4. Understand the [Repository Rules](governance/repository-rules.md)

---

## Contribution Workflow

### Step 1 — Create a Branch

Create a feature branch from `main` using the naming convention:

```
docs/<category>/<short-description>
```

Examples:

```
docs/accounts/add-savings-account
docs/governance/update-style-guide
docs/loans/fix-home-loan-eligibility
```

### Step 2 — Make Changes

- Use the appropriate [template](templates/README.md) for new documents
- Follow all governance standards
- Include complete YAML frontmatter metadata
- Add cross-references to related documents where applicable

### Step 3 — Self-Review

Before submitting, verify:

- [ ] Document follows the style guide
- [ ] All required metadata fields are present
- [ ] No duplicate information (cross-reference instead)
- [ ] Document is self-contained and understandable independently
- [ ] Spelling and grammar are correct
- [ ] All internal links are valid
- [ ] Customer-facing language is clear and simple

### Step 4 — Submit a Pull Request

- Use a descriptive PR title: `docs(<category>): <brief description>`
- Include a summary of changes in the PR description
- Tag appropriate reviewers (see [CODEOWNERS](CODEOWNERS))
- Link to any related issues or documents

### Step 5 — Address Review Feedback

- Respond to all review comments
- Make requested changes promptly
- Request re-review after updates

---

## Types of Contributions

| Type | Description | Approval Required |
|---|---|---|
| New Document | Adding a new product, service, or policy document | SME + Technical Writer |
| Content Update | Updating existing information (rates, processes) | SME |
| Correction | Fixing errors, typos, or outdated information | Technical Writer |
| Structural Change | Modifying folder structure, templates, or governance | Knowledge Base Owner |
| Metadata Update | Changing frontmatter or metadata schema | Knowledge Base Owner + AI Engineer |

---

## Commit Message Format

Use the following format for commit messages:

```
docs(<scope>): <short description>

<optional body explaining the change>
```

**Scopes**: `accounts`, `deposits`, `loans`, `cards`, `digital-banking`, `payments`, `services`, `policies`, `security`, `support`, `charges`, `rates`, `forms`, `faqs`, `scenarios`, `guides`, `glossary`, `governance`, `templates`, `metadata`

**Examples**:

```
docs(accounts): add savings account documentation
docs(governance): update review process checklist
docs(loans): fix home loan eligibility criteria
docs(faqs): add UPI transaction limit questions
```

---

## What NOT to Do

- Do not duplicate content that exists in another document — use cross-references instead
- Do not include internal employee procedures or confidential information
- Do not use marketing language or promotional content
- Do not include customer-specific data or personally identifiable information (PII)
- Do not modify governance documents without approval from the Knowledge Base Owner
- Do not create documents outside the established folder structure

---

## Questions?

If you are unsure about anything, refer to the [Governance Documentation](governance/README.md) or reach out to the Knowledge Base Owner.

---

*Last updated: 2026-08-02*
