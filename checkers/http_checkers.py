import json
from contextlib import contextmanager

import requests
from requests import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK, expected_title: str = "", expected_errors: dict = {}
):
    try:
        yield

        if expected_status_code != 200:
            raise AssertionError(f'Ожидаемый статус код должен быть равен {expected_status_code}')

        if expected_title:
            raise AssertionError(f'Должно быть получено сообщение "{expected_title}", но запрос прошел успешно')

        if expected_errors:
            raise AssertionError(f'Должны быть получены ошибки "{expected_errors}", но запрос прошел успешно')
    except HTTPError as e:
        actual_json = json.loads(e.response.text)
        actual_status_code = e.response.status_code
        actual_title = actual_json.get('title', '')
        actual_errors = actual_json.get('errors', {})

        assert actual_status_code == expected_status_code, f'Ожидался статус код {expected_status_code}, а получил {actual_status_code}'
        assert actual_title == expected_title, f'Ожидалось сообщение "{expected_title}", а получил "{actual_title}"'
        assert actual_errors == expected_errors, f'Ожидалась ошибка "{expected_errors}", а получила "{actual_errors}"'
