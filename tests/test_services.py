import pytest
from services import exist_check, create_question, get_answer


@pytest.mark.asyncio
@pytest.mark.parametrize('question_collection, expected_result',
                         [
                             ({1, 2, 3}, {1, 2}),
                             ({50, 10, 21}, {50, 10, 21})
                         ]
                         )
async def test_exist_check(setup_and_teardown_db, bulk_insert_in_db, question_collection, expected_result):
    async_session = setup_and_teardown_db
    await bulk_insert_in_db(async_session, expected_result)
    assert await exist_check(question_collection) == expected_result


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


# @pytest.mark.asyncio
# @pytest.mark.parametrize('questions_num'[(100)])
# async def test_get_answer(questions_num):
#     expected_result = [{x: 'test'} for x in range(questions_num)]
#     assert get_answer(questions_num) == expected_result