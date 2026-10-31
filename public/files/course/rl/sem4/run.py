# run.py — прогон: 1000 спринтов в движущемся мире, метрики из истории средних.
# В этом файле один пропуск — ПРОПУСК 3: стратегия в эксперименте (--exp).
# Куски — в snippets.py (группа 3); верного куска нет, выбор обосновывается.
# python3 run.py [--png] [--exp [--strategy ИМЯ] [--alpha 0.1] [--sigma 0.05]] [--trace B=1,0,2]

import argparse
import os
import sys

from agent import Agent
from environment import APPROACHES, SIGMA, Bandit

STEPS = 1000                                                           # сколько спринтов гоним одну стратегию
SEED = 7                                                               # один seed — один и тот же год

STRATEGIES = (                                                         # стратегии и правила обновления: имя → настройки агента
    ("жадная",             dict(mode="greedy")),
    ("ε-жадная 0,1 / 1n",  dict(mode="eps", epsilon=0.1)),
    ("ε-жадная 0,1 / α0,1", dict(mode="eps", epsilon=0.1, alpha=0.1)),
    ("ε-жадная 0,1 / α0,3", dict(mode="eps", epsilon=0.1, alpha=0.3)),
    ("UCB c = 2 / 1n",     dict(mode="ucb", c=2.0)),
    ("UCB c = 2 / α0,1",   dict(mode="ucb", c=2.0, alpha=0.1)),
    ("градиентная",        dict(mode="gradient", h_alpha=0.1)),
)

