from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        connections = self.active_connections.get(user_id, [])
        if websocket in connections:
            connections.remove(websocket)
            if not connections:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        connections = self.active_connections.get(user_id, [])
        for connection in connections:
            await connection.send_text(message)

    async def broadcast(self, message: str):
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_text(message)

    def is_user_online(self, user_id: str) -> bool:
        return user_id in self.active_connections and bool(self.active_connections[user_id])
