# Evaluation Plan (Local Harness)

## Scope
Evaluate retrieval grounding and answerability decisions across local fixture corpora.

## Case dataset
Location: `fixtures/eval/cases.json`

Each case defines:
- `case_id`
- `mode`
- `profile`
- `question`
- `expected_document_ids` and/or `expected_citation_titles`
- `expected_answerability` (`answerable` or `not_enough_evidence`)

Current coverage:
- `support_kb`: answerable case
- `academic_pdf`: answerable case
- insufficient evidence: unanswerable case

## Runner
- Module: `src/universal_rag_copilot/evaluation/runner.py`
- CLI: `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`

Runner behavior per case:
1. Build mode/profile index from fixtures
2. Run retrieval with configured controls
3. Evaluate answerability match
4. Evaluate expected-source match against retrieved docs/citations
5. Record per-case result and aggregate pass count

## Outputs
Written under `outputs/eval/`:
- `eval_<timestamp>.json`
- `eval_<timestamp>.md`

JSON report shape:
- `generated_at_utc`
- `total_cases`
- `passed_cases`
- `cases[]` with match flags and observed sources

## Next expansions
- Add hit@k / MRR style metrics
- Add adversarial distractor cases
- Add profile sensitivity sweeps (fine/balanced/coarse)
- Add conflict-handling cases for citation precision
