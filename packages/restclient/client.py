import uuid
from json import JSONDecodeError
from typing import (
    Optional,
)

import allure
import curlify
import requests
import structlog
from pydantic import BaseModel
from swagger_coverage_py.request_schema_handler import RequestSchemaHandler
from swagger_coverage_py.uri import URI

from packages.restclient.configuration import Configuration
from packages.restclient.utilities import allure_attach

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)], )


class RestResponse(requests.Response):
    def __init__(self, response: requests.Response, body_type: Optional[type[BaseModel]] = None):
        super().__init__()
        self.__dict__.update(response.__dict__)
        self._body_type = body_type
        self.body_as_object = self._json_as_object(response)

    def _json_as_object(self, resp):
        try:
            if self._body_type:
                return self._body_type(**resp.json())
            else:
                return resp.json()
        except Exception as e:
            return None


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
        with allure.step(f"GET {self.host + path}"):
            return self._send_request(method='GET', path=path, **kwargs)

    def post(
            self, path, **kwargs
    ):
        with allure.step(f"POST {self.host + path}"):
            return self._send_request(method='POST', path=path, **kwargs)

    def put(
            self, path, **kwargs
    ):
        with allure.step(f"PUT {self.host + path}"):
            return self._send_request(method='PUT', path=path, **kwargs)

    def patch(
            self, path, **kwargs
    ):
        with allure.step(f"PATCH {self.host + path}"):
            return self._send_request(method='PATCH', path=path, **kwargs)

    def delete(
            self, path, **kwargs
    ):
        with allure.step(f"DELETE {self.host + path}"):
            return self._send_request(method='DELETE', path=path, **kwargs)

    @allure_attach
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

        uri = URI(host=self.host, base_path="", unformatted_path=path, uri_params=kwargs.get("params"))
        RequestSchemaHandler(
            uri, method.lower(), rest_response, kwargs
        ).write_schema()

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
