# Architecture

## Design principles
- Local-first by default
- Clear module boundaries
- Corpus-aware behavior through modes
- Honest answering with explicit evidence limits

## Modules

### 1) Ingestion
Purpose: parse raw corpus inputs and normalize records.
- `support_kb`: preserve titles, headings, article metadata, procedural structure
- `academic_pdf`: preserve paper metadata, sections, page mapping, references

### 2) Chunking
Purpose: split normalized documents into retrieval units.
- Profiles: `fine`, `balanced`, `coarse`
- Strategy varies by mode to preserve useful context shape

### 3) Embeddings / Index
Purpose: provide the searchable evidence index used by the current demo.
- Current implementation uses a deterministic lexical index over chunk token sets
- Vector retrieval is intentionally not implemented in this local MVP

### 4) Retrieval
Purpose: map query to ranked evidence chunks.
- Responsible for top-k selection and metadata propagation
- Must expose retrieved evidence for answer grounding

### 5) Answering
Purpose: generate response grounded in retrieved evidence.
- Must include citations
- Must support "not enough evidence" output path

### 6) Evaluation
Purpose: validate retrieval and grounded-answer behavior.
- Query fixtures
- Expected evidence checks
- Failure case coverage

### 7) UI
Purpose: provide the local interaction surfaces that already exist.
- CLI for indexing, asking demo questions, and running eval
- Minimal API and plain browser UI for local demos

## Data flow (logical)
1. Raw corpus -> ingestion
2. Normalized docs -> chunking
3. Chunks -> embeddings/index
4. Query -> retrieval
5. Retrieved evidence -> answering
6. Outputs + logs -> evaluation artifacts
