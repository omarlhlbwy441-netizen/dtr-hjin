"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — WebSocket Endpoints                      ║
║  اتصال فوري ثنائي الاتجاه للوكلاء والمحادثات                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/ws", tags=["WebSocket"])
security = HTTPBearer()

# Active connections store
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        self.user_connections[id(websocket)] = websocket
        print(f"🔌 WebSocket connected: {client_id} (total: {len(self.user_connections)})")

    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            if websocket in self.active_connections[client_id]:
                self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        if id(websocket) in self.user_connections:
            del self.user_connections[id(websocket)]
        print(f"🔌 WebSocket disconnected: {client_id} (total: {len(self.user_connections)})")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict, client_id: Optional[str] = None):
        if client_id and client_id in self.active_connections:
            for connection in self.active_connections[client_id]:
                await connection.send_json(message)
        else:
            for connections in self.active_connections.values():
                for connection in connections:
                    await connection.send_json(message)

manager = ConnectionManager()


@router.websocket("/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """Real-time chat WebSocket endpoint"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()

            message_type = data.get("type", "message")
            content = data.get("content", "")
            agent_id = data.get("agent_id", "general")

            response = {
                "type": message_type,
                "content": content,
                "agent_id": agent_id,
                "client_id": client_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "received"
            }

            # Echo back with processing status
            await manager.send_personal_message(response, websocket)

            # Simulate AI processing
            await asyncio.sleep(0.5)

            ai_response = {
                "type": "ai_response",
                "content": f"Processed: {content}",
                "agent_id": agent_id,
                "client_id": client_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            await manager.send_personal_message(ai_response, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
    except Exception as e:
        manager.disconnect(websocket, client_id)
        print(f"WebSocket error: {e}")


@router.websocket("/agent/{agent_id}/{client_id}")
async def websocket_agent(websocket: WebSocket, agent_id: str, client_id: str):
    """Agent-specific WebSocket endpoint"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()

            response = {
                "type": "agent_message",
                "agent_id": agent_id,
                "client_id": client_id,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }

            await manager.send_personal_message(response, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


@router.get("/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "active_connections": len(manager.user_connections),
        "active_clients": len(manager.active_connections),
        "clients": list(manager.active_connections.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }
