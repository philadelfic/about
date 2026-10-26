# agent.py — агент: оценки q, счётчики n, update() и act().
# Проверка: python3 agent.py
#
# Теория на портале:
#   «Как двигается оценка» — семинар 3:
#   https://philadelfic.github.io/about/students/mai/rl/seminars/03-mnogorukij-bandit/
#   «ε-жадная стратегия» — тема 2:
#   https://philadelfic.github.io/about/students/mai/rl/topics/02-agent-i-sreda/

import math
import random

from environment import APPROACHES, OBS, mean


class Agent:                                                           # тимлид: оценки, счётчики, стратегия

    def __init__(self, env, mode="greedy", epsilon=0.1, q0=0.0, c=2.0,
                 alpha=None, h_alpha=0.1, seed=None):
        self.env = env                                                 # среда — только чтобы тянуть рычаг
        self.mode = mode                                               # greedy | eps | optimistic | ucb | gradient
        self.epsilon = epsilon                                         # доля шагов «наугад» у eps
        self.q0 = q0                                                   # стартовая оценка (оптимистичная — завышенная)
        self.c = c                                                     # масштаб бонуса неуверенности у ucb
        self.alpha = alpha                                             # постоянный шаг; None — честное 1/n
        self.h_alpha = h_alpha                                         # шаг у gradient
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        self.q = {a: self.q0 for a in APPROACHES}                      # оценки ценности подходов
        self.n = {a: 0 for a in APPROACHES}                            # сколько спринтов провели каждым
        self.h = {a: 0.0 for a in APPROACHES}                          # предпочтения у gradient
        self.t = 0                                                     # всего спринтов
        self.avg = 0.0                                                 # средний доход — базовая линия gradient

    def update(self, act, reward):
        first = self.n[act] == 0                                       # первое наблюдение по рычагу —
        self.t += 1                                                    # оценка становится равной ему,
        self.n[act] += 1                                               # дальше начинаем подтягивать
        if first:
            self.q[act] = reward
        else:
            step = self.alpha if self.alpha is not None else 1.0 / self.n[act]
            raise NotImplementedError("впишите правило обновления оценки в update()")
        if self.mode == "gradient":
            self.avg += (reward - self.avg) / self.t                   # базовая линия: средний доход
            prefs = self.preferences()
            for a in APPROACHES:
                grad = (1.0 if a == act else 0.0) - prefs[a]           # «сделал лучше среднего — растим»
                self.h[a] += self.h_alpha * (reward - self.avg) * grad

    def act(self):
        if self.mode == "eps":
            raise NotImplementedError("впишите ε-жадный выбор в act()")
        if self.mode == "gradient":
            prefs = self.preferences()
            return self.rng.choices(APPROACHES,
                                    weights=[prefs[a] for a in APPROACHES])[0]
        if self.mode == "ucb":
            return self.ucb_choice()
        return self.greedy_choice()

    def greedy_choice(self):                                           # максимум по оценкам; при равенстве — первый
        best_q = max(self.q.values())
        return [a for a in APPROACHES if self.q[a] == best_q][0]

    def ucb_choice(self):                                              # бонус неуверенности: редкий рычаг получает шанс
        for a in APPROACHES:
            if self.n[a] == 0:
                return a
        return max(APPROACHES,
                   key=lambda a: self.q[a] + self.c * math.sqrt(math.log(self.t) / self.n[a]))

    def preferences(self):                                             # softmax над предпочтениями
        top = max(self.h.values())
        exp = {a: math.exp(self.h[a] - top) for a in APPROACHES}
        z = sum(exp.values())
        return {a: exp[a] / z for a in APPROACHES}


def checks():                                                          # что проверяет у себя
    out = []
    env = None                                                         # для проверок среда не нужна

    a = Agent(env, mode="greedy")
    for r in (1, 0, 2):                                                # наблюдения по подходу B из семинара
        a.update("B", r)
    out.append((abs(a.q["B"] - 1.0) < 1e-12,
                "инкрементальное среднее по B: 1 → 0,5 → 1,0 (честное среднее 1,0)"))

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


def self_check(verbose=True):                                          # агент проверяет себя: python3 agent.py
    result = checks()
    if verbose:
        for ok, text in result:
            print("   [%s] агент: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


ALPHA = 0.5                                                            # α: 0.1 или 0.9 — ряд изменится


def trace(arm="B", observations=(1, 0, 2), alpha=ALPHA):               # ряд по шагам: 1/n и α
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
        trace()                                                        # ряд 1 → 0,5 → 1,0 при 1/n и α
    except NotImplementedError as e:
        print("\n   [нет] ряд пока не построить: %s" % e)

    print("\nПроверки агента:")
    try:
        ok = self_check()
    except NotImplementedError as e:
        print("   [нет] агент: %s" % e)
        print("   Впишите одну строку — и запустите снова: python3 agent.py")
        raise SystemExit(1)
    print("\nитог: все проверки агента сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
