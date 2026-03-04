"""Mode-aware chunking strategies for Stage 1."""

from __future__ import annotations

import re
from dataclasses import dataclass

from universal_rag_copilot.domain import Chunk, ChunkProfile, CorpusMode, Document


@dataclass(frozen=True)
class ChunkConfig:
    size: int
    overlap: int


CHUNK_CONFIG: dict[CorpusMode, dict[ChunkProfile, ChunkConfig]] = {
    CorpusMode.SUPPORT_KB: {
        ChunkProfile.FINE: ChunkConfig(size=24, overlap=6),
        ChunkProfile.BALANCED: ChunkConfig(size=45, overlap=10),
        ChunkProfile.COARSE: ChunkConfig(size=90, overlap=18),
    },
    CorpusMode.ACADEMIC_PDF: {
        ChunkProfile.FINE: ChunkConfig(size=90, overlap=18),
        ChunkProfile.BALANCED: ChunkConfig(size=150, overlap=28),
        ChunkProfile.COARSE: ChunkConfig(size=240, overlap=40),
    },
}


def _split_sections(markdown_text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
        elif not line.startswith("# "):
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))
    return [(title, text) for title, text in sections if text]


def _token_windows(text: str, size: int, overlap: int) -> list[str]:
    words = re.findall(r"\b\w+\b|[.,:;!?()-]", text)
    if not words:
        return []

    windows: list[str] = []
    step = max(1, size - overlap)
    for start in range(0, len(words), step):
        chunk_words = words[start : start + size]
        if not chunk_words:
            break
        windows.append(" ".join(chunk_words).replace(" ,", ",").replace(" .", "."))
        if start + size >= len(words):
            break
    return windows


def chunk_documents(documents: list[Document], profile: ChunkProfile) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        cfg = CHUNK_CONFIG[doc.mode][profile]
        sections = _split_sections(doc.text)
        section_index = 0
        for section_title, section_text in sections:
            for i, chunk_text in enumerate(
                _token_windows(section_text, cfg.size, cfg.overlap), start=1
            ):
                section_index += 1
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.document_id}:c{section_index:03d}",
                        document_id=doc.document_id,
                        title=doc.title,
                        mode=doc.mode,
                        profile=profile,
                        text=chunk_text,
                        metadata={"section": section_title, "window": str(i)},
                    )
                )
    return chunks
