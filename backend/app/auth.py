import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User
from app.config import get_config, Salt, JWT


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

router = APIRouter()

salt_config = get_config(Salt, 'salt')
jwt_config = get_config(JWT, 'jwt')

SECRET_KEY = jwt_config.key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(username: str, 
                   password: str, 
                   telegram_id: str,
                   db: Session = Depends(get_db)):

    hashed_password = pwd_context.hash(password)
    user = User(username=username, 
                hashed_password=hashed_password,
                telegram_id=telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f'New user: {username}, telegram_id: {telegram_id}')

    return {"message": "User registered"}


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token_data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    logger.info('Auth token taken')

    return {"access_token": token, "token_type": "bearer"}
