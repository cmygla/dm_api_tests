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
            self, email: str, login: str, password: str
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

    def get_v1_account(
            self, auth_token: str
    ):
        """
        Get user info
        :param auth_token:
        :return:
        """

        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        response = self.get(path='/v1/account', headers=headers)
        return response

    def delete_v1_account_login(
            self, auth_token: str
    ):
        """
        Logout current user
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        response = self.delete(path='/v1/account/login', headers=headers)
        return response

    def delete_v1_account_login_all(
            self, auth_token: str
    ):
        """
        Logout current user from every devices
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        response = self.delete(path='/v1/account/login/all', headers=headers)
        return response

    def post_v1_account_password(
            self, email: str, login: str, auth_token: str
    ):
        """
        Reset pass
        :param email:
        :param login:
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        json_data = {
            'login': login,
            'email': email
        }
        response = self.post(path='/v1/account/password', headers=headers, json=json_data)
        return response

    def put_v1_account_password(
            self, login: str, reset_token: str, old_pass: str, new_pass: str, auth_token: str
    ):
        """
        Change pass value
        :param login:
        :param reset_token:
        :param old_pass:
        :param new_pass:
        :param auth_token:
        :return:
        """
        headers = {
            'X-Dm-Auth-Token': auth_token
        }
        json_data = {
            'login': login,
            'token': reset_token,
            'oldPassword': old_pass,
            'newPassword': new_pass,
        }
        response = self.put(path='/v1/account/password', headers=headers, json=json_data)
        return response
