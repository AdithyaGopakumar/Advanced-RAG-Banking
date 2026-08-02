# Assets

This folder contains static resources used across the knowledge base, such as images, diagrams, and other media files.

---

## Folder Structure

```
assets/
├── images/          # Screenshots, product images, and illustrations
├── diagrams/        # Process flows, architecture diagrams, and charts
└── icons/           # Icons and small graphics
```

---

## Naming Conventions

All asset files must follow these naming rules:

- **Lowercase only** with hyphens as separators
- **Descriptive names** that indicate content and context
- **Category prefix** matching the documentation category

### Examples

```
accounts-savings-opening-process.png
loans-home-loan-eligibility-flow.svg
payments-neft-transfer-steps.png
cards-credit-card-comparison-chart.svg
```

---

## Supported Formats

| Type | Preferred Format | Alternatives |
|---|---|---|
| Screenshots | PNG | JPEG |
| Diagrams | SVG | PNG |
| Icons | SVG | PNG |
| Process Flows | SVG (Mermaid source in docs) | PNG |

---

## Usage in Documents

Reference assets using relative paths from the document location:

```markdown
![Savings Account Opening Process](../../assets/images/accounts-savings-opening-process.png)
```

---

## Related Resources

- [governance/naming-conventions.md](../governance/naming-conventions.md) — Full naming convention rules

---

*Last updated: 2026-08-02*
