from restclient.client import (
    RestClient,
    RestResponse,
)


class MailhogApi(RestClient):

    def get_api_v2_messages(
            self, params
    ):
        response = self.get(
            path='/api/v2/messages', params=params, verify=False
        )
        return RestResponse(response)
