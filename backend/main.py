from fastapi import FastAPI

from backend.authentication.urls import app_authentication
from backend.tree.urls import app_tree

app = FastAPI()
app.mount('/authentication', app_authentication)
app.mount('/tree', app_tree)
