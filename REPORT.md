# Stage 1 Report: First Vertical Slice

## Objective completed
Implemented the first thin, real end-to-end local path:
`ingest -> chunk -> index -> retrieve -> answer with citations`.

## What was added
- Demo fixture corpora for both modes:
  - `fixtures/support_kb/*.md`
  - `fixtures/academic_pdf/*.md`
- Typed domain models in `domain/models.py`:
  - `Document`, `Chunk`, `RetrievalResult`, `AnswerResult`, `Citation`
  - `CorpusMode`, `ChunkProfile`
- Ingestion layer:
  - local fixture reader with metadata normalization
- Chunking:
  - mode-aware section/chapter chunking
  - explicit `fine/balanced/coarse` profile settings
- Retrieval baseline:
  - deterministic token-overlap ranking
  - top-k results with scores and matched terms
- Answer composition:
  - grounded snippet-only answer behavior
  - citation list and insufficient-evidence guardrail
- CLI:
  - `index-demo`
  - `ask-demo`
- Tests:
  - chunking profile/mode differentiation
  - support and academic retrieval relevance
  - insufficient evidence / no unsupported answer behavior

## Architecture notes
- Stage 1 intentionally avoids external APIs and vector databases.
- Retrieval is pluggable: current lexical index can be replaced by embedding/vector retrieval later without changing domain contracts.

## Verification
- `make format`: pass (`python -m ruff format src tests`)
- `make lint`: pass (`python -m ruff check src tests`)
- `make test`: pass (`python -m pytest -q`, 4 passed)
