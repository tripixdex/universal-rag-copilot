# 1. Executive Verdict
- The repository is a real working local RAG vertical slice, not a doc-only skeleton. **VERIFIED** (runtime commands and tests passed).
- Core pipeline exists and is coherent: ingestion -> chunking -> lexical retrieval -> threshold gating -> answer composer with citations. **VERIFIED** (`src/universal_rag_copilot/pipeline.py:13`, `src/universal_rag_copilot/retrieval/pipeline.py:46`).
- Retrieval is deterministic via explicit sort by score then `chunk_id`. **VERIFIED** (`src/universal_rag_copilot/retrieval/baseline.py:58`) and repeated-run check.
- Groundedness contract is explicit (`answerable` vs `not_enough_evidence`) and enforced before answer synthesis. **VERIFIED** (`src/universal_rag_copilot/retrieval/pipeline.py:38`, `src/universal_rag_copilot/answering/composer.py:34`).
- The system can correctly return `not_enough_evidence` for weak retrieval under both default unanswerable case and stricter thresholding. **VERIFIED** (`tests/test_retrieval_answering.py:48`, CLI run with `--min-score-threshold 0.2`).
- Citation traceability is partial: chunk/document/title/section/score are returned, but no source path or byte/line offsets are exposed in API output. **VERIFIED** (`src/universal_rag_copilot/api/app.py:96`).
- Eval harness exists and runs, but credibility is limited by tiny fixture set (3 cases) and permissive source-match logic (set intersection only). **VERIFIED** (`fixtures/eval/cases.json:1`, `src/universal_rag_copilot/evaluation/runner.py:58`).
- API contract is stable enough for demo use; validation errors mostly return 422 and success shapes are tested. **VERIFIED** (`tests/test_api.py:34`, TestClient probes).
- `/run-eval` allows caller-controlled `output_dir` with no path policy. This is acceptable for local demo but unsafe default for any shared deployment. **VERIFIED** (`src/universal_rag_copilot/api/app.py:123`).
- No payload max length/rate limits; large inputs can drive CPU/memory use in tokenization/chunk scans. **VERIFIED** (`src/universal_rag_copilot/api/app.py:25`, no max length).
- Documentation has material drift: `docs/SCOPE.md` and `docs/ACCEPTANCE_CRITERIA.md` still describe a docstring-only foundation stage, conflicting with implemented runtime. **VERIFIED** (`docs/SCOPE.md:9`, `docs/ACCEPTANCE_CRITERIA.md:7`, `README.md:3`).
- Non-technical 60-second demo is plausible on a normal machine (`make up`/UI), but not fully verified in this sandbox due bind/connect restrictions. **NOT VERIFIED** for live browser flow; CLI path is **VERIFIED**.
- Testing breadth is decent for happy-path MVP but thin on adversarial retrieval, contract regression, and security boundaries. **VERIFIED** (test inventory + missing-case review).
- Reproducibility is decent for deterministic logic; operational reproducibility has an environment-sensitive port/bind issue during this audit context. **VERIFIED** (`make up` refusal and uvicorn bind permission failure observed).
- Portfolio signal: strong for principled MVP framing and explicit uncertainty handling; weaker on eval depth, docs integrity, and production-safety defaults.
- Final recommendation: **MVP BUT NEEDS FIXES**.

# 2. Project Understanding
The project is a local-first, fixture-backed RAG demo with two corpus modes (`support_kb`, `academic_pdf`) and three chunking profiles (`fine`, `balanced`, `coarse`). It ingests local markdown fixtures, chunks by mode/profile configs, performs deterministic lexical overlap retrieval, filters candidates by score/evidence thresholds, then either composes a snippet-based cited answer or returns a fixed insufficient-evidence response.

What it solves now:
- Demonstrates corpus-aware chunking + transparent retrieval controls.
- Demonstrates explicit answerability behavior and local eval report generation.
- Provides CLI + API + static HTML UI for local demo.

What it does not do:
- No embedding/vector retrieval, reranking, hybrid search, or query rewriting.
- No PDF parsing pipeline (academic mode uses markdown fixtures).
- No auth, multi-user controls, deployment hardening, or service-level protections.

