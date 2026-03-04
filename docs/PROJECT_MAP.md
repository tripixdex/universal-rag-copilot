# Project Map

## Current repository tree
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
  fixtures/
    support_kb/
    academic_pdf/
    eval/
      cases.json
  src/
    universal_rag_copilot/
      __init__.py
      __main__.py
      config.py
      pipeline.py
      api/
        __init__.py
        app.py
        ui_page.py
      domain/
        __init__.py
        models.py
      ingestion/
        __init__.py
        local_ingestion.py
      chunking/
        __init__.py
        strategies.py
      retrieval/
        __init__.py
        baseline.py
        pipeline.py
      answering/
        __init__.py
        composer.py
      evaluation/
        __init__.py
        runner.py
      ui/
        __init__.py
        cli.py
  tests/
    test_chunking.py
    test_retrieval_answering.py
    test_evaluation_runner.py
    test_api.py
  outputs/
  README.md
  pyproject.toml
  Makefile
  REPORT.md
```

## Module purpose summary
- `api/`: minimal FastAPI app and plain HTML/JS demo UI
- `domain/`: typed contracts, including explicit answerability
- `ingestion/`: local fixture loading
- `chunking/`: mode/profile-aware chunking
- `retrieval/`: baseline lexical retrieval + explicit retrieval pipeline controls
- `answering/`: grounded answer composition
- `evaluation/`: local fixture-driven eval harness and report writing
- `ui/`: CLI commands (`index-demo`, `ask-demo`, `run-eval`)
- `tests/`: retrieval/eval behavior and API endpoint tests
