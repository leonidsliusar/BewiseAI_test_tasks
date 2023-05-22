import asyncio
import io
import subprocess

import pytest
import pytest_asyncio
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette.testclient import TestClient

import services
from models import Base, User, Record
from main2 import app

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
    stop_command = 'docker rm test -f -v'  # force remove docker container
    subprocess.run(['bash', '-c', stop_command])


@pytest_asyncio.fixture
def insert_in_db():
    async def wrapper(async_session, file_content, file_name):
        async with async_session() as session:
            async with session.begin():
                user_data_raw = await session.execute(insert(User).values(name='Test').returning(User.id, User.UUID))
                user_data = user_data_raw.mappings().fetchone()
                user_id, token = user_data['id'], user_data['UUID']
                record_id_raw = await session.execute(insert(Record).values(
                    user_id=user_id,
                    content=file_content,
                    record_name=file_name
                ).returning(Record.record_id))
                record_id = record_id_raw.scalar()
                await session.commit()
        return user_id, record_id
    return wrapper


client = TestClient(app)


async def stub_get_item(record_id, user_id):
    mock_buffer = io.BytesIO()
    mock_buffer.write(b'test')
    mock_buffer.seek(0)
    return mock_buffer, 'test.mp3'


async def mock_add_user(user_name):
    return {'user_name': user_name}


async def stub_add_item(url, user_id, token, file):
    mock_response = url
    return mock_response


def mock_file():
    mock_buffer = io.BytesIO()
    mock_buffer.write(b'test')
    mock_buffer.seek(0)
    return mock_buffer.getvalue()
