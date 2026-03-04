from universal_rag_copilot.config import FIXTURES_DIR
from universal_rag_copilot.domain import Answerability, ChunkProfile, CorpusMode
from universal_rag_copilot.evaluation.runner import load_eval_cases
from universal_rag_copilot.pipeline import ask_demo, ask_demo_with_decision, build_demo_index
from universal_rag_copilot.retrieval import RetrievalConfig, run_retrieval


def test_answerability_threshold_behavior() -> None:
    index, _, _ = build_demo_index(CorpusMode.SUPPORT_KB, ChunkProfile.BALANCED)
    question = "How long do card refunds take to settle?"

    default_decision = run_retrieval(index=index, question=question, config=RetrievalConfig())
    strict_decision = run_retrieval(
        index=index,
        question=question,
        config=RetrievalConfig(min_score_threshold=0.2),
    )

    assert default_decision.answerability is Answerability.ANSWERABLE
    assert strict_decision.answerability is Answerability.NOT_ENOUGH_EVIDENCE


def test_retrieval_support_case_hits_expected_source() -> None:
    case = next(
        c
        for c in load_eval_cases(FIXTURES_DIR / "eval" / "cases.json")
        if c.mode is CorpusMode.SUPPORT_KB and c.expected_document_ids
    )
    _, decision = ask_demo_with_decision(
        question=case.question, mode=case.mode, profile=case.profile
    )
    assert decision.retrieved
    assert {r.chunk.document_id for r in decision.retrieved} & set(case.expected_document_ids)


def test_retrieval_academic_case_hits_expected_source() -> None:
    case = next(
        c
        for c in load_eval_cases(FIXTURES_DIR / "eval" / "cases.json")
        if c.mode is CorpusMode.ACADEMIC_PDF and c.expected_document_ids
    )
    _, decision = ask_demo_with_decision(
        question=case.question, mode=case.mode, profile=case.profile
    )
    assert decision.retrieved
    assert {r.chunk.document_id for r in decision.retrieved} & set(case.expected_document_ids)


def test_insufficient_evidence_case_is_unanswerable() -> None:
    answer = ask_demo(
        question="How do I renew a passport in Canada?",
        mode=CorpusMode.SUPPORT_KB,
        profile=ChunkProfile.BALANCED,
    )
    assert answer.answerability is Answerability.NOT_ENOUGH_EVIDENCE
    assert answer.insufficient_evidence is True
    assert not answer.citations
