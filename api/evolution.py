"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — Evolution Engine API                     ║
║  نقاط نهاية محرك التطور الذاتي                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from dtr_n.evolution_engine import DTREvolutionEngine, create_engine

router = APIRouter(prefix="/api/evolution", tags=["Evolution"])

# Global engine instance
evolution_engine: DTREvolutionEngine = create_engine()


class EvolutionTrigger(BaseModel):
    feedback: Optional[List[Dict[str, Any]]] = None
    auto: bool = True


class EvolutionResponse(BaseModel):
    status: str
    feature: Optional[str] = None
    iq_level: Optional[int] = None
    version: Optional[str] = None
    message: Optional[str] = None


@router.get("/status")
async def evolution_status():
    """Get current evolution engine status"""
    return {
        "status": "running" if evolution_engine.is_running else "idle",
        "iq_level": getattr(evolution_engine, 'iq_level', 1),
        "version": getattr(evolution_engine, 'version', '1.0.0'),
        "evolution_count": len(getattr(evolution_engine, 'evolution_log', [])),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/log")
async def evolution_log():
    """Get evolution history log"""
    log = getattr(evolution_engine, 'evolution_log', [])
    return {
        "log": log,
        "count": len(log),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/trigger", response_model=EvolutionResponse)
async def trigger_evolution(data: EvolutionTrigger, background_tasks: BackgroundTasks):
    """Trigger a single evolution cycle"""
    try:
        feedback = data.feedback or [{"type": "feature_request", "content": "auto", "priority": "medium"}]

        next_feature = await evolution_engine._determine_next_feature(feedback)
        if next_feature:
            code_result = await evolution_engine._generate_feature_code(next_feature)
            await evolution_engine._write_code_file(code_result)
            return EvolutionResponse(
                status="success",
                feature=next_feature.get("name"),
                iq_level=getattr(evolution_engine, 'iq_level', 1),
                version=getattr(evolution_engine, 'version', '1.0.0')
            )
        return EvolutionResponse(status="no_action", message="No feature determined")
    except Exception as e:
        return EvolutionResponse(status="error", message=str(e))


@router.post("/start-loop")
async def start_evolution_loop(background_tasks: BackgroundTasks):
    """Start continuous evolution loop"""
    if not evolution_engine.is_running:
        background_tasks.add_task(evolution_engine.start_evolution_loop)
        return {"status": "started", "message": "Evolution loop started"}
    return {"status": "already_running", "message": "Evolution loop is already running"}


@router.post("/stop-loop")
async def stop_evolution_loop():
    """Stop continuous evolution loop"""
    evolution_engine.is_running = False
    return {"status": "stopped", "message": "Evolution loop stopped"}


@router.get("/iq")
async def get_iq_level():
    """Get current IQ level"""
    return {
        "iq_level": getattr(evolution_engine, 'iq_level', 1),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/feedback")
async def submit_feedback(feedback: Dict[str, Any]):
    """Submit feedback for evolution engine"""
    try:
        result = await evolution_engine._determine_next_feature([feedback])
        return {
            "status": "success",
            "next_feature": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
