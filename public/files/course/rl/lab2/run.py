import argparse
import json
import os
import sys

from agent import Agent
from environment import CHANNELS, SIGMA, Bandit
from metrics import best_share, cell, income, regret, spread

TURNS = 1000
SEED = 7
AGENT_SEED = 100000

STRATEGIES = (
    ("жадная", dict(mode="greedy")),
    ("ε-жадная 0,1 / 1n", dict(mode="eps", epsilon=0.1)),
    ("ε-жадная 0,1 / α0,1", dict(mode="eps", epsilon=0.1, alpha=0.1)),
    ("UCB c2 / 1n", dict(mode="ucb", c=2.0)),
    ("UCB c2 / α0,1", dict(mode="ucb", c=2.0, alpha=0.1)),
    ("градиентная η0,1", dict(mode="gradient", eta=0.1)),
)


def one(kwargs, turns=TURNS, seed=SEED, sigma=SIGMA):
    env = Bandit(seed=seed, sigma=sigma)
    agent = Agent(seed=seed + AGENT_SEED, **kwargs)
    rewards = []
    actions = []
    for _ in range(turns):
        channel = agent.choose()
        reward = env.pull(channel)
        agent.update(channel, reward)
        rewards.append(reward)
        actions.append(channel)
    return {
        "income": income(rewards),
        "share": best_share(actions, env.history),
        "regret": regret(env.history, actions),
        "counts": [agent.n[c] for c in CHANNELS],
        "rewards": rewards,
        "actions": actions,
        "history": env.history,
    }


def series(kwargs, seeds, turns, sigma, offset=0):
    runs = [one(kwargs, turns=turns, seed=s, sigma=sigma)
            for s in range(1 + offset, 1 + offset + seeds)]
    return {
        "income": [r["income"] for r in runs],
        "share": [r["share"] for r in runs],
        "regret": [r["regret"] for r in runs],
    }


def summarize(data):
    return {
        "income": spread(data["income"]),
        "share": spread(data["share"]),
        "regret": spread(data["regret"]),
    }


def show_income(value):
    return "%.2f [%.2f–%.2f]" % value


def show_share(value):
    return cell(*value)


def table(seeds, turns, sigma, offset=0, strategies=STRATEGIES):
    print("\n%d сидов × %d шагов, σ = %.2f, сиды %d–%d"
          % (seeds, turns, sigma, 1 + offset, seeds + offset))
    print("   %-20s %20s %24s %18s" % ("стратегия", "доход", "доля лучшего", "regret"))
    rows = []
    for name, params in strategies:
        cells = summarize(series(params, seeds, turns, sigma, offset))
        rows.append((name, params, cells))
        print("   %-20s %20s %24s %18s" % (
            name, show_income(cells["income"]), show_share(cells["share"]),
            show_income(cells["regret"])))
    return rows


def study_rules(sigmas, seeds, turns, offset=0):
    print("\n1/n против α по скорости дрейфа, %d сидов × %d шагов" % (seeds, turns))
    print("   %-6s %24s %24s %10s" % ("σ", "ε-жадная 1/n", "ε-жадная α0,1", "разрыв"))
    rows = []
    for sigma in sigmas:
        plain = summarize(series(dict(mode="eps", epsilon=0.1), seeds, turns, sigma, offset))
        step = summarize(series(dict(mode="eps", epsilon=0.1, alpha=0.1), seeds, turns, sigma, offset))
        gap = step["share"][0] - plain["share"][0]
        rows.append(("σ = %.2f · 1/n" % sigma, dict(mode="eps", epsilon=0.1, sigma=sigma), plain))
        rows.append(("σ = %.2f · α0,1" % sigma, dict(mode="eps", epsilon=0.1, alpha=0.1, sigma=sigma), step))
        print("   %-6.2f %24s %24s %+10.0f" % (sigma, show_share(plain["share"]),
                                               show_share(step["share"]), 100 * gap))
    return rows


def study_eps(values, seeds, turns, sigma, offset=0):
    print("\nдоля исследования ε, %d сидов × %d шагов, σ = %.2f" % (seeds, turns, sigma))
    print("   %-6s %24s %18s" % ("ε", "доля лучшего", "regret"))
    rows = []
    for eps in values:
        cells = summarize(series(dict(mode="eps", epsilon=eps), seeds, turns, sigma, offset))
        rows.append(("ε-жадная %.2f" % eps, dict(mode="eps", epsilon=eps), cells))
        print("   %-6.2f %24s %18s" % (eps, show_share(cells["share"]),
                                       show_income(cells["regret"])))
    return rows


def study_ucb(values, seeds, turns, sigma, offset=0):
    print("\nцена и ширина доверия c, %d сидов × %d шагов, σ = %.2f" % (seeds, turns, sigma))
    print("   %-6s %24s %18s" % ("c", "доля лучшего", "regret"))
    rows = []
    for c in values:
        cells = summarize(series(dict(mode="ucb", c=c), seeds, turns, sigma, offset))
        rows.append(("UCB c%.1f" % c, dict(mode="ucb", c=c), cells))
        print("   %-6.2f %24s %18s" % (c, show_share(cells["share"]),
                                       show_income(cells["regret"])))
    return rows


