from helpers.mailhog_helper import MailhogHelper
from services.dm_api_account import DmApiAccount


class AccountHelper:
    def __init__(self, dm_api_account_client: DmApiAccount, mailhog_helper: MailhogHelper):
        self.mailhog_helper = mailhog_helper
        self.dm_api_account = dm_api_account_client
        self.auth_token = None

    def create_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_api_account.account_api.post_v1_account(json_data)
        assert response.status_code == 201, "Пользователь не был создан"

    def activate_user(self, token: str):
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

    def register_new_user(self, login: str, password: str, email: str):
        self.create_user(email=email, login=login, password=password)
        token = self.mailhog_helper.get_activation_token_by_login(login=login)
        self.activate_user(token)

    def login_user_raw(self, login: str, password: str):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data)
        return response

    def login_user(self, login: str, password: str):
        response = self.login_user_raw(login=login, password=password)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        self.auth_token = response.headers['X-Dm-Auth-Token']

    def authorizated_user(self, login: str, password: str, email: str):
        self.register_new_user(login=login, password=password, email=email)
        self.login_user(login=login, password=password)

    def update_email(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': f'new_{email}',
            'password': password,
        }
        response = self.dm_api_account.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "Email не был изменен"

    def get_user_info(self):
        headers = {
            'X-Dm-Auth-Token': self.auth_token
        }
        response = self.dm_api_account.account_api.get_v1_account(headers=headers)
        assert response.status_code == 200, "Информация о пользователе не получена"

    def delete_account_login(self):
        headers = {
            'X-Dm-Auth-Token': self.auth_token
        }
        response = self.dm_api_account.account_api.delete_v1_account_login(headers=headers)
        assert response.status_code == 204, "Логаут не был выполнен"

    def delete_acсount_login_all(self):
        headers = {
            'X-Dm-Auth-Token': self.auth_token
        }
        response = self.dm_api_account.account_api.delete_v1_account_login_all(headers=headers)
        assert response.status_code == 204, "Логаут на всех устройствах не был выполнен"

    def change_account_password(self, login: str, email: str, old_pass: str, new_pass: str):
        headers = {
            'X-Dm-Auth-Token': self.auth_token
        }
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_api_account.account_api.post_v1_account_password(headers=headers, json_data=json_data)

        assert response.status_code == 200, "Пароль не был сброшен"

        reset_token = self.mailhog_helper.get_activation_token_by_login(login=login, type_="reset")

        json_data = {
            'login': login,
            'token': reset_token,
            'oldPassword': old_pass,
            'newPassword': new_pass,
        }
        response = self.dm_api_account.account_api.put_v1_account_password(headers=headers, json_data=json_data)
        assert response.status_code == 200, "Пароль не был установлен"
