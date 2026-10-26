# environment.py — среда: три подхода, распределения, step(); средние невидимы.
# Проверка: python3 environment.py

import random

APPROACHES = ("A", "B", "C")                                           # три подхода — три рычага
TITLE = {
    "A": "дописать тесты",
    "B": "рефакторинг легаси",
    "C": "парное программирование на ревью",
}

OBS = (0, 1, 2)                                                        # вознаграждение за спринт: 0, 1 или 2

PROBS = {                                                              # вероятности исходов; средние 0,3 / 0,8 / 1,3
    "A": (0.8, 0.1, 0.1),                                              # 0·0,8 + 1·0,1 + 2·0,1 = 0,3
    "B": (0.3, 0.6, 0.1),                                              # 0·0,3 + 1·0,6 + 2·0,1 = 0,8
    "C": (0.1, 0.5, 0.4),                                              # 0·0,1 + 1·0,5 + 2·0,4 = 1,3
}


def mean(act):                                                         # истинная средняя подхода (агенту не видна)
    return sum(k * p for k, p in zip(OBS, PROBS[act]))


def best():                                                            # лучший подход по истинным средним
    return max(APPROACHES, key=mean)


class Bandit:                                                          # среда: три рычага, одно состояние

    def __init__(self, seed=None, rng=None):
        self.rng = rng if rng is not None else random.Random(seed)
        self.t = 0                                                     # сколько спринтов провели

    def reset(self):
        self.t = 0
        return 0                                                       # состояние одно — всегда оно

    def step(self, act):                                               # провести спринт подходом act
        self.t += 1
        return self.rng.choices(OBS, weights=PROBS[act])[0]

    def sample_mean(self, act, steps, seed=None):                      # средний доход подхода за steps шагов
        rng = random.Random(seed)
        got = [rng.choices(OBS, weights=PROBS[act])[0] for _ in range(steps)]
        return round(sum(got) / steps, 3)


def checks():                                                          # что проверяет у себя
    out = []

    for act in APPROACHES:
        row = PROBS[act]
        out.append((abs(sum(row) - 1.0) < 1e-12,
                    "строка %s даёт единицу (%.1f + %.1f + %.1f)" % (act, *row)))
    out.append((all(round(mean(a), 10) == m for a, m in zip(APPROACHES, (0.3, 0.8, 1.3))),
                "истинные средние: A = 0,3 · B = 0,8 · C = 1,3"))
    out.append((best() == "C", "лучший подход по истинным средним — C (1,3)"))

    env = Bandit(seed=7)
    draws = [env.step("B") for _ in range(10)]
    out.append((all(d in OBS for d in draws),
                "выборка по B (seed = 7): только наблюдения 0/1/2 — %s" % draws))

    got = Bandit().sample_mean("C", 1000, seed=3)
    out.append((abs(got - 1.3) < 0.1,
                "1000 спринтов по C (seed = 3): среднее %s ≈ 1,3" % got))

    return out


def self_check(verbose=True):                                          # среда проверяет себя: python3 environment.py
    result = checks()
    if verbose:
        for ok, text in result:
            print("   [%s] среда: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


if __name__ == "__main__":
    print("Среда: многорукий бандит — три подхода, состояние одно, награда сразу")
    print("\nПодходы:")
    for act in APPROACHES:
        print("   %s «%s» — истинная средняя %.1f" % (act, TITLE[act], mean(act)))
    print("\nРаспределения (вероятности наблюдений 0 / 1 / 2):")
    for act in APPROACHES:
        print("   %s: %.1f / %.1f / %.1f" % (act, *PROBS[act]))

    print("\nПроверки среды:")
    ok = self_check()
    print("\nитог: все проверки среды сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
