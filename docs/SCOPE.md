# Scope

## MVP (in scope now)
- Product specification for a local-first multi-mode RAG copilot
- Architecture boundaries and module responsibilities
- Definitions for two corpus modes and three chunking profiles
- Checkable acceptance criteria and demo scenarios
- Evaluation plan focused on retrieval and citation quality
- Minimal Python repository skeleton (docstring-only modules)

## Later (post-MVP implementation phases)
- Actual ingestion pipelines for support sources and PDFs
- Chunker implementations per profile
- Embeddings and vector index integration
- Retrieval ranking and query rewriting
- Answer generation logic with citation rendering
- CLI or lightweight UI
- Automated evaluation harness and metrics dashboard

## Out of scope for this stage
- Full end-to-end app implementation
- Hosted/cloud deployment
- Multi-user auth and permission systems
- Continuous ingestion and production scheduling
- Agentic tool use beyond RAG Q&A
- Large dependency stack or framework lock-in
