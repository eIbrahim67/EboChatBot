from typing import List
from langchain.embeddings.base import Embeddings

def nomic_embed_text(texts: List[str]) -> List[List[float]]:
    # Dummy implementation: returns a fixed 768-dimensional embedding
    return [[0.1] * 768 for _ in texts]

class LocalNomicEmbedder(Embeddings):
    def embed_query(self, query: str) -> List[float]:
        return nomic_embed_text([query])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return nomic_embed_text(texts)