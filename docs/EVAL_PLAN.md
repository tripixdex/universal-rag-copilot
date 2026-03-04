# Evaluation Plan (MVP-Oriented)

## Goal
Measure whether retrieval and answer grounding are trustworthy across `support_kb` and `academic_pdf` corpora.

## Dataset plan
- Build small fixture sets per mode in `fixtures/`.
- For each query, maintain expected relevant passages and non-relevant distractors.
- Include at least one insufficient-evidence query per mode.

## Retrieval-focused checks
- Top-k relevance: at least one gold passage appears in top-k for target queries.
- Mode sensitivity: same query evaluated under both modes should show different ranking behavior where appropriate.
- Profile sensitivity: `fine` vs `coarse` changes chunk granularity and retrieval candidates as expected.

## Answer-with-citations checks
- Every factual claim in answer should map to at least one retrieved citation.
- Citation precision: citation points to text that actually supports claim.
- Citation format consistency: source identifiers are readable and stable.

## Failure-case checks
- Insufficient evidence: assistant must respond with uncertainty instead of fabricated facts.
- Conflicting sources: assistant should acknowledge conflict and avoid overconfident conclusion.
- Off-topic query: assistant should avoid irrelevant synthesis and suggest re-scoping.

## Reporting
- Save run artifacts under `outputs/`.
- Track simple metrics first: retrieval hit@k, citation coverage rate, insufficient-evidence correctness.
- Add qualitative error notes per failed query to guide next iteration.
