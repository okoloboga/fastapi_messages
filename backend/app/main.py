import logging

from fastapi import FastAPI, WebSocket
from app.database import engine, Base
from app import auth, messages
from app.websocket import websocket_endpoint


# Создаем все таблицы в базе данных, если они еще не существуют.
Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI для обработки запросов.
app = FastAPI()

# Подключение маршрутов для REST API.
# auth.router - маршруты для регистрации и авторизации, messages.router - для работы с сообщениями.
app.include_router(auth.router, prefix="/api")
app.include_router(messages.router, prefix="/api")

# WebSocket маршрут для подключения пользователей по их username.
@app.websocket("/api/ws/{username}")
async def websocket_route(websocket: WebSocket, 
                          username: str, 
                          token: str):
    # Вызов функции websocket_endpoint для обработки WebSocket-соединения.
    await websocket_endpoint(websocket, username, token)

# Событие, которое выполняется при старте приложения.
@app.on_event("startup")
async def startup_event():
    print("Starting application...")

