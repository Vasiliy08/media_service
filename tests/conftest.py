import punq
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.infrastructure.di import init_container
from src.infrastructure.repositories.db_helper import DatabaseHelper
from src.main import web_app_factory

# TODO: Дописать тесты

@pytest.fixture(scope="function")
def container() -> punq.Container:
    return init_container()

@pytest.fixture(scope='session')
def app() -> FastAPI:
    app = web_app_factory()
    return app

@pytest_asyncio.fixture(scope='session')
def db():
    return DatabaseHelper()

@pytest_asyncio.fixture(scope='session')
async def client(app, db):
    async with AsyncClient(transport=ASGITransport(app=app),  base_url='http://localhost') as client:
        yield client
