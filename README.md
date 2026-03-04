# Universal RAG Copilot

Local-first RAG prototype with CLI, minimal API, and browser UI.

Current flow:
`ingest -> chunk -> index -> retrieve -> score-filter -> evidence decision -> answer with citations`

## Capabilities
- Local corpora: `support_kb`, `academic_pdf`
- Chunking profiles: `fine`, `balanced`, `coarse`
- Retrieval controls: `top_k`, `min_score_threshold`, `min_evidence_results`
- Explicit answerability contract:
  - `answerable`
  - `not_enough_evidence`
- Local eval harness with fixture cases and JSON/Markdown reports

## CLI path
Run checks:

```bash
make format
make lint
make test
```

Demo ask:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo \
  --mode support_kb \
  --profile balanced \
  --question "How long do card refunds take to settle?"
```

Run eval from CLI:

```bash
PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval
```

## API path
Start API locally:

```bash
PYTHONPATH=src uvicorn universal_rag_copilot.api.app:app --host 127.0.0.1 --port 8000
```

Or with installed script:

```bash
urc-api
```

Endpoints:
- `GET /health`
- `GET /ui`
- `POST /ask`
- `POST /run-eval`

Example `/ask`:

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

Run eval via API:

```bash
curl -s http://127.0.0.1:8000/run-eval -X POST -H 'content-type: application/json' -d '{}'
```

## Browser UI path
Open:
- `http://127.0.0.1:8000/ui`

UI supports:
- mode/profile selectors
- question input
- advanced retrieval controls
- Ask action with answer/citations/retrieval summary output
- Run Eval action with latest report path

## Limitations
- Lexical retrieval baseline only (no embedding/vector retrieval yet)
- No reranking or hybrid retrievers
- Academic mode still uses local text fixtures instead of PDF parsing
- Demo-focused local app, not production deployment
