import asyncio

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import subprocess
from models import Base, QuizQuestion


@pytest.fixture
async def setup_and_teardown_db():
    mock_engine = create_async_engine('postgresql+asyncpg://test:test@localhost5434/test')
    mock_session = async_sessionmaker(mock_engine, expire_on_commit=False)
    start_command = 'docker compose -f test_docker-compose.yml up -d'
    subprocess.run(['bash', '-c', start_command])
    async with mock_engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)
    mock_object_for_insert = []
    obj = QuizQuestion(
        id=1,
        question='test',
        answer='test',
        created_at='2022-01-01T0:00:00'
    )
    mock_object_for_insert.append(obj)
    async with mock_session() as session:
        session.add_all(mock_object_for_insert)
        await session.commit()
    asyncio.sleep(60)
    yield mock_session
    async with mock_engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)
    stop_command = 'docker rm test -f'
    subprocess.run(['bash', '-c', stop_command])
