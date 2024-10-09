from blackjack_entities.card import Card
from blackjack_entities.card_collection import CardCollection


class Deck(CardCollection):
    def __init__(self):
        super().__init__()
        self.used_cards = []

    def add_standard_decks(self, num_decks):
        for i in range(0, num_decks):
            for j in range(0, 4):
                for k in range(1, 14):
                    card = Card(k)
                    self.cards.append(card)

    def restore_used_cards(self):
        self.cards.extend(self.used_cards)
        self.used_cards.clear()
