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
    eval/
      cases.json
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
  outputs/
  README.md
  pyproject.toml
  Makefile
  REPORT.md
```

## Module purpose summary
- `domain/`: typed contracts, including explicit `Answerability`
- `ingestion/`: local fixture loading into `Document`
- `chunking/`: mode/profile-aware chunking strategies
- `retrieval/baseline.py`: deterministic token-overlap retrieval baseline
- `retrieval/pipeline.py`: explicit retrieval stages and quality controls
- `answering/`: grounded answer composition from eligible evidence
- `evaluation/`: fixture-driven evaluation runner and report writing
- `ui/`: CLI for index, ask, and eval flows
- `tests/`: chunking, retrieval quality controls, and eval harness checks
