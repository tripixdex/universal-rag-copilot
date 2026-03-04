"""Local evaluation harness for retrieval and answerability."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from universal_rag_copilot.config import FIXTURES_DIR, OUTPUTS_DIR
from universal_rag_copilot.domain import Answerability, ChunkProfile, CorpusMode
from universal_rag_copilot.pipeline import ask_demo_with_decision
from universal_rag_copilot.retrieval import RetrievalConfig


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    mode: CorpusMode
    profile: ChunkProfile
    question: str
    expected_document_ids: tuple[str, ...]
    expected_citation_titles: tuple[str, ...]
    expected_answerability: Answerability


@dataclass(frozen=True)
class EvalCaseResult:
    case_id: str
    mode: str
    profile: str
    question: str
    expected_answerability: str
    actual_answerability: str
    answerability_match: bool
    expected_source_match: bool
    actual_top_document_ids: tuple[str, ...]
    actual_citation_titles: tuple[str, ...]


def _parse_case(raw: dict[str, object]) -> EvalCase:
    return EvalCase(
        case_id=str(raw["case_id"]),
        mode=CorpusMode(str(raw["mode"])),
        profile=ChunkProfile(str(raw["profile"])),
        question=str(raw["question"]),
        expected_document_ids=tuple(str(v) for v in raw.get("expected_document_ids", [])),
        expected_citation_titles=tuple(str(v) for v in raw.get("expected_citation_titles", [])),
        expected_answerability=Answerability(str(raw["expected_answerability"])),
    )


def load_eval_cases(path: Path) -> list[EvalCase]:
    raw_cases = json.loads(path.read_text(encoding="utf-8"))
    return [_parse_case(item) for item in raw_cases]


def _matches_expected_sources(
    expected_document_ids: tuple[str, ...],
    expected_citation_titles: tuple[str, ...],
    actual_document_ids: tuple[str, ...],
    actual_citation_titles: tuple[str, ...],
) -> bool:
    if expected_document_ids and not set(expected_document_ids) & set(actual_document_ids):
        return False
    if expected_citation_titles and not set(expected_citation_titles) & set(actual_citation_titles):
        return False
    return True


def run_evaluation(
    *,
    cases_path: Path | None = None,
    output_dir: Path | None = None,
    config: RetrievalConfig | None = None,
) -> tuple[list[EvalCaseResult], Path, Path]:
    effective_cases_path = cases_path or (FIXTURES_DIR / "eval" / "cases.json")
    effective_output_dir = output_dir or (OUTPUTS_DIR / "eval")
    results: list[EvalCaseResult] = []
    for case in load_eval_cases(effective_cases_path):
        answer, decision = ask_demo_with_decision(
            question=case.question,
            mode=case.mode,
            profile=case.profile,
            config=config or RetrievalConfig(),
        )
        actual_docs = tuple(item.chunk.document_id for item in decision.retrieved)
        actual_titles = tuple(c.title for c in answer.citations)
        answerability_match = answer.answerability is case.expected_answerability
        expected_source_match = _matches_expected_sources(
            expected_document_ids=case.expected_document_ids,
            expected_citation_titles=case.expected_citation_titles,
            actual_document_ids=actual_docs,
            actual_citation_titles=actual_titles,
        )
        results.append(
            EvalCaseResult(
                case_id=case.case_id,
                mode=case.mode.value,
                profile=case.profile.value,
                question=case.question,
                expected_answerability=case.expected_answerability.value,
                actual_answerability=answer.answerability.value,
                answerability_match=answerability_match,
                expected_source_match=expected_source_match,
                actual_top_document_ids=actual_docs,
                actual_citation_titles=actual_titles,
            )
        )

    return _write_reports(results=results, output_dir=effective_output_dir)


def _write_reports(
    *, results: list[EvalCaseResult], output_dir: Path
) -> tuple[list[EvalCaseResult], Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    base_name = f"eval_{timestamp}"
    json_path = output_dir / f"{base_name}.json"
    md_path = output_dir / f"{base_name}.md"

    payload = {
        "generated_at_utc": timestamp,
        "total_cases": len(results),
        "passed_cases": sum(
            1 for item in results if item.answerability_match and item.expected_source_match
        ),
        "cases": [item.__dict__ for item in results],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Evaluation Report",
        "",
        f"Generated at (UTC): {timestamp}",
        f"Total cases: {payload['total_cases']}",
        f"Passed cases: {payload['passed_cases']}",
        "",
        "| Case ID | Mode | Profile | Answerability | Source Match |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            f"| {item.case_id} | {item.mode} | {item.profile} | "
            f"{item.answerability_match} ({item.actual_answerability}) | "
            f"{item.expected_source_match} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return results, json_path, md_path
