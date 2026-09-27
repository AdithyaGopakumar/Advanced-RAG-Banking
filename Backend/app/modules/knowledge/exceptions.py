"""Knowledge-engineering exceptions."""

from app.modules.knowledge.models import ValidationIssue


class KnowledgeValidationError(Exception):
    """A source file could not be accepted as a knowledge document."""

    def __init__(self, source_path: str, issues: list[ValidationIssue]) -> None:
        self.source_path = source_path
        self.issues = issues
        messages = "; ".join(issue.message for issue in issues) or "validation failed"
        super().__init__(f"{source_path}: {messages}")
