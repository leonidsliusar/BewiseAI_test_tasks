import asyncio
from datetime import datetime
from task1.main import app
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import subprocess
from fastapi.testclient import TestClient
from task1 import cache, services
from task1.models import Base, QuizQuestion


@pytest_asyncio.fixture
async def setup_and_teardown_db(monkeypatch):
    start_command = 'docker compose -f tests/test_docker-compose.yml up -d'  # start container
    subprocess.run(['bash', '-c', start_command])  # start container
    await asyncio.sleep(1)  # set time sleep for deploy container
    mock_engine = create_async_engine('postgresql+asyncpg://test:test@localhost:5434/test', echo=True)
    mock_session = async_sessionmaker(mock_engine, expire_on_commit=False)
    async with mock_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    monkeypatch.setattr(services, 'async_session', mock_session)  # mock session in module which define test subject
    yield mock_session
    stop_command = 'docker rm test -f'  # force remove docker container
    subprocess.run(['bash', '-c', stop_command])
    cache.cache.reset_cache


@pytest.fixture
def bulk_insert_in_db():
    async def wrapper(session, expected_result):
        mock_obj = []
        for id in expected_result:
            mock_obj.append(
                QuizQuestion(id=id,
                             question='test',
                             answer='test',
                             created_at=datetime.strptime(('2050-01-01T0:00:00.104'), "%Y-%m-%dT%H:%M:%S.%f")))
        async with session() as conn:
            conn.add_all(mock_obj)
            await conn.commit()

    return wrapper


async def mock_get_answer(quantity_question):
    return [{'quantity_question': quantity_question}]


async def mock_create_question(response_third_api):
    return response_third_api


client = TestClient(app)
