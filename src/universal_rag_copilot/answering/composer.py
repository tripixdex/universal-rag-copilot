"""Grounded answer composer for Stage 1."""

from __future__ import annotations

import re

from universal_rag_copilot.domain import AnswerResult, Citation, RetrievalResult
from universal_rag_copilot.retrieval.baseline import tokenize


def _best_snippets(text: str, query_terms: set[str], limit: int = 2) -> list[str]:
    snippets: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        sentence_terms = tokenize(sentence)
        if sentence_terms & query_terms:
            snippets.append(sentence.strip())
        if len(snippets) >= limit:
            break
    if not snippets and text:
        snippets.append(text.split(".")[0].strip() + ".")
    return [s for s in snippets if s]


def compose_answer(
    question: str, results: list[RetrievalResult], max_citations: int = 3
) -> AnswerResult:
    if not results or results[0].score < 0.07:
        return AnswerResult(
            answer="Not enough evidence in the indexed corpus to answer this question reliably.",
            citations=(),
            insufficient_evidence=True,
        )

    query_terms = tokenize(question)
    evidence_lines: list[str] = []
    citations: list[Citation] = []
    for result in results[:max_citations]:
        for snippet in _best_snippets(result.chunk.text, query_terms, limit=1):
            evidence_lines.append(snippet)
        citations.append(
            Citation(
                chunk_id=result.chunk.chunk_id,
                document_id=result.chunk.document_id,
                title=result.chunk.title,
                section=result.chunk.metadata.get("section", "Overview"),
                score=round(result.score, 4),
            )
        )

    answer = " ".join(evidence_lines).strip()
    if not answer:
        answer = "Not enough evidence in the indexed corpus to answer this question reliably."
        return AnswerResult(answer=answer, citations=tuple(citations), insufficient_evidence=True)

    return AnswerResult(answer=answer, citations=tuple(citations), insufficient_evidence=False)
