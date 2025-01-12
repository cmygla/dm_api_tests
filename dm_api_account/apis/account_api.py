from common.api_client.base_api import BaseApi


class AccountApi(BaseApi):
    def __init__(
            self, host="http://5.63.153.31:5051", headers=None
    ):
        super().__init__()
        self.host = host  #
        self.headers = headers

    def post_v1_account(
            self, email, login, password
    ):
        """
        Register user
        :param email:
        :param login:
        :param password:
        :return:
        """
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.post(
            url=f'{self.host}/v1/account', json=json_data
        )
        return response

    def put_v1_account_token(
            self, token
    ):
        """
        Activate user
        :param token:
        :return:
        """
        response = self.put(
            url=f'{self.host}/v1/account/{token}'
        )
        return response
