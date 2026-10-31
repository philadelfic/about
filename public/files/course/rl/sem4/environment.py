# environment.py — среда: три подхода, средние дрейфуют (нестационарный мир).
# В этом файле один пропуск — ПРОПУСК 1: шаг блуждания в Bandit.step().
# Куски — в snippets.py (группа 1). Проверка: python3 environment.py

import random

APPROACHES = ("A", "B", "C")                                           # три подхода — три рычага
TITLE = {
    "A": "дописать тесты",
    "B": "рефакторинг легаси",
    "C": "парное программирование на ревью",
}

OBS = (0, 1, 2)                                                        # вознаграждение за спринт: 0, 1 или 2

MU0 = {"A": 0.3, "B": 0.8, "C": 1.3}                                   # стартовые средние (агенту не видны)
SIGMA = 0.05                                                           # шаг блуждания: насколько сдвигается среднее за спринт
LO, HI = 0.1, 1.9                                                      # границы, за которые средние не уходят


def probs_from_mean(m):                                                # среднее → вероятности наблюдений 0 / 1 / 2
    m = min(max(m, LO), HI)                                            # кусочно-линейно: m < 1 тянет к нулю,
    if m < 1.0:                                                       # m > 1 — к двойке, остальное — единица
        return (1.0 - m, m, 0.0)
    if m > 1.0:
        return (0.0, 2.0 - m, m - 1.0)
    return (0.0, 1.0, 0.0)


def mean_from_probs(p):                                                # обратная операция: среднее из вероятностей
    return sum(k * q for k, q in zip(OBS, p))


def mean(act):                                                         # стартовое среднее подхода (агенту не видно)
    return mean_from_probs(probs_from_mean(MU0[act]))


def best(mu=None):                                                     # лучший подход по средним; при равенстве — первый
    mu = MU0 if mu is None else mu
    return max(APPROACHES, key=lambda a: mu[a])


class Bandit:                                                          # среда: три рычага, одно состояние, средние гуляют

    def __init__(self, seed=None, rng=None, sigma=SIGMA, mu0=None):
        self.rng = rng if rng is not None else random.Random(seed)
        self.sigma = sigma                                             # своё σ — для исследования в лабе
        self.mu0 = dict(MU0 if mu0 is None else mu0)
        self.reset()

    def reset(self):
        self.t = 0                                                     # сколько спринтов провели
        self.mu = dict(self.mu0)                                       # текущие средние рычагов
        self.mu_log = []                                               # история: log[t−1] — те μ, из которых снята награда
        return 0                                                       # состояние одно — всегда оно

    def best(self):                                                    # текущий лучший — по μ прямо сейчас
        return best(self.mu)

    def step(self, act):                                               # провести спринт подходом act
        self.t += 1
        reward = self.rng.choices(OBS, weights=probs_from_mean(self.mu[act]))[0]
        self.mu_log.append(tuple(self.mu[a] for a in APPROACHES))      # 1) записали μ, из которых сняли награду
        # 2) только теперь сдвигаем мир.
        # ← ПРОПУСК 1: сдвиньте среднее КАЖДОГО подхода на случайную величину
        #    и удержите его в границах LO..HI. Куски — в snippets.py, группа 1.
        #    Выбрали кусок — впишите его здесь двумя-тремя строками и объясните выбор на разборе.
        return reward

    def log_best(self, t):                                             # лучший на шаге t по записанной истории
        row = self.mu_log[t]
        return max(APPROACHES, key=lambda a: row[APPROACHES.index(a)])


def checks():                                                          # что проверяет у себя
    out = []

    for m in (0.1, 0.3, 0.8, 0.99, 1.0, 1.3, 1.9):
        p = probs_from_mean(m)
        out.append((abs(sum(p) - 1.0) < 1e-12,
                    "среднее %.2f даёт вероятности с суммой 1 (%s)" % (m, ", ".join("%.2f" % x for x in p))))
        out.append((abs(mean_from_probs(p) - m) < 1e-12,
                    "среднее %.2f восстанавливается из вероятностей" % m))

    env = Bandit(seed=7)
    draws = [env.step("B") for _ in range(10)]
    out.append((all(d in OBS for d in draws),
                "выборка по B (seed = 7): только наблюдения 0/1/2 — %s" % draws))
    out.append((len(env.mu_log) == 10 and env.t == 10,
                "история средних растёт синхронно со спринтами: %d записей" % len(env.mu_log)))

    env = Bandit(seed=7)
    env.step("C")
    logged = env.mu_log[0]
    out.append((abs(mean_from_probs(probs_from_mean(logged[2])) - 1.3) < 1e-12,
                "в истории на первом шаге — среднее ДО дрейфа (C = 1,3, не сдвинутое)"))

    env = Bandit(seed=7)
    for _ in range(1000):
        env.step(env.best())
    inside = all(LO <= m <= HI for row in env.mu_log for m in row)
    out.append((inside, "за 1000 спринтов средние не вышли из границ %.1f–%.1f" % (LO, HI)))
    out.append((abs(env.mu["A"] - MU0["A"]) < 1.0,
                "через 1000 спринтов A ушёл от старта, но остался в границах: %.2f" % env.mu["A"]))

    env = Bandit(seed=7)
    for _ in range(20):
        env.step("B")
    out.append((len(set(env.mu_log)) > 1,
                "средние сдвигаются от спринта к спринту (ПРОПУСК 1 заполнен)"))

    out.append((best() == "C", "лучший подход на старте — C (1,3)"))

    return out


def self_check(verbose=True):                                          # среда проверяет себя: python3 environment.py
    result = checks()
    if verbose:
        for ok, text in result:
            print("   [%s] среда: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


if __name__ == "__main__":
    print("Среда: многорукий бандит в движущемся мире — средние дрейфуют каждый спринт")
    print("\nПодходы и стартовые средние:")
    for act in APPROACHES:
        print("   %s «%s» — старт %.1f" % (act, TITLE[act], mean(act)))
    print("\nБлуждание: μ ← clip(μ + N(0; %.2f), %.1f; %.1f)" % (SIGMA, LO, HI))

    print("\nПроверки среды:")
    ok = self_check()
    print("\nитог: все проверки среды сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
