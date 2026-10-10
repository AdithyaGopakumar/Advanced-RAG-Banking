"""Deterministic PII detection and redaction for banking queries and outputs.

Detects and masks sensitive Indian financial identifiers:
- Permanent Account Number (PAN)
- Aadhaar (12-digit UID)
- Payment Cards (Credit / Debit Card 15-16 digits)
- Card Verification Value (CVV / CVC)
- Bank Account Numbers (9-18 digits with explicit context)
"""

import re
from typing import NamedTuple

# Indian PAN Card: 5 uppercase letters, 4 digits, 1 uppercase letter
_PAN_PATTERN = re.compile(r"\b[A-Za-z]{5}[0-9]{4}[A-Za-z]\b")

# Indian Aadhaar: 12 digits, first digit is 2-9, optional space or hyphen separators
_AADHAAR_PATTERN = re.compile(r"\b[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}\b")

# Payment Card numbers (16-digit cards, 15-digit Amex, 4-4-4-4 formatted)
_CARD_PATTERN = re.compile(
    r"\b(?:"
    r"4\d{3}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}"  # Visa
    r"|5[1-5]\d{2}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}"  # Mastercard
    r"|6(?:011|5\d{2})[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}"  # Discover / RuPay
    r"|3[47]\d{2}[ -]?\d{6}[ -]?\d{5}"  # Amex
    r"|(?:\d{4}[ -]){3}\d{4}"  # Generic 4x4
    r"|\d{16}"  # 16 contiguous digits
    r")\b"
)

# CVV / CVC preceded by keyword
_CVV_PATTERN = re.compile(
    r"(?i)\b(?:cvv|cvc|security code|card verification value)[\s#:=-]*(\d{3,4})\b"
)

# Bank Account Number: 9 to 18 digits explicitly prefixed with account markers
_ACCOUNT_PATTERN = re.compile(
    r"(?i)\b(?:saving\s+|savings\s+|current\s+)?(?:account|acct|a/c|acc\.?)(?:\s*(?:number|no\.?|num\.?))?(?:\s*(?:is|:|=|-|#))?\s*(\d{9,18})\b"
)


class PIIMatch(NamedTuple):
    """Details of a detected PII pattern."""

    category: str
    original: str
    redacted: str


def redact_pii(text: str) -> tuple[str, list[PIIMatch]]:
    """Mask sensitive banking PII in text and return sanitized string and matches."""
    if not text:
        return text, []

    matches: list[PIIMatch] = []
    sanitized = text

    # 1. CVV (replace only the digits group)
    def _replace_cvv(match: re.Match[str]) -> str:
        full = match.group(0)
        digits = match.group(1)
        matches.append(PIIMatch(category="CVV", original=digits, redacted="[REDACTED_CVV]"))
        return full.replace(digits, "[REDACTED_CVV]")

    sanitized = _CVV_PATTERN.sub(_replace_cvv, sanitized)

    # 2. Bank Account Number (replace only the digits group)
    def _replace_account(match: re.Match[str]) -> str:
        full = match.group(0)
        digits = match.group(1)
        matches.append(PIIMatch(category="ACCOUNT_NUMBER", original=digits, redacted="[REDACTED_ACCOUNT]"))
        return full.replace(digits, "[REDACTED_ACCOUNT]")

    sanitized = _ACCOUNT_PATTERN.sub(_replace_account, sanitized)

    # 3. Payment Cards
    for card_match in _CARD_PATTERN.finditer(sanitized):
        val = card_match.group(0)
        # Avoid double-redacting placeholders
        if "[REDACTED" not in val:
            matches.append(PIIMatch(category="CARD_NUMBER", original=val, redacted="[REDACTED_CARD]"))
    sanitized = _CARD_PATTERN.sub("[REDACTED_CARD]", sanitized)

    # 4. PAN Card
    for pan_match in _PAN_PATTERN.finditer(sanitized):
        val = pan_match.group(0)
        if "[REDACTED" not in val:
            matches.append(PIIMatch(category="PAN", original=val, redacted="[REDACTED_PAN]"))
    sanitized = _PAN_PATTERN.sub("[REDACTED_PAN]", sanitized)

    # 5. Aadhaar
    for aadhaar_match in _AADHAAR_PATTERN.finditer(sanitized):
        val = aadhaar_match.group(0)
        if "[REDACTED" not in val:
            matches.append(PIIMatch(category="AADHAAR", original=val, redacted="[REDACTED_AADHAAR]"))
    sanitized = _AADHAAR_PATTERN.sub("[REDACTED_AADHAAR]", sanitized)

    return sanitized, matches


def has_pii(text: str) -> bool:
    """Check whether text contains any unredacted PII patterns."""
    _, matches = redact_pii(text)
    return len(matches) > 0
