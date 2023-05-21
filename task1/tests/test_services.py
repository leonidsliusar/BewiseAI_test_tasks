import pytest
from services import exist_check, create_question


@pytest.mark.asyncio
@pytest.mark.parametrize('question_collection, expected_result',
                         [
                             ([{'id': 1}, {'id': 2}, {'id': 3}], {1, 2}),
                             ([{'id': 50}, {'id': 10}, {'id': 21}], {50, 10, 21})
                         ]
                         )
async def test_exist_check(setup_and_teardown_db, bulk_insert_in_db, question_collection, expected_result):
    mock_async_session = setup_and_teardown_db
    async with mock_async_session() as session:
        await bulk_insert_in_db(session, expected_result)
        assert await exist_check(question_collection, session) == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize('questions_collection_1, expected_result_1, questions_collection_2, expected_result_2',
                         [
                             ([{'id': 1, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'},
                              {'id': 2, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}],
                             [],
                             [{'id': 3, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}],
                             [{'id': 2, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}])
                         ]
                         )
async def test_create_question(setup_and_teardown_db, questions_collection_1, expected_result_1,
                               questions_collection_2, expected_result_2):
    res1 = await create_question(questions_collection_1)
    assert res1 == expected_result_1
    res2 = await create_question(questions_collection_2)
    assert res2 == expected_result_2


@pytest.mark.asyncio
@pytest.mark.parametrize('questions_collection_1, expected_result_1, questions_collection_2, expected_result_2',
                         [
                             ([{'id': 1, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'},
                              {'id': 2, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}],
                             [],
                             [{'id': 1, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'},
                              {'id': 2, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'},
                              {'id': 3, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}],
                             [{'id': 2, 'question': 'test', 'answer': 'test', 'created_at': '2050-01-01T00:00:00.104Z'}])
                         ]
                         )
async def test_create_repeatable_question(setup_and_teardown_db, questions_collection_1, expected_result_1,
                               questions_collection_2, expected_result_2):
    res1 = await create_question(questions_collection_1)
    assert res1 == expected_result_1
    res2 = await create_question(questions_collection_2)
    assert res2 == expected_result_2