def study_eta(values, seeds, turns, sigma, offset=0):
    print("\nшаг предпочтений η, %d сидов × %d шагов, σ = %.2f" % (seeds, turns, sigma))
    print("   %-6s %24s %18s" % ("η", "доля лучшего", "regret"))
    rows = []
    for eta in values:
        cells = summarize(series(dict(mode="gradient", eta=eta), seeds, turns, sigma, offset))
        rows.append(("градиентная η%.2f" % eta, dict(mode="gradient", eta=eta), cells))
        print("   %-6.3f %24s %18s" % (eta, show_share(cells["share"]),
                                       show_income(cells["regret"])))
    return rows


def write_log(path, command, rows, seeds, offset, turns, sigma):
    with open(path, "a", encoding="utf-8") as fh:
        for name, params, cells in rows:
            for metric in ("income", "share", "regret"):
                median, q1, q3 = cells[metric]
                fh.write(json.dumps({
                    "n_runs": seeds,
                    "seed_from": 1 + offset,
                    "seed_to": seeds + offset,
                    "turns": turns,
                    "sigma": params.get("sigma", sigma),
                    "metric": metric,
                    "command": command,
                    "strategy": name,
                    "params": params,
                    "median": round(median, 6),
                    "q1": round(q1, 6),
                    "q3": round(q3, 6),
                }, ensure_ascii=False) + "\n")


def show(name, run):
    print("\n%s" % name)
    print("   доход за шаг      %.3f" % run["income"])
    print("   доля лучшего      %.0f%%" % (100 * run["share"]))
    print("   regret за шаг     %.3f" % run["regret"])
    print("   выборы каналов    %s" % " / ".join(str(n) for n in run["counts"]))


def pick(name):
    for label, params in STRATEGIES:
        if label == name:
            return params
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--turns", type=int, default=TURNS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--sigma", type=float, default=SIGMA)
    parser.add_argument("--strategy", default=None)
    parser.add_argument("--study", default=None,
                        choices=("strategies", "rules", "eps", "ucb", "eta", "all"))
    parser.add_argument("--log", default=None)
    args = parser.parse_args()

    if args.turns < 2:
        print("шагов должно быть не меньше двух: --turns %d" % args.turns)
        sys.exit(1)
    if args.seeds == 1:
        print("для медианы и IQR нужно больше одного сида: --seeds 1 не годится")
        sys.exit(1)

    command = "python3 run.py " + " ".join(sys.argv[1:]).strip()
    if args.log:
        open(args.log, "w", encoding="utf-8").close()

    if args.study:
        seeds = args.seeds or 100
        if args.study in ("strategies", "all"):
            rows = table(seeds, args.turns, args.sigma, args.offset)
            if args.log:
                write_log(args.log, command, rows, seeds, args.offset, args.turns, args.sigma)
        if args.study in ("rules", "all"):
            rows = study_rules((0.0, 0.01, 0.05, 0.2, 0.5), seeds, args.turns, args.offset)
            if args.log:
                write_log(args.log, command, rows, seeds, args.offset, args.turns, args.sigma)
        if args.study in ("eps", "all"):
            rows = study_eps((0.01, 0.05, 0.1, 0.3), seeds, args.turns, args.sigma, args.offset)
            if args.log:
                write_log(args.log, command, rows, seeds, args.offset, args.turns, args.sigma)
        if args.study in ("ucb", "all"):
            rows = study_ucb((0.5, 1.0, 2.0, 4.0), seeds, args.turns, args.sigma, args.offset)
            if args.log:
                write_log(args.log, command, rows, seeds, args.offset, args.turns, args.sigma)
        if args.study in ("eta", "all"):
            rows = study_eta((0.01, 0.05, 0.1, 0.3), seeds, args.turns, args.sigma, args.offset)
            if args.log:
                write_log(args.log, command, rows, seeds, args.offset, args.turns, args.sigma)
        return

    if args.strategy:
        params = pick(args.strategy)
        if params is None:
            print("нет такой стратегии: %s" % args.strategy)
            print("есть: %s" % ", ".join(label for label, _ in STRATEGIES))
            sys.exit(1)
        show(args.strategy, one(params, turns=args.turns, seed=args.seed, sigma=args.sigma))
        return

    if args.seeds:
        rows = table(args.seeds, args.turns, args.sigma, args.offset)
        if args.log:
            write_log(args.log, command, rows, args.seeds, args.offset, args.turns, args.sigma)
        return

    for name, params in STRATEGIES:
        show(name, one(params, turns=args.turns, seed=args.seed, sigma=args.sigma))


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        print("\nне заполнено: %s" % exc)
        print("допишите четыре места в environment.py и agent.py, потом запустите python3 check.py")
        sys.exit(1)