STRATEGY_ALIASES = {                                                   # алиасы: имя в зале → mode
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

EXP_MODE = "eps"                                                       # стратегия для --exp
EXP_SEED = 7                                                           # другой seed — другая случайность
EXP_EPSILON = 0.1                                                      # доля шагов наугад (только для eps)
EXP_C = 2.0                                                            # масштаб бонуса неуверенности (только для ucb)
EXP_Q0 = 5.0                                                           # стартовая оценка (optimistic)
EXP_ALPHA = None                                                       # шаг оценки: None — 1/n, число — α
EXP_H_ALPHA = 0.1                                                      # шаг предпочтений (только для gradient)
EXP_STEPS = 1000                                                       # сколько спринтов гоним


def update_is_stub():                                                  # ПРОПУСК 2 ещё не заполнен?
    agent = Agent(None, mode="greedy", alpha=None)
    agent.update("A", 0.0)                                            # первое наблюдение: q = 0
    agent.update("B", 2.0)
    before = dict(agent.q)
    agent.update("A", 2.0)                                            # второе по A — должен быть сдвиг
    return dict(agent.q) == before


def env_is_stub():                                                     # ПРОПУСК 1 ещё не заполнен?
    env = Bandit(seed=0, sigma=0.05)
    before = dict(env.mu)
    for _ in range(20):
        env.step("A")
    return dict(env.mu) == before


def one_run(mode_kwargs, steps=STEPS, seed=SEED, sigma=SIGMA):          # один прогон: журнал и метрики
    env = Bandit(seed=seed, sigma=sigma)
    agent = Agent(env, seed=seed, **mode_kwargs)
    rewards, acts = [], []
    for _ in range(steps):
        act = agent.act()
        reward = env.step(act)
        agent.update(act, reward)
        rewards.append(reward)
        acts.append(act)

    hits = sum(1 for t, act in enumerate(acts) if act == env.log_best(t))  # «текущий лучший» — по истории μ
    n_last = [agent.n[a] for a in APPROACHES]
    skew = max(n_last) / max(1, min(n_last))                            # перекос: во сколько раз лидер чаще редкого
    return {
        "rewards": rewards,
        "acts": acts,
        "mu_log": env.mu_log,
        "income": sum(rewards) / len(rewards),                          # доход за спринт
        "share": hits / len(acts),                                      # доля выборов текущего лучшего
        "skew": skew,
        "n": n_last,
    }


def compare(steps=STEPS, seed=SEED, strategies=STRATEGIES, sigma=SIGMA):  # прогнать стратегии и собрать числа
    rows = []
    for name, kwargs in strategies:
        run = one_run(kwargs, steps=steps, seed=seed, sigma=sigma)
        rows.append((name, run["income"], run["share"], run["skew"]))
    return rows


def sliding(values, window):                                           # скользящее среднее — сглаживает шум
    return [sum(values[max(0, i - window):i + 1]) / len(values[max(0, i - window):i + 1])
            for i in range(len(values))]


def text_report(run, blocks=10):                                       # та же картина таблицей, без matplotlib
    n = len(run["acts"])
    step = max(1, n // blocks)
    print("   сводка по шагам (без картинки):")
    print("   %5s %8s %8s" % ("шаг", "доход", "доля лучшего"))
    for i in range(step - 1, n, step):
        lo = max(0, i - step + 1)
        chunk = run["rewards"][lo:i + 1]
        hits = sum(1 for t in range(lo, i + 1) if run["acts"][t] == _log_best(run, t))
        print("   %5d %8.2f %7.0f%%" % (i + 1, sum(chunk) / len(chunk), 100.0 * hits / len(chunk)))
    print("   потолок плывёт: лучший рычаг меняется вместе со средними — смотрите долю лучшего, не доход")


def _log_best(run, t):                                                 # лучший по записанной истории средних
    row = run["mu_log"][t]
    return max(APPROACHES, key=lambda a: row[APPROACHES.index(a)])


def print_table(rows, seeds=1):                                        # таблица сравнения стратегий
    print("\n1000 спринтов, seed = %d%s:" % (SEED, "" if seeds == 1 else ", сидов %d" % seeds))
    print("   %-22s %8s %10s %8s" % ("стратегия", "доход", "доля лучш.", "перекос n"))
    for name, income, share, skew in rows:
        print("   %-22s %8.3f %9.0f%% %8.1f" % (name, income, 100 * share, skew))
    print("\nпотолок — всегда тянуть текущего лучшего: доход ≈ 1,35–1,45, доля ≈ 100%")


def report(steps=STEPS, seed=SEED, quiet=False, sigma=SIGMA):          # проверки и таблица
    import environment as EN
    import agent as AG

    out = []
    out.append((EN.self_check(verbose=False), "среда: блуждание, вероятности и история средних сошлись"))
    out.append((AG.self_check(verbose=False), "агент: оценки и стратегии сошлись"))

    rows = compare(steps, seed, sigma=sigma)
    table = {name: (income, share, skew) for name, income, share, skew in rows}

    eps_n = table["ε-жадная 0,1 / 1n"]
    eps_a = table["ε-жадная 0,1 / α0,1"]
    ucb_n = table["UCB c = 2 / 1n"]
    grad = table["градиентная"]

    out.append((ucb_n[1] > 0.6, "UCB с 1/n держит текущего лучшего: %.0f%%" % (100 * ucb_n[1])))
    out.append((eps_a[1] > eps_n[1], "α обгоняет 1/n по доле лучшего: %.0f%% против %.0f%%"
                % (100 * eps_a[1], 100 * eps_n[1])))
    out.append((grad[1] < eps_a[1], "градиентная в дрейфе слабее ε-жадной с α: %.0f%% против %.0f%%"
                % (100 * grad[1], 100 * eps_a[1])))

    if not quiet:
        for ok, text in out:
            print("   [%s] прогон: %s" % ("ok" if ok else "нет", text))
        print_table(rows)

    return all(ok for ok, _ in out), rows


def plot(path, steps=STEPS, seed=SEED):                                # картинка «1000 спринтов»: средний доход
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 20, "axes.titlesize": 20, "axes.labelsize": 19,
                         "legend.fontsize": 17, "xtick.labelsize": 16, "ytick.labelsize": 16})

    window = 50
    plt.figure(figsize=(11.0, 5.6))
    for name, kwargs in STRATEGIES[:5]:
        run = one_run(kwargs, steps=steps, seed=seed)
        cum = []
        total = 0
        for i, r in enumerate(run["rewards"], 1):
            total += r
            cum.append(total / i)
        smooth = sliding(cum, window)
        plt.plot(range(1, len(smooth) + 1), smooth, label=name, linewidth=4.0)
    plt.axhline(1.3, color="gray", linestyle="--", linewidth=3.0,
                label="потолок на старте: C = 1,3")
    plt.xlabel("спринт (шаг t)")
    plt.ylabel("средний доход за спринт")
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def plot_experiment(run, path=None, show=False):                       # кривые одного прогона: доход, доли, средние
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    window = 50
    t = range(1, len(run["rewards"]) + 1)
    fig, axes = plt.subplots(3, 1, figsize=(9.0, 11.0), sharex=True)

    axes[0].plot(t, sliding(run["rewards"], window), linewidth=1.6, color="darkblue")
    axes[0].set_ylabel("доход (окно 50)")
    axes[0].set_title("1. доход за спринт: потолок плывёт вместе со средними")

    for a in APPROACHES:
        share = sliding([1.0 if x == a else 0.0 for x in run["acts"]], window)
        axes[1].plot(t, share, label=a, linewidth=1.2)
    axes[1].set_ylabel("доля выбора (окно 50)")
    axes[1].set_title("2. доли выбора: прижимается ли стратегия к текущему лучшему")
    axes[1].legend(loc="center right")

    for i, a in enumerate(APPROACHES):
        axes[2].plot(t, [row[i] for row in run["mu_log"]], label=a, linewidth=1.2)
    axes[2].set_ylabel("средние μ")
    axes[2].set_xlabel("спринт (шаг t)")
    axes[2].set_title("3. среда: как гуляют средние (агенту они не видны)")
    axes[2].legend(loc="center right")

    fig.suptitle("Эксперимент: доход %.3f, доля лучшего %.0f%%, перекос n %.1f"
                 % (run["income"], 100 * run["share"], run["skew"]))
    plt.tight_layout(rect=(0, 0, 1, 0.97))
    if path:
        plt.savefig(path, dpi=150)
    if show:
        plt.show()
    plt.close()
    return path


