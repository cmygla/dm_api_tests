from json import loads

from services.api_mailhog import Mailhog


class MailhogHelper:
    def __init__(self, mailhog: Mailhog):
        self.mailhog = mailhog

    def get_activation_token_by_login(self, login: str):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        token = self.get_activation_token(login, response)
        assert token is not None, "Токен не был получен"
        return token

    @staticmethod
    def get_activation_token(login, response):
        token = None
        for item in response.json()["items"]:
            user_data = loads(item.get('Content').get('Body'))
            user_login = user_data.get("Login")
            if user_login == login:
                token = user_data.get("ConfirmationLinkUrl").split('/')[-1]
                break
        return token
