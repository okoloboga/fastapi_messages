from functools import lru_cache
from typing import TypeVar, Type

from pydantic import BaseModel, PostgresDsn
from yaml import load

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


# Объявляем тип переменной ConfigType, который должен быть подклассом BaseModel из Pydantic.
ConfigType = TypeVar("ConfigType", bound=BaseModel)

# Класс для конфигурации базы данных.
# Содержит строку подключения к базе данных (dsn) и флаг для вывода SQL-запросов (is_echo).
class DbConfig(BaseModel):
    dsn: PostgresDsn
    is_echo: bool

# Класс для хранения соли для хеширования паролей.
class Salt(BaseModel):
    key: str

# Класс для конфигурации JWT.
# Содержит секретный ключ для подписи JWT.
class JWT(BaseModel):
    key: str

# Класс для конфигурации Telegram-бота.
# Содержит токен для доступа к Telegram API.
class Bot(BaseModel):
    token: str

# Функция для парсинга файла конфигурации с использованием lru_cache для кэширования результата.
# Возвращает словарь с данными из YAML-файла.
@lru_cache(maxsize=1)
def parse_config_file() -> dict:
    with open("app/config.yaml", "rb") as file:
        config_data = load(file, Loader=SafeLoader)
    return config_data

# Функция для получения конфигурации из YAML-файла и приведения её к указанной модели.
# Использует кэширование результата с помощью lru_cache.
@lru_cache
def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = parse_config_file()

    # Проверяем, что корневой ключ присутствует в словаре конфигурации.
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)

    # Возвращаем конфигурацию, преобразованную в указанную модель.
    return model.model_validate(config_dict[root_key])
