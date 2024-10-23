import logging
import json
from fastapi import WebSocket, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt

from app.database import get_db
from app.models import User, Message
from app.bot import notify_user
from app.config import JWT, get_config
from app.database import get_db

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Класс для управления подключениями WebSocket.
class ConnectionManager:
    def __init__(self):
        # Словарь для хранения активных WebSocket подключений, где ключ - имя пользователя.
        self.active_connections = {}

    # Метод для подключения пользователя.
    # Принимает WebSocket и имя пользователя, добавляет его в активные подключения.
    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    # Метод для отключения пользователя.
    # Удаляет пользователя из активных подключений.
    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    # Метод для отправки сообщения конкретному пользователю.
    # Использует имя пользователя для получения его WebSocket соединения.
    async def send_message(self, username: str, message: str):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_text(message)

    # Метод для проверки, находится ли пользователь в сети.
    def is_online(self, username: str) -> bool:
        return username in self.active_connections

# Создаем экземпляр менеджера подключений.
manager = ConnectionManager()

# Получаем конфигурацию JWT из файла конфигурации.
jwt_config = get_config(JWT, 'jwt')

# Определяем секретный ключ и алгоритм для подписи JWT.
SECRET_KEY = jwt_config.key
ALGORITHM = "HS256"

# Обработчик WebSocket соединения.
# Принимает WebSocket соединение, имя пользователя и токен.
async def websocket_endpoint(websocket: WebSocket, 
                             username: str, 
                             token: str = Query(...)):
    # Создаем сессию базы данных вручную.
    db = next(get_db())

    try:
        # Декодируем токен и проверяем, соответствует ли он пользователю.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub") != username:
            await websocket.close(code=403)
            return

        # Подключаем пользователя через WebSocket.
        await manager.connect(websocket, username)
        try:
            while True:
                # Получение сообщения от клиента.
                data = await websocket.receive_text()

                # Разбор сообщения (ожидаем формат JSON).
                message_data = json.loads(data)
                receiver_username = message_data["receiver"]
                message_text = message_data["message"]

                # Сохраняем сообщение в базе данных.
                new_message = Message(sender=username, 
                                      receiver=receiver_username, 
                                      message=message_text, 
                                      timestamp=datetime.utcnow())
                db.add(new_message)
                db.commit()

                # Проверяем, находится ли получатель в сети.
                is_receiver_online = manager.is_online(receiver_username)
                if is_receiver_online:
                    # Если получатель в сети, отправляем ему сообщение через WebSocket.
                    await manager.send_message(receiver_username, json.dumps({
                        "sender": username,
                        "message": message_text
                    }))
                else:
                    # Если получатель не в сети, отправляем уведомление через Telegram.
                    user = db.query(User).filter(User.username == receiver_username).first()
                    if user and user.telegram_id:
                        await notify_user(user.telegram_id, str(username + ": " + message_text))

                # Логируем сообщение.
                logger.info(f"Сообщение от {username} к {receiver_username}: {message_text}")

        except Exception as e:
            # Логируем ошибку, если произошла ошибка в процессе работы WebSocket.
            logger.error(f"Ошибка: {e}")
        finally:
            # Закрываем сессию базы данных.
            db.close()

    except JWTError:
        # Закрываем WebSocket, если токен не прошел проверку.
        await websocket.close(code=403)
    finally:
        # Отключаем пользователя, если клиент закрывает соединение.
        manager.disconnect(username)

