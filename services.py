from datetime import datetime
import aiohttp
from sqlalchemy import select

from db_config import async_session
from models import QuizQuestion
from cache import cache


async def get_answer(questions_num: int) -> list[dict]:  # make request to third party API
    url = f'https://jservice.io/api/random?count={questions_num}'
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            response = await response.json()
    questions_collection = {question['id'] for question in response}
    repeatable_questions = await exist_check(questions_collection)
    unique_question = [question for question in response if question['id'] not in repeatable_questions]
    if repeatable_questions:
        repeatable_response = await get_answer(len(repeatable_questions))
        unique_question.extend(repeatable_response)
    return unique_question


async def exist_check(question_collection: set[int]) -> set[int]:
    async with async_session() as session:
        query = select(QuizQuestion.id).where(QuizQuestion.id.in_(question_collection))
        repeatable_question = await session.execute(query)
        repeats = question_collection.intersection(repeatable_question)
    return repeats


async def create_question(questions_collection: list[dict]):  # make DB insertion and return previous saved entries
    previous_question = cache.get_cache
    objects_for_insert = []
    for question in questions_collection:
        obj = QuizQuestion(
            id=question['id'],
            question=question['question'],
            answer=question['answer'],
            created_at=datetime.strptime((question['created_at']), "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        objects_for_insert.append(obj)
    async with async_session() as session:
        session.add_all(objects_for_insert)
        await session.commit()
    cache.set_cache([objects_for_insert[-1]])
    return previous_question
