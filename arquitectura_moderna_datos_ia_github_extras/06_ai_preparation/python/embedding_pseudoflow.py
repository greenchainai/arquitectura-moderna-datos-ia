"""
Pseudoflujo de preparación documental y embeddings.
Sustituir las funciones NotImplemented por el stack corporativo real.
"""


def extract_text(document_path: str) -> str:
    raise NotImplementedError


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks


def create_embedding(text: str) -> list[float]:
    raise NotImplementedError


def upsert_vector(chunk_id: str, embedding: list[float], metadata: dict) -> None:
    raise NotImplementedError


def process_document(document_path: str, metadata: dict) -> None:
    text = extract_text(document_path)
    for index, chunk in enumerate(chunk_text(text)):
        chunk_id = f"{metadata['document_id']}_chunk_{index:04d}"
        embedding = create_embedding(chunk)
        upsert_vector(chunk_id, embedding, {**metadata, "chunk_index": index, "chunk_text": chunk})
