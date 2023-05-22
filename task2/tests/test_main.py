from starlette.testclient import TestClient
import task2.main as main


client = TestClient(main.app)


async def mock_get_item(record_id, user_id):
    return (b'test', 'test.mp3')


def test_get_record(monkeypatch, record_id=1, user_id=1):
    monkeypatch(main, 'get_item', mock_get_item)
    response = client.get(f'/record/?record_id={record_id}&user_id={user_id}')
    print(response)