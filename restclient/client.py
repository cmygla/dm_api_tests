import uuid
from json import JSONDecodeError
from typing import (
    TypeVar,
    Generic,
    Optional,
)

import curlify
import requests
import structlog

from restclient.configuration import Configuration

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)], )

T = TypeVar('T')


class RestResponse(Generic[T], requests.Response):
    def __init__(self, response: requests.Response, body_type: Optional[type[T]] = None):
        super().__init__()
        self.__dict__.update(response.__dict__)
        self.body = self._get_json()
        if not body_type:
            self.body_as_object = None
        else:
            try:
                self.body_as_object = body_type(**response.json())
            except Exception as e:
                print(f'Ошибка преобразования тела ответа: {e}')
                self.body_as_object = None

    def _get_json(self):
        try:
            return self.json()
        except JSONDecodeError:
            return self.text


class RestClient:
    def __init__(
            self, configuration: Configuration
    ):
        self.host = configuration.host  #
        self.set_headers(configuration.headers)
        self.disable_logs = configuration.disable_logs
        self.session = requests.Session()
        self.log = structlog.getLogger(__name__).bind(service='api')

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def get(
            self, path, **kwargs
    ):
        return self._send_request(method='GET', path=path, **kwargs)

    def post(
            self, path, **kwargs
    ):
        return self._send_request(method='POST', path=path, **kwargs)

    def put(
            self, path, **kwargs
    ):
        return self._send_request(method='PUT', path=path, **kwargs)

    def patch(
            self, path, **kwargs
    ):
        return self._send_request(method='PATCH', path=path, **kwargs)

    def delete(
            self, path, **kwargs
    ):
        return self._send_request(method='DELETE', path=path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path
        if self.disable_logs:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event="Request",
            method=method,
            full_url=full_url,
            params=kwargs.get("params"),
            headers=kwargs.get("headers"),
            json=kwargs.get("json"),
            data=kwargs.get("data"), )

        rest_response = self.session.request(method=method, url=full_url, **kwargs)

        curl = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event="Response",
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response)
        )
        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
