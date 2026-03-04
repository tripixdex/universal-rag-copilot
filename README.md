# Universal RAG Copilot

Stage 1 implements a thin, local-first vertical slice:
`ingest -> chunk -> index -> retrieve -> answer with citations`.

## Implemented in Stage 1
- Two corpus modes from local fixtures:
  - `support_kb`
  - `academic_pdf`
- Three explicit chunking profiles:
  - `fine`
  - `balanced`
  - `coarse`
- Local fixture ingestion into typed document models
- Mode/profile-aware chunking into typed chunk models
- Deterministic token-overlap retrieval baseline (no vector DB)
- Grounded answer composer with citations and insufficient-evidence guard
- Minimal CLI commands:
  - `index-demo`
  - `ask-demo`
- Tests for chunking behavior, retrieval relevance, and insufficient-evidence handling

## Not implemented yet
- Embeddings and vector database retrieval
- PDF parsing pipeline (academic corpus currently uses text/markdown fixtures)
- Hybrid reranking, feedback loops, and advanced evaluation metrics
- Web UI

## Quickstart
Run from repo root:

```bash
make format
make lint
make test
```

Index demo data:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli index-demo --mode support_kb --profile balanced
```

Ask a grounded question:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode support_kb \
  --profile balanced \
  --question "How long do card refunds take to settle?"
```

Academic mode example:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode academic_pdf \
  --profile balanced \
  --question "What is gradient descent used for?"
```
