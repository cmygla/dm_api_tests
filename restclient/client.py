import uuid
from json import JSONDecodeError

import curlify
import requests
import structlog

from restclient.configuration import Configuration

structlog.configure(
    processors=[structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)], )


class RestClient:
    def __init__(
            self, configuration: Configuration
    ):
        self.host = configuration.host  #
        self.headers = configuration.headers
        self.disable_logs = configuration.disable_logs
        self.session = requests.Session()
        self.log = structlog.getLogger(__name__).bind(service='api')

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
            return rest_response

        log.msg(
            event="Request", method=method, full_url=full_url, params=kwargs.get("params"),
            headers=kwargs.get("headers"), json=kwargs.get("json"), data=kwargs.get("data"), )

        rest_response = self.session.request(method=method, url=full_url, **kwargs)

        curl = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event="Response", status_code=rest_response.status_code, headers=rest_response.headers,
            json=self._get_json(rest_response)
        )
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
