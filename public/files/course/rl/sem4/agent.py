# agent.py — агент: оценки q, счётчики n, update() и act().
# В этом файле один пропуск — ПРОПУСК 2: правило обновления оценки в Agent.update().
# Куски — в snippets.py (группа 2). Проверка: python3 agent.py

import math
import random
import sys

from environment import APPROACHES


class Agent:

    def __init__(self, env, mode="greedy", epsilon=0.1, q0=0.0, c=2.0,
                 alpha=None, h_alpha=0.1, seed=None):
        self.env = env                 # среда — только чтобы тянуть рычаг
        self.mode = mode               # greedy | eps | optimistic | ucb | gradient
        self.epsilon = epsilon         # доля шагов «наугад» у eps
        self.q0 = q0                   # стартовая оценка; у оптимистичной — завышенная
        self.c = c                     # масштаб бонуса неуверенности у ucb
        self.alpha = alpha             # постоянный шаг; None — честное 1/n
        self.h_alpha = h_alpha         # шаг предпочтений у gradient
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        # всё, что копится за прогон: оценки, счётчики, предпочтения
        self.q = {a: self.q0 for a in APPROACHES}
        self.n = {a: 0 for a in APPROACHES}
        self.h = {a: 0.0 for a in APPROACHES}
        self.t = 0
        self.avg = 0.0

    def update(self, act, reward):
        first = self.n[act] == 0
        self.t += 1
        self.n[act] += 1
        if first:
            # первое наблюдение якорит оценку: усреднять пока не с чем
            self.q[act] = reward
        else:
            # ← ПРОПУСК 2: две строки пишем РУКАМИ (не копируем):
            #    step = ...   — какой шаг: честное 1/n или постоянное α
            #    self.q[act] += ...  — сдвиг оценки на долю разницы (reward - self.q[act])
            #    Куски — в snippets.py, группа 2.
            pass
        if self.mode == "gradient":
            self.avg += (reward - self.avg) / self.t
            prefs = self.preferences()
            for a in APPROACHES:
                grad = (1.0 if a == act else 0.0) - prefs[a]
                # сделал лучше среднего — предпочтение растёт
                self.h[a] += self.h_alpha * (reward - self.avg) * grad

    def act(self):
        if self.mode == "eps" and self.rng.random() < self.epsilon:
            return self.rng.choice(APPROACHES)
        if self.mode == "gradient":
            prefs = self.preferences()
            return self.rng.choices(APPROACHES, weights=[prefs[a] for a in APPROACHES])[0]
        if self.mode == "ucb":
            return self.ucb_choice()
        return self.greedy_choice()

    def greedy_choice(self):
        # максимум по оценкам; при равенстве — первый по порядку
        best_q = max(self.q.values())
        return [a for a in APPROACHES if self.q[a] == best_q][0]

    def ucb_choice(self):
        # бонус неуверенности: редко тянутый рычаг получает шанс
        for a in APPROACHES:
            if self.n[a] == 0:
                return a
        return max(APPROACHES,
                   key=lambda a: self.q[a] + self.c * math.sqrt(math.log(self.t) / self.n[a]))

    def preferences(self):
        # softmax над предпочтениями: h превращается в вероятности выбора
        top = max(self.h.values())
        exp = {a: math.exp(self.h[a] - top) for a in APPROACHES}
        z = sum(exp.values())
        return {a: exp[a] / z for a in APPROACHES}


def checks():
    out = []
    env = None                     # для проверок среда не нужна

    a = Agent(env, mode="greedy")
    seen = []
    try:
        for r in (1, 0, 2):        # наблюдения по подходу B из семинара
            a.update("B", r)
            seen.append(round(a.q["B"], 12))
        note = "инкрементальное среднее по B: 1 → 0,5 → 1,0 (честное среднее 1,0)"
    except TypeError:
        note = "шаг оценки пустой: правило не написано или взята одна ветка α без 1/n"
    # сверяем весь ряд, а не только последнее число: с пустым update() выйдет 1 → 1 → 1
    out.append((seen == [1.0, 0.5, 1.0], note))

    a = Agent(env, mode="greedy", alpha=0.5)
    for r in (1, 0, 2):
        a.update("B", r)
    out.append((abs(a.q["B"] - 1.25) < 1e-12,
                "тот же ряд при α = 0,5: 1 → 0,5 → 1,25"))

    a = Agent(env, mode="greedy")
    a.q.update({"A": 0.5, "B": 1.2, "C": 0.9})
    out.append((a.act() == "B", "жадный выбор по оценкам 0,5 / 1,2 / 0,9 — B"))

    a = Agent(env, mode="ucb")
    out.append((a.act() in APPROACHES and a.n[a.act()] == 0,
                "ucb на старте тянет нетронутый рычаг"))

    a = Agent(env, mode="greedy")
    a.n.update({"A": 10, "B": 10, "C": 1})
    a.t = 21
    a.q.update({"A": 0.8, "B": 0.85, "C": 1.1})
    chosen = a.ucb_choice()
    out.append((chosen == "C",
                "ucb берёт не самую частую, а самую неуверенную: C (n = 1)"))

    return out


def self_check(verbose=True):
    result = checks()
    if verbose:
        for ok, text in result:
            print("   [%s] агент: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


ALPHA = 0.5                        # шаг для ряда ниже: поставьте 0,1 или 0,9 — ряд изменится


def trace(arm="B", observations=(1, 0, 2), alpha=ALPHA):
    # один и тот же update(), но два правила рядом: честное среднее и постоянный шаг
    a_mean = Agent(None, mode="greedy")
    a_step = Agent(None, mode="greedy", alpha=alpha)
    lines = ["   шаг  награда    n   Q при 1/n   Q при α = %.2f" % alpha]
    for i, r in enumerate(observations, 1):
        a_mean.update(arm, r)
        a_step.update(arm, r)
        lines.append("   %2d   %7d   %2d   %9.3f   %12.3f"
                     % (i, r, a_mean.n[arm], a_mean.q[arm], a_step.q[arm]))
    print("\nРяд по подходу %s: наблюдения %s" % (arm, ", ".join(str(r) for r in observations)))
    print("\n".join(lines))
    print("   при 1/n оценка равна честному среднему; при α — тянется к свежему")


if __name__ == "__main__":
    print("Агент: тимлид и пять стратегий выбора подхода")
    print("   greedy · eps · optimistic · ucb · gradient")
    print("\nИстинные средние среды (агенту не видны): A = 0,3 · B = 0,8 · C = 1,3")

    try:
        trace()                    # ряд 1 → 0,5 → 1,0 и тот же ряд при α
    except TypeError:
        print("\n   [нет] ряд не построить: шаг оценки пустой — кусок «б» (step = self.alpha)")
        print("   работает только вместе с веткой 1/n: шаг выбирается по self.alpha.")

    print("\nПроверки агента:")
    ok = self_check()
    print("\nитог: все проверки агента сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
    sys.exit(0 if ok else 1)       # код возврата: 0 — сошлось, 1 — есть [нет]
