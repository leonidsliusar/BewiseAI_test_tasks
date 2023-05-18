import asyncio

import pytest
from services import exist_check, create_question


@pytest.mark.asyncio
@pytest.mark.parametrize('question_collection, expected_result',
                         [
                             pytest.param({1, 2, 3}, {1, 2}, id='param'),
                             pytest.param({50, 10, 21}, {50, 10, 21}, id='param')
                         ]
                         )
async def test_exist_check(setup_and_teardown_db, question_collection, expected_result):
    assert await exist_check(question_collection) == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize('question_collection_1, expected_result_1, question_collection_2, expected_result_2',
                         [
                             pytest.param([1, 2, 3], [], [4, 5, 6], [3], id='param'),
                         ]
                         )
async def test_create_question(setup_and_teardown_db, questions_collection_1, expected_result_1, question_collection_2, expected_result_2):
    assert await create_question(questions_collection_1) == expected_result_1
    assert await create_question(question_collection_2) == expected_result_2
