import time
from json import loads

from retrying import retry

from services.api_mailhog import Mailhog


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(func):
    def wraps(*args, **kwargs):
        resp = None
        count = 1
        while resp is None:
            print(f'Retry:{count}')
            resp = func(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено время ожидания ответа")
            if resp:
                return resp
            time.sleep(1)

    return wraps


class MailhogHelper:
    def __init__(self, mailhog_client: Mailhog):
        self.mailhog = mailhog_client

    def get_activation_token_by_login(self, login: str):
        token = self.get_activation_token(login)
        return token

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none)
    def get_activation_token(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        for item in response.json()["items"]:
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get("Login")
            if user_login == login:
                token = user_data.get("ConfirmationLinkUrl").split('/')[-1]
                break
        return token
