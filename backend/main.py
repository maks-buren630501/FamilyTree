from fastapi import FastAPI

from backend.login.urls import app_login
from backend.tree.urls import app_tree

app = FastAPI()
app.mount('login', app_login)
app.mount('tree', app_tree)
