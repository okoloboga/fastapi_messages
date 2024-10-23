import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base


# Модель пользователя для базы данных.
# Хранит информацию о пользователях, включая имя пользователя, хешированный пароль и Telegram ID.
class User(Base):
    __tablename__ = "users"

    # Уникальный идентификатор пользователя.
    id = Column(Integer, primary_key=True, index=True)

    # Имя пользователя, должно быть уникальным.
    username = Column(String, unique=True, index=True)

    # Хешированный пароль пользователя.
    hashed_password = Column(String)

    # Telegram ID пользователя, обязательное поле.
    telegram_id = Column(String, nullable=False)

# Модель сообщения для базы данных.
# Хранит информацию о сообщениях, включая отправителя, получателя, текст сообщения и время отправки.
class Message(Base):
    __tablename__ = "messages"

    # Уникальный идентификатор сообщения.
    id = Column(Integer, primary_key=True, index=True)

    # Имя отправителя сообщения.
    sender = Column(String)

    # Имя получателя сообщения.
    receiver = Column(String)

    # Текст сообщения.
    message = Column(String)

    # Время отправки сообщения, по умолчанию текущее время.
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

