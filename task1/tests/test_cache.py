from datetime import datetime

import pytest
from cache import cache
from models import QuizQuestion


@pytest.mark.parametrize('collection', [([{1: 1}, {2: 2}, {3: 3}])])
def test_get_cache(collection):
    cache.set_cache(collection)
    assert cache.get_cache == collection


@pytest.mark.parametrize('collection', [([{1: 1}, {2: 2}, {3: 3}])])
def test_reset_cache(collection):
    cache.set_cache(collection)
    cache.reset_cache
    assert cache.get_cache == []


def test_json_from_cache():
    objects = []
    obj = QuizQuestion(
        id=1,
        question='question',
        answer='answer',
        created_at=datetime.strptime('2022-12-30T21:14:45.587Z', '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    objects.append(obj)
    cache.set_cache(objects[-1].to_json())
    assert cache.get_cache == obj.to_json()
