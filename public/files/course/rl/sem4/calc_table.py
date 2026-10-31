#!/usr/bin/env python3
"""calc_table.py — таблица для лабораторной 2: считает по ВАШЕМУ коду.

Что делает: гоняет вашу среду и вашего агента по многим сидам и для каждой стратегии
печатает три числа распределения — доход за спринт, долю выборов текущего лучшего
и перекос счётчиков — медиану, IQR (первый и третий квартиль) и разброс.
Пишет сырые прогоны в CSV и строки в run_log.jsonl (те самые поля, что требует ТЗ).

Запуск (из папки, где лежат ваши agent.py, environment.py, run.py):
    python3 calc_table.py
    python3 calc_table.py --seeds 240 --sigma 0.05 --csv table.csv --log run_log.jsonl

Если ваш код лежит в другой папке:
    python3 calc_table.py --code путь/к/папке

Что считать «своими» числами: медиана и IQR по сидам. Один прогон ничего не доказывает —
минимум 100 сидов на точку таблицы (ТЗ, раздел 6).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from pathlib import Path


def load_code(code_dir: Path):
    """Подключить модули студента: agent.py, environment.py, run.py."""
    if not code_dir.is_dir():
        sys.exit("папка с кодом не найдена: %s" % code_dir)
    sys.path.insert(0, str(code_dir))
    try:
        import run as R  # noqa: E402
    except Exception as exc:  # noqa: BLE001
        sys.exit("не удалось импортировать run.py из %s: %s" % (code_dir, exc))
    return R


class Oracle:
    """Стратегия «всегда текущий лучший» — верхняя граница дохода в движущемся мире."""

    def __init__(self, env):
        self.env = env
        self.n = {}

    def act(self):
        return self.env.best()

    def update(self, act, reward):
        self.n[act] = self.n.get(act, 0) + 1


def one_run(R, kwargs, steps, seed, sigma, oracle=False):
    """Один прогон: доход, доля текущего лучшего, перекос счётчиков."""
    env = R.Bandit(seed=seed, sigma=sigma)
    agent = Oracle(env) if oracle else R.Agent(env, seed=seed, **kwargs)
    rewards, acts = [], []
    for _ in range(steps):
        act = agent.act()
        reward = env.step(act)
        agent.update(act, reward)
        rewards.append(reward)
        acts.append(act)
    hits = sum(1 for t, act in enumerate(acts) if act == env.log_best(t))
    counts = [agent.n.get(a, 0) for a in R.APPROACHES]
    return {
        "income": sum(rewards) / len(rewards),
        "share": 100.0 * hits / len(acts),
        "skew": max(counts) / max(1, min(counts)),
    }


def quartiles(values):
    """Медиана, квартили, среднее, разброс, минимум и максимум."""
    ordered = sorted(values)
    if len(ordered) < 2:
        return {"median": ordered[0], "q1": ordered[0], "q3": ordered[0],
                "mean": ordered[0], "min": ordered[0], "max": ordered[0]}
    q1, _, q3 = statistics.quantiles(ordered, n=4)
    return {
        "median": statistics.median(ordered),
        "q1": q1,
        "q3": q3,
        "mean": sum(ordered) / len(ordered),
        "min": ordered[0],
        "max": ordered[-1],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="таблица лабораторной 2 по вашему коду")
    here = Path(__file__).resolve().parent
    ap.add_argument("--code", default=str(here), help="папка с agent.py, environment.py, run.py")
    ap.add_argument("--seeds", type=int, default=100, help="сколько сидов на точку (минимум 100)")
    ap.add_argument("--seed-from", type=int, default=1, help="первый сид")
    ap.add_argument("--steps", type=int, default=1000, help="сколько спринтов в прогоне")
    ap.add_argument("--sigma", type=float, default=0.05, help="скорость дрейфа средних")
    ap.add_argument("--csv", default=None, help="куда записать сырые прогоны (CSV)")
    ap.add_argument("--log", default=None, help="куда дописать строки run_log.jsonl")
    ap.add_argument("--with-oracle", action="store_true", help="добавить оракула (потолок дохода)")
    ap.add_argument("--allow-empty", action="store_true", help="считать даже с незаполненными пропусками")
    args = ap.parse_args()

    code_dir = Path(args.code).resolve()
    R = load_code(code_dir)

    # Пропуски не заполнены — числа бессмысленны, предупреждаем и останавливаемся.
    if hasattr(R, "env_is_stub") and hasattr(R, "update_is_stub") and not args.allow_empty:
        problems = []
        if R.env_is_stub():
            problems.append("ПРОПУСК 1 — среда стоит: σ ни на что не влияет")
        if R.update_is_stub():
            problems.append("ПРОПУСК 2 — оценки q не двигаются")
        if problems:
            print("ВНИМАНИЕ: не заполнено — " + "; ".join(problems))
            print("Сначала заполните пропуски (см. руководство на портале), потом считайте таблицу.")
            print("Посмотреть полный список мест — python3 run.py")
            return 2

    configs = [
        ("жадная · 1/n", dict(mode="greedy"), False),
        ("ε-жадная 0,1 · 1/n", dict(mode="eps", epsilon=0.1), False),
        ("ε-жадная 0,1 · α 0,1", dict(mode="eps", epsilon=0.1, alpha=0.1), False),
        ("ε-жадная 0,1 · α 0,3", dict(mode="eps", epsilon=0.1, alpha=0.3), False),
        ("UCB c = 2 · 1/n", dict(mode="ucb", c=2.0), False),
        ("UCB c = 2 · α 0,1", dict(mode="ucb", c=2.0, alpha=0.1), False),
        ("градиентная h 0,1", dict(mode="gradient", h_alpha=0.1), False),
    ]
    if args.with_oracle:
        configs.append(("оракул: всегда текущий лучший", dict(), True))

    seeds = list(range(args.seed_from, args.seed_from + args.seeds))
    rows = []
    summary = []
    for name, kwargs, oracle in configs:
        incomes, shares, skews = [], [], []
        for seed in seeds:
            row = one_run(R, kwargs, args.steps, seed, args.sigma, oracle=oracle)
            incomes.append(row["income"])
            shares.append(row["share"])
            skews.append(row["skew"])
            rows.append({"strategy": name, "seed": seed, "sigma": args.sigma,
                         "steps": args.steps, "income": row["income"],
                         "share_best": row["share"], "skew": row["skew"]})
        summary.append((name, quartiles(incomes), quartiles(shares), quartiles(skews)))

    print("%d сидов (с %d по %d) × %d спринтов, σ = %s\n"
          % (args.seeds, seeds[0], seeds[-1], args.steps, args.sigma))
    print("| Стратегия | Доход: медиана [IQR] | Доля лучшего: медиана [IQR], разброс | Перекос n (медиана) |")
    print("| --- | --- | --- | --- |")
    for name, inc, share, skew in summary:
        print("| %s | %.2f [%.2f–%.2f] | %.0f%% [%.0f–%.0f], %d–%d | %.1f |"
              % (name, inc["median"], inc["q1"], inc["q3"],
                 share["median"], share["q1"], share["q3"],
                 round(share["min"]), round(share["max"]), skew["median"]))

    print("\nсредние по сидам (для сверки с планом):")
    for name, inc, share, _ in summary:
        print("   %-24s доход %.2f ± %.2f   доля %.0f%% ± %.0f"
              % (name, inc["mean"], (inc["q3"] - inc["q1"]) / 2,
                 share["mean"], (share["q3"] - share["q1"]) / 2))

    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print("\nсырые прогоны: %s (%d строк)" % (args.csv, len(rows)))

    if args.log:
        command = "python3 %s --seeds %d --seed-from %d --steps %d --sigma %s" % (
            os.path.basename(__file__), args.seeds, args.seed_from, args.steps, args.sigma)
        with open(args.log, "a", encoding="utf-8") as fh:
            for name, inc, share, skew in summary:
                for metric, stats in (("income", inc), ("share_best", share), ("skew", skew)):
                    fh.write(json.dumps({
                        "n_runs": args.seeds,
                        "seed_from": seeds[0],
                        "seed_to": seeds[-1],
                        "metric": "%s:%s:median[%.4f..%.4f]" % (
                            name, metric, stats["q1"], stats["q3"]),
                        "command": command,
                    }, ensure_ascii=False) + "\n")
        print("строки лога дописаны: %s" % args.log)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
