# Stage 3 Report: Local API and Browser UI Demoability

## Objective completed
Added a minimal local FastAPI API and browser UI while preserving the local-first architecture and existing CLI behavior.

## What was added
- New API module:
  - `src/universal_rag_copilot/api/app.py`
  - `src/universal_rag_copilot/api/ui_page.py`
  - `src/universal_rag_copilot/api/__init__.py`
- Endpoints:
  - `GET /health`
  - `GET /ui`
  - `POST /ask`
  - `POST /run-eval`
- `/ask` supports:
  - `mode`, `profile`, `question`
  - optional retrieval controls: `top_k`, `min_score_threshold`, `min_evidence_results`
- `/ask` response includes:
  - `answerability`, `answer`, `citations`, `retrieval_summary`
- `/run-eval` executes local eval harness and returns:
  - `total_cases`, `passed_cases`, `json_report_path`, `markdown_report_path`
- Browser UI (plain HTML/CSS/JS):
  - mode/profile selectors
  - question input
  - retrieval controls
  - Ask action with result rendering
  - Run Eval action with latest eval path display
- Packaging updates:
  - added lightweight dependencies: FastAPI, Uvicorn, httpx
  - added `urc-api` console script

## Existing CLI status
- `index-demo`, `ask-demo`, and `run-eval` remain intact.

## Tests added
- `tests/test_api.py`:
  - `/health`
  - `/ui` content-type
  - `/ask` happy path
  - `/ask` insufficient-evidence case
  - `/run-eval` response shape

## Verification
- `make format`: pass
- `make lint`: pass
- `make test`: pass

## Constraints respected
- No external APIs
- No heavy frontend stack
- Local-first architecture preserved
- Demo-focused implementation (not production deployment)
