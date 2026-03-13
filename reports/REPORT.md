# Hardening Sprint Report

## What changed

### VERIFIED: startup ergonomics
- `make up` now launches the API with `PYTHONPATH=src` via `LOCAL_PYTHONPATH`, so a clean source checkout no longer depends on a hidden shell import path.
- README and demo docs now use commands that match the actual source-checkout behavior.

### VERIFIED: docs truth pass
- Rewrote stale docs that still described a foundation-only scaffold.
- Docs now consistently describe the repo as a local-first demo MVP with current capabilities and known limitations.

### VERIFIED: API input validation hardening
- Added a `400` character ceiling for `/ask.question`.
- Added numeric ceilings for `/ask.top_k`, `/ask.min_score_threshold`, and `/ask.min_evidence_results`.
- Rejected extra request fields on `/ask` and `/run-eval`.

### VERIFIED: `/run-eval` output safety
- Removed caller-controlled `output_dir` from the public API request model.
- `POST /run-eval` now always writes reports under repo-local `outputs/eval/`.
- Added tests that reject a caller-supplied `output_dir`.

### VERIFIED: eval credibility
- Expanded eval coverage from `3` to `18` deterministic cases.
- Added support, academic, distractor, near-miss, false-friend, and unanswerable cases.
- Replaced permissive any-overlap source matching with stricter subset-plus-top-document checks.

### VERIFIED: UI readability
- Replaced raw JSON dumping for ask results with separate answerability, answer, citation, and retrieval-summary sections.
- Replaced raw JSON dumping for eval results with a compact pass-count and report-path summary.

## Why it changed
- The audit found five concrete blockers: broken source-checkout startup, stale maturity docs, weak API ceilings, unsafe API-controlled eval output paths, and an eval harness too small and permissive to be credible.
- Every code and doc change in this sprint maps directly to one of those blockers.

## Exact files modified
- `Makefile`
- `README.md`
- `docs/SCOPE.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/DEMO_SCENARIOS.md`
- `docs/EVAL_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/PRD.md`
- `fixtures/eval/cases.json`
- `src/universal_rag_copilot/api/app.py`
- `src/universal_rag_copilot/api/ui_page.py`
- `src/universal_rag_copilot/evaluation/runner.py`
- `tests/test_api.py`
- `tests/test_evaluation_runner.py`
- `HARDENING_SPRINT_SUMMARY.md`
- `REPORT.md`

## Commands run
- `make lint`
- `make test`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How long do card refunds take to settle?"`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How do I renew a passport in Canada?"`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`
- `make up`
- `curl -sS http://127.0.0.1:8000/health`
- `curl -sS http://127.0.0.1:8000/run-eval -X POST -H 'content-type: application/json' -d '{}'`
- `PYTHONPATH=src python - <<'PY' ... TestClient validation checks ... PY`

## Results

### VERIFIED
- `make lint` passed.
- `make test` passed with `19 passed in 0.11s`.
- CLI answerable demo returned `answerable` with `Returns and Refunds` citation.
- CLI insufficient-evidence demo returned `not_enough_evidence` with no citations.
- CLI eval completed and wrote reports under `outputs/eval/`.
- Latest eval report showed `18` total cases and `18` passed cases.
- In-process API checks returned `422` for:
  - overly long question
  - `top_k` above ceiling
  - `min_score_threshold` above ceiling
  - `min_evidence_results` above ceiling
  - caller-supplied `output_dir` on `/run-eval`
- `make up` no longer fails with `ModuleNotFoundError`.
- `.tmp/api.log` showed successful app startup and one `GET /health` `200 OK` during the `make up` health probe.

### INFERRED
- The startup path is internally consistent for clean source checkouts because the import-path fix is explicit in `Makefile` and the API module now starts far enough for the health probe to succeed.

### NOT VERIFIED
- Stable live socket availability across separate terminal exec sessions in this environment.
- Real browser rendering in a live browser session.

## Remaining limitations
- The system is still a lexical local demo, not a semantic or production-grade RAG stack.
- CLI `run-eval --output-dir` remains available for local developer use; the API surface is the part that was locked down.
- The environment used for this sprint is still unreliable for strong live-socket claims, so browser-level verification remains out of scope for this report.
