from clients.http.api_mailhog.apis.mailhog_api import MailhogApi
from packages.restclient.configuration import Configuration


class Mailhog:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(self.configuration)
