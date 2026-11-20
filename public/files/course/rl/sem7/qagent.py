# Q-обучение: TD-обновление таблицы после каждого хода.
#
# Ошибка по времени разности (TD-ошибка):
#     target = R                         если партия кончилась
#     target = R + gamma * max Q(s', b)  иначе
#     Q(s, a) <- Q(s, a) + alpha * (target - Q(s, a))
#
# max по будущим клеткам — значит, оценка учится у лучшего возможного хода,
# а не у того, который агент правда сделает. Это off-policy: см. sarsa.py.

import knobs
from base import Agent
from game import closed_cells


class QAgent(Agent):
    def learn(self, state, action, reward, next_state, next_action, done, alpha):
        # next_action не нужен: максимум берём сами.
        if done:
            target = reward
        else:
            future = max(self.q(next_state, b) for b in closed_cells(next_state))
            target = reward + knobs.GAMMA * future
        old = self.q(state, action)
        self.table[(state, action)] = old + alpha * (target - old)
