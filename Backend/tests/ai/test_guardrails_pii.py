"""Unit tests for deterministic PII detection and redaction."""

from app.ai.guardrails.pii import has_pii, redact_pii


def test_redact_pan_card():
    text = "My PAN number is ABCDE1234F and I want to know about accounts."
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_PAN]" in sanitized
    assert "ABCDE1234F" not in sanitized
    assert len(matches) == 1
    assert matches[0].category == "PAN"
    assert matches[0].original == "ABCDE1234F"


def test_redact_aadhaar_number():
    text = "Here is my Aadhaar: 5432 1234 5678 for opening an account."
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_AADHAAR]" in sanitized
    assert "5432 1234 5678" not in sanitized
    assert len(matches) == 1
    assert matches[0].category == "AADHAAR"


def test_redact_payment_card():
    text = "My debit card number is 4111-2222-3333-4444, what is the expiry rule?"
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_CARD]" in sanitized
    assert "4111-2222-3333-4444" not in sanitized
    assert len(matches) == 1
    assert matches[0].category == "CARD_NUMBER"


def test_redact_cvv():
    text = "Security code is CVV: 789 on the back."
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_CVV]" in sanitized
    assert "789" not in sanitized
    assert len(matches) == 1
    assert matches[0].category == "CVV"


def test_redact_account_number():
    text = "Please check account # 1234567890123 for fees."
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_ACCOUNT]" in sanitized
    assert "1234567890123" not in sanitized
    assert len(matches) == 1
    assert matches[0].category == "ACCOUNT_NUMBER"


def test_multiple_pii_in_one_query():
    text = "PAN: ABCDE1234F, Aadhaar: 9876-5432-1098, card: 5123 4567 8901 2345"
    sanitized, matches = redact_pii(text)
    assert "[REDACTED_PAN]" in sanitized
    assert "[REDACTED_AADHAAR]" in sanitized
    assert "[REDACTED_CARD]" in sanitized
    assert len(matches) == 3


def test_text_without_pii_remains_intact():
    text = "Who is eligible to open a Basic Savings Bank Deposit Account?"
    sanitized, matches = redact_pii(text)
    assert sanitized == text
    assert matches == []
    assert not has_pii(text)


def test_has_pii_returns_true_when_pii_present():
    assert has_pii("My PAN is BNZPA9988C")
    assert not has_pii("What are the transaction limits for BSBDA?")
