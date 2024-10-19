from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_config, DbConfig


db_config = get_config(DbConfig, 'db')
dsn = str(db_config.dsn)

engine = create_engine(dsn, echo=db_config.is_echo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

