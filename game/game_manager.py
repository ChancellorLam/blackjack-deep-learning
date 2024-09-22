from blackjack_entities.deck import Deck


class GameManager:
    def __init__(self):
        self.player_money = 500
        self.current_bet = 15
        self.game_deck = Deck()

    def load_game_deck_with_standard_decks(self, num_decks):
        self.game_deck.add_standard_decks(num_decks)

    def deal_cards(self, current_game):
        current_game.dealer_hand.add_card(self.game_deck.pop_left_card())
        for hand in current_game.player_hands.values():
            hand.add_card(self.game_deck.pop_left_card())
