from fastapi import FastAPI
from services import get_answer, create_question

app = FastAPI()


@app.post('/')
async def add_question(questions_num: int) -> list[dict]:
    response_third_api = await get_answer(questions_num)  # async request to 3rd party API, await list of questions
    response = await create_question(response_third_api)  # async insert to DB, await last saved entries
    return response
