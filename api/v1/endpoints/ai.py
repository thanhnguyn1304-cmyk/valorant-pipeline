from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from backend.core.database import get_session
from backend.services.ai_service import generate_coaching_report_stream

router = APIRouter()


@router.get("/report/{puuid}", response_class=StreamingResponse)
async def get_coaching_report(puuid: str, db: Session = Depends(get_session)):
    """
    Stream a personalized coaching report for the given player.
    """
    return StreamingResponse(
        generate_coaching_report_stream(puuid, db),
        media_type="text/event-stream"
    )
