from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.base_config import Settings
from src.config.rabbitmq_config import RabbitMQManager
from src.api.v1.auth import router as auth_router
from src.api.v1.user import router as user_router

rabbitmq_manager = RabbitMQManager(Settings().rabbitmq_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_manager.ensure_connection()
    yield
    await rabbitmq_manager.close_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