# 3. Verification Summary
| Item | Status | Evidence |
|---|---|---|
| Repository state clean | VERIFIED | `git status -sb` -> `## master` |
| Lint quality | VERIFIED | `make lint` -> `All checks passed!` |
| Test suite health | VERIFIED | `make test` -> `13 passed in 0.11s` |
| Eval harness executes | VERIFIED | `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval` produced JSON/MD reports |
| Eval pass count (current fixtures) | VERIFIED | `outputs/eval/eval_20260310T180502Z.json` -> `total_cases=3`, `passed_cases=3` |
| Core retrieval threshold gating | VERIFIED | `src/universal_rag_copilot/retrieval/pipeline.py:52-54` |
| Deterministic retrieval order | VERIFIED | `src/universal_rag_copilot/retrieval/baseline.py:58` + repeated-run command returned identical results |
| Not-enough-evidence behavior | VERIFIED | `tests/test_retrieval_answering.py:48`, CLI strict-threshold run returned `not_enough_evidence` |
| API request validation semantics | VERIFIED | TestClient command: invalid mode/profile, empty question, `top_k=0` all returned 422 |
| Live HTTP probing through running uvicorn in this environment | NOT VERIFIED | sandbox bind/connect restrictions: uvicorn bind error `[Errno 1] operation not permitted`; `curl` connection failures |
| UI usability in real browser | NOT VERIFIED | No browser automation/run in this audit environment |
| Docs consistency across repo | VERIFIED | Direct contradiction between `README.md` and foundation-only docs |

