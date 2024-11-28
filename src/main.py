import punq
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.application.router import main_router
from src.infrastructure.di import init_container
from src.infrastructure.repositories.media import MediaRepository
from src.settings.config import settings
from src.cron import sheduler, trigger


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: punq.Container = init_container()
    container: MediaRepository = container.resolve(MediaRepository)
    settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    sheduler.add_job(container.delete_unused_files, trigger=trigger)
    sheduler.start()

    yield

    sheduler.shutdown()


def web_app_factory() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/api/docs",
    )
    app.include_router(main_router)
    return app
