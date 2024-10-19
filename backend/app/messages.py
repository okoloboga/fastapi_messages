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

router = APIRouter()


@router.post("/send-message/")
async def send_message(sender: str, 
                       receiver: str, 
                       message: str, 
                       db: Session = Depends(get_db)):

    new_message = Message(sender=sender, receiver=receiver, message=message, timestamp=datetime.utcnow())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    logger.info(f'new_message: {new_message} from {sender} to {receiver}')

    return new_message


@router.get("/history/{user1}/{user2}")
async def get_history(user1: str, 
                      user2: str, 
                      db: Session = Depends(get_db)):

    logger.info(f'Get message history from {user1} to {user2}')

    history = db.query(Message).filter(
        ((Message.sender == user1) & (Message.receiver == user2)) |
        ((Message.sender == user2) & (Message.receiver == user1))
    ).order_by(Message.timestamp).all()

    logger.info(f'Message history: {history}')

    return history