def trace(arm="B", observations=(1, 0, 2), alpha=0.5):                  # ряд по шагам: 1/n и α
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


def seeds_table(strategies=STRATEGIES, steps=STEPS, n_seeds=30, sigma=SIGMA):  # несколько сидов: среднее, медиана, IQR
    import statistics

    rows = []
    for name, kwargs in strategies:
        incomes, shares, skews = [], [], []
        for seed in range(1, n_seeds + 1):
            run = one_run(kwargs, steps=steps, seed=seed, sigma=sigma)
            incomes.append(run["income"])
            shares.append(100.0 * run["share"])
            skews.append(run["skew"])
        rows.append((name, incomes, shares, skews))

    print("\n%d сидов × %d спринтов: распределение, а не один прогон" % (n_seeds, steps))
    print("   %-22s %14s %18s %8s" % ("стратегия", "доход мед.", "доля лучшего мед.", "перекос"))
    for name, incomes, shares, skews in rows:
        q = statistics.quantiles(shares, n=4)
        print("   %-22s %10.2f %10.0f%% [%3.0f–%3.0f] %8.1f"
              % (name, statistics.median(incomes), statistics.median(shares), q[0], q[2],
                 statistics.median(skews)))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", action="store_true", help="нарисовать картинку")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     "bandit-1000.png"))
    parser.add_argument("--exp", action="store_true", help="прогнать эксперимент и нарисовать кривые обучения")
    parser.add_argument("--strategy", default=None,
                        help="стратегия для --exp, если в коде ещё не выбрана: " + ", ".join(NAMES))
    parser.add_argument("--show", action="store_true", help="показать окно с графиком (иначе сохранить PNG)")
    parser.add_argument("--trace", default=None, metavar="ARM=R1,R2,...",
                        help="шаг за шагом: как двигается оценка, напр. B=1,0,2")
    parser.add_argument("--alpha", type=float, default=None,
                        help="постоянный шаг: None — 1/n, число — α (например 0,1)")
    parser.add_argument("--sigma", type=float, default=SIGMA,
                        help="шаг блуждания средних: своё σ вместо SIGMA (по умолчанию %.2f)" % SIGMA)
    parser.add_argument("--seeds", type=int, default=0,
                        help="сколько сидов прогнать для таблицы распределения (0 — один прогон)")
    args = parser.parse_args()

    stubs = []
    if env_is_stub():
        stubs.append("ПРОПУСК 1 — среда стоит: σ ни на что не влияет")
    if update_is_stub():
        stubs.append("ПРОПУСК 2 — оценки q не двигаются: строки с α совпадают с 1/n")
    if stubs:
        print("\nВНИМАНИЕ: не заполнено — " + "; ".join(stubs))
        print("   Пока пропуски пустые, числа ниже ничего не значат. Куски — snippets.py,")
        print("   группы 1 и 2; проверка — python3 environment.py и python3 agent.py\n")

    quiet = bool(args.exp or args.trace)
    if args.seeds:
        seeds_table(steps=min(STEPS, 1000), n_seeds=args.seeds, sigma=args.sigma)
        sys.exit(0)

    ok, rows = report(steps=STEPS if not quiet else STEPS, quiet=quiet, sigma=args.sigma)

    if args.png:
        path = os.path.abspath(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            print("\nкартинка:", plot(path))
        except ImportError:
            print("\nкартинка не построена: matplotlib не найден — pip install matplotlib")
            print("   таблица и проверки выше работают и без него.")

    if args.exp:
        # ← ПРОПУСК 3: выберите кусок из snippets.py (группа 3) и задайте mode и его параметры.
        #    Верного куска нет: все три стратегии законны, нужен обоснованный выбор.
        #    Можно и без правки файла: python3 run.py --exp --strategy ИМЯ (тогда выбор — в обосновании).
        mode = None
        if mode is None and args.strategy is not None:
            mode = STRATEGY_ALIASES.get(args.strategy, args.strategy)
            print("\nстратегия взята из --strategy: %s — будьте готовы объяснить выбор" % args.strategy)
        if mode is None:
            print("\nпропуск 3 не заполнен: выберите стратегию из snippets.py, группа 3,")
            print("   или передайте её флагом: python3 run.py --exp --strategy ИМЯ")
            sys.exit(1)

        if mode not in ("greedy", "eps", "optimistic", "ucb", "gradient"):
            print("\nнет такой стратегии: %s (есть: %s)" % (args.strategy, ", ".join(NAMES)))
            sys.exit(1)
        kwargs = dict(mode=mode)
        if mode == "eps":
            kwargs["epsilon"] = EXP_EPSILON
        if mode == "ucb":
            kwargs["c"] = EXP_C
        if mode == "optimistic":
            kwargs["q0"] = EXP_Q0
        if mode == "gradient":
            kwargs["h_alpha"] = EXP_H_ALPHA
        if args.alpha is not None:
            kwargs["alpha"] = args.alpha

        run = one_run(kwargs, steps=EXP_STEPS, seed=EXP_SEED, sigma=args.sigma)
        print("\nэксперимент: mode = %s%s, seed = %d, спринтов %d"
              % (mode, "" if args.alpha is None else ", α = %.2f" % args.alpha, EXP_SEED, EXP_STEPS))
        print("   метрики из истории средних (mu_log):")
        print("   доход за спринт          %.3f" % run["income"])
        print("   доля текущего лучшего    %.0f%%" % (100 * run["share"]))
        print("   перекос частот max/min   %.1f  (n = %s)"
              % (run["skew"], " / ".join(str(n) for n in run["n"])))

        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "experiment.png")
        try:
            print("   картинка:", plot_experiment(run, path=path, show=args.show))
        except ImportError:
            print("   matplotlib не найден — кривые не построены: pip install matplotlib")
            text_report(run)

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
        trace(arm, observations, 0.5 if args.alpha is None else args.alpha)

    print("\nитог: все проверки прогона сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
    sys.exit(0 if ok else 1)
