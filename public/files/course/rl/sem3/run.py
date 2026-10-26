# run.py — прогон: 1000 спринтов, сравнение стратегий, графики.
# python3 run.py [--png] [--exp [--strategy ИМЯ]] [--trace B=1,0,2] [--alpha 0.5]

import argparse
import os
import random
import sys

from agent import Agent
from environment import APPROACHES, Bandit, best, mean

STEPS = 1000                                                           # сколько спринтов гоним одну стратегию
SEED = 7                                                               # один seed — один и тот же год

STRATEGIES = (                                                         # пять стратегий: имя → настройки агента
    ("жадная",        dict(mode="greedy")),
    ("ε-жадная 0,1",  dict(mode="eps", epsilon=0.1)),
    ("оптимист. 5",   dict(mode="optimistic", q0=5.0)),
    ("UCB c = 2",     dict(mode="ucb", c=2.0)),
    ("градиентная",   dict(mode="gradient", h_alpha=0.1)),
)

# Меняете число ниже — запускаете — смотрите, как меняется процесс обучения:
#
#     python3 run.py --exp         # картинка experiment.png рядом с этим файлом
#     python3 run.py --exp --show  # то же, но сразу открыть окно с графиком
#
# На картинке три кривых по ходу спринтов:
#     1. средний доход (окно 50) — как быстро стратегия ползёт к потолку 1,3;
#     2. оценки Q рычагов — сходятся ли к 0,3 / 0,8 / 1,3 (пунктир — истина);
#     3. доли выбора рычагов (окно 50) — к чему прижимается стратегия.
#
# Задания — меняйте по одному параметру, остальное не трогайте:
#   1. EXP_MODE = "greedy" и разные EXP_SEED (3, 42, 100): где застряла
#      жадная? почему у всех один и тот же рычаг?
#   2. EXP_EPSILON = 0,01 и 0,5 (режим eps): что стало с долями выбора C?
#      почему маленькое ε тоже плохо? (сравните кривые с ε = 0,1)
#   3. EXP_C = 0,5 и 4 (режим ucb): как масштаб бонуса меняет разведку?
#   4. EXP_ALPHA = 0,9 и 0,01 (режим eps): что происходит с оценками Q
#      на средней кривой? как это связано с нестационарностью?

EXP_MODE = "eps"                                                       # стратегия: greedy | eps | optimistic | ucb | gradient
EXP_SEED = 7                                                           # другой seed — другая случайность
EXP_EPSILON = 0.1                                                      # доля шагов наугад (только для eps)
EXP_C = 2.0                                                            # масштаб бонуса неуверенности (только для ucb)
EXP_Q0 = 5.0                                                           # стартовая оценка (optimistic; 5 — завышена)
EXP_ALPHA = None                                                       # шаг оценки: None — 1/n, число — α
EXP_H_ALPHA = 0.1                                                      # шаг предпочтений (только для gradient)
EXP_STEPS = 1000                                                       # сколько спринтов гоним

STRATEGY_ALIASES = {                                                   # алиасы: имя в зале → EXP_MODE
    "жадная": "greedy",
    "ε-жадная": "eps",
    "eps": "eps",
    "оптимистичная": "optimistic",
    "оптимист": "optimistic",
    "UCB": "ucb",
    "ucb": "ucb",
    "градиентная": "gradient",
    "gradient": "gradient",
}
NAMES = ("жадная", "ε-жадная", "оптимистичная", "UCB", "градиентная")  # как зовём в зале


