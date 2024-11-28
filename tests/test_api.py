import pytest
from faker import Faker
from httpx import AsyncClient, Response
from sqlalchemy import text


@pytest.mark.asyncio
async def test_file_not_found(client: AsyncClient, faker: Faker):
    fake_uuid = faker.uuid4()
    response: Response = await client.get(f"/download/{fake_uuid}/")

    assert response.status_code == 400
    assert response.json() == {
        "detail": {"error": f"Файл c uuid {fake_uuid} не найден"}
    }


@pytest.mark.asyncio
async def test_conn(db):
    # Проверка на соединение с БД
    async with db.session_factory() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
