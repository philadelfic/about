# SARSA: the same table, the same TD update, the difference is one line.
#
#     Q-learning: target = R + gamma * max Q(s', b)   — estimate of the best move
#     SARSA:      target = R + gamma * Q(s', a')      — estimate of its own move
#
# a' is the move the agent will choose from s' by the same eps-greedy rule, with the
# same random probes. That is why SARSA is called on-policy: it teaches the table
# to value the line of behaviour the agent actually follows, exploration included.

import knobs
from base import Agent


class SarsaAgent(Agent):
    def learn(self, state, action, reward, next_state, next_action, done, alpha):
        if done:
            target = reward
        else:
            target = reward + knobs.GAMMA * self.q(next_state, next_action)
        old = self.q(state, action)
        self.table[(state, action)] = old + alpha * (target - old)
