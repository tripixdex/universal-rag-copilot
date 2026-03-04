import json

from universal_rag_copilot.config import FIXTURES_DIR
from universal_rag_copilot.evaluation import run_evaluation


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
        "actual_top_document_ids",
        "actual_citation_titles",
    }
