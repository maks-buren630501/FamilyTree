from typing import Callable

from pydantic import BaseSettings


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class BaseUrlConfig(BaseSettings):
    tags: list
    name: str
    description: str
    response_model: Callable
    status_code: int

    class Config:
        frozen = True

