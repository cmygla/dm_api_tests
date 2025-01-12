from common.api_client.base_api import BaseApi


class LoginApi(BaseApi):
    def __init__(
            self, host="http://5.63.153.31:5051", headers=None
    ):
        super().__init__()
        self.host = host  #
        self.headers = headers

    def post_v1_account_login(
            self, login, password
    ):
        """
        Authenticate via credentials
        :param login:
        :param password:
        :return:
        """
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.post(url=f'{self.host}/v1/account/login', json=json_data)
        return response
