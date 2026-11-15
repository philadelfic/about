# UCB: бонус за давно непробованные блюда.

import math

import knobs
from base import BanditAgent


class UcbAgent(BanditAgent):
    # Выбирает максимум оценки плюс бонус c * sqrt(ln t / n).
#
    # Нетронутые блюда перебираются в первую очередь (иначе деление
    # на ноль).

    def __init__(self, n_arms, step="alpha", c=None):
        super().__init__(n_arms, step)
        self.c = knobs.C_UCB if c is None else c

    def choose(self, rng):
        for arm in range(self.n_arms):
            if self.n[arm] == 0:
                return arm
        return max(
            range(self.n_arms),
            key=lambda i: self.q[i] + self.c * math.sqrt(math.log(max(self.t, 2)) / self.n[i]),
        )
