from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db

router = APIRouter()

# Эндпоинт для получения списка всех username.
@router.get("/users", response_model=list[str])
def get_usernames(db: Session = Depends(get_db)):
    
    # Получаем всех пользователей и вытаскиваем только поле username.
    usernames = db.query(models.User.username).all()
    
    # Извлекаем только строки из результата, так как .all() возвращает список кортежей.
    return [username[0] for username in usernames]
