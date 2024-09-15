from abc import ABC
from game.card import Card
import random


class CardCollection(ABC):
    def __init__(self):
        self.cards = []

    def __repr__(self):
        cards = [str(card.get_card()) for card in self.cards]
        formatted_output = "[" + ", ".join(cards) + "]"
        return formatted_output

    def get_top_card(self):
        return self.cards[0]

    def shuffle(self):
        random.shuffle(self.cards)

    def _validate_card(self, card):
        if not isinstance(card, Card):
            raise TypeError('Only card objects can be added to CardCollection')