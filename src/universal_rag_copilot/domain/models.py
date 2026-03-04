"""Core typed models for the Stage 1 vertical slice."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class CorpusMode(StrEnum):
    SUPPORT_KB = "support_kb"
    ACADEMIC_PDF = "academic_pdf"


class ChunkProfile(StrEnum):
    FINE = "fine"
    BALANCED = "balanced"
    COARSE = "coarse"


class Answerability(StrEnum):
    ANSWERABLE = "answerable"
    NOT_ENOUGH_EVIDENCE = "not_enough_evidence"


@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    mode: CorpusMode
    source_path: Path
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    title: str
    mode: CorpusMode
    profile: ChunkProfile
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    chunk: Chunk
    score: float
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class Citation:
    chunk_id: str
    document_id: str
    title: str
    section: str
    score: float


@dataclass(frozen=True)
class AnswerResult:
    answer: str
    citations: tuple[Citation, ...]
    answerability: Answerability

    @property
    def insufficient_evidence(self) -> bool:
        return self.answerability is Answerability.NOT_ENOUGH_EVIDENCE
