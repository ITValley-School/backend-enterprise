import json
from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[Dict]] = {}

    async def connect(self, websocket: WebSocket, channel_id: str, user_id: str):
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = []
        self.active_connections[channel_id].append({
            "socket": websocket,
            "user_id": user_id
        })

    def disconnect(self, websocket: WebSocket, channel_id: str):
        connections = self.active_connections.get(channel_id, [])
        connections = [conn for conn in connections if conn["socket"] != websocket]
        if connections:
            self.active_connections[channel_id] = connections
        else:
            del self.active_connections[channel_id]

    async def send_channel_message(self, message: dict, channel_id: str):
        for conn in self.active_connections.get(channel_id, []):
            await conn["socket"].send_text(json.dumps(message))

    def is_user_online(self, user_id: str) -> bool:
        for connections in self.active_connections.values():
            if any(conn["user_id"] == user_id for conn in connections):
                return True
        return False
