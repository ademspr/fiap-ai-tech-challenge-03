import os

import chromadb
from sentence_transformers import SentenceTransformer

from model import PubMedSource

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIR = os.path.join(BASE_DIR, "data", "chroma_db")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class PubMedSearcher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        client = chromadb.PersistentClient(path=PERSIST_DIR)

        self._initialized = True
        self._collection = client.get_collection("pubmedqa")
        self._model = SentenceTransformer(EMBEDDING_MODEL)

    def search(self, query: str, top_k: int = 2) -> list[PubMedSource]:
        query_embedding = self._model.encode([query])[0].tolist()
        results = self._collection.query(
            query_embeddings=[query_embedding], n_results=top_k
        )

        sources = []
        for metadata in results.get("metadatas", [[]])[0]:
            if metadata is None:
                continue

            sources.append(
                PubMedSource(
                    pmid=metadata.get("pmid", ""),
                    question=metadata.get("question", ""),
                    contexts=metadata.get("contexts", "").split("|||"),
                    labels=metadata.get("labels", "").split(","),
                    year=metadata.get("year", "N/A"),
                    meshes=metadata.get("meshes", "").split(",")
                    if metadata.get("meshes")
                    else [],
                )
            )

        return sources


def search_pubmed(query: str, top_k: int = 2) -> list[PubMedSource]:
    return PubMedSearcher().search(query, top_k)
