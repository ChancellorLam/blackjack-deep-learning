from blackjack_entities.hand import Hand
from menu_tools.menus import selection_menu
import time


class BlackjackGame:
    def __init__(self, current_bet):
        self.dealer_hand = Hand()
        self.player_hands = [Hand(current_bet)]
        self.turn = 0

    def play_single_blackjack_game(self, game_deck, blackjack_ratio):
        self.deal_starting_cards(game_deck)
        dealer_has_blackjack, player_has_blackjack = self.get_blackjack_results()

        if any((dealer_has_blackjack, player_has_blackjack)):
            self.print_game_state(reveal_dealer_hand=True)
            time.sleep(2)

            self.player_hands[0].transfer_all_cards_to(game_deck.used_cards)
            self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)

            if dealer_has_blackjack and player_has_blackjack:
                print("Push!")
                return [0], [0]
            elif dealer_has_blackjack:
                print("Dealer has Blackjack! You lose!")
                return [0], [self.player_hands[0].bet]
            elif player_has_blackjack:
                print("Player Blackjack! You win!")
                return [(self.player_hands[0].bet * blackjack_ratio)], [0]

        i = 0
        while i < len(self.player_hands):
            self.play_player_hand(self.player_hands[i], game_deck, i)
            i = i + 1

        self.play_dealer_hand(game_deck)

        if len(self.player_hands) == 1:
            print(self.generate_result_message(self.player_hands[0]))
            payout = self.get_game_result(self.player_hands[0])
            self.player_hands[0].transfer_all_cards_to(game_deck.used_cards)
            self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)
            return [payout], [self.player_hands[0].bet]

        player_payouts = []
        costs = []
        for index, hand in enumerate(self.player_hands):
            print(f"Hand {index + 1}: {self.generate_result_message(hand)}")
            player_payouts.append(self.get_game_result(hand))
            hand.transfer_all_cards_to(game_deck.used_cards)
            costs.append(hand.bet)
        self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)
        return player_payouts, costs

    def play_player_hand(self, hand, game_deck, i):
        player_still_playing = True

        while player_still_playing:
            if hand.is_bust():
                print("Bust! Dealer wins!")
                player_still_playing = False
                time.sleep(2)
            elif hand.sum_hand(hard_sum_only=True) == 21:
                player_still_playing = False
                time.sleep(2)
            else:
                choice = self.get_player_choice(i)
                if choice == 1:
                    self.hit(hand, game_deck)
                elif choice == 2:
                    print("Standing...\n")
                    player_still_playing = False
                elif choice == 3:
                    print("Doubling...\n")
                    self.hit(hand, game_deck)
                    hand.double_bet()
                    self.print_game_state(hand_index=i)
                    time.sleep(2)
                    if hand.is_bust():
                        print("Bust! Dealer wins!")
                    player_still_playing = False
                elif choice == 4:
                    new_hand = Hand(hand.bet)
                    new_hand.add_card(hand.pop_left_card())
                    self.hit(hand, game_deck)
                    self.hit(new_hand, game_deck)
                    self.player_hands.append(new_hand)

                if player_still_playing:
                    self.print_game_state(hand_index=i)
                self.turn = self.turn + 1

    def play_dealer_hand(self, game_deck):
        if self.dealer_hand.sum_hand(hard_sum_only=True) < 17:
            self.print_game_state(reveal_dealer_hand=True)
            time.sleep(2)
            while self.dealer_hand.sum_hand(hard_sum_only=True) < 17:
                self.hit(self.dealer_hand, game_deck)
                print(f"Dealer hits.")
                self.print_game_state(reveal_dealer_hand=True)
                if not self.dealer_hand.is_bust():
                    time.sleep(2)
        elif self.dealer_hand.is_bust():
            print(f"Dealer busts!")
            self.print_game_state(reveal_dealer_hand=True)
        else:
            print(f"Dealer stands.")
            self.print_game_state(reveal_dealer_hand=True)

        print(f"Dealer final hand value: {self.dealer_hand.sum_hand(hard_sum_only=True)}")

    def generate_result_message(self, hand):
        player_value = hand.sum_hand(hard_sum_only=True)
        dealer_value = self.dealer_hand.sum_hand(hard_sum_only=True)
        if player_value > 21:
            return "Dealer wins!"
        elif dealer_value > 21:
            return "Dealer busts! You win!"
        else:
            if dealer_value > player_value:
                return "Dealer wins!"
            elif dealer_value < player_value:
                return "You win!"
            else:
                return "Push!"

    def get_game_result(self, hand):
        player_value = hand.sum_hand(hard_sum_only=True)
        dealer_value = self.dealer_hand.sum_hand(hard_sum_only=True)

        if player_value > 21:
            return 0
        elif dealer_value > 21:
            return hand.bet * 2
        else:
            if dealer_value > player_value:
                return 0
            elif dealer_value < player_value:
                return hand.bet * 2
            else:
                return hand.bet

    def deal_starting_cards(self, game_deck):
        for i in range(0, 2):
            self.player_hands[0].add_card(game_deck.pop_left_card())
            self.dealer_hand.add_card(game_deck.pop_left_card())

    def get_blackjack_results(self):
        return self.dealer_hand.has_blackjack(), self.player_hands[0].has_blackjack()

    def print_game_state(self, reveal_dealer_hand=False, hand_index=0):
        if reveal_dealer_hand:
            print(f"Dealer's Hand: {self.dealer_hand}")
        else:
            print(f"Dealer's Upcard: [{self.dealer_hand.get_top_card()}]")

        if len(self.player_hands) == 1:
            print(f"Player's Hand: {self.player_hands[0]}")
            hand_value = self.player_hands[hand_index].sum_hand()
            if isinstance(hand_value, int):
                print(f"Your hand value is: {hand_value}")
            elif isinstance(hand_value, tuple) and len(hand_value) == 2:
                print(f"Your hand value is: {hand_value[0]}/{hand_value[1]}")
        else:
            for index, hand in enumerate(self.player_hands):
                print(f"Player Hand {index}: {self.player_hands[index]}")
            for index, hand in enumerate(self.player_hands):
                hand_value = hand.sum_hand()
                if isinstance(hand_value, int):
                    print(f"Hand {index} Value: {hand_value}")
                elif isinstance(hand_value, tuple) and len(hand_value) == 2:
                    print(f"Hand {index} Value: {hand_value[0]}/{hand_value[1]}")
        print()

    def get_player_choice(self, hand_index):
        choice_and_possible_decisions = self.construct_prompt_based_on_game_state(hand_index)
        choice = choice_and_possible_decisions[0]
        decisions = choice_and_possible_decisions[1]
        return selection_menu(choice, decisions)

    @classmethod
    def hit(cls, hand, game_deck):
        hand.add_card(game_deck.pop_left_card())

    def construct_prompt_based_on_game_state(self, i):
        self.print_game_state(hand_index=i)
        prompt = "Would you like to "
        decisions = ["Hit", "Stand"]
        if self.turn == 0:
            decisions.append("Double")
            if self.player_hands[0].can_split():
                decisions.append("Split")

        specific_hand = ""
        if len(self.player_hands) > 1:
            specific_hand = f" for Hand {i}"

        if len(decisions) == 2:
            return f"{prompt}{decisions[0]} or {decisions[1]}{specific_hand}?", decisions

        # Join decisions with commas and 'or' for the last item
        return f"{prompt}{', '.join(decisions[:-1])}, or {decisions[-1]}{specific_hand}?", decisions
