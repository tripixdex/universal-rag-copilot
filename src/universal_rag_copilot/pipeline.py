"""Small orchestration helpers for demo flows."""

from __future__ import annotations

from universal_rag_copilot.answering import compose_answer
from universal_rag_copilot.chunking import chunk_documents
from universal_rag_copilot.domain import AnswerResult, ChunkProfile, CorpusMode
from universal_rag_copilot.ingestion import load_fixture_documents
from universal_rag_copilot.retrieval import RetrievalIndex, build_index, retrieve


def build_demo_index(mode: CorpusMode, profile: ChunkProfile) -> tuple[RetrievalIndex, int, int]:
    documents = load_fixture_documents(mode)
    chunks = chunk_documents(documents, profile)
    return build_index(chunks), len(documents), len(chunks)


def ask_demo(
    question: str, mode: CorpusMode, profile: ChunkProfile, top_k: int = 4
) -> AnswerResult:
    index, _, _ = build_demo_index(mode=mode, profile=profile)
    results = retrieve(index=index, query=question, top_k=top_k)
    return compose_answer(question=question, results=results)
