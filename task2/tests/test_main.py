import io

from fastapi import UploadFile

import main2
import services
from tests.conftest import client, stub_get_item, mock_add_user, mock_file, stub_add_item


def test_get_record(monkeypatch, record_id=1, user_id=1):
    monkeypatch.setattr(main2, 'get_item', stub_get_item)
    response = client.get(f'/record/?record_id={record_id}&user_id={user_id}')
    assert response.status_code == 200
    assert response.content == b'test'


def test_create_user(monkeypatch, user_name='test'):
    monkeypatch.setattr(main2, 'add_user', mock_add_user)
    response = client.post(f'/new_user/?user_name={user_name}')
    assert response.json() == {'user_name': user_name}
    assert response.status_code == 200


def test_add_record(monkeypatch, user_id=1, token='1d6bb4e0-3514-4827-9616-c6e153173671', file=mock_file()):
    monkeypatch.setattr(main2, 'add_item', stub_add_item)
    mock_url = f'/record?user_id={user_id}&token={token}'
    response = client.post(mock_url, files={'file': file})
    assert response.status_code == 200
    assert response.text == str(client.base_url) + mock_url
