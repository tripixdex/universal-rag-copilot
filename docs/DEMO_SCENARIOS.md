# Demo Scenarios (Design-Time)

These are walkthrough scenarios for validating MVP intent before full implementation.

## Scenario 1: `support_kb`
- Corpus: internal support docs with FAQs and troubleshooting pages
- Mode: `support_kb`
- Chunking profile: `balanced`
- User question: "How do I reset a 2FA device if the old phone is lost?"
- Expected behavior:
  - Retrieval prioritizes procedural sections and exact policy steps
  - Answer provides clear steps in order
  - Citations point to specific support pages/sections used

## Scenario 2: `academic_pdf`
- Corpus: a small set of scientific PDFs on one topic
- Mode: `academic_pdf`
- Chunking profile: `coarse`
- User question: "What evidence is reported for method X improving recall?"
- Expected behavior:
  - Retrieval favors larger context windows from relevant paper sections
  - Answer summarizes evidence conservatively
  - Citations include paper title + section/page anchors when available

## Scenario 3: Not enough evidence
- Corpus: either mode, but missing direct support for the claim
- User question: "Does the corpus prove that method X is always optimal?"
- Expected behavior:
  - System does not fabricate certainty
  - Answer explicitly states evidence is insufficient
  - Citations (if any) show related but non-conclusive sources
  - User gets a suggestion to refine query or add more documents