Command log (all commands run):
1. `git status -sb && git rev-parse --short HEAD && pwd`
2. `rg --files`
3. `sed -n '1,260p' README.md`
4. `sed -n '1,260p' docs/PRD.md`
5. `sed -n '1,260p' docs/SCOPE.md`
6. `sed -n '1,260p' docs/ARCHITECTURE.md`
7. `sed -n '1,260p' docs/EVAL_PLAN.md`
8. `sed -n '1,260p' docs/ACCEPTANCE_CRITERIA.md`
9. `sed -n '1,260p' docs/MODES_AND_PROFILES.md`
10. `sed -n '1,260p' docs/PROJECT_MAP.md`
11. `sed -n '1,260p' docs/DEMO_SCENARIOS.md`
12. `sed -n '1,260p' pyproject.toml`
13. `sed -n '1,260p' Makefile`
14. `sed -n '1,260p' src/universal_rag_copilot/domain/models.py`
15. `sed -n '1,260p' src/universal_rag_copilot/config.py`
16. `sed -n '1,260p' src/universal_rag_copilot/ingestion/local_ingestion.py`
17. `sed -n '1,260p' src/universal_rag_copilot/chunking/strategies.py`
18. `sed -n '1,280p' src/universal_rag_copilot/retrieval/baseline.py`
19. `sed -n '1,280p' src/universal_rag_copilot/retrieval/pipeline.py`
20. `sed -n '1,280p' src/universal_rag_copilot/answering/composer.py`
21. `sed -n '1,320p' src/universal_rag_copilot/pipeline.py`
22. `sed -n '1,360p' src/universal_rag_copilot/evaluation/runner.py`
23. `sed -n '1,360p' src/universal_rag_copilot/api/app.py`
24. `sed -n '1,360p' src/universal_rag_copilot/api/ui_page.py`
25. `sed -n '1,360p' src/universal_rag_copilot/ui/cli.py`
26. `sed -n '1,200p' src/universal_rag_copilot/__main__.py`
27. `sed -n '1,320p' tests/test_chunking.py`
28. `sed -n '1,360p' tests/test_retrieval_answering.py`
29. `sed -n '1,360p' tests/test_evaluation_runner.py`
30. `sed -n '1,360p' tests/test_api.py`
31. `sed -n '1,260p' fixtures/eval/cases.json`
32. `sed -n '1,260p' REPORT.md`
33. `sed -n '1,260p' fixtures/support_kb/returns_and_refunds.md`
34. `sed -n '1,260p' fixtures/support_kb/account_access_security.md`
35. `sed -n '1,260p' fixtures/support_kb/billing_and_invoices.md`
36. `sed -n '1,260p' fixtures/academic_pdf/optimization_intro.md`
37. `sed -n '1,260p' fixtures/academic_pdf/neural_networks_basics.md`
38. `sed -n '1,260p' fixtures/academic_pdf/probability_for_ml.md`
39. `make lint`
40. `make test`
41. `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`
42. `sed -n '1,260p' outputs/eval/eval_20260310T180502Z.json`
43. `sed -n '1,260p' outputs/eval/eval_20260310T180502Z.md`
44. `make up` (failed: port-in-use refusal)
45. `curl -sS http://127.0.0.1:8000/health` (failed connect)
46. `curl -sSI http://127.0.0.1:8000/ui` (failed connect)
47. `curl -sS http://127.0.0.1:8000/ | head -n 5` (failed connect)
48. `lsof -n -iTCP:8000 -sTCP:LISTEN`
49. `python - <<'PY' ... socket.connect_ex(('127.0.0.1',8000)) ... PY`
50. `mkdir -p .tmp && PYTHONPATH=src uvicorn ... --port 8011 > .tmp/audit_api.log 2>&1 & echo $!`
51. `curl -sS http://127.0.0.1:8011/health` (failed connect)
52. `curl -sSI http://127.0.0.1:8011/ui` (failed connect)
53. `curl -sS -X POST http://127.0.0.1:8011/ask ...` (failed connect)
54. `sed -n '1,200p' .tmp/audit_api.log`
55. `ps -p 4056 -o pid,ppid,stat,command` (sandbox denied)
56. `PYTHONPATH=src uvicorn universal_rag_copilot.api.app:app --host 127.0.0.1 --port 8011` (bind denied)
57. `mkdir -p .tmp && PYTHONPATH=src uvicorn ... --port 8011 > .tmp/audit_api.log 2>&1 & echo $!` (escalated)
58. `curl -s http://127.0.0.1:8011/health` (escalated; failed connect)
59. `sed -n '1,200p' .tmp/audit_api.log`
60. `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question 'How long do card refunds take to settle?'`
61. `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question 'How long do card refunds take to settle?' --min-score-threshold 0.2`
62. `PYTHONPATH=src python -m universal_rag_copilot.ui.cli index-demo --mode academic_pdf --profile coarse`
63. `sed -n '1,220p' src/universal_rag_copilot/retrieval/__init__.py`
64. `sed -n '1,220p' src/universal_rag_copilot/chunking/__init__.py`
65. `sed -n '1,220p' src/universal_rag_copilot/evaluation/__init__.py`
66. `PYTHONPATH=src python - <<'PY' ... TestClient invalid payload checks ... PY`
67. `PYTHONPATH=src python - <<'PY' ... repeated ask_demo_with_decision determinism check ... PY`
68. `rg -n "foundation only|not full implementation|Local-first RAG prototype|/ask|/run-eval|Limitations|top_k|min_score_threshold|min_evidence_results" README.md docs/*.md src/universal_rag_copilot/**/*.py tests/*.py`
69. `nl -ba src/universal_rag_copilot/retrieval/pipeline.py | sed -n '1,260p'`
70. `nl -ba src/universal_rag_copilot/evaluation/runner.py | sed -n '1,320p'`
71. `nl -ba src/universal_rag_copilot/retrieval/baseline.py | sed -n '1,260p'`
72. `nl -ba src/universal_rag_copilot/answering/composer.py | sed -n '1,300p'`
73. `nl -ba src/universal_rag_copilot/api/app.py | sed -n '1,320p'`
74. `nl -ba src/universal_rag_copilot/chunking/strategies.py | sed -n '1,320p'`
75. `nl -ba README.md | sed -n '1,260p'`
76. `nl -ba docs/SCOPE.md | sed -n '1,260p'`
77. `nl -ba docs/ACCEPTANCE_CRITERIA.md | sed -n '1,260p'`
78. `nl -ba docs/EVAL_PLAN.md | sed -n '1,280p'`
79. `nl -ba docs/PRD.md | sed -n '1,260p'`
80. `nl -ba docs/DEMO_SCENARIOS.md | sed -n '1,260p'`
81. `sed -n '1,220p' .gitignore`
82. `wc -l $(rg --files) | sort -nr | sed -n '1,20p'`

# 4. Strengths
- Explicit answerability model prevents silent hallucination-by-default behavior. **VERIFIED** (`src/universal_rag_copilot/domain/models.py:19`, `src/universal_rag_copilot/retrieval/pipeline.py:38`).
- Retrieval controls are first-class and exposed across CLI/API/UI (`top_k`, `min_score_threshold`, `min_evidence_results`). **VERIFIED** (`src/universal_rag_copilot/api/app.py:22`, `src/universal_rag_copilot/ui/cli.py:35`, `src/universal_rag_copilot/api/ui_page.py:44`).
- Deterministic retrieval ordering supports reproducible demos/tests. **VERIFIED** (`src/universal_rag_copilot/retrieval/baseline.py:58`).
- Eval runner produces machine-readable + human-readable reports with per-case detail. **VERIFIED** (`src/universal_rag_copilot/evaluation/runner.py:114`).
- Good minimal dependency footprint for local MVP (`fastapi`, `httpx`, `uvicorn`). **VERIFIED** (`pyproject.toml:9`).
- Make targets include operational safeguards against killing unrelated processes (PID tracking and port refusal). **VERIFIED** (`Makefile:14`).

