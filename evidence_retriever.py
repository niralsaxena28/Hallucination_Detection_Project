"""
evidence_retriever.py

Retrieves supporting evidence for a claim using sentence embeddings + FAISS
similarity search.

 - Evidence stored with metadata (source, reliability) instead of plain strings.
 - Cosine similarity via normalized embeddings + IndexFlatIP.
 - A similarity threshold, so "no relevant evidence found" is a possible result.
 - Evidence lives in an external JSON file (path + settings from config.py).
"""

import json
import os
from typing import Dict, List, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import (
    EMBEDDING_MODEL_NAME,
    EVIDENCE_DATA_PATH,
    EVIDENCE_SIMILARITY_THRESHOLD,
    EVIDENCE_TOP_K,
)


DEFAULT_EVIDENCE = [
    {
        "text": "India gained independence from British rule on 15 August 1947.",
        "source": "Wikipedia - Indian independence movement",
        "reliability": "high",
    },
    {
        "text": "Jawaharlal Nehru became the first Prime Minister of independent India.",
        "source": "Wikipedia - Jawaharlal Nehru",
        "reliability": "high",
    },
    {
        "text": "India is a country located in South Asia.",
        "source": "Wikipedia - India",
        "reliability": "high",
    },
    {
        "text": "The capital of India is New Delhi.",
        "source": "Wikipedia - New Delhi",
        "reliability": "high",
    },
]


class EvidenceRetriever:
    """Wraps the embedding model + FAISS index so the evidence database can
    be reloaded, extended, or swapped out without changing the calling code.
    """

    def __init__(self, evidence_path: Optional[str] = None, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.evidence_path = evidence_path or EVIDENCE_DATA_PATH
        self.evidence_database: List[Dict] = self._load_evidence()
        self.index = None
        self._build_index()

    # ------------------------------------------------------------------ #
    # Data loading
    # ------------------------------------------------------------------ #
    def _load_evidence(self) -> List[Dict]:
        if os.path.exists(self.evidence_path):
            with open(self.evidence_path, "r", encoding="utf-8") as f:
                return json.load(f)

        self._save_evidence(DEFAULT_EVIDENCE)
        return list(DEFAULT_EVIDENCE)

    def _save_evidence(self, evidence: List[Dict]) -> None:
        with open(self.evidence_path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------ #
    # Index building
    # ------------------------------------------------------------------ #
    def _build_index(self) -> None:
        texts = [item["text"] for item in self.evidence_database]
        embeddings = self._embed(texts)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def _embed(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.astype("float32")
        faiss.normalize_L2(embeddings)
        return embeddings

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def add_evidence(self, text: str, source: str = "unknown", reliability: str = "unverified") -> None:
        self.evidence_database.append({"text": text, "source": source, "reliability": reliability})
        self._save_evidence(self.evidence_database)
        self._build_index()

    def retrieve_evidence(
        self,
        claim: str,
        top_k: int = EVIDENCE_TOP_K,
        threshold: float = EVIDENCE_SIMILARITY_THRESHOLD,
    ) -> List[Dict]:
        if not self.evidence_database:
            return []

        claim_embedding = self._embed([claim])
        k = min(top_k, len(self.evidence_database))

        scores, indices = self.index.search(claim_embedding, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < threshold:
                continue
            item = self.evidence_database[idx]
            results.append(
                {
                    "text": item["text"],
                    "source": item.get("source", "unknown"),
                    "reliability": item.get("reliability", "unverified"),
                    "score": float(score),
                }
            )

        return results


# ---------------------------------------------------------------------- #
# Module-level convenience API — keeps `from evidence_retriever import
# retrieve_evidence` working unchanged in main.py / claim_extractor.py.
# ---------------------------------------------------------------------- #
_retriever = EvidenceRetriever()


def retrieve_evidence(
    claim: str, top_k: int = EVIDENCE_TOP_K, threshold: float = EVIDENCE_SIMILARITY_THRESHOLD
) -> List[Dict]:
    return _retriever.retrieve_evidence(claim, top_k=top_k, threshold=threshold)


def add_evidence(text: str, source: str = "unknown", reliability: str = "unverified") -> None:
    _retriever.add_evidence(text, source=source, reliability=reliability)


if __name__ == "__main__":
    test_claims = [
        "India became independent in 1947.",
        "Jawaharlal Nehru was the first Prime Minister of India.",
        "The Eiffel Tower is located in Rome.",
    ]

    for claim in test_claims:
        print(f"\nClaim: {claim}")
        evidence = retrieve_evidence(claim)
        if not evidence:
            print("  -> No sufficiently relevant evidence found.")
        else:
            for e in evidence:
                print(f"  -> [{e['score']:.3f}] {e['text']}  (source: {e['source']})")