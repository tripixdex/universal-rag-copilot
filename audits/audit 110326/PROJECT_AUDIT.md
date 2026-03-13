Wrote the audit artifacts:

  - PROJECT_AUDIT.md
  - TERMINAL_EVIDENCE.md
  - MACHINE_READABLE_SUMMARY.json

  Current verdict is MVP BUT NEEDS FIXES, scored 7.1/10. The repo is real and
  runnable: make lint passed, make test passed with 19 passed, CLI demos ran,
  and eval produced 18/18 on the current fixture set. The biggest verified
  blocker is credibility, not missing implementation: the academic demo answer
  still pulls irrelevant snippets while the eval harness passes it, so answer
  quality is softer than the green eval suggests.

  The other hard blocker before freeze is trust: AUDIT_EXPERT_REPORT.md is stale
  and now false in multiple places. Live browser/socket behavior also remains
  not fully verified in this environment; in-process API checks passed, but
  stable external curl verification did not.


# PROJECT AUDIT

## Executive summary
- VERIFIED: This repository is a real local RAG demo, not a scaffold. The codebase contains ingestion, chunking, lexical retrieval, answer composition, a CLI, a FastAPI app, a browser UI page, and an eval harness. `make lint` passed, `make test` passed with `19 passed`, CLI demos ran, and eval produced fresh reports.
- VERIFIED: The repository is still local-demo grade. Retrieval is lexical only, corpora are tiny fixture sets, academic mode is markdown-backed rather than PDF-backed, and there is no auth, rate limiting, or deployment hardening.
- VERIFIED: The API surface is tighter than older audit material suggests. `/ask` enforces max question length and bounded numeric controls, and `/run-eval` no longer accepts `output_dir`.
- VERIFIED: The weakest current portfolio issue is answer quality credibility, not repo existence. A verified academic demo answer included off-topic snippets and citations while still passing eval, which shows the eval harness does not test answer-text relevance.
- NOT VERIFIED: Stable live browser demo in this audit environment. `make up` reported success and `.tmp/api.log` shows a `GET /health` `200`, but follow-up `curl` requests from separate exec calls failed, and direct uvicorn binds sometimes errored with `operation not permitted`.