def experiment():                                                      # один прогон стратегии: журнал по шагам
    kwargs = dict(mode=EXP_MODE, seed=EXP_SEED)
    if EXP_MODE == "eps":
        kwargs["epsilon"] = EXP_EPSILON
    if EXP_MODE == "ucb":
        kwargs["c"] = EXP_C
    if EXP_MODE == "optimistic":
        kwargs["q0"] = EXP_Q0
    if EXP_ALPHA is not None:
        kwargs["alpha"] = EXP_ALPHA
    if EXP_MODE == "gradient":
        kwargs["h_alpha"] = EXP_H_ALPHA
    env = Bandit(seed=EXP_SEED)
    agent = Agent(env, **kwargs)
    log = {"t": [], "act": [], "reward": [], "q": {a: [] for a in APPROACHES}}
    for t in range(1, EXP_STEPS + 1):
        act = agent.act()
        reward = env.step(act)
        agent.update(act, reward)
        log["t"].append(t)
        log["act"].append(act)
        log["reward"].append(reward)
        for a in APPROACHES:
            log["q"][a].append(agent.q[a])
    return log


def sliding(values, window):                                           # скользящее среднее — сглаживает шум
    return [sum(values[max(0, i - window):i + 1]) / len(values[max(0, i - window):i + 1])
            for i in range(len(values))]


