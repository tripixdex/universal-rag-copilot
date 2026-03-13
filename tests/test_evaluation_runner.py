import json

from universal_rag_copilot.config import FIXTURES_DIR
from universal_rag_copilot.evaluation import run_evaluation
from universal_rag_copilot.evaluation.runner import _matches_expected_sources, load_eval_cases


def test_evaluation_runner_output_shape(tmp_path) -> None:
    results, json_path, md_path = run_evaluation(
        cases_path=FIXTURES_DIR / "eval" / "cases.json",
        output_dir=tmp_path,
    )

    assert results
    assert json_path.exists()
    assert md_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert set(payload) == {"generated_at_utc", "total_cases", "passed_cases", "cases"}
    assert payload["total_cases"] == len(results)
    assert payload["total_cases"] >= 15
    assert isinstance(payload["passed_cases"], int)

    first_case = payload["cases"][0]
    assert set(first_case) == {
        "case_id",
        "mode",
        "profile",
        "question",
        "expected_answerability",
        "actual_answerability",
        "answerability_match",
        "expected_source_match",
        "actual_top_document_id",
        "actual_top_document_ids",
        "actual_citation_titles",
    }


def test_load_eval_cases_expanded_fixture_set() -> None:
    cases = load_eval_cases(FIXTURES_DIR / "eval" / "cases.json")
    assert len(cases) >= 15
    assert any(case.expected_answerability.value == "not_enough_evidence" for case in cases)
    assert any(case.expected_top_document_id for case in cases)


def test_expected_source_matching_requires_subset_and_top_rank() -> None:
    assert _matches_expected_sources(
        expected_document_ids=("billing_and_invoices",),
        expected_citation_titles=("Billing and Invoices",),
        expected_top_document_id="billing_and_invoices",
        actual_document_ids=("billing_and_invoices", "returns_and_refunds"),
        actual_citation_titles=("Billing and Invoices",),
    )
    assert not _matches_expected_sources(
        expected_document_ids=("billing_and_invoices",),
        expected_citation_titles=("Billing and Invoices",),
        expected_top_document_id="billing_and_invoices",
        actual_document_ids=("returns_and_refunds", "billing_and_invoices"),
        actual_citation_titles=("Billing and Invoices",),
    )
    assert not _matches_expected_sources(
        expected_document_ids=("billing_and_invoices", "account_access_security"),
        expected_citation_titles=("Billing and Invoices",),
        expected_top_document_id="billing_and_invoices",
        actual_document_ids=("billing_and_invoices",),
        actual_citation_titles=("Billing and Invoices",),
    )


def test_expected_source_matching_for_unanswerable_case_requires_no_citations() -> None:
    assert _matches_expected_sources(
        expected_document_ids=(),
        expected_citation_titles=(),
        expected_top_document_id=None,
        actual_document_ids=(),
        actual_citation_titles=(),
    )
    assert not _matches_expected_sources(
        expected_document_ids=(),
        expected_citation_titles=(),
        expected_top_document_id=None,
        actual_document_ids=("returns_and_refunds",),
        actual_citation_titles=("Returns and Refunds",),
    )
