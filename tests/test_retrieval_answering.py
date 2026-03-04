from universal_rag_copilot.answering import compose_answer
from universal_rag_copilot.chunking import chunk_documents
from universal_rag_copilot.domain import ChunkProfile, CorpusMode
from universal_rag_copilot.ingestion import load_fixture_documents
from universal_rag_copilot.retrieval import build_index, retrieve


def _run_query(mode: CorpusMode, profile: ChunkProfile, query: str):
    docs = load_fixture_documents(mode)
    chunks = chunk_documents(docs, profile)
    index = build_index(chunks)
    return retrieve(index=index, query=query, top_k=4)


def test_retrieval_support_question_hits_refund_content() -> None:
    results = _run_query(
        CorpusMode.SUPPORT_KB,
        ChunkProfile.BALANCED,
        "How long do card refunds take to settle?",
    )
    assert results
    assert (
        "5 - 10 business days" in results[0].chunk.text
        or "5-10 business days" in results[0].chunk.text
    )


def test_retrieval_academic_question_hits_gradient_descent() -> None:
    results = _run_query(
        CorpusMode.ACADEMIC_PDF,
        ChunkProfile.BALANCED,
        "What is gradient descent used for?",
    )
    assert results
    assert "gradient descent" in results[0].chunk.text.lower()


def test_insufficient_evidence_and_no_hallucination() -> None:
    question = "How do I renew a passport in Canada?"
    results = _run_query(CorpusMode.SUPPORT_KB, ChunkProfile.BALANCED, question)
    answer = compose_answer(question=question, results=results)

    assert answer.insufficient_evidence is True
    assert "Not enough evidence" in answer.answer
    assert not answer.citations