def text_report(log, blocks=10):                                       # та же картина таблицей, без matplotlib
    n = len(log["t"])
    step = max(1, n // blocks)
    print("   сводка по шагам (без картинки):")
    print("   %5s %8s %8s %s" % ("шаг", "доход", "доля C", "Q: A / B / C"))
    for i in range(step - 1, n, step):
        lo = max(0, i - step + 1)
        chunk = log["reward"][lo:i + 1]
        acts = log["act"][lo:i + 1]
        share = 100.0 * sum(1 for a in acts if a == best()) / len(acts)
        q = " / ".join("%.2f" % log["q"][a][i] for a in APPROACHES)
        print("   %5d %8.2f %7.0f%% %s" % (log["t"][i], sum(chunk) / len(chunk), share, q))
    print("   истина: A = 0,3 · B = 0,8 · C = 1,3 (потолок — всегда C)")
    print("   доход — средний за последний блок шагов: он шумный, смотрите тренд, а не цифру")


def plot_experiment(log, path=None, show=False):                       # три кривых: доход, оценки Q, доли выбора
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    window = 50
    t = log["t"]
    fig, axes = plt.subplots(3, 1, figsize=(9.0, 11.0), sharex=True)

    axes[0].plot(t, sliding(log["reward"], window), linewidth=1.6, color="darkblue")
    axes[0].axhline(mean(best()), color="gray", linestyle="--", linewidth=1.2)
    axes[0].set_ylabel("средний доход (окно 50)")
    axes[0].set_title("1. доход: как быстро стратегия ползёт к потолку 1,3")

    for a in APPROACHES:
        axes[1].step(t, log["q"][a], where="post", label=a, linewidth=1.2)
        axes[1].axhline(mean(a), color="gray", linestyle=":", linewidth=0.9)
    axes[1].set_ylabel("оценки Q")
    axes[1].set_title("2. оценки Q: сходятся ли к 0,3 / 0,8 / 1,3? (пунктир — истина)")
    axes[1].legend(loc="center right")

    for a in APPROACHES:
        share = sliding([1.0 if x == a else 0.0 for x in log["act"]], window)
        axes[2].plot(t, share, label=a, linewidth=1.2)
    axes[2].set_ylabel("доля выбора (окно 50)")
    axes[2].set_xlabel("спринт (шаг t)")
    axes[2].set_title("3. доли выбора: к какому рычагу прижимается стратегия")
    axes[2].legend(loc="center right")

    fig.suptitle("Эксперимент: %s, seed = %d, шагов %d"
                 % (EXP_MODE, EXP_SEED, EXP_STEPS))
    plt.tight_layout(rect=(0, 0, 1, 0.97))
    if path:
        plt.savefig(path, dpi=150)
    if show:
        plt.show()
    plt.close()
    return path


def trace(arm="B", observations=(1, 0, 2), alpha=0.5):                 # ряд по шагам: 1/n и α
    a_mean = Agent(None, mode="greedy", alpha=None)
    a_step = Agent(None, mode="greedy", alpha=alpha)
    print("\nряд по подходу %s: %s   (считает тот же update(), что в файле)"
          % (arm, " → ".join(str(r) for r in observations)))
    print("   %4s %12s %4s %12s %14s"
          % ("шаг", "наблюдение", "n", "Q при 1/n", "Q при α = %.2f" % alpha))
    for i, reward in enumerate(observations, 1):
        a_mean.update(arm, reward)
        a_step.update(arm, reward)
        print("   %4d %12d %4d %12.3f %14.3f"
              % (i, reward, i, a_mean.q[arm], a_step.q[arm]))
    print("   первое наблюдение якорит оценку: Q := R1, дальше шаг = 1/n или α")


def series(mode_kwargs, steps=STEPS, seed=SEED):                       # один год: steps спринтов одной стратегией
    env = Bandit(seed=seed)
    agent = Agent(env, seed=seed, **mode_kwargs)
    rewards = []
    for _ in range(steps):
        act = agent.act()
        rewards.append(env.step(act))
        agent.update(act, rewards[-1])
    return rewards


def stats(rewards):                                                    # средний доход и доля лучшего
    avg = sum(rewards) / len(rewards)
    return avg, None                                                   # доля считается в compare()


def compare(steps=STEPS, seed=SEED, strategies=STRATEGIES):            # прогнать стратегии и собрать числа
    rows = []
    for name, kwargs in strategies:
        env = Bandit(seed=seed)
        agent = Agent(env, seed=seed, **kwargs)
        total, hits = 0, 0
        curve = []
        for t in range(1, steps + 1):
            act = agent.act()
            reward = env.step(act)
            agent.update(act, reward)
            total += reward
            hits += (act == best())
            curve.append(total / t)
        rows.append((name, total / steps, hits / steps, curve))
    return rows


def plot(path, steps=STEPS, seed=SEED):                                # картинка «1000 спринтов»: скользящее среднее
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 20, "axes.titlesize": 20, "axes.labelsize": 19,  # крупный шрифт, толстые линии
                         "legend.fontsize": 17, "xtick.labelsize": 16, "ytick.labelsize": 16})

    rows = compare(min(steps, 1000), seed, STRATEGIES[:4])             # градиентную на график не тянем
    window = 50
    plt.figure(figsize=(11.0, 5.6))
    for name, _, _, curve in rows:
        smooth = [sum(curve[max(0, i - window):i + 1]) / len(curve[max(0, i - window):i + 1])
                  for i in range(len(curve))]
        plt.plot(range(1, len(smooth) + 1), smooth, label=name, linewidth=4.0)
    plt.axhline(mean(best()), color="gray", linestyle="--", linewidth=3.0,
                label="потолок: C = 1,3")
    plt.xlabel("спринт (шаг t)")
    plt.ylabel("средний доход за спринт")
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def report(steps=STEPS, seed=SEED, numbers=True):                      # проверки и таблица; numbers=False — без чисел
    import environment as EN
    import agent as AG

    out = []
    out.append((EN.self_check(verbose=False), "среда: распределения и средние сошлись"))
    out.append((AG.self_check(verbose=False), "агент: оценки и стратегии сошлись"))

    rows = compare(steps, seed) if numbers else []
    table = {name: (avg, share) for name, avg, share, _ in rows}

    if not numbers:
        if verbose_report():
            for ok, text in out:
                print("   [%s] прогон: %s" % ("ok" if ok else "нет", text))
        return all(ok for ok, _ in out), rows

    out.append((table["UCB c = 2"][1] > 0.9,
                "UCB находит C и держит её: доля выбора C = %.0f%%"
                % (100 * table["UCB c = 2"][1])))
    out.append((table["жадная"][0] < table["ε-жадная 0,1"][0],
                "жадная проигрывает ε-жадной: %.2f против %.2f"
                % (table["жадная"][0], table["ε-жадная 0,1"][0])))
    out.append((table["ε-жадная 0,1"][0] <= table["UCB c = 2"][0],
                "ε-жадная не обгоняет UCB: %.2f против %.2f"
                % (table["ε-жадная 0,1"][0], table["UCB c = 2"][0])))

    if verbose_report():
        for ok, text in out:
            print("   [%s] прогон: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in out), rows


_VERBOSE = True


def verbose_report():
    return _VERBOSE


def print_table(rows):
    print("\n1000 спринтов тимлида (seed = %d):" % SEED)
    print("   %-16s %8s %12s" % ("стратегия", "средний", "доля C"))
    for name, avg, share, _ in sorted(rows, key=lambda r: -r[1]):
        print("   %-16s %8.3f %11.0f%%" % (name, avg, 100 * share))
    print("\nпотолок — всегда тянуть C: средняя 1,3 (истинная средняя лучшего подхода)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", action="store_true", help="нарисовать картинку")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "bandit-1000.png"))
    parser.add_argument("--exp", action="store_true", help="прогнать эксперимент и нарисовать кривые обучения")
    parser.add_argument("--strategy", default=EXP_MODE,
                        help="стратегия для --exp (по умолчанию EXP_MODE): " + ", ".join(NAMES))
    parser.add_argument("--show", action="store_true", help="показать окно с графиком (иначе сохранить PNG)")
    parser.add_argument("--trace", default=None, metavar="ARM=R1,R2,...",
                        help="шаг за шагом: как двигается оценка, напр. B=1,0,2")
    parser.add_argument("--alpha", type=float, default=0.5,
                        help="постоянный шаг для --trace (по умолчанию 0,5)")
    args = parser.parse_args()

    quiet = bool(args.exp or args.trace)
    try:
        ok, rows = report(numbers=not quiet)
    except NotImplementedError as e:
        print("\n   [нет] прогон: %s" % e)
        print("   Допишите недостающее место в agent.py — и запустите снова.")
        raise SystemExit(1)
    if not quiet:
        print_table(rows)                                              # на --exp таблицу не печатаем: пары меряют сами

    if args.png:
        path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            print("\nкартинка:", plot(path))
        except ImportError:
            print("\nкартинка не построена: matplotlib не найден — pip install matplotlib")
            print("   таблица и проверки выше работают и без него.")

    if args.exp:
        mode = STRATEGY_ALIASES.get(args.strategy, args.strategy)
        if mode not in ("greedy", "eps", "optimistic", "ucb", "gradient"):
            print("\nнет такой стратегии: %s (есть: %s)"
                  % (args.strategy, ", ".join(NAMES)))
            sys.exit(1)
        EXP_MODE = mode                                                # параметры подхватит своя стратегия
        log = experiment()
        total = sum(log["reward"])
        hits = sum(1 for a in log["act"] if a == best())
        print("\nэксперимент: mode = %s, seed = %d" % (EXP_MODE, EXP_SEED))
        print("   средний доход %.3f · доля C %.0f%%"
              % (total / len(log["reward"]), 100.0 * hits / len(log["act"])))
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "experiment.png")
        try:
            print("   картинка:", plot_experiment(log, path=path, show=args.show))
        except ImportError:
            print("   matplotlib не найден — кривые не построены: pip install matplotlib")
            text_report(log)

    if args.trace:
        arm, _, seq = args.trace.partition("=")
        arm = (arm or "B").strip().upper()
        if arm not in APPROACHES:
            print("\nнет такого подхода: %s (есть: %s)" % (arm, ", ".join(APPROACHES)))
            sys.exit(1)
        observations = [int(x) for x in seq.replace(" ", "").split(",") if x != ""]
        if not observations:
            print("\nнужен ряд наблюдений, например --trace B=1,0,2")
            sys.exit(1)
        trace(arm, observations, args.alpha)

    print("\nитог: все проверки прогона сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
    sys.exit(0 if ok else 1)
