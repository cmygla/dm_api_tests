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

    def get_activation_token_by_login(self, login: str, type_: str = "registration"):
        token = self.get_activation_token(login=login, type_=type_)
        return token

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none)
    def get_activation_token(self, login: str, type_: str, limit: str = 20):
        token = None
        params = {
            'limit': limit, }
        response = self.mailhog.mailhog_api.get_api_v2_messages(params)
        token_name = "ConfirmationLinkUrl" if type_.lower() == "registration" else "ConfirmationLinkUri"

        for item in response.body["items"]:
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get("Login")
            if user_login == login:
                confirmation_link = user_data.get(token_name)
                if confirmation_link is not None:
                    token = confirmation_link.split('/')[-1]
                    break
        return token
