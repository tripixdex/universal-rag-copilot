# Stage 2 Report: Retrieval Quality and Evaluation Harness

## Objective completed
Strengthened the local-first prototype from a basic vertical slice to a more credible RAG baseline focused on retrieval quality control and explicit answerability behavior.

## What was added
- Explicit retrieval pipeline in `retrieval/pipeline.py` with separated stages:
  - indexing (existing baseline index)
  - retrieval (`retrieve_candidates`)
  - scoring/thresholding (`score_candidates`)
  - evidence sufficiency decision (`assess_evidence`)
  - answer composition (`answer_from_retrieval`)
- Retrieval quality controls:
  - `top_k`
  - `min_score_threshold`
  - `min_evidence_results`
- Explicit answerability contract:
  - `Answerability.ANSWERABLE`
  - `Answerability.NOT_ENOUGH_EVIDENCE`
- Evaluation harness:
  - fixture cases in `fixtures/eval/cases.json`
  - runner in `evaluation/runner.py`
  - report outputs to `outputs/eval/` as JSON and Markdown
  - CLI command: `run-eval`
- CLI improvements:
  - `ask-demo` now exposes retrieval quality controls and prints answerability
- Tests added/updated:
  - threshold behavior
  - expected-source retrieval for support and academic eval cases
  - insufficient evidence remains unanswerable
  - evaluation runner output shape

## Verification
- `make format`: pass (`python -m ruff format src tests`)
- `make lint`: pass (`python -m ruff check src tests`)
- `make test`: pass (`python -m pytest -q`, 6 passed)
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`: pass
  - Generated:
    - `outputs/eval/eval_20260304T231638Z.json`
    - `outputs/eval/eval_20260304T231638Z.md`
  - Result: `passed_cases=3/3`

## Notes
- No web UI and no external APIs were added.
- All functionality remains local-first and dependency-light.
