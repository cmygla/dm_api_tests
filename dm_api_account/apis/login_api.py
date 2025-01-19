from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self, json_data
    ):
        response = self.post(path='/v1/account/login', json=json_data)
        return response
