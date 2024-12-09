from blackjack_entities.hand import Hand
from game.blackjack_game import BlackjackGame


class QLearningGame(BlackjackGame):
    def __init__(self, current_bet, q_agent):
        super().__init__(current_bet)
        self.q_agent = q_agent
        self.state_action_pairs = []

    def q_play_single_blackjack_game(self, game_deck, blackjack_ratio):
        self.deal_starting_cards(game_deck)
        dealer_has_blackjack, player_has_blackjack = self.get_blackjack_results()

        if any((dealer_has_blackjack, player_has_blackjack)):

            self.player_hands[0].transfer_all_cards_to(game_deck.used_cards)
            self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)

            if dealer_has_blackjack and player_has_blackjack:
                return [0], [0]
            elif dealer_has_blackjack:
                return [0], [self.player_hands[0].bet]
            elif player_has_blackjack:
                return [(self.player_hands[0].bet * blackjack_ratio)], [0]

        i = 0
        while i < len(self.player_hands):
            self.q_play_player_hand(self.player_hands[i], game_deck, i)
            i = i + 1

        self.q_play_dealer_hand(game_deck)

        for hand in self.player_hands:
            # Get the reward for the hand based on the game result
            final_reward = self.get_end_reward(hand)
            for pair in self.state_action_pairs:
                for state, action in pair:
                    self.q_agent.update_q_value(state, action, final_reward, state, done=True)

        if len(self.player_hands) == 1:
            payout = self.get_game_result(self.player_hands[0])
            self.player_hands[0].transfer_all_cards_to(game_deck.used_cards)
            self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)
            return [payout], [self.player_hands[0].bet]

        player_payouts = []
        costs = []
        for index, hand in enumerate(self.player_hands):
            player_payouts.append(self.get_game_result(hand))
            hand.transfer_all_cards_to(game_deck.used_cards)
            costs.append(hand.bet)
        self.dealer_hand.transfer_all_cards_to(game_deck.used_cards)
        return player_payouts, costs

    def q_play_player_hand(self, hand, game_deck, i):
        player_still_playing = True
        choices_made = []

        while player_still_playing:
            if hand.is_bust() or hand.sum_hand(hard_sum_only=True) == 21:
                player_still_playing = False
            else:
                # Construct the state (player hand value, dealer's upcard)
                hand_value, has_usable_ace = hand.get_state_of_hand()
                state = (hand_value, has_usable_ace, self.dealer_hand.get_top_card())
                choice = self.q_agent.choose_action(state, self.get_possible_actions(i))
                choices_made.append((state, choice))

                if choice == 1: # hit
                    self.hit(hand, game_deck)
                elif choice == 2: # stand
                    player_still_playing = False
                elif choice == 3: # double
                    self.hit(hand, game_deck)
                    hand.double_bet()
                    player_still_playing = False
                elif choice == 4: # split
                    new_hand = Hand(hand.bet)
                    new_hand.add_card(hand.pop_left_card())
                    self.hit(hand, game_deck)
                    self.hit(new_hand, game_deck)
                    self.player_hands.append(new_hand)

                self.turn = self.turn + 1

                # After the agent's decision, update the Q-values (reward needs to be calculated)
                hand_value, has_usable_ace = hand.get_state_of_hand()
                reward = self.get_action_reward(hand)
                next_state = (hand_value, has_usable_ace, self.dealer_hand.get_top_card())
                done = not player_still_playing
                self.q_agent.update_q_value(state, choice, reward, next_state, done)

        self.state_action_pairs.append(choices_made)

    def q_play_dealer_hand(self, game_deck):
        while self.dealer_hand.sum_hand(hard_sum_only=True) < 17:
            self.hit(self.dealer_hand, game_deck)

    @classmethod
    def get_action_reward(cls, hand):
        player_value = hand.sum_hand(hard_sum_only=True)
        if player_value == 21: # this is a very desirable outcome
            return 5
        if player_value > 21: # bust, but punishment will be left to get_end_reward
            return -10
        else: # game continues, small reward for not busting
            return 0.25

    def get_end_reward(self, hand):
        player_value = hand.sum_hand(hard_sum_only=True)
        dealer_value = self.dealer_hand.sum_hand(hard_sum_only=True)

        end_reward_modifier = 1
        # If the agent doubled, we need to modify the reward
        if hand.doubled:
            end_reward_modifier = 2

        # Define the reward structure: win (+1), lose (-1), draw (0)
        if player_value > 21:  # this is a very undesirable outcome, agent busts
            return -1 * end_reward_modifier
        elif dealer_value > 21: # dealer busts
            return 1 * end_reward_modifier
        else:
            if dealer_value > player_value: # dealer wins
                return -1 * end_reward_modifier
            elif dealer_value < player_value: # player wins
                return 1 * end_reward_modifier
            else: # push
                return 0 * end_reward_modifier

    def get_possible_actions(self, i):
        actions = [1, 2] # [hit, stand]
        if self.turn == 0:
            actions.append(3) # double
            if self.player_hands[i].can_split():
                actions.append(4)

        return actions
