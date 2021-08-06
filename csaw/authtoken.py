import requests.auth


class _AuthToken(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['token'] = self.token
        return r



