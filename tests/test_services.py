import subprocess

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import db_config
from models import QuizQuestion, Base
from services import exist_check


@pytest.mark.asyncio
@pytest.mark.parametrize('question_collection, questions_collection',
                         [({1, 2, 3}, (2, 'test', 'test', '2022-01-01T0:00:00'))])
async def test_exist_check(monkeypatch, setup_and_teardown_db, question_collection, questions_collection):
    monkeypatch.setattr(db_config, 'async_session', setup_and_teardown_db)
    assert await exist_check(question_collection) == set([1])
