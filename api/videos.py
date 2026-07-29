"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — Videos API                                ║
║  نقاط نهاية نظام توليد الفيديو                                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from dtr_n.video_architect import get_video_architect

router = APIRouter(prefix="/api/videos", tags=["Videos"])
video_architect = get_video_architect()


class VideoGenerateRequest(BaseModel):
    template_type: str
    title: str
    script: Optional[str] = None
    custom_config: Optional[Dict[str, Any]] = None


@router.get("/templates")
async def list_video_templates():
    """قائمة قوالب الفيديو المتاحة"""
    return {
        "templates": video_architect.list_templates(),
        "count": len(video_architect.list_templates()),
        "ffmpeg_available": video_architect.ffmpeg_available
    }


@router.post("/generate")
async def generate_video(request: VideoGenerateRequest):
    """توليد فيديو جديد"""
    try:
        result = video_architect.generate_video(
            template_type=request.template_type,
            title=request.title,
            script=request.script,
            custom_config=request.custom_config
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_generated_videos():
    """قائمة الفيديوهات المولدة"""
    return {
        "videos": video_architect.list_videos(),
        "count": len(video_architect.list_videos())
    }
