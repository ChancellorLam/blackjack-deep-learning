from blackjack_entities.card_collection import CardCollection

class Hand(CardCollection):

    def sum_hand(self):
        hard_sum = 0
        num_aces = 0

        for card in self.cards:
            if card.get_card() == "A":
                num_aces = num_aces + 1
            hard_sum = hard_sum + card.get_value()

        while num_aces > 0 and hard_sum > 21:
            num_aces = num_aces - 1
            hard_sum = hard_sum - 10

        if num_aces > 0 and hard_sum - 10 > 0:
            soft_sum = (hard_sum - 10, hard_sum)
            return soft_sum
        return hard_sum

    def can_split(self):
        return self.cards[0].get_card() == self.cards[1].get_card()

    def has_blackjack(self):
        return self.cards[0].get_value() + self.cards[1].get_value() == 21

    def is_bust(self):
        lower_sum, higher_sum = self.sum_hand()
        return lower_sum > 21
