import io

import main2
from tests.conftest import client, stub_get_item, mock_add_user


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


def test_add_record(monkeypatch, request, user_id, token, file):
    pass

