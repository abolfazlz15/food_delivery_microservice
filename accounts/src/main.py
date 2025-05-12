from fastapi import FastAPI
from src.api.v1.auth import router as auth_router
from src.api.v1.user import router as user_router

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
