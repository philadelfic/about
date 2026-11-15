# Жадная стратегия: выбрал раз — сидишь дальше.

from base import BanditAgent


class GreedyAgent(BanditAgent):
    # Всегда берёт блюдо с максимальной оценкой.

    def choose(self, rng):
        return self.greedy_arm()
