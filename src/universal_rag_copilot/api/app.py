"""Minimal local FastAPI app for demoing QA and eval."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from universal_rag_copilot.api.ui_page import UI_HTML
from universal_rag_copilot.domain import ChunkProfile, CorpusMode
from universal_rag_copilot.evaluation import run_evaluation
from universal_rag_copilot.pipeline import ask_demo_with_decision
from universal_rag_copilot.retrieval import RetrievalConfig

app = FastAPI(title="Universal RAG Copilot API", version="0.1.0")


class AskRequest(BaseModel):
    mode: str
    profile: str
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1)
    min_score_threshold: float = Field(default=0.07, ge=0)
    min_evidence_results: int = Field(default=1, ge=1)


class RunEvalRequest(BaseModel):
    output_dir: str | None = None


def _parse_mode(value: str) -> CorpusMode:
    try:
        return CorpusMode(value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"Invalid mode: {value}") from exc


def _parse_profile(value: str) -> ChunkProfile:
    try:
        return ChunkProfile(value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"Invalid profile: {value}") from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ui", response_class=HTMLResponse)
def ui() -> HTMLResponse:
    return HTMLResponse(content=UI_HTML)


@app.post("/ask")
def ask(payload: AskRequest) -> dict[str, object]:
    mode = _parse_mode(payload.mode)
    profile = _parse_profile(payload.profile)
    config = RetrievalConfig(
        top_k=payload.top_k,
        min_score_threshold=payload.min_score_threshold,
        min_evidence_results=payload.min_evidence_results,
    )
    answer, decision = ask_demo_with_decision(
        question=payload.question,
        mode=mode,
        profile=profile,
        config=config,
    )

    citations = [asdict(citation) for citation in answer.citations]
    retrieval_summary = {
        "top_k": config.top_k,
        "min_score_threshold": config.min_score_threshold,
        "min_evidence_results": config.min_evidence_results,
        "retrieved_count": len(decision.retrieved),
        "eligible_count": len(decision.eligible),
        "top_results": [
            {
                "document_id": item.chunk.document_id,
                "chunk_id": item.chunk.chunk_id,
                "title": item.chunk.title,
                "score": round(item.score, 4),
                "matched_terms": list(item.matched_terms),
            }
            for item in decision.retrieved
        ],
    }
    return {
        "answerability": answer.answerability.value,
        "answer": answer.answer,
        "citations": citations,
        "retrieval_summary": retrieval_summary,
    }


@app.post("/run-eval")
def run_eval(payload: RunEvalRequest) -> dict[str, object]:
    output_dir = Path(payload.output_dir) if payload.output_dir else None
    results, json_path, md_path = run_evaluation(output_dir=output_dir)
    passed = sum(1 for item in results if item.answerability_match and item.expected_source_match)
    return {
        "total_cases": len(results),
        "passed_cases": passed,
        "json_report_path": str(json_path),
        "markdown_report_path": str(md_path),
    }


def run() -> None:
    uvicorn.run(
        "universal_rag_copilot.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    run()
