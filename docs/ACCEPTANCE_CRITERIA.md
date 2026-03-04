# Acceptance Criteria

All criteria are for this foundation stage only.

## Repository structure
1. Required directories exist: `docs/`, `src/universal_rag_copilot/`, `tests/`, `fixtures/`, `outputs/`.
2. Required source modules exist under `src/universal_rag_copilot/` and are near-empty/docstring-only.
3. Hygiene files exist: `README.md`, `.gitignore`, `pyproject.toml`, `Makefile`, `REPORT.md`.

## Product documentation quality
4. `docs/PRD.md` states problem, target users, value proposition, and rationale for multiple corpus modes.
5. `docs/SCOPE.md` clearly separates MVP, later work, and out-of-scope items.
6. `docs/DEMO_SCENARIOS.md` includes `support_kb`, `academic_pdf`, and "not enough evidence" scenarios.
7. `docs/EVAL_PLAN.md` defines retrieval checks, citation checks, and failure-case checks.

## Architecture documentation quality
8. `docs/ARCHITECTURE.md` describes modules: ingestion, chunking, embeddings/index, retrieval, answering, evaluation, ui.
9. `docs/PROJECT_MAP.md` includes intended repo tree plus purpose of each area.
10. `docs/MODES_AND_PROFILES.md` explains both corpus modes, all chunking profiles, and why chunking differs by corpus type.

## Honesty and constraints
11. Docs explicitly state that this stage is foundation only and not full implementation.
12. No unnecessary runtime dependencies are introduced in `pyproject.toml`.
13. No file in this stage exceeds 200 lines.
