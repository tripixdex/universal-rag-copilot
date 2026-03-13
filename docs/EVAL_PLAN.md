# Evaluation Plan

## Goal
Provide a believable local quality signal for the current lexical RAG demo without introducing external services or nondeterminism.

## Dataset
- Fixture file: `fixtures/eval/cases.json`
- Current size: 18 cases
- Case categories:
  - answerable support questions
  - answerable academic questions
  - clearly unanswerable questions
  - distractor-heavy wording
  - near-miss wording
  - false-friend wording
  - cases where the wrong chunk or title could win if ranking regresses

## Per-case fields
- `case_id`
- `mode`
- `profile`
- `question`
- `expected_document_ids`
- `expected_citation_titles`
- `expected_top_document_id`
- `expected_answerability`

## Matching logic
Each case checks two things:

1. Answerability:
   expected vs actual `answerable` / `not_enough_evidence`

2. Source match:
   - `expected_top_document_id` must match the actual top retrieved document when provided
   - `expected_document_ids` must be a subset of the retrieved document ids
   - `expected_citation_titles` must be a subset of the emitted citation titles
   - cases with no expected sources only pass when the answer emits no citations

This is intentionally stricter than the earlier any-overlap rule.

## Runner
- Module: `src/universal_rag_copilot/evaluation/runner.py`
- CLI:
  `PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval`
- API:
  `POST /run-eval`

The runner is deterministic and writes reports under `outputs/eval/`.

## Outputs
- `outputs/eval/eval_<timestamp>.json`
- `outputs/eval/eval_<timestamp>.md`

JSON reports include:
- aggregate totals
- per-case answerability match
- per-case source match
- observed top document id
- observed retrieved document ids
- observed citation titles

## Current limitations
- The eval reflects a lexical baseline, so it validates stability of the implemented system rather than semantic excellence
- There are no aggregate ranking metrics such as MRR yet
- The corpus is still fixture-sized and intentionally local
