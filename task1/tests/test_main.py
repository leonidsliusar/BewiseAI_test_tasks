import pytest
import main
from tests.conftest import mock_get_answer, mock_create_question, client


@pytest.mark.parametrize('quantity_question', [(1), ])
def test_add_question(monkeypatch, quantity_question):
    monkeypatch.setattr(main, 'get_answer', mock_get_answer)
    monkeypatch.setattr(main, 'create_question', mock_create_question)
    response = client.post(f'/?quantity_question={quantity_question}')
    assert response.json() == [{'quantity_question': quantity_question}]
