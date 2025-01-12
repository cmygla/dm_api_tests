from json import loads


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()["items"]:
        user_data = loads(item.get('Content').get('Body'))
        user_login = user_data.get("Login")
        if user_login == login:
            token = user_data.get("ConfirmationLinkUrl").split('/')[-1]
    return token
