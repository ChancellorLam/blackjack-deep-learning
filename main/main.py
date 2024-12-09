from game.game_manager import GameManager

def main():
    game_manager = GameManager()
    # game_manager.continuously_play_blackjack()
    game_manager.q_learning_blackjack()

if __name__ == '__main__':
    main()
