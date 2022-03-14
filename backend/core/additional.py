from typing import Callable

from pydantic import BaseSettings


class BaseUrlConfig(BaseSettings):
    tags: list
    name: str
    description: str
    response_model: Callable
    status_code: int

    class Config:
        frozen = True

