from restclient.client import RestClient


class MailhogApi(RestClient):
    def __init__(
            self
    ):
        super().__init__(host="http://5.63.153.31:5025")

    def get_api_v2_messages(
            self, limit=20
    ):
        """
        Get user's emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = self.get(
            path='/api/v2/messages', params=params, verify=False
        )
        return response
