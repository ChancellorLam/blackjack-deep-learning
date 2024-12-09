from blackjack_entities.deck import Deck
from game.blackjack_game import BlackjackGame
import random
from machine_learning.q_learning.q_learning_agent import QLearningAgent
from machine_learning.q_learning.q_learning_game import QLearningGame


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
                deck_penetration_shuffle_point = round( random.uniform(0.4, 0.6) * len(self.game_deck) )

    def q_learning_blackjack(self):
        self.load_game_deck_with_standard_decks(8)
        deck_penetration_shuffle_point = round(random.uniform(0.4, 0.6) * len(self.game_deck))
        self.game_deck.shuffle()
        q_agent = QLearningAgent([1, 2, 3, 4])
        for _ in range(0, 50):
            self.player_money = 15000000
            initial_iteration_balance = self.player_money

            for __ in range(0, 1000000):
                game = QLearningGame(self.current_bet, q_agent)
                payouts, costs = game.q_play_single_blackjack_game(self.game_deck, self.blackjack_ratio)
                for payout in payouts:
                    self.player_money = self.player_money + payout
                for cost in costs:
                    self.player_money = self.player_money - cost
                if len(self.game_deck.used_cards) >= deck_penetration_shuffle_point:
                    self.game_deck.restore_used_cards()
                    self.game_deck.shuffle()
                    deck_penetration_shuffle_point = round(random.uniform(0.4, 0.6) * len(self.game_deck))

            print(f"Starting Balance: {initial_iteration_balance}")
            print(f"Balance After Iteration: {self.player_money}")
            print(f"Percent Change: "
                  f"{((self.player_money - initial_iteration_balance) / initial_iteration_balance) * 100}%\n")

