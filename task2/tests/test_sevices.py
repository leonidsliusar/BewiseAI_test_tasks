import pytest
from asyncpg.pgproto.pgproto import UUID
from fastapi import UploadFile, HTTPException
from services import add_user, add_item, user_validation, get_item


@pytest.mark.asyncio
async def test_add_user(setup_and_teardown_db, user_name='test'):
    response = await add_user(user_name)
    assert type(response['id']) == int
    assert isinstance(response['UUID'], UUID)
    assert response['UUID'].version == 4


@pytest.mark.asyncio
async def test_user_validation(setup_and_teardown_db):
    response = await add_user('test')
    user_id, token = *(x for x in response.values()),
    result = await user_validation(user_id, token)
    assert result == True


@pytest.mark.asyncio
async def test_add_item_invalid_token(url='localhost:8000/?', user_id=0, token='None', file='tests/sample-3s.wav'):
    try:
        await add_item(url, user_id, token, file)
    except HTTPException as e:
        assert e.detail == 'Invalid token'
        assert e.status_code == 400


@pytest.mark.asyncio
async def test_add_item_invalid_document_type(url='localhost:8000/', user_id=0,
                                              token=UUID('466dab7a-1121-4e73-9c68-44fd122100ff'), file_path='tests/test.txt'):
    with open(file_path, 'rb') as file:
        mock_file = UploadFile(file, filename=file_path.rsplit('/', 0), headers={"content-type": "text/txt"})
    try:
        await add_item(url, user_id, token, mock_file)
    except HTTPException as e:
        assert e.detail == 'Invalid document type'
        assert e.status_code == 400


@pytest.mark.asyncio
async def test_add_item_invalid_user(setup_and_teardown_db, url='localhost:8000/', user_id=0,
                                     token=UUID('466dab7a-1121-4e73-9c68-44fd122100ff'), file_path='tests/sample-3s.wav'):
    with open(file_path, 'rb') as file:
        mock_file = UploadFile(file, filename=file_path.rsplit('/', 0), headers={"content-type": "audio/wav"})
    try:
        await add_item(url, user_id, token, mock_file)
    except HTTPException as e:
        assert e.detail == 'User doesn\'t exist'
        assert e.status_code == 401


@pytest.mark.asyncio
async def test_add_item(setup_and_teardown_db, url='localhost:8000/record?', file_path='tests/sample-3s.wav'):
    user_data = await add_user('test')
    user_id, token = user_data['id'], user_data['UUID']
    with open(file_path, 'rb') as file:
        mock_file = UploadFile(file, filename=file_path.rsplit('/', 0)[0], headers={"content-type": "audio/wav"})
        result = await add_item(url, user_id, token, mock_file)
    assert result == url + 'record_id=1&user_id=1'


@pytest.mark.asyncio
async def test_get_item(setup_and_teardown_db, insert_in_db, file_content=b'test', file_name='test.txt'):
    session = setup_and_teardown_db
    user_id, record_id = await insert_in_db(session, file_content, file_name)
    file, filename = await get_item(record_id, user_id)
    assert file.read() == file_content
    assert filename == filename
