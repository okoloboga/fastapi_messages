from functools import lru_cache
from typing import TypeVar, Type

from pydantic import BaseModel, PostgresDsn
from yaml import load

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


ConfigType = TypeVar("ConfigType", bound=BaseModel)


class DbConfig(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


class Salt(BaseModel):
    key: str


class JWT(BaseModel):
    key: str


class Bot(BaseModel):
    token: str


@lru_cache(maxsize=1)
def parse_config_file() -> dict:

    with open ("app/config.yaml", "rb") as file:
        config_data = load(file, Loader=SafeLoader)
    return config_data


@lru_cache
def get_config(model: Type[ConfigType],
               root_key: str) -> ConfigType:

    config_dict = parse_config_file()
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)
    return model.model_validate(config_dict[root_key])