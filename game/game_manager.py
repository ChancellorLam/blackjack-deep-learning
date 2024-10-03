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
        print(f"You are currently starting with: {self.player_money}")
        while True:
            print(f"Game is starting!\nPlacing bets...")
            self.player_money = self.player_money - self.current_bet
            print(f"You now have: {self.player_money}\n")
            game = BlackjackGame(self.current_bet)
            payouts, costs = game.play_single_blackjack_game(self.game_deck, self.player_money, (3 / 2))
            for payout in payouts:
                self.player_money = self.player_money + payout
            self.player_money = self.player_money + self.current_bet
            for cost in costs:
                self.player_money = self.player_money - cost
            input(f"\nYou currently have: {self.player_money}\nPress Enter to Continue.")
