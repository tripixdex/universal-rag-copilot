"""Local fixture ingestion."""

from __future__ import annotations

from pathlib import Path

from universal_rag_copilot.config import FIXTURES_DIR
from universal_rag_copilot.domain import CorpusMode, Document


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def load_fixture_documents(mode: CorpusMode, fixtures_dir: Path = FIXTURES_DIR) -> list[Document]:
    mode_dir = fixtures_dir / mode.value
    if not mode_dir.exists():
        raise FileNotFoundError(f"Fixture directory not found: {mode_dir}")

    docs: list[Document] = []
    for path in sorted(mode_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        docs.append(
            Document(
                document_id=path.stem,
                title=_extract_title(text, path.stem.replace("_", " ").title()),
                mode=mode,
                source_path=path,
                text=text,
                metadata={"filename": path.name},
            )
        )
    return docs
