from blackjack_entities.deck import Deck
from game.blackjack_game import BlackjackGame

class GameManager:
    def __init__(self):
        self.player_money = 500
        self.current_bet = 15
        self.game_deck = Deck()

    def load_game_deck_with_standard_decks(self, num_decks):
        self.game_deck.add_standard_decks(num_decks)

    def deal_starting_cards(self, current_game):
        for i in range(0, 2):
            current_game.player_hands[0].add_card(self.game_deck.pop_left_card())
            current_game.dealer_hand.add_card(self.game_deck.pop_left_card())
