from abc import ABC
import random


class CardCollection(ABC):
    def __init__(self):
        self.cards = []

    def __repr__(self):
        cards = [str(card.get_card()) for card in self.cards]
        formatted_output = "[" + ", ".join(cards) + "]"
        return formatted_output

    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def pop_left_card(self):
        return self.cards.pop(0)

    def get_top_card(self):
        return self.cards[0].get_card()

    def shuffle(self):
        random.shuffle(self.cards)

    def transfer_all_cards_to(self, destination):
        destination.extend(self.cards)
        self.cards.clear()
