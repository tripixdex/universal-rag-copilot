# Universal RAG Copilot

Local-first RAG demo that shows when a grounded answer should be returned and when the system should stop and say the evidence is insufficient.

## Why it matters

This repo is a compact showcase of RAG judgment rather than just retrieval plumbing. It focuses on a reviewer-friendly question: can a local QA system answer with citations when the corpus supports it, and refuse cleanly when it does not?

## Capabilities

- Local support and academic demo corpora under `fixtures/`
- Deterministic pipeline: `ingest -> chunk -> lexical retrieve -> score filter -> evidence decision -> answer`
- Three chunking profiles: `fine`, `balanced`, `coarse`
- Explicit answerability contract: `answerable` or `not_enough_evidence`
- CLI, FastAPI API, and plain HTML UI for the same core flow
- Local eval harness with 18 fixture cases and JSON/Markdown reports

## Quick Demo

Install and run from a source checkout:

```bash
python -m pip install -e .
make up
```

Then open `http://127.0.0.1:8000/ui`.

Fastest CLI demo:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode support_kb \
  --profile balanced \
  --question "How long do card refunds take to settle?"
```

Negative-path demo:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode support_kb \
  --profile balanced \
  --question "How do I renew a passport in Canada?"
```

Run the local evaluation harness:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval
```

## Verification

The lightweight verification path for this repo is:

```bash
make lint
make test
PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval
```

Reports are written under `outputs/eval/`.

## API and Demo Surface

- `GET /health`
- `GET /ui`
- `POST /ask`
- `POST /run-eval`

Example request:

```bash
curl -s http://127.0.0.1:8000/ask -X POST -H 'content-type: application/json' -d '{
  "mode":"support_kb",
  "profile":"balanced",
  "question":"How long do card refunds take to settle?",
  "top_k":4,
  "min_score_threshold":0.07,
  "min_evidence_results":1
}'
```

## Limitations

- This is a local demo, not a production RAG service
- Retrieval is lexical only; there are no embeddings, reranking, or hybrid search
- `academic_pdf` uses curated markdown fixtures instead of real PDF parsing
- No auth, persistence, rate limiting, or multi-user concerns are implemented
- Some restricted environments may block live socket binding even though tests still pass in-process

## Why it is interesting in a portfolio

This repo is strongest as a small, inspectable example of grounded-answer behavior, deterministic evaluation, and honest failure modes.

## Docs

- [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/docs/DEMO_SCENARIOS.md)
- [docs/MODES_AND_PROFILES.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/docs/MODES_AND_PROFILES.md)
- [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/docs/ARCHITECTURE.md)
- [docs/SCOPE.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/docs/SCOPE.md)
