from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self, json_data
    ):
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

    def put_v1_account_email(self, json_data):
        response = self.put(
            path='/v1/account/email', json=json_data
        )
        return response

    def get_v1_account(self, headers):
        response = self.get(path='/v1/account', headers=headers)
        return response

    def delete_v1_account_login(self, headers):
        response = self.delete(path='/v1/account/login', headers=headers)
        return response

    def delete_v1_account_login_all(self, headers):
        response = self.delete(path='/v1/account/login/all', headers=headers)
        return response

    def post_v1_account_password(self, headers, json_data):
        response = self.post(path='/v1/account/password', headers=headers, json=json_data)
        return response

    def put_v1_account_password(self, headers, json_data):
        response = self.put(path='/v1/account/password', headers=headers, json=json_data)
        return response
