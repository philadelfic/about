# Базовый агент: таблица Q и выбор хода.
#
# Q — словарь (состояние, клетка) -> оценка шанса на победу.
# Начинаем с нулей: «ничего не знаю обо всём».

from game import closed_cells


class Agent:
    def __init__(self):
        self.table = {}

    def q(self, state, action):
        return self.table.get((state, action), 0.0)

    def choose(self, state, rng, epsilon):
        # ε-жадный выбор: с вероятностью epsilon — наугад, иначе — лучшее.
        # При равных Q берётся клетка с меньшим номером (строгое `>` в цикле);
        # тот же порядок в top — иначе на слайде была бы одна клетка,
        # а на паре агент открывал бы другую.
        closed = closed_cells(state)
        if rng.random() < epsilon:
            return rng.choice(closed)
        best, best_q = None, None
        for a in closed:
            v = self.q(state, a)
            if best_q is None or v > best_q:
                best, best_q = a, v
        return best

    def top(self, state, k=3):
        # Лучшие k закрытых клеток с оценками — для демонстрации залу.
        scored = sorted(
            closed_cells(state), key=lambda a: (-self.q(state, a), a)
        )
        return [(self.q(state, a), a) for a in scored[:k]]
