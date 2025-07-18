from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.exceptions.exception_handler import handle_app_exception
from src.common.exceptions.exceptions import AppBaseException
from src.api.v1.auth import router as auth_router
from src.api.v1.user import router as user_router
from src.config.base_config import settings
from src.config.rabbitmq_config import RabbitMQManager

rabbitmq_manager = RabbitMQManager(settings.rabbitmq_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_manager.ensure_connection()
    yield
    await rabbitmq_manager.close_connection()


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(AppBaseException, handle_app_exception)  # type: ignore


app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
