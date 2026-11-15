# Стратегии выбора блюда.
#
# Каждый модуль содержит ровно один агент. У всех один интерфейс:
# choose(rng) -> номер блюда, update(arm, reward).
#
# Имена, которые видит студент: завсегдатай, пятница, любопытный,
# тянущийся, оптимист. Латинские синонимы — на случай, если команду
# набирают по-английски.

from epsilon import EpsilonAgent
from gradient import GradientAgent
from greedy import GreedyAgent
from optimistic import OptimisticAgent
from ucb import UcbAgent

AGENTS = {
    # имена персонажей
    "завсегдатай": GreedyAgent,
    "пятница": EpsilonAgent,
    "любопытный": UcbAgent,
    "тянущийся": GradientAgent,
    "оптимист": OptimisticAgent,
    # латинские синонимы
    "greedy": GreedyAgent,    "сидит": GreedyAgent,    "жадный": GreedyAgent,
    "eps": EpsilonAgent,
    "ucb": UcbAgent,
    "gradient": GradientAgent,
    "optimistic": OptimisticAgent,
}

# Правило обновления после двоеточия в команде: пятница:avg или пятница:alpha
STEPS = ("alpha", "avg")
