"""Unit tests for output guardrails and output PII sanitization."""

from app.ai.guardrails.output import SAFE_FALLBACK, output_is_safe, sanitize_output
from app.ai.prompts.generation import GENERATION_SYSTEM_PROMPT


def test_safe_output_passes():
    text = "A resident Indian who is 18 years and above can open a BSBDA account."
    assert output_is_safe(text)


def test_empty_output_fails():
    assert not output_is_safe("")
    assert not output_is_safe("   \n  ")


def test_system_prompt_echo_fails():
    assert not output_is_safe(GENERATION_SYSTEM_PROMPT[:60])
    assert not output_is_safe("Here is the answer: <<<evidence>>>")
    assert not output_is_safe("You are a helpful banking assistant answering from documents.")


def test_traceback_leak_fails():
    traceback_text = "Traceback (most recent call last):\n  File 'app.py', line 12, in <module>\nValueError"
    assert not output_is_safe(traceback_text)


def test_output_pii_sanitization():
    draft = "Your account number is 1234567890123 and PAN is ABCDE1234F."
    sanitized = sanitize_output(draft)
    assert "[REDACTED_ACCOUNT]" in sanitized
    assert "[REDACTED_PAN]" in sanitized
    assert "1234567890123" not in sanitized
    assert "ABCDE1234F" not in sanitized
