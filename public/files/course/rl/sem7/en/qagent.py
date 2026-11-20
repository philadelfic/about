# Q-learning: TD update of the table after every move.
#
# Temporal-difference (TD) error:
#     target = R                         if the game is over
#     target = R + gamma * max Q(s', b)  otherwise
#     Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))
#
# The max over future cells means the estimate is learned from the best possible
# move, not from the one the agent will really make. That is off-policy: see sarsa.py.

import knobs
from base import Agent
from game import closed_cells


class QAgent(Agent):
    def learn(self, state, action, reward, next_state, next_action, done, alpha):
        # next_action is not needed here: we take the maximum ourselves.
        if done:
            target = reward
        else:
            future = max(self.q(next_state, b) for b in closed_cells(next_state))
            target = reward + knobs.GAMMA * future
        old = self.q(state, action)
        self.table[(state, action)] = old + alpha * (target - old)