# 5. Weaknesses
## Critical
- No critical defects found for current stated local-demo scope.

## High
- Issue: Documentation truth drift (foundation-only docs vs implemented runtime app).
- Evidence: `docs/SCOPE.md:9`, `docs/SCOPE.md:21`, `docs/ACCEPTANCE_CRITERIA.md:7` conflict with `README.md:3` and working modules/tests.
- Why it matters: Hiring managers read docs first; contradiction undermines trust and architecture intent.
- Consequence: Portfolio credibility hit; reviewers may assume process immaturity.

- Issue: Eval harness can pass with weak retrieval quality because source match only requires intersection, not rank/coverage/precision.
- Evidence: `_matches_expected_sources` uses set intersection (`src/universal_rag_copilot/evaluation/runner.py:64`), current suite only 3 cases (`fixtures/eval/cases.json:1`).
- Why it matters: Groundedness claims can be overstated by permissive scoring.
- Consequence: False confidence; regressions can slip while eval still shows green.

## Medium
- Issue: `/run-eval` accepts arbitrary `output_dir` path.
- Evidence: `RunEvalRequest.output_dir` and direct `Path(payload.output_dir)` write path (`src/universal_rag_copilot/api/app.py:31`, `src/universal_rag_copilot/api/app.py:124`).
- Why it matters: In any non-local exposure, this becomes a filesystem write primitive.
- Consequence: Path abuse / unintended file writes.

- Issue: API input size/rate safety is absent.
- Evidence: `question` only has `min_length=1` and no max limits (`src/universal_rag_copilot/api/app.py:25`).
- Why it matters: Large payloads increase CPU/memory and can degrade availability.
- Consequence: Easy local DoS / unstable demos under abuse.

- Issue: Citation traceability lacks direct source path and offsets in response contract.
- Evidence: Citation model/API response contain `chunk_id`, `document_id`, `title`, `section`, `score` only (`src/universal_rag_copilot/domain/models.py:52`, `src/universal_rag_copilot/api/app.py:96`).
- Why it matters: Harder to audit exact provenance from client side.
- Consequence: Reduced explainability and trust for evidence-centric UX.

## Low
- Issue: Demo scenario docs still labeled design-time pre-implementation.
- Evidence: `docs/DEMO_SCENARIOS.md:1-3`.
- Why it matters: Minor but contributes to narrative inconsistency.
- Consequence: Confusion about project maturity stage.

- Issue: UI is functionally clear but raw JSON-first and not citation-humanized.
- Evidence: `askResult.textContent = JSON.stringify(body, null, 2)` (`src/universal_rag_copilot/api/ui_page.py:80`).
- Why it matters: Non-technical demos require immediate readability.
- Consequence: Higher demo friction.

# 6. RAG Groundedness Review
- Grounding mechanism is retrieval-first and explicit: answerability decision occurs before answer text is composed. **VERIFIED** (`src/universal_rag_copilot/retrieval/pipeline.py:52`, `src/universal_rag_copilot/answering/composer.py:34`).
- `not_enough_evidence` behavior is implemented and observed in tests + CLI strict-threshold run. **VERIFIED**.
- Citation usefulness is moderate: includes semantic fields, but lacks pointer back to original file path/range for full auditability. **VERIFIED**.
- Composer still concatenates matched snippets without contradiction checks or confidence explanation. **VERIFIED** (`src/universal_rag_copilot/answering/composer.py:57`).
- Eval claims groundedness, but fixture count/strictness is too low for robust confidence. **VERIFIED**.

Assessment:
- Correctness for demo scope: **6.8/10**.
- Groundedness confidence under realistic noise/adversarial data: **4.5/10**.

