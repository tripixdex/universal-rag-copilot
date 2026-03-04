"""Small orchestration helpers for demo flows."""

from __future__ import annotations

from universal_rag_copilot.chunking import chunk_documents
from universal_rag_copilot.domain import AnswerResult, ChunkProfile, CorpusMode
from universal_rag_copilot.ingestion import load_fixture_documents
from universal_rag_copilot.retrieval import (
    RetrievalConfig,
    RetrievalDecision,
    RetrievalIndex,
    answer_from_retrieval,
    build_index,
    run_retrieval,
)


def build_demo_index(mode: CorpusMode, profile: ChunkProfile) -> tuple[RetrievalIndex, int, int]:
    documents = load_fixture_documents(mode)
    chunks = chunk_documents(documents, profile)
    return build_index(chunks), len(documents), len(chunks)


def ask_demo(
    question: str,
    mode: CorpusMode,
    profile: ChunkProfile,
    top_k: int = 4,
    min_score_threshold: float = 0.07,
    min_evidence_results: int = 1,
) -> AnswerResult:
    index, _, _ = build_demo_index(mode=mode, profile=profile)
    decision = run_retrieval(
        index=index,
        question=question,
        config=RetrievalConfig(
            top_k=top_k,
            min_score_threshold=min_score_threshold,
            min_evidence_results=min_evidence_results,
        ),
    )
    return answer_from_retrieval(decision)


def ask_demo_with_decision(
    question: str,
    mode: CorpusMode,
    profile: ChunkProfile,
    config: RetrievalConfig | None = None,
) -> tuple[AnswerResult, RetrievalDecision]:
    index, _, _ = build_demo_index(mode=mode, profile=profile)
    decision = run_retrieval(
        index=index,
        question=question,
        config=config or RetrievalConfig(),
    )
    return answer_from_retrieval(decision), decision
