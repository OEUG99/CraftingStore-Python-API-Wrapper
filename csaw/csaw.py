import requests
from csaw.authtoken import _AuthToken
from csaw.giftcard import GiftCard


class CSAW:

    def __init__(self):
        self._token = None

    def auth(self, token):
        """
        Used to verify if the authentication token provided is valid.
        :param token:
        :return:
        """

        r = requests.get('https://api.craftingstore.net/v7/information', auth=_AuthToken(token))

        results = r.json()

        if results["success"] is True:
            self._token = token
            return self
        else:
            raise ValueError('CSAW: Invalid auth token provided.')

    def get_information(self):
        """
        Returns a dictionary containing general information.
        :return:
        """
        r = requests.get('https://api.craftingstore.net/v7/information', auth=_AuthToken(self._token))
        return r.json()

    def get_giftcards(self, page=0, json=False):
        """
        Fetches payments by page, returns a list of payment dictionaries as a result.
        :param json:
        :param page:
        :return:
        """
        req = requests.get(f'https://api.craftingstore.net/v7/gift-cards?page={page}', auth=_AuthToken(self._token))
        raw_results = req.json()["data"]

        if json is False:
            results = []
            for giftcardData in raw_results:
                results.append(GiftCard(self._token, giftcardData))
        else:
            results = raw_results

        return results

    def get_giftcard(self, id):
        """

        :param id:
        :return:
        """
        req = requests.get(f'https://api.craftingstore.net/v7/gift-cards/{id}', auth=_AuthToken(self._token))
        data = req.json()["data"]
        if data is None:
            raise ValueError('CSAW: Invalid giftcard ID used.')
        else:
            return GiftCard(self._token, data)

    def create_giftcard(self, amount=15, packages=None, categories=None, applyTo=0):

        if type(amount) is not int:
            raise ValueError('CSAW: Type error, CraftingStore only supports integers.')

        if packages is None:
            packages = []
        if categories is None:
            categories = []

        payload = {'amount': amount, 'packages': packages, 'categories': categories, 'applyTo': applyTo}

        req = requests.post('https://api.craftingstore.net/v7/gift-cards', json=payload, auth=_AuthToken(self._token))
        data = req.json()["data"]

        return GiftCard(self._token, data)

    def get_payments(self, page=1):
        """
        Fetches payments by page, returns a list of payment dictionaries as a result.
        :param page:
        :return:
        """
        req = requests.get(f'https://api.craftingstore.net/v7/payments?page={page}', auth=_AuthToken(self._token))
        data = req.json()["data"]

        return data

    def get_communitygoals(self, page=1):
        """
        Fetches the active community goals. (CraftingStore only supports active community goals.)
        :param page:
        :return:
        """

        req = requests.get(f'https://api.craftingstore.net/v7/communitygoals?page={page}', auth=_AuthToken(self._token))
        data = req.json()["data"]

        return data
