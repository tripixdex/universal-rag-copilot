# Foundation Report: Universal RAG Copilot

## Summary of what was created
- Established a docs-first project foundation for a local-first multi-mode RAG assistant.
- Added product documents: PRD, scope boundaries, acceptance criteria, demo scenarios, and evaluation plan.
- Added architecture documents: module design, project map, and corpus mode/chunking profile rationale.
- Added minimal Python package skeleton with docstring-only modules.
- Added basic repository hygiene files (`README`, `.gitignore`, `pyproject`, `Makefile`).

## Files created
- `README.md`
- `.gitignore`
- `pyproject.toml`
- `Makefile`
- `REPORT.md`
- `docs/PRD.md`
- `docs/SCOPE.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/DEMO_SCENARIOS.md`
- `docs/EVAL_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/PROJECT_MAP.md`
- `docs/MODES_AND_PROFILES.md`
- `src/universal_rag_copilot/__init__.py`
- `src/universal_rag_copilot/config.py`
- `src/universal_rag_copilot/domain/__init__.py`
- `src/universal_rag_copilot/domain/models.py`
- `src/universal_rag_copilot/ingestion/__init__.py`
- `src/universal_rag_copilot/chunking/__init__.py`
- `src/universal_rag_copilot/retrieval/__init__.py`
- `src/universal_rag_copilot/answering/__init__.py`
- `src/universal_rag_copilot/evaluation/__init__.py`
- `src/universal_rag_copilot/ui/__init__.py`
- `tests/.gitkeep`
- `fixtures/.gitkeep`
- `outputs/.gitkeep`

## Open questions
- What initial local embedding/index stack should be preferred in implementation stage?
- Should `balanced` be global default, or mode-specific defaults (`fine` for support, `coarse` for academic)?
- What citation format is required for first user-facing demos (section-only vs section+page)?

## Suggested next stage
- Stage 1: implement minimal end-to-end vertical slice:
  - one fixture corpus per mode
  - simple chunker profiles
  - local retrieval baseline
  - answer composer with citation stubs
  - first automated acceptance checks in `tests/`
