from common.api_client.base_api import BaseApi


class MailhogApi(BaseApi):
    def __init__(
            self, host="http://5.63.153.31:5025", headers=None
    ):
        super().__init__()
        self.host = host  #
        self.headers = headers

    def get_api_v2_messages(
            self, limit=50
    ):
        """
        Get user's emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = self.get(
            url=f'{self.host}/api/v2/messages', params=params, verify=False
        )
        return response
