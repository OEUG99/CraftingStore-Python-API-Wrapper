import requests

from csaw.authtoken import _AuthToken


class GiftCard:

    def __init__(self, auth, data):
        self._auth = auth

        # Automatically creates attributes based on data.
        for key in data:
            setattr(self, f"_{key}", data[key])

    @property
    def id(self):
        return self._id

    @property
    def amount(self):
        return self._amount

    @property
    def amountRemaining(self):
        return self._amountRemaining

    @property
    def code(self):
        return self._code

    def add_funds(self, increment: int):
        if type(increment) is not int:
            raise ValueError('CSAW: Type error, CraftingStore only supports integers.')

        payload = {'amount': increment}

        res = requests.put(f'https://api.craftingstore.net/v7/gift-cards/{self._id}',
                           json=payload, auth=self._auth)

        data = res.json()["data"]

        self._amount = data["amount"]
        self._amountRemaining = data["amountRemaining"]
        return self

    def remove_funds(self, increment: int):
        self.add_funds(increment)

    def delete(self):
        r = requests.delete(f'https://api.craftingstore.net/v7/gift-cards/{self._id}', auth=self._auth)
        del self
