# environment.py — среда: три подхода, средние дрейфуют (нестационарный мир).
# В этом файле один пропуск — ПРОПУСК 1: шаг блуждания в Bandit.step().
# Куски — в snippets.py (группа 1). Проверка: python3 environment.py

import random
import sys

APPROACHES = ("A", "B", "C")
TITLE = {
    "A": "дописать тесты",
    "B": "рефакторинг легаси",
    "C": "парное программирование на ревью",
}

OBS = (0, 1, 2)                # вознаграждение за спринт: 0, 1 или 2

MU0 = {"A": 0.3, "B": 0.8, "C": 1.3}     # стартовые средние; агенту они не видны
SIGMA = 0.05                             # насколько сдвигается среднее за спринт
LO, HI = 0.1, 1.9                        # границы, за которые средние не уходят


def probs_from_mean(m):
    # среднее → вероятности наблюдений 0 / 1 / 2: вес перетекает от середины к краям
    m = min(max(m, LO), HI)
    if m < 1.0:
        return (1.0 - m, m, 0.0)
    if m > 1.0:
        return (0.0, 2.0 - m, m - 1.0)
    return (0.0, 1.0, 0.0)


def mean_from_probs(p):
    # обратная операция: среднее из вероятностей
    return sum(k * q for k, q in zip(OBS, p))


def mean(act):
    return mean_from_probs(probs_from_mean(MU0[act]))


def best(mu=None):
    # лучший подход по средним; при равенстве — первый по порядку
    mu = MU0 if mu is None else mu
    return max(APPROACHES, key=lambda a: mu[a])


class Bandit:

    def __init__(self, seed=None, rng=None, sigma=SIGMA, mu0=None):
        self.rng = rng if rng is not None else random.Random(seed)
        self.sigma = sigma             # своё σ — для исследования в лабе
        self.mu0 = dict(MU0 if mu0 is None else mu0)
        self.reset()

    def reset(self):
        self.t = 0
        self.mu = dict(self.mu0)
        self.mu_log = []               # log[t−1] — те μ, из которых снята награда
        return 0                       # состояние одно — всегда оно

    def best(self):
        return best(self.mu)

    def step(self, act):
        self.t += 1
        reward = self.rng.choices(OBS, weights=probs_from_mean(self.mu[act]))[0]
        # сначала записываем μ, из которых сняли награду, и только потом сдвигаем мир
        self.mu_log.append(tuple(self.mu[a] for a in APPROACHES))
        # ← ПРОПУСК 1: сдвиньте среднее КАЖДОГО подхода на случайную величину
        #    и удержите его в границах LO..HI. Куски — в snippets.py, группа 1.
        #    Выбрали кусок — впишите его здесь двумя-тремя строками и объясните выбор на разборе.
        return reward

    def log_best(self, t):
        # лучший на шаге t по записанной истории
        row = self.mu_log[t]
        return max(APPROACHES, key=lambda a: row[APPROACHES.index(a)])


def drift_size(sigma, seed=7, sprints=200):
    # средний сдвиг среднего за спринт — мера того, насколько бурный мир
    env = Bandit(seed=seed, sigma=sigma)
    total = 0.0
    for _ in range(sprints):
        before = dict(env.mu)
        env.step("B")
        total += sum(abs(env.mu[a] - before[a]) for a in APPROACHES)
    return total / (sprints * len(APPROACHES))


def checks():
    out = []

    for m in (0.1, 0.8, 1.0, 1.9):
        p = probs_from_mean(m)
        ok = abs(sum(p) - 1.0) < 1e-12 and abs(mean_from_probs(p) - m) < 1e-12
        out.append((ok, "среднее %.1f: вероятности в сумме 1 и среднее восстанавливается (%s)"
                    % (m, ", ".join("%.2f" % x for x in p))))

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
    out.append((abs(env.mu["A"] - MU0["A"]) > 0.01,
                "через 1000 спринтов A ушёл от старта: %.2f (старт %.1f)" % (env.mu["A"], MU0["A"])))

    # дальше — три проверки на саму физику дрейфа
    env = Bandit(seed=7)
    for _ in range(20):
        env.step("B")
    out.append((len(set(env.mu_log)) > 1,
                "средние сдвигаются от спринта к спринту (ПРОПУСК 1 заполнен)"))

    a, b = Bandit(seed=7), Bandit(seed=7)
    for _ in range(200):
        a.step("B")
        b.step("B")
    out.append((a.mu_log == b.mu_log and len(set(a.mu_log)) > 1,
                "один и тот же seed даёт ту же историю средних (дрейф идёт через self.rng)"))

    slow, fast = drift_size(0.05), drift_size(0.5)
    out.append((fast > 3 * slow,
                "σ задаёт размах дрейфа: средний сдвиг %.3f при σ = 0,05 и %.3f при σ = 0,5"
                % (slow, fast)))

    out.append((best() == "C", "лучший подход на старте — C (1,3)"))

    return out


def self_check(verbose=True):
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
    sys.exit(0 if ok else 1)       # код возврата: 0 — сошлось, 1 — есть [нет]
