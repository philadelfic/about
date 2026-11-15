# Оптимистичная инициализация: всё кажется отличным, пока не попробуешь.

import knobs
from base import BanditAgent


class OptimisticAgent(BanditAgent):
    # Жадный выбор по оценкам, стартующим выше любого возможного среднего.
#
    # Завышенный старт сам заставляет перебрать все блюда.

    def __init__(self, n_arms, step="alpha"):
        super().__init__(n_arms, step)
        self.q = [knobs.Q0] * n_arms

    def choose(self, rng):
        return self.greedy_arm()
