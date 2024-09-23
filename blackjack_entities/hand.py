from blackjack_entities.card_collection import CardCollection

class Hand(CardCollection):

    def sum_hand(self):
        lower_sum = 0
        higher_sum = 0
        num_aces = 0

        for card in self.cards:
            if card.get_card() == "A":
                num_aces = num_aces + 1
            higher_sum = higher_sum + card.get_value()

        while num_aces > 0 and higher_sum > 21:
            num_aces = num_aces - 1
            higher_sum = higher_sum - 10

        if num_aces > 0 and higher_sum - 10 > 0:
            lower_sum = higher_sum - 10
        return [lower_sum, higher_sum]

    def can_split(self):
        return self.cards[0].get_card() == self.cards[1].get_card()
