import requests.auth


class AuthToken(requests.auth.AuthBase):
    """
    Class that handles authentications for http request.
    """
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['token'] = self.token
        return r



