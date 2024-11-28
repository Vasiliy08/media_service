from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.application.router import main_router
from src.settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):    
    settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    yield

# TODO: тесты, линтеры, крон задачу (добавить поле в БД когда последний раз скачиваля файл) по нему удалять

def web_app_factory() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/api/docs",
    )
    app.include_router(main_router)
    return app
