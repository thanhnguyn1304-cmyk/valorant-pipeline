"""Quick debug script to test full seed with error details."""
import sys, os, time, traceback
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core import database
database.engine.echo = False  # Quiet SQL logs

from google import genai
from google.genai import types
from sqlmodel import Session, select, text
from core.config import settings
from core.database import engine
from models.coaching_tip import CoachingTip
from services.coaching_knowledge import COACHING_KNOWLEDGE

EMBEDDING_MODEL = "gemini-embedding-001"
BATCH_SIZE = 10

def seed_debug():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    texts = [item["content"] for item in COACHING_KNOWLEDGE]
    print(f"[Seed] Embedding {len(texts)} tips...")

    # Batch embed
    embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        chunk = texts[i : i + BATCH_SIZE]
        print(f"  Batch {i // BATCH_SIZE + 1} ({len(chunk)} tips)...")
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=chunk,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )
        embeddings.extend([e.values for e in result.embeddings])
        if i + BATCH_SIZE < len(texts):
            time.sleep(15)

    print(f"[Seed] Got {len(embeddings)} embeddings, dims={len(embeddings[0])}")

    # Clear + insert
    with Session(engine) as db:
        # Use raw SQL to truncate for speed
        db.exec(text("DELETE FROM coachingtip"))
        db.commit()
        print("[Seed] Cleared table.")

        # Insert one by one to find the problematic tip
        for i, item in enumerate(COACHING_KNOWLEDGE):
            try:
                tip = CoachingTip(
                    content=item["content"],
                    agent=item["agent"],
                    map_name=item["map"],
                    category=item["category"],
                    embedding=embeddings[i],
                )
                db.add(tip)
                db.flush()  # force insert now
            except Exception as e:
                print(f"\n!!! FAILED at tip {i}: {e}")
                print(f"    agent={item['agent']}, map={item['map']}, cat={item['category']}")
                print(f"    content preview: {item['content'][:80]}")
                traceback.print_exc()
                db.rollback()
                return

        db.commit()
        count = len(db.exec(select(CoachingTip)).all())
        print(f"[Seed] Inserted {count} tips. Done!")

if __name__ == "__main__":
    seed_debug()
