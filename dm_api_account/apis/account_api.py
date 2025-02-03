from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import (
    RestClient,
    RestResponse,
)


class AccountApi(RestClient):

    def post_v1_account(
            self, registration: Registration
    ):
        response = self.post(
            path='/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return RestResponse(response)

    def put_v1_account_token(
            self, token
    ):
        response = self.put(
            path=f'/v1/account/{token}'
        )
        return RestResponse(response, UserEnvelope)

    def put_v1_account_email(self, json_data):
        response = self.put(
            path='/v1/account/email', json=json_data
        )
        return RestResponse(response, UserEnvelope)

    def get_v1_account(self):
        response = self.get(path='/v1/account')
        return RestResponse(response, UserDetailsEnvelope)

    def post_v1_account_password(self, reset_password: ResetPassword):
        response = self.post(
            path='/v1/account/password', json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        return RestResponse(response, UserEnvelope)

    def put_v1_account_password(self, change_password: ChangePassword):
        response = self.put(
            path='/v1/account/password', json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        return RestResponse(response, UserEnvelope)
