from abc import ABC, abstractmethod
from game.card import Card


class CardCollection(ABC):
    def __init__(self):
        self.cards = []

    @abstractmethod
    def get_top_card(self):
        pass

    @abstractmethod
    def shuffle(self):
        pass

    def _validate_card(self, card):
        if not isinstance(card, Card):
            raise TypeError('Only card objects can be added to CardCollection')