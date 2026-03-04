from universal_rag_copilot.chunking import chunk_documents
from universal_rag_copilot.domain import ChunkProfile, CorpusMode
from universal_rag_copilot.ingestion import load_fixture_documents


def _avg_words(chunks):
    return sum(len(c.text.split()) for c in chunks) / len(chunks)


def test_chunking_varies_by_mode_and_profile() -> None:
    support_docs = load_fixture_documents(CorpusMode.SUPPORT_KB)
    academic_docs = load_fixture_documents(CorpusMode.ACADEMIC_PDF)

    support_fine = chunk_documents(support_docs, ChunkProfile.FINE)
    support_coarse = chunk_documents(support_docs, ChunkProfile.COARSE)
    academic_balanced = chunk_documents(academic_docs, ChunkProfile.BALANCED)

    assert len(support_fine) > len(support_coarse)
    assert _avg_words(support_fine) < _avg_words(support_coarse)
    assert _avg_words(support_coarse) < _avg_words(academic_balanced)
