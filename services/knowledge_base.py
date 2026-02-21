"""
Knowledge Base Service - The "Librarian"
Searches coaching tips using pgvector cosine similarity in PostgreSQL.

All embeddings live in the `coachingtip` table (seeded by scripts/seed_knowledge.py).
At query time, we embed the search text with Gemini and let pgvector rank results.
"""

from google import genai
from google.genai import types
from sqlmodel import Session, select
from core.config import settings
from models.coaching_tip import CoachingTip

# ─── Config ───────────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "gemini-embedding-001"

# Shared Gemini client (created once, reused)
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _embed_query(text: str) -> list[float]:
    """Embed a single query string using Gemini."""
    client = _get_client()
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return result.embeddings[0].values


# ─── Public API ───────────────────────────────────────────────────────────────

def search_knowledge(
    query: str,
    db: Session,
    top_k: int = 3,
    agent_filter: str | None = None,
    map_filter: str | None = None,
) -> list[dict]:
    """
    Search the coaching knowledge base using pgvector cosine distance.

    Args:
        query: Natural language search query (e.g., "low headshot tips")
        db: SQLModel database session
        top_k: Number of results to return
        agent_filter: Optional agent name to filter by
        map_filter: Optional map name to filter by

    Returns:
        List of dicts with 'content', 'agent', 'map', 'category', 'score'
    """
    query_vec = _embed_query(query)

    # Build the pgvector query — ORDER BY cosine distance (ascending = most similar first)
    stmt = select(
        CoachingTip,
        CoachingTip.embedding.cosine_distance(query_vec).label("distance"),
    )

    # Apply metadata filters (but always include "all" tips)
    if agent_filter:
        stmt = stmt.where(CoachingTip.agent.in_([agent_filter, "all"]))
    if map_filter:
        stmt = stmt.where(CoachingTip.map_name.in_([map_filter, "all"]))

    stmt = stmt.order_by("distance").limit(top_k)

    results = db.exec(stmt).all()

    return [
        {
            "content": tip.content,
            "agent": tip.agent,
            "map": tip.map_name,
            "category": tip.category,
            "score": round(1.0 - distance, 4),  # Convert distance to similarity
        }
        for tip, distance in results
    ]
