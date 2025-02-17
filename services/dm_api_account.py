from clients.http.dm_api_account.apis.account_api import AccountApi
from clients.http.dm_api_account.apis.login_api import LoginApi
from packages.restclient.configuration import Configuration


class DmApiAccount:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.login_api = LoginApi(self.configuration)
        self.account_api = AccountApi(self.configuration)
