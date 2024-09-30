from blackjack_entities.card_collection import CardCollection

class Hand(CardCollection):
    def __init__(self, bet=None):
        super().__init__()
        self.bet = bet

    def sum_hand(self, hard_sum_only=False):
        hard_sum = 0
        num_aces_counting_as_eleven = 0

        for card in self.cards:
            if card.get_card() == "A":
                num_aces_counting_as_eleven = num_aces_counting_as_eleven + 1
            hard_sum = hard_sum + card.get_value()

        while num_aces_counting_as_eleven > 0 and hard_sum > 21:
            num_aces_counting_as_eleven = num_aces_counting_as_eleven - 1
            hard_sum = hard_sum - 10

        if not hard_sum_only:
            can_count_as_soft_sum = num_aces_counting_as_eleven > 0 and hard_sum - 10 > 0

            if can_count_as_soft_sum:
                soft_sum = (hard_sum - 10, hard_sum)
                return soft_sum

        return hard_sum

    def can_split(self):
        return self.cards[0].get_card() == self.cards[1].get_card()

    def has_blackjack(self):
        return self.cards[0].get_value() + self.cards[1].get_value() == 21

    def is_bust(self):
        hand_value = self.sum_hand()

        if isinstance(hand_value, int):
            return hand_value > 21
        elif isinstance(hand_value, tuple) and len(hand_value) == 2:
            return hand_value[0] > 21 and hand_value[1] > 21

    def double_bet(self):
        self.bet = self.bet * 2
