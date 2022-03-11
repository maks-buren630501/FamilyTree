from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from backend.login.urls import app_login
from backend.tree.urls import app_tree


app = FastAPI(middleware=[Middleware(CORSMiddleware,  allow_origins=['*'], allow_methods=["*"], allow_headers=["*"])])
app.mount('login', app_login)
app.mount('tree', app_tree)


