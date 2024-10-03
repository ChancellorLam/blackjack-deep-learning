from blackjack_entities.deck import Deck
from game.blackjack_game import BlackjackGame


class GameManager:
    def __init__(self):
        self.player_money = 500
        self.current_bet = 15
        self.game_deck = Deck()

    def load_game_deck_with_standard_decks(self, num_decks):
        self.game_deck.add_standard_decks(num_decks)

    def continuously_play_blackjack(self):
        self.load_game_deck_with_standard_decks(8)
        self.game_deck.shuffle()
        while True:
            game = BlackjackGame(self.current_bet)
            game.play_single_blackjack_game(self.game_deck, (3 / 2))
            input("Press Enter to Continue.\n")
