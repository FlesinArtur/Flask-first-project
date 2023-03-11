import pytest
from main import app


@pytest.mark.parametrize('test_input, expected', [(1, 'info: 1'), (100, 'info: 100'), (101, 'info: 101'), (994, 'info: 994')])
def test_info_id_route(test_input, expected):
    response = app.test_client().get(f'/info/{test_input}/')

    assert response.status_code == 200
    assert response.text == expected
