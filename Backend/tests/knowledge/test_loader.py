"""Directory loading tests for the knowledge foundation."""

from pathlib import Path

from app.modules.knowledge.loader import load_documents, resolve_knowledge_root

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[3] / "knowledge-base"


def test_loader_skips_non_markdown_and_excluded_trees(tmp_path):
    corpus = tmp_path / "knowledge-base"
    accounts = corpus / "docs" / "accounts"
    accounts.mkdir(parents=True)
    (corpus / "faqs").mkdir()
    (corpus / "scenarios").mkdir()
    (corpus / "decision-guides").mkdir()
    (corpus / "glossary").mkdir()
    governance = corpus / "governance"
    governance.mkdir()
    (accounts / "notes.txt").write_text("ignore me", encoding="utf-8")
    (accounts / "savings.md").write_text(
        "---\nid: ACCT-SA-001\ntitle: Savings Account\nslug: savings\n"
        "document_type: product\nversion: '1.0'\nstatus: approved\n---\n\n"
        "# Savings Account\n\n## Eligibility\n\nResident individuals.\n",
        encoding="utf-8",
    )
    (governance / "rules.md").write_text(
        "---\nid: GOV-001\ntitle: Rules\nslug: rules\n"
        "document_type: policy\nversion: '1.0'\nstatus: draft\n---\n\n"
        "# Rules\n",
        encoding="utf-8",
    )

    result = load_documents(corpus)

    assert [document.document_id for document in result.documents] == ["ACCT-SA-001"]
    assert result.failures == []
    assert all("governance" not in document.source_path for document in result.documents)


def test_explicit_directory_can_load_an_otherwise_excluded_tree(tmp_path):
    governance = tmp_path / "governance"
    governance.mkdir()
    (governance / "rules.md").write_text(
        "---\nid: GOV-001\ntitle: Rules\nslug: rules\n"
        "document_type: policy\nversion: '1.0'\nstatus: draft\n---\n\n"
        "# Rules\n",
        encoding="utf-8",
    )

    result = load_documents(governance)

    assert [document.document_id for document in result.documents] == ["GOV-001"]


def test_real_account_documents_load():
    result = load_documents(KNOWLEDGE_ROOT / "docs" / "accounts")

    assert [failure.source_path for failure in result.failures] == ["docs/accounts/README.md"]
    assert any(document.document_id == "ACCT-BSBDA-001" for document in result.documents)
    assert len(result.documents) == 12


def test_knowledge_root_skips_governance_directory():
    result = load_documents(KNOWLEDGE_ROOT)
    loaded_paths = [document.source_path for document in result.documents]
    failed_paths = [failure.source_path for failure in result.failures]

    assert resolve_knowledge_root(KNOWLEDGE_ROOT) == KNOWLEDGE_ROOT.resolve()
    assert any(path == "docs/accounts/bsbda.md" for path in loaded_paths)
    assert all(not path.startswith("governance/") for path in loaded_paths)
    assert all(not path.startswith("templates/") for path in loaded_paths)
    assert all(not path.startswith("governance/") for path in failed_paths)
    assert all(not path.startswith("metadata/") for path in failed_paths)
