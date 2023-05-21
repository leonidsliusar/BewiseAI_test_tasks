import io
import re
from uuid import UUID

from fastapi import UploadFile, HTTPException
from pydub import AudioSegment
from sqlalchemy import insert, select

from db_config import async_session
from models import User, Record


async def add_user(user_name: str) -> dict[int, str]:
    async with async_session() as session:
        result = await session.execute(insert(User).values(
            name=user_name).returning(
            User.id, User.UUID))
        await session.commit()
        return result.mappings().fetchone()


async def convert_wav_to_mp3(file: UploadFile) -> io.BytesIO:
    content = await file.read()  # read the record
    buffer_wav = io.BytesIO(content)  # save bytes wav record in memory
    buffer_mp3 = io.BytesIO()  # create new buffer for store record in mp3
    audio = AudioSegment.from_wav(buffer_wav)  # convert wav file to convert with pydub
    audio.export(buffer_mp3, format='mp3')  # save mp3 record in buffer
    return buffer_mp3


async def user_validation(user_id: int, token: UUID) -> bool:
    async with async_session() as session:
        exists_query = select(User).where(User.id == user_id, User.UUID == token).exists()
        exists = await session.execute(select(exists_query))
        return exists.scalar()


async def add_item(url: str, user_id: id, token: UUID, file: UploadFile) -> str:
    if not isinstance(token, UUID):  # validation token format
        raise HTTPException(400, detail="Invalid token")
    if file.content_type != 'audio/wav':  # validation file format
        raise HTTPException(400, detail="Invalid document type")
    if await user_validation(user_id, token) is False:  # validates if the user exists
        raise HTTPException(401, detail='User doesn\'t exist')
    record_mp3 = await convert_wav_to_mp3(file)  # send file to converter
    record_name = file.filename.replace('wav', 'mp3')  # save original file name and new data format
    async with async_session() as session:
        record_id = await session.execute(insert(Record).values(
            user_id=user_id,
            content=record_mp3.getvalue(),  # write in db bytes
            record_name=record_name
        ).returning(Record.record_id))
        await session.commit()
    url_root = re.match(r'(.*)\?', url).group(1)  # take root path from request url
    response = f'{url_root}?record_id={record_id.scalar()}&user_id={user_id}'  # generate url for downloading
    return response


async def get_item(record_id: int, user_id: int) -> tuple[io.BytesIO, str]:
    async with async_session() as session:
        content = await session.execute(select(Record.content, Record.record_name).where(
            Record.record_id == record_id, Record.user_id == user_id))
        file = content.fetchone()  # get file name and file content
        if not file:  # if file not found return 404
            raise HTTPException(404, detail='File not found')
        file_content, file_name = file  # unpack tuple
        buffer = io.BytesIO()  # create buffer
        buffer.write(file_content)  # write file content into buffer
        buffer.seek(0)  # set pointer to start
    return buffer, file_name
