import pytest
from main import app


def test_info_id_route():
    response = app.test_client().get('/info/1/')

    assert response.status_code == 200
    assert response.text == 'info: 1'
