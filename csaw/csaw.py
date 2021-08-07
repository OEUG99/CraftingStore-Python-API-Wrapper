import requests
from csaw.authtoken import AuthToken
from csaw.giftcard import Giftcard


class CSAW:
    """ CraftingStore.net API wrapper."""

    def __init__(self, token):
        """
        Creates a new instance of the API
        """
        # Checking if token is valid, then assigning it.
        self._auth = self.validate_token(AuthToken(token))

    def validate_token(self, auth):
        """
        Makes a request to check if the token is valid or not.

        :return:
        :raise: ValueError: The authentication token is invalid.
        """
        r = requests.get('https://api.craftingstore.net/v7/information', auth=auth)

        results = r.json()

        if results["success"] is True:
            return auth
        else:
            raise ValueError('CSAW: Invalid authentication token provided.')

    @property
    def get_information(self):
        """
        Returns a dictionary containing general information.
        :return:
        """
        r = requests.get('https://api.craftingstore.net/v7/information', auth=self._auth)
        return r.json()

    @property
    def get_giftcards(self, page=0, json=False):
        """
        Fetches payments by page.
        :param json:
        :param page:
        :rtype: list
        :return: Returns a list of payment dictionaries as a result.
        """
        req = requests.get(f'https://api.craftingstore.net/v7/gift-cards?page={page}', auth=self._auth)
        raw_results = req.json()["data"]

        if json is False:
            results = []
            for giftcardData in raw_results:
                results.append(Giftcard(self._auth, giftcardData))
        else:
            results = raw_results

        return results

    def get_giftcard(self, card_id):
        """
        Returns a :class:`csaw.giftcard.GiftCard` object representing a giftcard, that corresponds to a specific
        giftcard id.

        :param card_id:
        :return: returns a :class:`csaw.giftcard.Giftcard` that represents a
        :rtype: :class:`csaw.giftcard.Giftcard`
        :raise: ValueError: The authentication token is invalid.
        """
        req = requests.get(f'https://api.craftingstore.net/v7/gift-cards/{card_id}', auth=self._auth)
        data = req.json()["data"]
        if data is None:
            raise ValueError('CSAW: Invalid giftcard ID used.')
        else:
            return Giftcard(self._auth, data)

    def create_giftcard(self, amount=15, packages=None, categories=None, applyTo=0):
        """
        Creates a giftcard.

        :param amount:
        :param packages:
        :param categories:
        :param applyTo:
        :return: returns a :class:`csaw.giftcard.Giftcard` object that represents the giftcard.
        :rtype: :class:`csaw.giftcard.Giftcard`
        """

        if type(amount) is not int:
            raise ValueError('CSAW: Type error, CraftingStore only supports integers.')

        if packages is None:
            packages = []
        if categories is None:
            categories = []

        payload = {'amount': amount, 'packages': packages, 'categories': categories, 'applyTo': applyTo}

        req = requests.post('https://api.craftingstore.net/v7/gift-cards', json=payload, auth=self._auth)
        data = req.json()["data"]

        return Giftcard(self._auth, data)

    @property
    def get_payments(self, page=1):
        """
        Fetches payments by page
        :param page:
        :return: returns a list of payment dictionaries as a result.
        :rtype: list
        """
        req = requests.get(f'https://api.craftingstore.net/v7/payments?page={page}', auth=self._auth)
        data = req.json()["data"]

        return data

    @property
    def get_communitygoals(self, page=1):
        """
        Fetches the active community goals. (CraftingStore only supports active community goals.)
        :param page:
        :rtype: list
        :return: Returns a list of community goals.
        """

        req = requests.get(f'https://api.craftingstore.net/v7/communitygoals?page={page}', auth=self._auth)
        data = req.json()["data"]

        return data

