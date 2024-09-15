from blackjack_entities.card import Card
from blackjack_entities.card_collection import CardCollection


class CardShoe(CardCollection):

    def add_standard_decks(self, num_decks):
        for i in range(0, num_decks):
            for j in range(0, 4):
                for k in range(1, 14):
                    card = Card(k)
                    self.cards.append(card)
