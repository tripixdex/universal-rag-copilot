"""Explicit retrieval pipeline with quality controls."""

from __future__ import annotations

from dataclasses import dataclass

from universal_rag_copilot.answering import compose_answer
from universal_rag_copilot.domain import Answerability, AnswerResult, RetrievalResult
from universal_rag_copilot.retrieval.baseline import RetrievalIndex, retrieve


@dataclass(frozen=True)
class RetrievalConfig:
    top_k: int = 4
    min_score_threshold: float = 0.07
    min_evidence_results: int = 1


@dataclass(frozen=True)
class RetrievalDecision:
    question: str
    config: RetrievalConfig
    retrieved: tuple[RetrievalResult, ...]
    eligible: tuple[RetrievalResult, ...]
    answerability: Answerability


def retrieve_candidates(index: RetrievalIndex, query: str, top_k: int) -> list[RetrievalResult]:
    return retrieve(index=index, query=query, top_k=top_k)


def score_candidates(
    candidates: list[RetrievalResult], min_score_threshold: float
) -> list[RetrievalResult]:
    return [item for item in candidates if item.score >= min_score_threshold]


def assess_evidence(
    eligible_results: list[RetrievalResult], min_evidence_results: int
) -> Answerability:
    if len(eligible_results) < max(1, min_evidence_results):
        return Answerability.NOT_ENOUGH_EVIDENCE
    return Answerability.ANSWERABLE


def run_retrieval(
    *,
    index: RetrievalIndex,
    question: str,
    config: RetrievalConfig,
) -> RetrievalDecision:
    retrieved = retrieve_candidates(index=index, query=question, top_k=config.top_k)
    eligible = score_candidates(retrieved, min_score_threshold=config.min_score_threshold)
    answerability = assess_evidence(eligible, min_evidence_results=config.min_evidence_results)
    return RetrievalDecision(
        question=question,
        config=config,
        retrieved=tuple(retrieved),
        eligible=tuple(eligible),
        answerability=answerability,
    )


def answer_from_retrieval(decision: RetrievalDecision) -> AnswerResult:
    return compose_answer(
        question=decision.question,
        results=list(decision.eligible),
        answerability=decision.answerability,
    )
