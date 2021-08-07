import requests


class Giftcard:
    """ Class that represents a giftcard. Allows for easy accessing of a giftcard, and easy updating both locally
    and via the REST api.
    """
    def __init__(self, auth, data):
        self._auth = auth

        # Automatically creates attributes based on data.
        for key in data:
            setattr(self, f"_{key}", data[key])

    @property
    def id(self):
        """ fetches the giftcard's ID

        :rtype: int
        :return: returns an int that corresponds with the giftcard's id.
        """
        return self._id

    @property
    def amount(self):
        """ fetches the giftcard's initial amount of money. (The total that was on the card before any spending occurred.)

        :rtype: int
        :return: returns an int that corresponds with the giftcard's initial amount.
        """
        return self._amount

    @property
    def amountRemaining(self):
        """ fetches the giftcard's remaining amount of money. (The total amount remaining on the card.)

        :rtype: int
        :return: returns an int that corresponds with the giftcards initial amount.
        """
        return self._amountRemaining

    @property
    def code(self):
        """Fetches the giftcard's redemption code.

        :rtype: str
        :return: returns a str that represents the redemption code for the giftcard.
        """
        return self._code

    def add_funds(self, increment: int):
        """Adds more money to the giftcard.

        :param increment: The amount of money to add.
        :rtype: :class:`csaw.giftcard.Giftcard`
        :return: returns the :class:`csaw.giftcard.Giftcard` object that was just updated with new funds.
        """
        if type(increment) is not int:
            raise ValueError('CSAW: Type error, CraftingStore only supports integers.')

        payload = {'amount': increment}

        res = requests.put(f'https://api.craftingstore.net/v7/gift-cards/{self._id}',
                           json=payload, auth=self._auth)

        data = res.json()["data"]

        self._amount = data["amount"]
        self._amountRemaining = data["amountRemaining"]
        return self

    def remove_funds(self, decrement: int):
        """Identical to :meth:`csaw.giftcard.Giftcard.add_funds`, remove an amount of money from a giftcard.

        :param decrement: The amount of money to remove.
        :rtype: :class:`csaw.giftcard.Giftcard`
        :return: returns the :class:`csaw.giftcard.Giftcard` object that was just updated with the new funds.
        """
        self.add_funds(-abs(decrement))

    def delete(self):
        """Deletes the :class:`csaw.giftcard.Giftcard` and sends a delete request to CraftingStore.

        :return:
        """
        requests.delete(f'https://api.craftingstore.net/v7/gift-cards/{self._id}', auth=self._auth)
        del self
