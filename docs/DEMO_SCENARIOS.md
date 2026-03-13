# Demo Scenarios

These scenarios reflect the current runnable demo.

## Scenario 1: Answerable support question
- Command:
  `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How long do card refunds take to settle?"`
- Expected behavior:
  - Returns an `answerable` result
  - Mentions the 5-10 business day card-settlement timeline
  - Cites `Returns and Refunds`

## Scenario 2: Answerable academic question
- Command:
  `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode academic_pdf --profile balanced --question "In batch gradient descent, what data does each step use?"`
- Expected behavior:
  - Returns an `answerable` result
  - Grounds the answer in `Optimization for Machine Learning`
  - Shows citations rather than free-form unsupported text

## Scenario 3: Not enough evidence
- Command:
  `PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How do I renew a passport in Canada?"`
- Expected behavior:
  - Returns `not_enough_evidence`
  - Produces no citations
  - Avoids fabricating an answer

## Scenario 4: Eval credibility pass
- Command:
  `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`
- Expected behavior:
  - Runs the expanded deterministic eval set
  - Writes JSON and Markdown reports under `outputs/eval/`
  - Reports at least 15 total cases

## Scenario 5: Local API/UI demo
- Commands:
  `make up`
  then open `http://127.0.0.1:8000/ui`
- Expected behavior:
  - `/ui` loads the plain HTML demo
  - Ask results display answerability, answer text, citations, and retrieval summary in separate sections
  - Eval results display pass count and report paths

## Known limitation for restricted environments
- If local socket binding is blocked by the environment, API behavior can still be verified with `make test` and FastAPI `TestClient`, but live browser/socket verification cannot be claimed.
