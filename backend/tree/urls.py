from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.core.middleware import error_handler_middleware

app_tree = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])
