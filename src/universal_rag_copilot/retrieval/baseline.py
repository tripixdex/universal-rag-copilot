"""Deterministic token-overlap retrieval baseline."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from universal_rag_copilot.domain import Chunk, RetrievalResult

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "how",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "with",
}


def tokenize(text: str) -> set[str]:
    tokens = {t.lower() for t in re.findall(r"\b[a-zA-Z0-9]+\b", text)}
    return {t for t in tokens if t not in STOPWORDS and len(t) > 1}


@dataclass(frozen=True)
class RetrievalIndex:
    chunks: tuple[Chunk, ...]
    token_sets: tuple[set[str], ...]


def build_index(chunks: list[Chunk]) -> RetrievalIndex:
    return RetrievalIndex(chunks=tuple(chunks), token_sets=tuple(tokenize(c.text) for c in chunks))


def retrieve(index: RetrievalIndex, query: str, top_k: int = 4) -> list[RetrievalResult]:
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scored: list[RetrievalResult] = []
    for chunk, chunk_tokens in zip(index.chunks, index.token_sets, strict=True):
        overlap = sorted(query_tokens & chunk_tokens)
        if not overlap:
            continue
        score = len(overlap) / math.sqrt(len(query_tokens) * max(1, len(chunk_tokens)))
        scored.append(RetrievalResult(chunk=chunk, score=score, matched_terms=tuple(overlap)))

    scored.sort(key=lambda item: (-item.score, item.chunk.chunk_id))
    return scored[:top_k]
