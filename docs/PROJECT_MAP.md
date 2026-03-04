# Project Map

## Intended repository tree
```text
universal-rag-copilot/
  docs/
    PRD.md
    SCOPE.md
    ACCEPTANCE_CRITERIA.md
    DEMO_SCENARIOS.md
    EVAL_PLAN.md
    ARCHITECTURE.md
    PROJECT_MAP.md
    MODES_AND_PROFILES.md
  src/
    universal_rag_copilot/
      __init__.py
      config.py
      domain/
        __init__.py
        models.py
      ingestion/
        __init__.py
      chunking/
        __init__.py
      retrieval/
        __init__.py
      answering/
        __init__.py
      evaluation/
        __init__.py
      ui/
        __init__.py
  tests/
  fixtures/
  outputs/
  README.md
  pyproject.toml
  Makefile
  .gitignore
  REPORT.md
```

## Module purpose summary
- `docs/`: single source of truth for product and architecture direction
- `domain/`: core data models shared across modules
- `ingestion/`: raw corpus parsing and normalization contracts
- `chunking/`: chunk strategy interfaces and profile behavior
- `retrieval/`: retrieval pipeline contracts and ranking interfaces
- `answering/`: grounded answer generation contracts
- `evaluation/`: evaluation fixtures and scoring contracts
- `ui/`: user interaction boundary
- `tests/`: verification suite (to be added)
- `fixtures/`: sample corpora, queries, expected evidence
- `outputs/`: generated run/evaluation artifacts
