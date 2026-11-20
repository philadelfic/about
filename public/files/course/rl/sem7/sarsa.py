# SARSA: та же таблица, та же TD-правка, отличие в одной строке.
#
#     Q-обучение: target = R + gamma * max Q(s', b)   — оценка у лучшего хода
#     SARSA:      target = R + gamma * Q(s', a')      — оценка у своего хода
#
# a' — ход, который агент выберет из s' тем же eps-жадным правилом, с теми же
# случайными пробами. Поэтому SARSA называют on-policy: она учит таблицу
# ценить ту линию поведения, которую агент ведёт, вместе с её разведкой.

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
