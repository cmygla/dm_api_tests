from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self, registration: Registration
    ):
        response = self.post(
            path='/v1/account', json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response.body

    def put_v1_account_token(
            self, token, validate_response=True
    ):
        response = self.put(
            path=f'/v1/account/{token}'
        )
        return UserEnvelope(**response.body)

    def put_v1_account_email(self, json_data, validate_response=True):
        response = self.put(
            path='/v1/account/email', json=json_data
        )
        return UserEnvelope(**response.body)

    def get_v1_account(self, validate_response=True):
        response = self.get(path='/v1/account')
        return UserDetailsEnvelope(**response.body)

    def delete_v1_account_login(self):
        response = self.delete(path='/v1/account/login')
        return response.body

    def delete_v1_account_login_all(self):
        response = self.delete(path='/v1/account/login/all')
        return response.body

    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=True):
        response = self.post(
            path='/v1/account/password', json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        return UserEnvelope(**response.body)

    def put_v1_account_password(self, change_password: ChangePassword, validate_response=True):
        response = self.put(
            path='/v1/account/password', json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        UserEnvelope(**response.body)