## Repo purpose
- VERIFIED: The repo presents itself as "Local-first RAG demo MVP with a CLI, a minimal FastAPI API, and a plain HTML/JS UI" in [README.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/README.md#L1).
- VERIFIED: The implemented flow is `ingest -> chunk -> lexical retrieve -> score filter -> evidence decision -> answer with citations` per [README.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/README.md#L5) and [pipeline.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/pipeline.py#L18).
- INFERRED: The intended portfolio pitch is "principled local RAG MVP with explicit answerability," not "production-ready assistant."

## Current verified capabilities
- VERIFIED: Ingestion exists via local markdown fixture loading in [local_ingestion.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/ingestion/local_ingestion.py#L18).
- VERIFIED: Chunking exists with mode/profile-specific configs in [strategies.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/chunking/strategies.py#L17).
- VERIFIED: Retrieval exists as deterministic lexical token-overlap ranking in [baseline.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/retrieval/baseline.py#L45).
- VERIFIED: Evidence gating exists in [pipeline.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/retrieval/pipeline.py#L38).
- VERIFIED: Grounded answer composition exists in [composer.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/answering/composer.py#L28).
- VERIFIED: Explicit `not_enough_evidence` behavior exists in [composer.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/answering/composer.py#L34) and was observed in CLI and TestClient runs.
- VERIFIED: CLI entrypoints exist in [cli.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/ui/cli.py#L20) and module entrypoint exists in [__main__.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/__main__.py#L1).
- VERIFIED: FastAPI app exists with `GET /health`, `GET /ui`, `POST /ask`, `POST /run-eval` in [app.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/app.py#L62).
- VERIFIED: Browser UI exists as a static HTML/JS page in [ui_page.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/ui_page.py#L4).
- VERIFIED: Eval harness exists in [runner.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/evaluation/runner.py#L85) and fixture cases exist in [cases.json](/Users/vladgurov/Desktop/work/universal-rag-copilot/fixtures/eval/cases.json#L1).
- VERIFIED: The current eval fixture count is 18, not 3, and the latest run passed 18/18.
- VERIFIED: `index-demo` ran and reported `documents=3 chunks=9` for `academic_pdf/coarse`.
- VERIFIED: Support ask-demo returned the refund timeline with one citation.
- VERIFIED: Academic ask-demo returned an answer, but the answer text mixed in irrelevant neural-network snippets. This is a real quality defect in the current demo output.

## Docs truth audit
- VERIFIED: `README.md`, `docs/SCOPE.md`, `docs/ACCEPTANCE_CRITERIA.md`, `docs/DEMO_SCENARIOS.md`, and `docs/EVAL_PLAN.md` are mostly aligned with current repo state.
- VERIFIED: README honestly labels the repo a local demo and explicitly says live socket binding can be blocked in restricted environments in [README.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/README.md#L16).
- VERIFIED: `docs/ARCHITECTURE.md` still overstates academic ingestion by claiming page mapping and references preservation in [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/docs/ARCHITECTURE.md#L11). The actual ingestion code just loads local markdown files and extracts a title.
- VERIFIED: `AUDIT_EXPERT_REPORT.md` is stale and materially false for the current repo. It still claims a 3-case eval set, missing max-length validation, caller-controlled `/run-eval output_dir`, stale scope docs, and raw-JSON UI issues in [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L8), [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L10), [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L11), [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L12), and [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L177).
- VERIFIED: `REPORT.md` is mostly consistent with current code and observed behavior, but it is a hardening report, not a neutral current-state audit.
- INFERRED: Keeping the stale expert audit in the repo hurts trust more than having no audit file at all.

## Entrypoints and run commands
- VERIFIED: Main package entrypoint: [__main__.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/__main__.py#L1)
- VERIFIED: CLI implementation: [cli.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/ui/cli.py#L20)
- VERIFIED: API app: [app.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/app.py#L19)
- VERIFIED: UI page: [ui_page.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/ui_page.py#L4)
- VERIFIED: Eval runner: [runner.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/evaluation/runner.py#L85)

Documented or discovered commands:
- VERIFIED: Lint: `make lint`
- VERIFIED: Tests: `make test`
- NOT VERIFIED: Install from scratch: `python -m pip install -e .`
- VERIFIED: Start API: `make up`
- VERIFIED: Start API directly: `PYTHONPATH=src uvicorn universal_rag_copilot.api.app:app --host 127.0.0.1 --port 8000`
- NOT VERIFIED: Start UI separately. There is no separate UI server; UI is served from `/ui` on the API.
- VERIFIED: Demo question: `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How long do card refunds take to settle?"`
- VERIFIED: Demo question, academic: `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode academic_pdf --profile balanced --question "In batch gradient descent, what data does each step use?"`
- VERIFIED: Run evals: `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`

## Tests/evals audit
- VERIFIED: Test files present:
  - [tests/test_chunking.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/tests/test_chunking.py#L1)
  - [tests/test_retrieval_answering.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/tests/test_retrieval_answering.py#L1)
  - [tests/test_evaluation_runner.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/tests/test_evaluation_runner.py#L1)
  - [tests/test_api.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/tests/test_api.py#L1)
- VERIFIED: Test coverage is basic but real. It covers chunk sizing behavior, happy-path retrieval, insufficient-evidence behavior, eval output shape, API response shape, and validation failures.
- VERIFIED: Eval fixture set has 18 cases spanning support, academic, near-miss, false-friend, distractor-like wording, and unanswerable cases in [cases.json](/Users/vladgurov/Desktop/work/universal-rag-copilot/fixtures/eval/cases.json#L1).
- VERIFIED: Eval matching is stricter than the stale audit claims. It checks top document id, expected doc-id subsets, citation-title subsets, and zero-citation behavior for unanswerable cases in [runner.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/evaluation/runner.py#L63).
- VERIFIED: Eval coverage is still weak on answer-text quality. The academic demo answer pulled unrelated snippets, yet the eval still passes 18/18 because it does not score textual faithfulness or citation precision.
- VERIFIED: There are no adversarial tests for large payloads beyond schema limits, no latency/perf tests, no browser tests, and no snapshot tests for exact API output contracts.
- INFERRED: The eval harness is useful for regression on this exact lexical fixture setup, but it is not strong evidence of general RAG quality.

## API/UI audit
- VERIFIED: `/ask` validates whitespace, max question length 400, `top_k <= 8`, `min_score_threshold <= 1`, `min_evidence_results <= 4`, and forbids extra fields in [app.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/app.py#L21).
- VERIFIED: `/run-eval` does not accept `output_dir`; the request model is empty and forbids extra fields in [app.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/app.py#L44).
- VERIFIED: API responses include answerability, answer, citations, and retrieval summary in [app.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/app.py#L93).
- VERIFIED: UI renders answerability, answer, citations, and retrieval summary sections rather than raw JSON in [ui_page.py](/Users/vladgurov/Desktop/work/universal-rag-copilot/src/universal_rag_copilot/api/ui_page.py#L85).
- VERIFIED: The app is documented as local-only demo software in README and scope docs.
- NOT VERIFIED: End-to-end browser rendering in this environment.
- NOT VERIFIED: Stable live HTTP access from this audit environment outside in-process testing.

## Security/safety audit
- VERIFIED: `/run-eval` API output directory handling is now safe by default for the HTTP surface. Reports always write under repo-local `outputs/eval/`.
- VERIFIED: `/ask` has basic size ceilings and field forbidding.
- VERIFIED: There is still no auth, rate limiting, CSRF protection, or deployment hardening.
- VERIFIED: There is no body-size middleware limit beyond Pydantic field limits.
- VERIFIED: The CLI still allows `run-eval --output-dir`; that is acceptable for local developer usage, but it is not an HTTP exposure.
- VERIFIED: The repo is clearly framed as local-only, which is important because the API is not hardened for public exposure.
- INFERRED: If this were ever shown as anything more than local demo software, the security story would collapse quickly.

## Portfolio readiness assessment
- VERIFIED: The repo has enough implemented surface to show real engineering work: modular code, typed domain models, deterministic retrieval, explicit answerability, tests, eval artifacts, CLI, API, and UI.
- VERIFIED: It is not freeze-ready for a strong portfolio submission because the current answer quality can visibly drift off-topic, and the stale `AUDIT_EXPERT_REPORT.md` undermines trust.
- VERIFIED: The worktree is currently dirty and contains prior generated audit artifacts, which is not ideal for a portfolio freeze.
- INFERRED: With one short hardening pass focused on answer quality credibility and repo narrative cleanup, this becomes a presentable local MVP.

## Top blockers before freeze
- VERIFIED: Remove or rewrite the stale [AUDIT_EXPERT_REPORT.md](/Users/vladgurov/Desktop/work/universal-rag-copilot/AUDIT_EXPERT_REPORT.md#L1). It is now demonstrably outdated.
- VERIFIED: Fix answer composition quality. The academic demo answer currently includes irrelevant content despite passing eval.
- VERIFIED: Tighten eval to score answer-text relevance or citation precision, not just source presence.
- VERIFIED: Resolve the remaining architecture doc overstatement around academic ingestion/page mapping.
- NOT VERIFIED: A stable live browser demo on this exact environment. If portfolio freeze requires recorded live HTTP/browser proof, that proof is still missing here.

## Recommended next sprint
- VERIFIED: Add answer-level eval assertions for academic/support cases so off-topic snippet concatenation fails.
- VERIFIED: Make citations more auditable by including source path and chunk window metadata in API responses.
- VERIFIED: Delete stale audit/report files or clearly mark them historical.
- VERIFIED: Add one clean, repeatable demo script that exercises CLI and TestClient, since live socket startup is environment-sensitive.
- INFERRED: If you want this to read as senior-level portfolio work, the next sprint should prioritize credibility and presentation, not more features.

## Final verdict
- Verdict: MVP BUT NEEDS FIXES
- Portfolio readiness score: 7.1/10
- Reason:
  - VERIFIED: The repo is implemented and test-backed.
  - VERIFIED: The local MVP story is real.
  - VERIFIED: The current quality bar is still too soft for freeze because answer quality and documentation trust are not tight enough.
