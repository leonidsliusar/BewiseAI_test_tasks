import re
from datetime import datetime
from typing import Optional

import aiohttp
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from db_config import async_session
from models import QuizQuestion
from cache import cache


async def get_answer(questions_num: int) -> list[dict]:  # make request to third party API
    url = f'https://jservice.io/api/random?count={questions_num}'
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            return await response.json()


async def exist_check(question_collection: list[dict], unique_question: Optional[list[dict] | None] = None) -> set[int]:
    collections_for_check_unique = {question['id'] for question in question_collection}  # set id's collection for check unique constraint
    repeatable_prev_response = None
    if unique_question:
        unique_collection = {question['id'] for question in unique_question}  # set id's collection for unique from prev response
        repeatable_prev_response = unique_collection.intersection(collections_for_check_unique)  # check current response for unique relatively prev response
        collections_for_check_unique = collections_for_check_unique.difference(repeatable_prev_response)  # get unique id's set compair with prev response
    async with async_session() as session:
        query = select(QuizQuestion.id).where(QuizQuestion.id.in_(collections_for_check_unique))  # check for unique questions compair db
        repeatable_question = await session.scalars(query)  # get iterator of not unique questions
    repeatable_set = {id for id in repeatable_question}  # get not unique id's set
    if repeatable_prev_response:  # if is repeats compared prev response
        repeatable_set = repeatable_set.union(repeatable_prev_response)  # get union of repeats in db and repeats in prev response
    return repeatable_set  # return set of repeats


async def create_question(questions_collection: list[dict]) -> list[dict]:  # make DB insertion and return previous saved entries
    previous_question = cache.get_cache  # get last added entries
    repeatable_set = await exist_check(questions_collection)  # find repeat questions in db
    unique_question = [question for question in questions_collection if question['id'] not in repeatable_set]  # set the DB's unique questions
    repeatable_response = None
    while repeatable_set:  # while id's not unique in db or not unique db and responses
        repeatable_response = await get_answer(len(repeatable_set))  # keep send request to 3rd party API in size of repeatable set
        repeatable_set = await exist_check(repeatable_response, unique_question)  # keep check response for unique constraint in db in repeat requests
    if repeatable_response:
        unique_question.extend(repeatable_response)  # extend unique questions list with unique questions from repeatable request
    objects_for_insert = []  # prepare iterable for bulk insertion
    for question in unique_question:
        obj = QuizQuestion(
            id=question['id'],
            question=question['question'],
            answer=question['answer'],
            created_at=datetime.strptime((question['created_at']), "%Y-%m-%dT%H:%M:%S.%f%z")
        )
        objects_for_insert.append(obj)
    async with async_session() as session:
        async with session.begin():  # run transaction
            await session.execute(text("LOCK TABLE quiz_question IN ROW EXCLUSIVE MODE;"))  # set lock on table including insertion
            try:
                session.add_all(objects_for_insert)
                await session.commit()
            except IntegrityError:  # if another transaction already insert same data
                await session.rollback()
                await create_question(unique_question)
    cache.set_cache((objects_for_insert[-1]).to_json())
    return previous_question
