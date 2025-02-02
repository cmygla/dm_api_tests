from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import (
    RestClient,
    RestResponse,
)


class LoginApi(RestClient):

    def post_v1_account_login(
            self, login_credentials: LoginCredentials
    ):
        response = self.post(
            path='/v1/account/login', json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        return RestResponse(response, UserEnvelope)

    def delete_v1_account_login(self):
        response = self.delete(path='/v1/account/login')
        return RestResponse(response)

    def delete_v1_account_login_all(self):
        response = self.delete(path='/v1/account/login/all')
        return RestResponse(response)
