"""Retrieval baseline exports."""

from universal_rag_copilot.retrieval.baseline import RetrievalIndex, build_index, retrieve
from universal_rag_copilot.retrieval.pipeline import (
    RetrievalConfig,
    RetrievalDecision,
    answer_from_retrieval,
    assess_evidence,
    retrieve_candidates,
    run_retrieval,
    score_candidates,
)

__all__ = [
    "RetrievalConfig",
    "RetrievalDecision",
    "RetrievalIndex",
    "answer_from_retrieval",
    "assess_evidence",
    "build_index",
    "retrieve",
    "retrieve_candidates",
    "run_retrieval",
    "score_candidates",
]
