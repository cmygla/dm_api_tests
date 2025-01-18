from helpers.mailhog_helper import MailhogHelper
from services.dm_api_account import DmApiAccount


class AccountHelper:
    def __init__(self, dm_api_account_client: DmApiAccount, mailhog_helper: MailhogHelper):
        self.mailhog_helper = mailhog_helper
        self.dm_api_account = dm_api_account_client

    def create_user(self, login: str, password: str, email: str):
        response = self.dm_api_account.account_api.post_v1_account(
            email=email, login=login, password=password
        )
        assert response.status_code == 201, "Пользователь не был создан"

    def activate_user(self, token: str):
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

    def register_new_user(self, login: str, password: str, email: str):
        self.create_user(email=email, login=login, password=password)
        token = self.mailhog_helper.get_activation_token_by_login(login=login)
        self.activate_user(token)

    def login_user(self, login: str, password: str):
        response = self.dm_api_account.login_api.post_v1_account_login(
            login=login, password=password
        )
        assert response.status_code == 200, "Пользователь не смог авторизоваться"

    def update_email(self, login: str, password: str, email: str):
        response = self.dm_api_account.account_api.put_v1_account_email(
            email=f'new_{email}', login=login, password=password
        )
        assert response.status_code == 200, "Email не был изменен"
