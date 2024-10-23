import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Message

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Создаем экземпляр APIRouter для организации маршрутов, связанных с сообщениями.
router = APIRouter()

# Маршрут для получения истории сообщений между двумя пользователями.
@router.get("/history/{user1}/{user2}")
async def get_history(user1: str, 
                      user2: str, 
                      db: Session = Depends(get_db)):
    # Логируем попытку получения истории сообщений между двумя пользователями.
    logger.info(f'Get message history from {user1} to {user2}')

    # Запрашиваем из базы данных все сообщения между user1 и user2.
    history = db.query(Message).filter(
        ((Message.sender == user1) & (Message.receiver == user2)) |
        ((Message.sender == user2) & (Message.receiver == user1))
    ).order_by(Message.timestamp).all()

    # Логируем найденную историю сообщений.
    logger.info(f'Message history: {history}')

    # Возвращаем историю сообщений.
    return history

