# Градиентная стратегия: предпочтения вместо оценок.

import math

import knobs
from base import BanditAgent


class GradientAgent(BanditAgent):
    # Выбор по softmax над предпочтениями h.
#
    # Обновление: h_i += ETA * (R - R_avg) * (1[a=i] - pi_i).
    # Выбранное блюдо растёт, невыбранные снижаются; награда хуже
    # среднего даёт отрицательный сдвиг. Оценки q не используются.

    def __init__(self, n_arms, step="alpha", eta=None):
        super().__init__(n_arms, step)
        self.eta = knobs.ETA if eta is None else eta
        self.h = [0.0] * n_arms
        self.avg = 0.0

    def probs(self):
        top = max(self.h)
        exp = [math.exp(x - top) for x in self.h]
        total = sum(exp)
        return [x / total for x in exp]

    def choose(self, rng):
        probs = self.probs()
        roll, acc = rng.random(), 0.0
        for arm, p in enumerate(probs):
            acc += p
            if roll <= acc:
                return arm
        return self.n_arms - 1

    def update(self, arm, reward):
        self.t += 1
        self.n[arm] += 1
        self.avg += (reward - self.avg) / self.t
        probs = self.probs()
        for i in range(self.n_arms):
            grad = (1.0 if i == arm else 0.0) - probs[i]
            self.h[i] += self.eta * (reward - self.avg) * grad
