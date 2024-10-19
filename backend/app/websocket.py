import logging

from fastapi import WebSocket, Depends, FastAPI
from sqlalchemy.orm import Session
from httpx import AsyncClient

from app.database import get_db
from app.models import User
from app.bot import notify_user


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_message(self, username: str, message: str):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_text(message)

    def is_online(self, username: str) -> bool:
        return username in self.active_connections


manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, 
                             username: str, 
                             db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        await websocket.close()
        return

    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()

            logger.info(f"Received message from {username}: {data}")

            receiver_username = "target_user"
            message_text = data

            async with AsyncClient() as client:
                await client.post(
                    "http://localhost:8000/send-message/",
                    json={"receiver_username": receiver_username, "message_text": message_text}
                )
    except Exception as e:

        logger.info(f"User {username} disconnected: {e}")
    
    finally:
        manager.disconnect(username)


@app.post("/send-message/")
async def send_message(receiver_username: str, 
                       message_text: str, 
                       db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == receiver_username).first()
    if user:
        is_offline = not manager.is_online(user.username)

        if is_offline and user.telegram_id:
            await notify_user(user.telegram_id, message_text)
            return {"message": "Уведомление отправлено через Telegram"}

        return {"message": "Пользователь онлайн, уведомление не отправлено"}

    return {"error": "Пользователь не найден"}