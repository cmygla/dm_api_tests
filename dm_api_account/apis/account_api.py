import requests


class AccountApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host  #
        self.headers = headers

    def post_v1_account(
            self,
            email,
            login,
            password
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
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate user
        :param token:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/{token}'
        )
        return response
