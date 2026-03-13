# Scope

## In scope now
- Local-first demo MVP covering ingestion, chunking, lexical retrieval, evidence gating, answer composition, CLI, API, UI, and local eval
- Two fixture-backed corpus modes: `support_kb` and `academic_pdf`
- Three chunking profiles: `fine`, `balanced`, `coarse`
- Explicit answerability behavior with cited answers or `not_enough_evidence`
- Repo-local eval reporting under `outputs/eval/`

## Current capabilities
- Runnable CLI commands: `index-demo`, `ask-demo`, `run-eval`
- Runnable FastAPI app with `GET /health`, `GET /ui`, `POST /ask`, and `POST /run-eval`
- Plain browser UI for local demos
- Deterministic eval set with answerable, distractor, near-miss, false-friend, and unanswerable cases

## Known limitations
- Lexical retrieval baseline only
- No hosted deployment, auth, or external services
- No production-grade observability, background jobs, or persistence layer
- Academic mode uses local markdown fixtures instead of actual PDF parsing

## Out of scope for this demo sprint
- Architecture redesign
- Cloud infrastructure or managed databases
- Embedding models, vector databases, rerankers, or LLM integrations
- Multi-user features, auth, or internet-facing hardening
