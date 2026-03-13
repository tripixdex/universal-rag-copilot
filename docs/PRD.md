# PRD: Universal RAG Copilot

## Problem
Teams store knowledge in different forms: support documentation and academic papers are common examples. A single retrieval pipeline often performs poorly across both because text structure, metadata, and evidence expectations differ.

## Users
- Solo builders and small teams working locally
- Support engineers searching operational guidance
- Researchers and technical readers validating claims in papers

## Product goal
Create a local-first RAG assistant that can switch corpus behavior through explicit modes, while keeping a consistent query and answer workflow.

## Core value proposition
- One assistant, multiple corpus behaviors
- Better retrieval quality by selecting corpus-aware ingestion/chunking
- Transparent answers with citations and graceful uncertainty
- Local-first default for privacy and low operational overhead

## Why multiple corpus modes exist
A support knowledge base and an academic PDF corpus are structurally different:
- Support KB: short procedural sections, FAQs, troubleshooting steps, frequent headings/lists
- Academic PDFs: long-form arguments, dense context, references, equations, sections

Using one ingestion/chunking strategy for both either fragments academic context or makes support answers too coarse. Modes allow targeted defaults without changing the user-facing product concept.

## MVP definition
MVP supports:
- Corpus modes: `support_kb`, `academic_pdf`
- Chunking profiles: `fine`, `balanced`, `coarse`
- Retrieval-first answer flow with citations
- Explicit "not enough evidence" behavior

The current repo delivers a runnable local demo MVP. It is intentionally not a production system.
