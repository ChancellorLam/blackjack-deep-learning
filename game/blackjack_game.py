from blackjack_entities.hand import Hand


class BlackjackGame:
    def __init__(self):
        self.dealer_hand = Hand()
        self.player_hands = {"Player 1": Hand()}
