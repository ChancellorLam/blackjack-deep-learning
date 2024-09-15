from abc import ABC
from game.card import Card
import random


class CardCollection(ABC):
    def __init__(self):
        self.cards = []

    def get_top_card(self):
        return self.cards[0]

    def shuffle(self):
        random.shuffle(self.cards)

    def _validate_card(self, card):
        if not isinstance(card, Card):
            raise TypeError('Only card objects can be added to CardCollection')