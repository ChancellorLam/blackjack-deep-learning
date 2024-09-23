from blackjack_entities.hand import Hand
from menu_tools.menus import selection_menu


class BlackjackGame:
    def __init__(self):
        self.dealer_hand = Hand()
        self.player_hands = [Hand()]
        self.turn = 0

    def get_player_decision(self):
        prompt_with_decisions = self.construct_prompt_based_on_game_state()
        prompt = prompt_with_decisions[0]
        decisions = prompt_with_decisions[1]
        return selection_menu(prompt, decisions)

    def construct_prompt_based_on_game_state(self):
        prompt = "Would you like to Hit"
        decisions = ["Stand"]
        if self.turn == 0:
            decisions.append("Double")
            if self.player_hands[0].can_split():
                decisions.append("Split")

        if len(decisions) == 1:
            return f"{prompt} or {decisions[0]}?", decisions

        # Join decisions with commas and 'or' for the last item
        return f"{prompt}, " + ", ".join(decisions[:-1]) + f", or {decisions[-1]}?", decisions
