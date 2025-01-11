import requests


class LoginApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host  #
        self.headers = headers

    def post_v1_account_login(
            self,
            login,
            password
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
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response
