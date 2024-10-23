import logging

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from app.models import User
from app.config import get_config, Salt, JWT


# Создаем контекст для хеширования паролей с использованием bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получаем конфигурацию для соли и JWT из файла конфигурации.
salt_config = get_config(Salt, 'salt')
jwt_config = get_config(JWT, 'jwt')

# Определяем секретный ключ и алгоритм для подписи JWT.
SECRET_KEY = jwt_config.key
ALGORITHM = "HS256"

# Функция для проверки пароля.
# Сравнивает предоставленный пароль (plain_password) с хешированным паролем (hashed_password).
def verify_password(plain_password, 
                    hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для генерации хэшированного пароля.
# Принимает пароль и возвращает его хеш.
def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для получения пользователя из базы данных по имени пользователя.
def get_user(db: Session, 
             username: str):
    return db.query(User).filter(User.username == username).first()

# Функция для аутентификации пользователя.
# Проверяет наличие пользователя в базе данных и правильность пароля.
def authenticate_user(db: Session, 
                      username: str, 
                      password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Функция для создания токена доступа.
# Принимает словарь данных и, опционально, время истечения токена.
def create_access_token(data: dict, 
                        expires_delta: timedelta | None = None):
    # Создаем копию данных для кодирования.
    to_encode = data.copy()

    # Определяем время истечения токена.
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # Добавляем время истечения в данные для кодирования.
    to_encode.update({"exp": expire})

    # Кодируем данные и создаем JWT токен.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
