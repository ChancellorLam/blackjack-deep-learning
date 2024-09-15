
class Card:
    def __init__(self, card_num):
        if 1 <= card_num <= 13:
            self.card_num = card_num
        else:
            raise ValueError

    def get_card(self):
        if self.card_num == 1:
            return "A"
        elif self.card_num == 11:
            return "J"
        elif self.card_num == 12:
            return "Q"
        elif self.card_num == 13:
            return "K"
        else:
            return str(self.card_num)

    def get_value(self):
        if self.card_num in (11, 12, 13):
            return 10
        elif self.card_num == 1:
            return 11
        else:
            return self.card_num
