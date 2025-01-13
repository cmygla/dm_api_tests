import json
from pprint import pprint

import requests


class BaseApi:
    def __init__(
            self
    ):
        self.session = requests.Session()

    @staticmethod
    def log_response(
            func
    ):
        def wrapper(
                *args, **kwargs
        ):
            # Логируем параметры запроса
            # Формируем команду curl
            method = func.__name__.upper()
            url = kwargs.get('url')
            params = kwargs.get('params')
            param_string = ''
            if params:
                param_string = '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            command_parts = [f"curl -X {method} '{url}'{param_string}"]

            headers = kwargs.get('headers') or {}
            for key, value in headers.items():
                command_parts.append(f"-H '{key}: {value}'")

            data = kwargs.get('data')
            if data:
                command_parts.append(f"--data '{data}'")

            json_data = kwargs.get('json')
            if json_data:
                command_parts.append("--header 'Content-Type: application/json'")
                command_parts.append(f"--data-raw '{json.dumps(json_data)}'")

            # Логируем команду curl
            print(f"\nREQUEST: {' '.join(command_parts)}")

            # Выполняем запрос
            response = func(*args, **kwargs)
            try:
                # Логируем ответ
                print('RESPONSE:')
                if 'json' in response.headers.get('Content-Type', ''):
                    pprint(response.json())
                else:
                    print(response.text)
            except Exception as e:
                print(f"Произошла ошибка при обработке ответа: {e}")
            finally:
                return response

        return wrapper

    @log_response
    def get(
            self, url, params=None, **kwargs
    ):
        return self.session.get(url, params=params, **kwargs)

    @log_response
    def post(
            self, url, data=None, json=None, **kwargs
    ):
        return self.session.post(url, data=data, json=json, **kwargs)

    @log_response
    def put(
            self, url, data=None, **kwargs
    ):
        return self.session.put(url, data=data, **kwargs)

    @log_response
    def patch(
            self, url, data=None, **kwargs
    ):
        return self.session.patch(url, data=data, **kwargs)

    @log_response
    def delete(
            self, url, **kwargs
    ):
        return self.session.delete(url, **kwargs)
