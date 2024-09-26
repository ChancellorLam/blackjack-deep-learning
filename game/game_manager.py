from blackjack_entities.deck import Deck

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

    def check_and_process_blackjack_results(self, current_game, blackjack_ratio):
        print("Dealer's Hand: " + str(current_game.dealer_hand))
        if current_game.player_hands[0].has_blackjack() and current_game.dealer_hand.has_blackjack():
            print("Push!")
        elif current_game.player_hands[0].has_blackjack():
            self.player_money = self.player_money + self.current_bet * blackjack_ratio
            print("Player Blackjack! You win!")
        elif current_game.dealer_hand.has_blackjack():
            self.player_money = self.player_money - self.current_bet
            print("Dealer has Blackjack! You lose!")
        else:
            return False
        return True
