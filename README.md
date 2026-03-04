# Universal RAG Copilot

Local-first RAG prototype focused on retrieval quality control and grounded answers.

Current flow:
`ingest -> chunk -> index -> retrieve -> score-filter -> evidence decision -> answer with citations`

## Implemented
- Two corpus modes from local fixtures: `support_kb`, `academic_pdf`
- Three chunking profiles: `fine`, `balanced`, `coarse`
- Explicit retrieval pipeline with modular stages:
  - indexing
  - retrieval
  - scoring/thresholding
  - answer composition
- Retrieval quality controls:
  - `top_k`
  - minimum score threshold
  - evidence sufficiency rule (minimum eligible results)
- Explicit answerability contract:
  - `answerable`
  - `not_enough_evidence`
- Local evaluation harness with fixture-driven cases and output reports
- CLI commands:
  - `index-demo`
  - `ask-demo`
  - `run-eval`

## Quickstart
Run from repo root:

```bash
make format
make lint
make test
```

## Demo Question Answering
Index fixtures for a mode/profile:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli index-demo --mode support_kb --profile balanced
```

Ask a grounded question:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode support_kb \
  --profile balanced \
  --question "How long do card refunds take to settle?" \
  --top-k 4 \
  --min-score-threshold 0.07 \
  --min-evidence-results 1
```

## Evaluation
Run local evaluation cases from `fixtures/eval/cases.json`:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval
```

Reports are written to `outputs/eval/` as timestamped JSON and Markdown files.

## Current Limitations
- Lexical token-overlap retrieval only (no embeddings/vector DB yet)
- No reranking or hybrid retrieval
- Academic mode still uses text fixtures, not real PDF parsing
- Metrics are simple pass/fail checks, not benchmark-grade scoring
- No UI yet (CLI only)
