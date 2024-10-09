from blackjack_entities.deck import Deck
from game.blackjack_game import BlackjackGame
import random


class GameManager:
    def __init__(self):
        self.player_money = 500
        self.current_bet = 15
        self.game_deck = Deck()
        self.blackjack_ratio = 3 / 2

    def load_game_deck_with_standard_decks(self, num_decks):
        self.game_deck.add_standard_decks(num_decks)

    def continuously_play_blackjack(self):
        player_still_playing = True

        self.load_game_deck_with_standard_decks(8)
        deck_penetration_shuffle_point = round(random.uniform(0.4, 0.6) * len(self.game_deck))
        self.game_deck.shuffle()
        print(f"You are currently starting with: {self.player_money}")
        while player_still_playing:
            print(f"Game is starting!\nPlacing bets...")
            self.player_money = self.player_money - self.current_bet
            print(f"You now have: {self.player_money}\n")
            game = BlackjackGame(self.current_bet)
            payouts, costs = game.play_single_blackjack_game(self.game_deck, self.blackjack_ratio)
            for payout in payouts:
                self.player_money = self.player_money + payout
            self.player_money = self.player_money + self.current_bet
            for cost in costs:
                self.player_money = self.player_money - cost
            if input(f"\nYou currently have: {self.player_money}\n"
                     f"Press Enter to Continue or Enter 'Quit' to Exit the Game.\n").lower() == 'quit':
                player_still_playing = False

            if len(self.game_deck.used_cards) >= deck_penetration_shuffle_point:
                print("Reshuffling deck...\n")
                self.game_deck.restore_used_cards()
                self.game_deck.shuffle()
                deck_penetration_shuffle_point = round(random.uniform(0.4, 0.6) * len(self.game_deck))
