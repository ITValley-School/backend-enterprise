from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from api.v1.repository.chat_repository import save_message
from api.v1.services.chat_ws_manager import ConnectionManager
from db.models.chat_message import ChatMessage
from db.session import get_db
import json

manager = ConnectionManager()
router = APIRouter()


@router.websocket("/ws/{channel_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: str, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()

    await manager.connect(websocket, channel_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                from_id = message_data["from"]
                to_id = message_data["to"]
                content = message_data["message"]

                save_message(db, from_id=from_id, to_id=to_id, content=content)

                # Broadcast para todos no canal
                await manager.send_channel_message({
                    "from_id": from_id,
                    "to_id": to_id,
                    "content": content,
                    "created_at": str(datetime.utcnow())
                }, channel_id)
            except (KeyError, json.JSONDecodeError):
                await websocket.send_text("Formato inválido. Envie JSON: {\"from\": \"...\", \"to\": \"...\", \"message\": \"...\"}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel_id)

@router.websocket("/ws/presence-{user_id}")
async def presence_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    await manager.connect(websocket, f"presence-{user_id}", user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, f"presence-{user_id}")

@router.get("/history/{user1_id}/{user2_id}")
def chat_history(user1_id: str, user2_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.from_id == user1_id) & (ChatMessage.to_id == user2_id)) |
        ((ChatMessage.from_id == user2_id) & (ChatMessage.to_id == user1_id))
    ).order_by(ChatMessage.created_at).all()

    return [
        {
            "from_id": msg.from_id,
            "to_id": msg.to_id,
            "content": msg.content,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@router.get("/status/{user_id}")
def get_user_status(user_id: str):
    is_online = manager.is_user_online(user_id)
    return {"user_id": user_id, "status": "online" if is_online else "offline"}
