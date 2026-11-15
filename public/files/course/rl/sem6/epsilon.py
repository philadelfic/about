# Эпсилон-жадная стратегия: почти всегда своё, изредка пробуешь новое.

import knobs
from base import BanditAgent


class EpsilonAgent(BanditAgent):
    # С вероятностью ε (knobs.EPSILON) выбор случайный, иначе жадный.

    def __init__(self, n_arms, step="alpha", epsilon=None):
        super().__init__(n_arms, step)
        self.epsilon = knobs.EPSILON if epsilon is None else epsilon

    def choose(self, rng):
        if rng.random() < self.epsilon:
            return rng.randrange(self.n_arms)
        return self.greedy_arm()
