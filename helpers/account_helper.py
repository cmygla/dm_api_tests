import time
from collections import namedtuple

import allure

from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from helpers.mailhog_helper import MailhogHelper
from services.dm_api_account import DmApiAccount

Credentials = namedtuple('Credentials', ['login', 'password', 'email'])


class AccountHelper:
    def __init__(self, dm_api_account_client: DmApiAccount, mailhog_helper: MailhogHelper):
        self._email = None
        self._login = None
        self._password = None
        self.mailhog_helper = mailhog_helper
        self.dm_api_account = dm_api_account_client

    @allure.step("Получение креденшелов пользователя")
    def get_credentials(self):
        return Credentials(self._login, self._password, self._email)

    @allure.step("Создание пользователя")
    def create_user(self, login: str, password: str, email: str):
        reigistaration = Registration(login=login, password=password, email=email)
        response = self.dm_api_account.account_api.post_v1_account(reigistaration)

    @allure.step("Активация пользователя")
    def activate_user(self, token: str):
        response = self.dm_api_account.account_api.put_v1_account_token(
            token=token
        )

    @allure.step("Регистрация пользователя")
    def register_new_user(self, login: str, password: str, email: str):
        self.create_user(email=email, login=login, password=password)
        start_time = time.time()
        token = self.mailhog_helper.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        self.activate_user(token)

    @allure.step("Аутентификация пользователя")
    def login_user_raw(self, login: str, password: str):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=True)
        response = self.dm_api_account.login_api.post_v1_account_login(login_credentials)
        return response

    def login_user(self, login: str, password: str):
        response = self.login_user_raw(login=login, password=password)
        assert response.headers['X-Dm-Auth-Token'], "Токен для пользователя не получен"
        return response

    @allure.step("Генерация авторизованного пользователя")
    def auth_client(self, login: str, password: str, email: str):
        self.register_new_user(login=login, password=password, email=email)
        response = self.login_user_raw(login=login, password=password)
        headers = {
            'X-Dm-Auth-Token': response.headers['X-Dm-Auth-Token']}
        self.dm_api_account.account_api.set_headers(headers=headers)
        self.dm_api_account.login_api.set_headers(headers=headers)
        self._login = login
        self._password = password
        self._email = email

    def update_email(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': f'new_{email}',
            'password': password, }
        response = self.dm_api_account.account_api.put_v1_account_email(json_data)

    def get_user_info(self):
        response = self.dm_api_account.account_api.get_v1_account()
        return response

    def delete_account_login(self):
        response = self.dm_api_account.login_api.delete_v1_account_login()

    def delete_acсount_login_all(self):
        response = self.dm_api_account.login_api.delete_v1_account_login_all()

    def change_account_password(self, login: str, email: str, old_pass: str, new_pass: str):
        reset_password = ResetPassword(login=login, email=email)
        response = self.dm_api_account.account_api.post_v1_account_password(
            reset_password=reset_password
        )

        reset_token = self.mailhog_helper.get_activation_token_by_login(login=login, type_="reset")

        change_password = ChangePassword(login=login, token=reset_token, old_password=old_pass, new_password=new_pass)
        response = self.dm_api_account.account_api.put_v1_account_password(change_password=change_password)
