# tournament.py — турнир стратегий, практика 5, 06.11.2026.
#
# Запуск:   python3 tournament.py --config <1..10|all> --world <1|2|3>
#
# Первая проверка (должно выйти ровно так):
#   python3 tournament.py --config 6 --world 1
#   конфиг  6 (    UCB c2 · 1/n) | доля лучшего    67% [  66– 68] | ...
#
# Сид мира вшит в скрипт: один конфиг на одном мире даёт одни и те же цифры. Скрипт не редактируем.


import argparse
import sys
import time

import numpy as np

ARMS = 5                                    # количество рычагов
MU0 = np.array([0.3, 0.7, 1.1, 1.5, 1.9])   # стартовые средние
LO, HI = 0.1, 1.9                           # границы, в которых живут средние
WORLD_SIGMA = 0.05                          # размах шага дрейфа
WORLD_SEED_BASE = 777                       # сид мира = база + номер мира

STEPS = 1000                                # спринтов в прогоне
AGENT_SEEDS = 30                            # сидов агента на конфиг-мир
REWARD_SIGMA = 0.3                          # шум награды
AGENT_SEED_BASE = 50_000                    # база сидов агента

# меню драфта: стратегия и значения ручек; порядок не по силе
CONFIGS = {
    1:  ("eps",      {"eps": 0.05, "alpha": 0.10}),
    2:  ("ucb",      {"c": 4.0, "rule": "1/n"}),
    3:  ("gradient", {"eta": 0.05}),
    4:  ("eps",      {"eps": 0.20, "rule": "1/n"}),
    5:  ("ucb",      {"c": 1.0, "alpha": 0.10}),
    6:  ("ucb",      {"c": 2.0, "rule": "1/n"}),
    7:  ("greedy",   {"rule": "1/n"}),
    8:  ("gradient", {"eta": 0.20}),
    9:  ("eps",      {"eps": 0.10, "alpha": 0.30}),
    10: ("eps",      {"eps": 0.02, "rule": "1/n"}),
}

NAMES = {
    1:  "eps 0.05 · α 0.1",
    2:  "UCB c4 · 1/n",
    3:  "gradient η 0.05",
    4:  "eps 0.2 · 1/n",
    5:  "UCB c1 · α 0.1",
    6:  "UCB c2 · 1/n",
    7:  "greedy",
    8:  "gradient η 0.2",
    9:  "eps 0.1 · α 0.3",
    10: "eps 0.02 · 1/n",
}


def world_drift(world: int) -> np.ndarray:
    # путь дрейфа мира: один и тот же для всех конфигов и всех команд
    rng = np.random.default_rng(WORLD_SEED_BASE + world)
    return rng.normal(0.0, WORLD_SIGMA, size=(STEPS, ARMS))


def run_episode(cfg_id: int, drift: np.ndarray, agent_seed: int):
    # один прогон: 1000 спринтов; возвращает (доход, доля лучшего, regret)
    kind, p = CONFIGS[cfg_id]
    rng = np.random.default_rng(agent_seed)
    mu = MU0.copy()
    q = np.zeros(ARMS)
    n = np.zeros(ARMS)
    H = np.zeros(ARMS)
    avg = 0.0
    total_r = 0.0
    best_cnt = 0
    total_regret = 0.0

    for step in range(STEPS):
        mu = np.clip(mu + drift[step], LO, HI)
        t = step + 1

        if kind == "greedy":
            a = int(np.argmax(q))
        elif kind == "eps":
            if rng.random() < p["eps"]:
                a = int(rng.integers(ARMS))
            else:
                a = int(np.argmax(q))
        elif kind == "ucb":
            if np.any(n == 0):
                a = int(np.argmax(n == 0))
            else:
                a = int(np.argmax(q + p["c"] * np.sqrt(np.log(t) / n)))
        else:  # gradient
            e = np.exp(H - H.max())
            prob = e / e.sum()
            a = int(rng.choice(ARMS, p=prob))

        r = float(rng.normal(mu[a], REWARD_SIGMA))
        total_r += r
        best = mu.max()
        total_regret += best - mu[a]
        if mu[a] >= best - 1e-12:
            best_cnt += 1

        if kind == "gradient":
            avg += (r - avg) / t
            grad = (np.arange(ARMS) == a).astype(float) - prob
            H += p["eta"] * (r - avg) * grad
        else:
            n[a] += 1
            if n[a] == 1:
                q[a] = r
            elif p.get("rule") == "1/n":
                q[a] += (r - q[a]) / n[a]
            else:
                q[a] += p["alpha"] * (r - q[a])

    return total_r / STEPS, best_cnt / STEPS, total_regret / STEPS


def spread(values):
    # медиана и коридор: сортировка и квартили
    m = float(np.percentile(values, 50))
    a = float(np.percentile(values, 25))
    b = float(np.percentile(values, 75))
    return (m, a, b)


def run_config(cfg_id: int, world: int):
    drift = world_drift(world)
    incomes, shares, regrets = [], [], []
    for i in range(AGENT_SEEDS):
        seed = AGENT_SEED_BASE + world * 10_000 + cfg_id * 100 + i
        inc, sh, rg = run_episode(cfg_id, drift, seed)
        incomes.append(inc)
        shares.append(sh)
        regrets.append(rg)
    return {
        "income": spread(incomes),
        "share":  spread(shares),
        "regret": spread(regrets),
    }


def fmt(cell, pct=False):
    m, a, b = cell
    if pct:
        return f"{m*100:5.0f}% [{a*100:4.0f}–{b*100:3.0f}]"
    return f"{m:5.2f} [{a:4.2f}–{b:4.2f}]"


def main():
    # на Windows-консоли без этого падают кириллица и «·»
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Турнир стратегий, практика 5")
    ap.add_argument("--config", required=True,
                    help="номер конфигурации 1..10 или all")
    ap.add_argument("--world", type=int, required=True, choices=[1, 2, 3],
                    help="мир (сид среды зафиксирован)")
    args = ap.parse_args()

    if args.config == "all":
        ids = list(CONFIGS)
    else:
        try:
            cid = int(args.config)
        except ValueError:
            ap.error("--config: нужно число 1..10 или all")
        if cid not in CONFIGS:
            ap.error("--config: такой конфигурации нет, есть 1..10 или all")
        ids = [cid]
    t0 = time.time()
    print(f"мир {args.world} · {AGENT_SEEDS} сидов агента × {STEPS} спринтов")
    for cid in ids:
        res = run_config(cid, args.world)
        print(f"конфиг {cid:2d} ({NAMES[cid]:>16}) | "
              f"доля лучшего {fmt(res['share'], pct=True)} | "
              f"доход {fmt(res['income'])} | regret {fmt(res['regret'])}")
    print(f"считалось {time.time() - t0:.1f} с")


if __name__ == "__main__":
    main()
