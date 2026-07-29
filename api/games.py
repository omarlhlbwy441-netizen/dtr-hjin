"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — Games API                                ║
║  نقاط نهاية نظام توليد الألعاب                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from dtr_n.game_architect import get_game_architect

router = APIRouter(prefix="/api/games", tags=["Games"])
game_architect = get_game_architect()


class GameGenerateRequest(BaseModel):
    game_type: str
    title: str
    custom_config: Optional[Dict[str, Any]] = None


class GameResponse(BaseModel):
    status: str
    game_id: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    play_url: Optional[str] = None
    files: Optional[List[str]] = None
    message: Optional[str] = None


@router.get("/templates")
async def list_game_templates():
    """قائمة قوالب الألعاب المتاحة"""
    return {
        "templates": game_architect.list_templates(),
        "count": len(game_architect.list_templates())
    }


@router.post("/generate", response_model=GameResponse)
async def generate_game(request: GameGenerateRequest):
    """توليد لعبة جديدة"""
    try:
        result = game_architect.generate_game(
            game_type=request.game_type,
            title=request.title,
            custom_config=request.custom_config
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return GameResponse(
            status="success",
            game_id=result["game_id"],
            title=result["title"],
            type=result["type"],
            play_url=result["play_url"],
            files=result["files"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_generated_games():
    """قائمة الألعاب المولدة"""
    return {
        "games": game_architect.list_games(),
        "count": len(game_architect.list_games())
    }


@router.get("/{game_id}")
async def get_game(game_id: str):
    """الحصول على معلومات لعبة محددة"""
    game = game_architect.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game