# 7. Retrieval & Chunking Review
- Mode/profile chunk configs are coherent and reflect intended corpus differences. **VERIFIED** (`src/universal_rag_copilot/chunking/strategies.py:17`).
- Section-aware chunk metadata (`section`, `window`) is useful for citation context. **VERIFIED** (`src/universal_rag_copilot/chunking/strategies.py:84`).
- Retrieval scoring is deterministic and simple overlap-normalized; stable but brittle semantically. **VERIFIED** (`src/universal_rag_copilot/retrieval/baseline.py:55`).
- Failure modes:
- Synonym/paraphrase miss (lexical-only).
- Stopword/token heuristic may drop meaningful short terms.
- No query expansion/reranking means top-k quality degrades quickly on ambiguous prompts.
- Tuning knobs exist and work (`top_k`, `min_score_threshold`, `min_evidence_results`) but defaults are uncalibrated beyond 3 fixtures. **VERIFIED/INFERRED**.

# 8. API / Contracts Review
- `/ask` request model: includes mode/profile/question and retrieval controls with basic numeric constraints. **VERIFIED** (`src/universal_rag_copilot/api/app.py:22`).
- `/ask` response contains answerability, answer, citations, and retrieval summary including top results/matched terms. **VERIFIED** (`src/universal_rag_copilot/api/app.py:114`).
- `/run-eval` returns aggregate counts + report paths. **VERIFIED** (`src/universal_rag_copilot/api/app.py:127`).
- Error taxonomy is minimal: many failures map to 422; no structured domain error codes. **VERIFIED** (TestClient checks).
- Contract/docs alignment is mostly good for endpoints in README, but maturity docs are inconsistent repo-wide. **VERIFIED**.
- Live socket-level HTTP probing from this environment is **NOT VERIFIED** due sandbox restrictions; endpoint behavior is validated via FastAPI TestClient and tests.

# 9. UI / UX Review
- 60-second demo feasibility:
- CLI: yes, verified (`ask-demo`, `run-eval`, `index-demo`).
- Browser UI: plausible by design, not fully live-verified here.
- Readability:
- Current UI dumps raw JSON; technical users fine, non-technical users less so.
- Citations are not rendered as clickable/source-friendly artifacts.
- Friction points:
- No inline validation messaging for bad inputs.
- No loading/error states around fetch failures.

# 10. Testing & Evaluation Review
- Tested:
- Chunking size behavior by mode/profile.
- Retrieval source hit for support and academic sample queries.
- Insufficient-evidence path.
- Eval report shape and API endpoint basics.
- Not tested (highest risk gaps):
- Adversarial distractor docs and false-positive suppression.
- Citation faithfulness to exact source spans.
- Contract regression snapshots for `/ask` JSON shape over time.
- Large input/perf boundary tests.
- File/path safety tests around `output_dir`.
- Eval harness credibility: usable MVP start, not yet decision-grade for strong groundedness claims.

# 11. Security / Safety Review
- Input limits: no max question length; no rate limits. **VERIFIED**.
- Path/file handling: `output_dir` is user-controlled on API surface. **VERIFIED**.
- Secret hygiene: no obvious secrets in repo; `.gitignore` covers common local artifacts and outputs. **VERIFIED** (`.gitignore:1`).
- Unsafe defaults for shared deployment:
- Exposes filesystem report path behavior.
- No auth/authorization boundaries.
- These are acceptable only if enforced local-only.

# 12. Documentation Review
- README is practical and mostly accurate for CLI/API usage. **VERIFIED**.
- Core docs (`SCOPE`, `ACCEPTANCE_CRITERIA`, `DEMO_SCENARIOS`) are stale relative to implementation stage. **VERIFIED**.
- EVAL plan generally matches runner behavior but omits limitations of permissive source matching. **INFERRED** improvement need.
- Highest-priority doc fix is establishing one truthful maturity narrative.

# 13. Portfolio / Hiring Manager View
What looks senior:
- Explicit uncertainty contract and deterministic retrieval behavior.
- Clean module boundaries and local eval artifact discipline.
- Pragmatic local-first scope with minimal dependencies.

What looks prototype/junior:
- Documentation drift and mixed stage messaging.
- Small permissive eval set presented without explicit confidence caveats.
- Missing safety constraints on API input/path parameters.

Portfolio score: **6.9/10**.

