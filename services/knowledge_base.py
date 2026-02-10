"""
Knowledge Base Service - The "Librarian"
Embeds coaching content using Gemini and performs in-memory cosine similarity search.

On first run, embeddings are generated and cached to a JSON file.
Subsequent runs load from cache (instant startup).
"""

import json
import os
import numpy as np
import google.generativeai as genai
from backend.core.config import settings
from backend.services.coaching_knowledge import COACHING_KNOWLEDGE

# ─── Config ───────────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "models/gemini-embedding-001"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "embeddings_cache.json")

# ─── Singleton: loaded once, reused for all requests ─────────────────────────

_knowledge_store: list[dict] | None = None


def _get_gemini_embeddings(texts: list[str]) -> list[list[float]]:
    """Call Gemini API to embed a batch of texts."""
    genai.configure(api_key=settings.GEMINI_API_KEY)
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=texts,
        task_type="retrieval_document",
    )
    return result["embedding"]


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def _build_and_cache_embeddings() -> list[dict]:
    """
    Embed all coaching tips and save to a JSON cache file.
    Only runs once — subsequent calls load from cache.
    """
    print("[Knowledge Base] Generating embeddings for coaching content...")

    texts = [item["content"] for item in COACHING_KNOWLEDGE]

    # Gemini supports batch embedding — send all at once
    embeddings = _get_gemini_embeddings(texts)

    store = []
    for i, item in enumerate(COACHING_KNOWLEDGE):
        store.append({
            "content": item["content"],
            "agent": item["agent"],
            "map": item["map"],
            "category": item["category"],
            "embedding": embeddings[i],
        })

    # Cache to disk
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f)

    print(f"[Knowledge Base] Cached {len(store)} embeddings to {CACHE_FILE}")
    return store


def _load_knowledge_store() -> list[dict]:
    """Load embeddings from cache, or generate if cache doesn't exist."""
    global _knowledge_store

    if _knowledge_store is not None:
        return _knowledge_store

    if os.path.exists(CACHE_FILE):
        print("[Knowledge Base] Loading embeddings from cache...")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            _knowledge_store = json.load(f)
        print(f"[Knowledge Base] Loaded {len(_knowledge_store)} embeddings")
    else:
        _knowledge_store = _build_and_cache_embeddings()

    return _knowledge_store


# ─── Public API ───────────────────────────────────────────────────────────────

def search_knowledge(
    query: str,
    top_k: int = 3,
    agent_filter: str | None = None,
    map_filter: str | None = None,
) -> list[dict]:
    """
    Search the coaching knowledge base using cosine similarity.

    Args:
        query: Natural language search query (e.g., "low headshot tips")
        top_k: Number of results to return
        agent_filter: Optional agent name to prioritize (still returns 'all' tips)
        map_filter: Optional map name to prioritize (still returns 'all' tips)

    Returns:
        List of dicts with 'content', 'agent', 'map', 'category', 'score'
    """
    store = _load_knowledge_store()

    # Embed the query
    genai.configure(api_key=settings.GEMINI_API_KEY)
    query_result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
        task_type="retrieval_query",
    )
    query_vec = np.array(query_result["embedding"])

    # Score each item
    scored = []
    for item in store:
        item_vec = np.array(item["embedding"])
        score = _cosine_similarity(query_vec, item_vec)

        # Boost score for matching agent/map filters
        if agent_filter and item["agent"] in (agent_filter, "all"):
            score += 0.05
        if map_filter and item["map"] in (map_filter, "all"):
            score += 0.05

        scored.append({
            "content": item["content"],
            "agent": item["agent"],
            "map": item["map"],
            "category": item["category"],
            "score": round(score, 4),
        })

    # Sort by score, return top_k
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def initialize_knowledge_base():
    """Pre-load the knowledge base (call at app startup)."""
    _load_knowledge_store()
    print("[Knowledge Base] Ready.")
