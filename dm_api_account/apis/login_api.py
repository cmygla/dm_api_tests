from restclient.client import RestClient


class LoginApi(RestClient):

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
