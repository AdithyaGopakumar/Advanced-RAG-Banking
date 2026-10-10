"""Unit tests for transaction and operational scope guardrail."""

from app.ai.guardrails.scope import check_scope


def test_reject_direct_money_transfer():
    decision = check_scope("Please transfer 5000 to account 9876543210")
    assert not decision.allowed
    assert decision.reason_code == "TRANSACTION_OUT_OF_SCOPE"
    assert "cannot execute financial transactions" in (decision.response or "")


def test_reject_bill_payment():
    decision = check_scope("Pay electricity bill of 1500 rupees")
    assert not decision.allowed
    assert decision.reason_code == "TRANSACTION_OUT_OF_SCOPE"


def test_reject_personal_balance_enquiry():
    for q in ["Check my balance", "What is my account balance?", "Show me my bank statement"]:
        decision = check_scope(q)
        assert not decision.allowed, f"Expected reject for: {q}"
        assert decision.reason_code == "TRANSACTION_OUT_OF_SCOPE"


def test_reject_credential_change_and_blocking():
    for q in ["Reset my ATM PIN immediately", "Block my debit card", "Change my mobile number"]:
        decision = check_scope(q)
        assert not decision.allowed, f"Expected reject for: {q}"
        assert decision.reason_code == "TRANSACTION_OUT_OF_SCOPE"


def test_reject_direct_loan_application():
    decision = check_scope("Apply for a loan for me right now")
    assert not decision.allowed
    assert decision.reason_code == "TRANSACTION_OUT_OF_SCOPE"


def test_allow_informational_procedural_questions():
    informational_queries = [
        "How do I transfer money using NEFT?",
        "What is the procedure to reset ATM PIN?",
        "What are the rules for blocking a lost debit card?",
        "How can a customer check account balance through missed call service?",
        "What are the transaction charges for IMPS transfer?",
        "Who is eligible to apply for a home loan?",
        "Can a customer have multiple BSBDA accounts?",
    ]
    for q in informational_queries:
        decision = check_scope(q)
        assert decision.allowed, f"Expected allow for informational query: {q}"
        assert decision.reason_code == "IN_SCOPE"
