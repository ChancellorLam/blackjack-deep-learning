from blackjack_entities.hand import Hand
from menu_tools.menus import selection_menu


class BlackjackGame:
    def __init__(self, current_bet):
        self.dealer_hand = Hand()
        self.player_hands = [Hand(current_bet)]
        self.turn = 0

    def play_player_hand(self, hand, game_deck):
        player_still_playing = True

        while player_still_playing:
            if hand.is_bust() or hand.sum_hand(hard_sum_only=True) == 21:
                player_still_playing = False
            else:
                choice = self.get_player_choice()
                if choice == 1:
                    self.hit(hand, game_deck)
                elif choice == 2:
                    print("Standing...")
                    player_still_playing = False
                elif choice == 3:
                    print("Doubling...")
                    self.hit(hand, game_deck)
                    hand.double_bet()
                    player_still_playing = False
                elif choice == 4:
                    print("Split is not currently supported.")
                self.turn = self.turn + 1

    def play_dealer_hand(self, game_deck):
        while self.dealer_hand.sum_hand() < 17:
            self.hit(self.dealer_hand, game_deck)
            print(f"Dealer hits.\nDealer Hand: {self.dealer_hand}")

    def generate_result_message(self, hand_index):
        player_value = self.player_hands[hand_index].sum_hand(hard_sum_only=True)
        dealer_value = self.dealer_hand.sum_hand()

        if dealer_value > 21:
            return "Dealer busts! You win!"
        else:
            if dealer_value > player_value:
                return "Dealer wins!"
            elif dealer_value < player_value:
                return "You win!"
            else:
                return "Push!"

    def deal_starting_cards(self, game_deck):
        for i in range(0, 2):
            self.player_hands[0].add_card(game_deck.pop_left_card())
            self.dealer_hand.add_card(game_deck.pop_left_card())

    def get_blackjack_results(self):
        return self.dealer_hand.has_blackjack(), self.player_hands[0].has_blackjack()

    def print_game_state(self):
        print(f"Dealer's Upcard: {self.dealer_hand.get_top_card()}")
        print(f"Player's Hand: {self.player_hands[0]}")

        hand_value = self.player_hands[0].sum_hand()
        if isinstance(hand_value, int):
            print(f"Your hand value is: {hand_value}")
        elif isinstance(hand_value, tuple) and len(hand_value) == 2:
            print(f"Your hand value is: {hand_value[0]}/{hand_value[1]}")

    def get_player_choice(self):
        choice_and_possible_decisions = self.construct_prompt_based_on_game_state()
        choice = choice_and_possible_decisions[0]
        decisions = choice_and_possible_decisions[1]
        return selection_menu(choice, decisions)

    def hit(self, hand, game_deck):
        hand.add_card(game_deck.pop_left_card())
        self.print_game_state()

    def construct_prompt_based_on_game_state(self):
        self.print_game_state()
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
