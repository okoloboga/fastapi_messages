import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.config import get_config, Salt, JWT
from app.utils import authenticate_user, create_access_token


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')
           
# Создаем экземпляр APIRouter для управления маршрутами этого модуля.
router = APIRouter()

# Создаем контекст для хеширования паролей с использованием bcrypt. 'deprecated="auto"' позволяет использовать новые схемы автоматически.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Время жизни токена доступа — 30 минут.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Описание модели данных для регистрации пользователя с полями: имя пользователя, Telegram ID и пароль.
class RegisterRequest(BaseModel):
    username: str
    telegram_id: str
    password: str


# Маршрут для регистрации нового пользователя.
# Получает данные пользователя, хеширует пароль и сохраняет информацию в базе данных.
@router.post("/register")
async def register(request: RegisterRequest, 
                   db: Session = Depends(get_db)):
    # Логируем информацию о попытке регистрации пользователя.
    logger.info(f'User trying to register: {request.username}')

    # Хешируем пароль пользователя перед сохранением в базе данных для обеспечения безопасности.
    hashed_password = pwd_context.hash(request.password)

    # Создаем объект пользователя с захешированным паролем.
    user = User(username=request.username, 
                hashed_password=hashed_password,
                telegram_id=request.telegram_id)

    # Добавляем пользователя в базу данных, сохраняем изменения и обновляем данные.
    db.add(user)
    db.commit()
    db.refresh(user)

    # Возвращаем сообщение о том, что пользователь зарегистрирован.
    return {"message": "User registered"}


# Маршрут для получения токена доступа.
# Принимает данные формы с именем пользователя и паролем и возвращает токен доступа, если аутентификация прошла успешно.
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                 db: Session = Depends(get_db)):
    # Логируем информацию о попытке входа пользователя.
    logger.info(f'User trying to login: {form_data.username}')

    # Аутентифицируем пользователя с использованием предоставленных данных.
    user = authenticate_user(db, form_data.username, form_data.password)

    # Если пользователь не найден или пароль неверен, возвращаем ошибку 401.
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Определяем время жизни токена доступа.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Создаем токен доступа, который содержит имя пользователя в качестве субъекта.
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Логируем успешный вход пользователя.
    logger.info(f'User logged in: {user.username}')

    # Возвращаем токен доступа и тип токена (Bearer).
    return {"access_token": access_token, "token_type": "bearer"}

