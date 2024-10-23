from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_config, DbConfig


# Получаем конфигурацию базы данных из файла конфигурации.
db_config = get_config(DbConfig, 'db')

# Преобразуем DSN из объекта конфигурации в строку для использования при подключении к базе данных.
dsn = str(db_config.dsn)

# Создаем движок базы данных с помощью SQLAlchemy с заданным DSN и флагом вывода SQL-запросов.
engine = create_engine(dsn, echo=db_config.is_echo)

# Создаем фабрику сессий для работы с базой данных. Настройки включают:
# autocommit=False - изменения применяются вручную, autoflush=False - отключаем автоматическую запись изменений.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для моделей базы данных с помощью SQLAlchemy.
Base = declarative_base()

# Функция для получения сессии базы данных.
# Используется в качестве зависимости FastAPI для создания и закрытия сессии в каждом запросе.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

