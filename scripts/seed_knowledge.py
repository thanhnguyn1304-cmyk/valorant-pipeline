"""
Incremental Seed Knowledge Base — embeds coaching tips one by one and inserts them.
This approach handles strict rate limits by committing progress and allows for resuming.

Usage:
    docker-compose exec backend python scripts/seed_knowledge.py
"""

import sys
import os
import time
import hashlib

# Add the backend root to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google import genai
from google.genai import types
from sqlmodel import Session, select
from core.config import settings
from core.database import engine
from models.coaching_tip import CoachingTip
from services.coaching_knowledge import COACHING_KNOWLEDGE

EMBEDDING_MODEL = "gemini-embedding-001"


def get_content_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def seed():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    print(f"[Seed] Processing {len(COACHING_KNOWLEDGE)} coaching tips...")

    with Session(engine) as db:
        # Load existing tips to skip them
        existing_tips = db.exec(select(CoachingTip)).all()
        existing_content = {tip.content for tip in existing_tips}
        print(f"[Seed] Found {len(existing_content)} tips already in DB.")

        newly_inserted = 0
        skipped = 0

        for i, item in enumerate(COACHING_KNOWLEDGE):
            content = item["content"]
            
            if content in existing_content:
                skipped += 1
                continue

            print(f"[Seed] ({i+1}/{len(COACHING_KNOWLEDGE)}) Embedding new tip: {content[:50]}...")
            
            # Retry logic for a single tip
            embedding = None
            for attempt in range(5):
                try:
                    result = client.models.embed_content(
                        model=EMBEDDING_MODEL,
                        contents=content,
                        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
                    )
                    embedding = result.embeddings[0].values
                    break
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        wait_time = (attempt + 1) * 30
                        print(f"    Rate limit hit. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                    else:
                        print(f"    Unexpected error: {e}")
                        raise e
            
            if embedding:
                tip = CoachingTip(
                    content=item["content"],
                    agent=item["agent"],
                    map_name=item["map"],
                    category=item["category"],
                    embedding=embedding,
                )
                db.add(tip)
                db.commit() # Commit each one to save progress
                existing_content.add(content)
                newly_inserted += 1
                
                # Small delay to stay under limit
                time.sleep(1) 
            else:
                print(f"    Failed to embed tip {i+1} after 5 attempts. Stopping for now.")
                break

        print(f"[Seed] Finished. Newly inserted: {newly_inserted}, Skipped: {skipped}, Total in DB: {len(existing_content)}")


if __name__ == "__main__":
    seed()
