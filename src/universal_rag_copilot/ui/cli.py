"""CLI for demo QA and local evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

from universal_rag_copilot.domain import ChunkProfile, CorpusMode
from universal_rag_copilot.evaluation import run_evaluation
from universal_rag_copilot.pipeline import ask_demo, build_demo_index


def _enum_parser(enum_cls: type[CorpusMode] | type[ChunkProfile], value: str):
    try:
        return enum_cls(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Universal RAG Copilot CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index-demo", help="Ingest and index fixture corpus")
    index_parser.add_argument("--mode", type=lambda v: _enum_parser(CorpusMode, v), required=True)
    index_parser.add_argument(
        "--profile", type=lambda v: _enum_parser(ChunkProfile, v), required=True
    )

    ask_parser = subparsers.add_parser("ask-demo", help="Ask grounded question over fixture corpus")
    ask_parser.add_argument("--mode", type=lambda v: _enum_parser(CorpusMode, v), required=True)
    ask_parser.add_argument(
        "--profile", type=lambda v: _enum_parser(ChunkProfile, v), required=True
    )
    ask_parser.add_argument("--question", required=True)
    ask_parser.add_argument("--top-k", type=int, default=4)
    ask_parser.add_argument("--min-score-threshold", type=float, default=0.07)
    ask_parser.add_argument("--min-evidence-results", type=int, default=1)

    eval_parser = subparsers.add_parser("run-eval", help="Run local retrieval/answerability eval")
    eval_parser.add_argument("--cases", type=Path, default=None)
    eval_parser.add_argument("--output-dir", type=Path, default=None)

    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "index-demo":
        _, doc_count, chunk_count = build_demo_index(mode=args.mode, profile=args.profile)
        print(
            f"Indexed mode={args.mode.value} profile={args.profile.value}: "
            f"documents={doc_count} chunks={chunk_count}"
        )
        return 0

    if args.command == "ask-demo":
        result = ask_demo(
            question=args.question,
            mode=args.mode,
            profile=args.profile,
            top_k=args.top_k,
            min_score_threshold=args.min_score_threshold,
            min_evidence_results=args.min_evidence_results,
        )
        print(result.answer)
        print(f"\nAnswerability: {result.answerability.value}")
        if result.citations:
            print("\nCitations:")
            for c in result.citations:
                print(
                    f"- {c.title} | section: {c.section} | chunk: {c.chunk_id} | score: {c.score}"
                )
        else:
            print("\nCitations: none")
        return 0

    _, json_path, md_path = run_evaluation(cases_path=args.cases, output_dir=args.output_dir)
    print(f"Evaluation completed. JSON report: {json_path}")
    print(f"Evaluation completed. Markdown report: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
