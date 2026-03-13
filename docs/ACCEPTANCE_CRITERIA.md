# Acceptance Criteria

These criteria describe the current local demo MVP, not a foundation-only scaffold.

## Runtime paths
1. `make up` starts the API from a clean source checkout without requiring an implicit shell `PYTHONPATH`.
2. `make lint` passes.
3. `make test` passes.
4. CLI demo commands work with `PYTHONPATH=src` from the repo root.

## Product behavior
5. `POST /ask` returns either `answerable` with citations or `not_enough_evidence`.
6. API validation rejects empty, malformed, or excessive user inputs with `422` errors.
7. `POST /run-eval` always writes reports under repo-local `outputs/eval/`.
8. The UI shows answerability, answer text, citations, and eval summary in a readable form.

## Evaluation credibility
9. The eval set contains at least 15 deterministic cases.
10. Eval coverage includes answerable support questions, answerable academic questions, distractors, near-misses, false-friend wording, and clearly unanswerable questions.
11. Source validation requires more than any single overlap; expected sources and top-document expectations must match the observed results.

## Documentation honesty
12. `README.md`, `docs/SCOPE.md`, `docs/DEMO_SCENARIOS.md`, and `docs/EVAL_PLAN.md` describe the repo as a local-first demo MVP that already runs.
13. Docs clearly state known limitations and avoid implying production readiness.
