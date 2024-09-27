from blackjack_entities.hand import Hand
from menu_tools.menus import selection_menu


class BlackjackGame:
    def __init__(self):
        self.dealer_hand = Hand()
        self.player_hands = [Hand()]
        self.turn = 0

    def deal_starting_cards(self, game_deck):
        for i in range(0, 2):
            self.player_hands[0].add_card(game_deck.pop_left_card())
            self.dealer_hand.add_card(game_deck.pop_left_card())

    def check_and_print_blackjack_results(self):
        dealer_has_blackjack = self.dealer_hand.has_blackjack()
        player_has_blackjack = self.player_hands[0].has_blackjack()

        if player_has_blackjack and dealer_has_blackjack:
            print("Push!")
        elif player_has_blackjack:
            print("Player Blackjack! You win!")
        elif dealer_has_blackjack:
            print("Dealer has Blackjack! You lose!")

        return dealer_has_blackjack, player_has_blackjack

    def print_game_state(self):
        print(f"Dealer's Hand: {self.dealer_hand}")
        print(f"Player's Hand: {self.player_hands[0]}")
        lower_sum, higher_sum = self.player_hands[0].sum_hand()
        if lower_sum == higher_sum:
            print(f"Your hand value is: {higher_sum}")
        else:
            print(f"Your hand value is: {lower_sum}/{higher_sum}")

    def get_player_choice(self):
        choice_and_possible_decisions = self.construct_prompt_based_on_game_state()
        choice = choice_and_possible_decisions[0]
        decisions = choice_and_possible_decisions[1]
        return selection_menu(choice, decisions)

    def construct_prompt_based_on_game_state(self):
        prompt = "Would you like to "
        decisions = ["Hit", "Stand"]
        if self.turn == 0:
            decisions.append("Double")
            if self.player_hands[0].can_split():
                decisions.append("Split")

        if len(decisions) == 2:
            return f"{prompt}{decisions[0]} or {decisions[1]}?", decisions

        # Join decisions with commas and 'or' for the last item
        return f"{prompt}{', '.join(decisions[:-1])}, or {decisions[-1]}?", decisions
