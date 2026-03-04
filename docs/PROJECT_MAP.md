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
      returns_and_refunds.md
      billing_and_invoices.md
      account_access_security.md
    academic_pdf/
      optimization_intro.md
      neural_networks_basics.md
      probability_for_ml.md
  src/
    universal_rag_copilot/
      __init__.py
      __main__.py
      config.py
      pipeline.py
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
      answering/
        __init__.py
        composer.py
      evaluation/
        __init__.py
      ui/
        __init__.py
        cli.py
  tests/
    test_chunking.py
    test_retrieval_answering.py
  outputs/
  README.md
  pyproject.toml
  Makefile
  REPORT.md
```

## Module purpose summary
- `domain/`: typed contracts for document, chunk, retrieval result, citation, answer result
- `ingestion/`: local fixture loading and normalization into `Document`
- `chunking/`: mode/profile-aware chunking policies
- `retrieval/`: deterministic token-overlap index and ranking
- `answering/`: grounded answer synthesis with citation output and evidence gating
- `ui/`: thin CLI (`index-demo`, `ask-demo`)
- `tests/`: first behavior tests for chunking, retrieval, and insufficient evidence
