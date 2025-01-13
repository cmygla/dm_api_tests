from restclient.client import RestClient


class AccountApi(RestClient):

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
            path='/v1/account', json=json_data
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
            path=f'/v1/account/{token}'
        )
        return response

    def put_v1_account_email(
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
        response = self.put(
            path='/v1/account/email', json=json_data
        )
        return response
