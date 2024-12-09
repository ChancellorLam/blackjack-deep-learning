import random

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.001, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {} # Dictionary to hold Q-values for each state-action pair

    def get_q_value(self, state, action):
        """ Returns the Q-value for a state-action pair. """
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.actions}
        return self.q_table[state].get(action, 0)

    def update_q_value(self, state, action, reward, next_state, done):
        """ Updates the Q-value based on the Q-learning formula. """
        max_future_q = 0 if done else max(self.get_q_value(next_state, a) for a in self.actions)
        current_q = self.get_q_value(state, action)
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

    def choose_action(self, state, possible_actions):
        """ Chooses an action based on epsilon-greedy strategy. """
        if random.random() < self.exploration_rate:
            return random.choice(possible_actions)  # Explore: choose a random action
        else:
            # Exploit: choose the action with the highest Q-value for this state
            q_values = [self.get_q_value(state, action) for action in self.actions]
            max_q = max(q_values)
            best_actions = [action for action, q in zip(self.actions, q_values) if q == max_q]
            return random.choice(best_actions)  # If multiple actions have the same Q-value, choose randomly