# 14. MVP Readiness Assessment
- Product value: **7.2/10** - clear local demo value, narrow but real.
- Engineering quality: **7.0/10** - coherent code, deterministic behavior, good hygiene.
- Reliability: **6.6/10** - stable core logic; limited runtime stress and env variability coverage.
- UX: **5.9/10** - functional but raw output style for non-technical audiences.
- Documentation: **5.0/10** - practical README, but major drift in scope/acceptance docs.
- Demo readiness: **6.8/10** - CLI-ready, browser path likely works locally but not fully verified here.
- Maintainability: **7.1/10** - modular structure and small codebase aid iteration.
- Security hygiene: **5.4/10** - local-safe assumptions leak into API defaults.
- Evaluation credibility: **4.8/10** - too few cases and permissive matching logic.

Overall MVP score: **6.2/10**.

# 15. Top 15 Improvements
1. Unify docs to current stage (impact: High, effort: Low, why now: trust/candidate signal).
2. Tighten eval source matching to ranked expectations + minimum precision (impact: High, effort: Medium, why now: avoid false confidence).
3. Expand eval set to 25-50 cases incl. adversarial negatives (impact: High, effort: Medium, why now: establish groundedness credibility).
4. Add `max_length` for question and request body size guard (impact: High, effort: Low, why now: basic abuse resistance).
5. Restrict `/run-eval` `output_dir` to safe subtree or disable external path in API (impact: High, effort: Low, why now: remove filesystem-write footgun).
6. Add contract tests that snapshot `/ask` response schema and key semantics (impact: Medium, effort: Low, why now: prevent silent contract drift).
7. Include source path + section/window in API citations (impact: Medium, effort: Low, why now: stronger traceability).
8. Add confidence/explanation field for `not_enough_evidence` decisions (impact: Medium, effort: Low, why now: better UX and auditability).
9. Add stress tests for large input and top_k extremes (impact: Medium, effort: Medium, why now: reliability under non-ideal usage).
10. Introduce retrieval metrics (hit@k, MRR, nDCG-lite) in eval output (impact: Medium, effort: Medium, why now: quantitative progress tracking).
11. Improve UI rendering: readable answer card + citation list + expandable retrieval summary (impact: Medium, effort: Medium, why now: demo conversion).
12. Add explicit local-only warning and threat model in README (impact: Medium, effort: Low, why now: safety framing).
13. Add deterministic fixture checksum/versioning for eval reproducibility (impact: Low, effort: Low, why now: consistent benchmark lineage).
14. Add Make target for non-mutating format check (impact: Low, effort: Low, why now: CI-friendly auditing).
15. Add simple benchmark command for end-to-end latency on fixture sets (impact: Low, effort: Medium, why now: performance baseline).

# 16. Fastest Path to Elite Portfolio Quality
- 30 min plan:
1. Resolve docs drift (`README`, `SCOPE`, `ACCEPTANCE_CRITERIA`, `DEMO_SCENARIOS`) to one truthful maturity state.
2. Add README security note: local demo only, no public exposure.
3. Add API `max_length` on question and restrict/remove arbitrary `output_dir`.

- 2 hours plan:
1. Strengthen eval matcher (ranked target checks, minimum expected precision).
2. Add 10-15 new eval cases (negatives, distractors, near-miss paraphrases).
3. Add regression tests for invalid payloads and `not_enough_evidence` boundary behavior.

- 1 day plan:
1. Add richer citation payload (source path, section, window, chunk text preview).
2. Improve UI for non-technical demos (formatted answer + citation cards + clear errors).
3. Add metric outputs and trendable eval summary.

- 3 days plan:
1. Add optional embedding retriever behind interface while preserving deterministic lexical baseline for comparison.
2. Build side-by-side eval comparing lexical vs embedding on same fixture suite.
3. Produce concise architecture and evaluation narrative aimed at hiring managers.

# 17. Final Recommendation
**MVP BUT NEEDS FIXES**.

Rationale:
- Core MVP mechanics work and are test-backed.
- The current biggest blockers are trust/credibility issues (doc drift + shallow/permissive eval), plus basic safety hardening on API inputs/path handling.
- After targeted fixes, this can become a strong portfolio artifact.

Terminal summary:
1. final recommendation: MVP BUT NEEDS FIXES
2. MVP score: 6.2/10
3. portfolio score: 6.9/10
4. top 3 weaknesses: docs maturity drift; eval permissiveness + tiny dataset; unsafe `output_dir`/input limits for API
5. top 3 next actions: unify docs; harden eval rigor and expand cases; add API safety guards (`max_length`, safe output path)
