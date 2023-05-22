import uuid
from fastapi import FastAPI, Request, File, UploadFile
from starlette.responses import Response, StreamingResponse
from services import add_user, add_item, get_item

app = FastAPI()


@app.get('/record')
async def get_record(record_id: int, user_id: int) -> StreamingResponse:
    file_content, file_name = await get_item(record_id, user_id)
    headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
    return StreamingResponse(file_content, media_type='audio/mp3', headers=headers)


@app.post('/new_user')
async def create_user(user_name: str) -> dict:
    response = await add_user(user_name)
    return response


@app.post('/record')
async def add_record(request: Request, user_id: int, token: str, file: UploadFile = File(...)) -> Response:
    response = await add_item(str(request.url), user_id, uuid.UUID(token), file)
    return Response(response, media_type='text/html')
