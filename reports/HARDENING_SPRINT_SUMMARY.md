# Hardening Sprint Summary

## Implemented fixes by audit finding
- Broken `make up` on clean source checkout:
  fixed by running the API with `PYTHONPATH=src` inside `Makefile`
- Docs maturity drift:
  rewrote README and core docs to describe the actual local demo MVP instead of a scaffold
- Missing API abuse guards:
  added question-length and numeric ceilings with FastAPI/Pydantic validation
- Unsafe `/run-eval` filesystem writes:
  removed caller-controlled output paths from the API and always write under `outputs/eval/`
- Tiny, permissive eval:
  expanded to 18 deterministic cases and tightened expected-source matching
- Raw UI output:
  reformatted ask and eval results into readable sections without redesigning the UI

## What was intentionally not changed
- No architecture redesign
- No cloud services, auth, or production infrastructure
- No embeddings, vector database, reranking, or LLM integrations
- No attempt to turn the browser UI into a larger frontend project
- No changes to the local lexical retrieval architecture beyond eval validation around it

## Updated local demo commands
- `make lint`
- `make test`
- `make up`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How long do card refunds take to settle?"`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How do I renew a passport in Canada?"`
- `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`

## Remaining non-blocking limitations
- The demo still uses lexical retrieval only
- Academic mode still uses markdown fixtures instead of live PDF parsing
- Browser-level live verification remains environment-dependent
- CLI `run-eval --output-dir` is still available for local developer workflows

## Freeze recommendation
YES
