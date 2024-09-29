from blackjack_entities.hand import Hand
from menu_tools.menus import selection_menu


class BlackjackGame:
    def __init__(self):
        self.dealer_hand = Hand()
        self.player_hands = [Hand()]
        self.turn = 0

    def play_player_hand(self, hand, game_deck):
        while not hand.is_bust():
            choice = self.get_player_choice()
            if choice == 1:
                self.hit(hand, game_deck)
            elif choice == 2:
                self.stand()
            elif choice == 3:
                self.double(hand, game_deck)
            elif choice == 4:
                print("Split is not currently supported.")
            self.turn = self.turn + 1

    def play_dealer_hand(self, game_deck, player_value):
        while self.dealer_hand.sum_hand() < 17:
            self.hit(self.dealer_hand, game_deck)
            print(f"Dealer hits.\nDealer Hand: {self.dealer_hand}")

        dealer_value = self.dealer_hand.sum_hand()
        print(f"Dealer final hand value: {dealer_value}")
        if dealer_value > 21:
            print("Dealer busts! You win!")
        else:
            if dealer_value > player_value:
                print("Dealer wins!")
            elif dealer_value < player_value:
                print("You win!")
            else:
                print("Push!")

    def deal_starting_cards(self, game_deck):
        for i in range(0, 2):
            self.player_hands[0].add_card(game_deck.pop_left_card())
            self.dealer_hand.add_card(game_deck.pop_left_card())

    def check_and_print_blackjack_results(self):
        dealer_has_blackjack = self.dealer_hand.has_blackjack()
        player_has_blackjack = self.player_hands[0].has_blackjack()

        self.print_game_state()
        if player_has_blackjack and dealer_has_blackjack:
            print("Push!")
        elif player_has_blackjack:
            print("Player Blackjack! You win!")
        elif dealer_has_blackjack:
            print("Dealer has Blackjack! You lose!")

        return dealer_has_blackjack, player_has_blackjack

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

    def stand(self):
        print("Standing...")

    def double(self, hand, game_deck):
        self.hit(hand, game_deck)

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
