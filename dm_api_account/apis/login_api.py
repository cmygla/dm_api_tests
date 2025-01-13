from restclient.client import RestClient


class LoginApi(RestClient):
    def __init__(
            self
    ):
        super().__init__(host="http://5.63.153.31:5051")

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
        response = self.post(path='/v1/account/login', json=json_data)
        return response
