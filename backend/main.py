from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from backend.authentication.urls import app_authentication
from backend.tree.urls import app_tree

app = FastAPI(middleware=[Middleware(CORSMiddleware,  allow_origins=['*'], allow_methods=["*"], allow_headers=["*"])])
app.mount('/authentication', app_authentication)
app.mount('/tree', app_tree)



