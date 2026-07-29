"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — Websites API                              ║
║  نقاط نهاية نظام بناء المواقع                                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from dtr_n.web_architect import get_web_architect

router = APIRouter(prefix="/api/websites", tags=["Websites"])
web_architect = get_web_architect()


class WebsiteGenerateRequest(BaseModel):
    template_type: str
    title: str
    custom_config: Optional[Dict[str, Any]] = None


@router.get("/templates")
async def list_website_templates():
    """قائمة قوالب المواقع المتاحة"""
    return {
        "templates": web_architect.list_templates(),
        "count": len(web_architect.list_templates())
    }


@router.post("/generate")
async def generate_website(request: WebsiteGenerateRequest):
    """توليد موقع جديد"""
    try:
        result = web_architect.generate_website(
            template_type=request.template_type,
            title=request.title,
            custom_config=request.custom_config
        )

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_generated_websites():
    """قائمة المواقع المولدة"""
    return {
        "websites": web_architect.list_websites(),
        "count": len(web_architect.list_websites())
    }
