# sigma_ladder.py — опыт «где 1/n сдаётся»: лестница σ, две стратегии, точка перелома.
# python3 sigma_ladder.py [--sigmas 0,0.01,0.05,0.2,1.0] [--seeds 100] [--steps 1000] [--alpha 0.1]
#                        [--csv ladder.csv] [--log run_log.jsonl]
#
# Зачем: в стоячем мире (σ = 0) честное среднее 1/n точнее постоянного шага α,
# а в движущемся — наоборот. Здесь мы не верим эталону, а ищем перелом сами:
# где по σ стратегии меняются местами и почему при большом σ α уже не спасает.
#
# Строки для run_log.jsonl пишет флаг --log — те же поля, что у calc_table.py.

import argparse
import json
import os
import statistics
import sys

from run import one_run, update_is_stub, env_is_stub

LADDER = (0.0, 0.01, 0.05, 0.2, 1.0)                                   # σ: от стоячего мира к скачущему
NAME_MEAN = "ε 0,1 · 1/n"                                              # честное среднее
NAME_STEP = "ε 0,1 · α{alpha}"                                        # постоянный шаг (α подставляется)
METRICS = (("доход за спринт", "", 2),                                 # метрика · знак · знаков после запятой
           ("доля лучшего", "%", 0))


def fmt(value, digits):                                                # число по-русски: 1,31 · 69
    return ("%.*f" % (digits, value)).replace(".", ",")


def spread(values):                                                    # медиана и квартили по сидам
    q1, _, q3 = statistics.quantiles(values, n=4)
    return {"median": statistics.median(values), "q1": q1, "q3": q3}


def measure(kwargs, sigma, seeds, steps):                              # медиана и IQR по сидам для двух метрик
    shares, incomes = [], []
    for seed in range(1, seeds + 1):
        run = one_run(kwargs, steps=steps, seed=seed, sigma=sigma)
        shares.append(100.0 * run["share"])
        incomes.append(run["income"])
    return {"доход за спринт": spread(incomes), "доля лучшего": spread(shares)}


def main(argv=None):
    parser = argparse.ArgumentParser(description="лестница σ: где 1/n и α меняются местами")
    parser.add_argument("--sigmas", default=",".join("%g" % s for s in LADDER),
                        help="значения σ через запятую (по умолчанию 0,0.01,0.05,0.2,1.0)")
    parser.add_argument("--seeds", type=int, default=100, help="сидов на точку (по умолчанию 100)")
    parser.add_argument("--steps", type=int, default=1000, help="спринтов в прогоне (по умолчанию 1000)")
    parser.add_argument("--alpha", type=float, default=0.1, help="постоянный шаг α (по умолчанию 0,1)")
    parser.add_argument("--csv", default=None, help="куда сохранить таблицу")
    parser.add_argument("--log", default=None, help="куда дописать строки run_log.jsonl")
    args = parser.parse_args(argv)
    if env_is_stub() or update_is_stub():
        print("\nЛестница пока не имеет смысла: не заполнены пропуски.")
        if env_is_stub():
            print("   ПРОПУСК 1 — среда стоит: σ не влияет ни на что (environment.py).")
        if update_is_stub():
            print("   ПРОПУСК 2 — оценки q не двигаются: строки с α совпадают с 1/n (agent.py).")
        print("   Куски — snippets.py, группы 1 и 2; проверка — environment.py и agent.py.\n")
        return 1
    if args.seeds < 2:
        print("сидов нужно хотя бы два: по одному квартили не считаются")
        return 1

    try:
        sigmas = [float(x) for x in args.sigmas.replace(" ", "").split(",") if x]
    except ValueError:
        print("σ задаются числами через запятую, например: --sigmas 0,0.05,0.2")
        return 1

    pairs = ((NAME_MEAN, dict(mode="eps", epsilon=0.1)),
             (NAME_STEP.format(alpha=("%g" % args.alpha).replace(".", ",")),
              dict(mode="eps", epsilon=0.1, alpha=args.alpha)))

    rows = []
    for sigma in sigmas:
        cells = {}
        for name, kwargs in pairs:
            cells[name] = measure(kwargs, sigma, args.seeds, args.steps)
        rows.append((sigma, cells))

    name_mean, name_step = pairs[0][0], pairs[1][0]
    print("\nлестница σ: доля текущего лучшего, медиана [IQR] — %d сидов × %d спринтов"
          % (args.seeds, args.steps))
    print("   %8s  %-24s %-24s %8s" % ("σ", name_mean, name_step, "разрыв"))
    for sigma, cells in rows:
        mean_share = cells[name_mean]["доля лучшего"]
        step_share = cells[name_step]["доля лучшего"]
        gap = step_share["median"] - mean_share["median"]
        print("   %8g  %5.0f%% [%3.0f-%3.0f] %5.2f   %5.0f%% [%3.0f-%3.0f] %5.2f  %+7.0f"
              % (sigma, mean_share["median"], mean_share["q1"], mean_share["q3"],
                 cells[name_mean]["доход за спринт"]["median"],
                 step_share["median"], step_share["q1"], step_share["q3"],
                 cells[name_step]["доход за спринт"]["median"], gap))

    # где шаг обгоняет честное среднее и где разрыв самый большой
    share_of = lambda cells, name: cells[name]["доля лучшего"]["median"]  # noqa: E731
    cross = next((s for s, c in rows if s > 0 and share_of(c, name_step) > share_of(c, name_mean)), None)
    best = max(rows, key=lambda item: share_of(item[1], name_step) - share_of(item[1], name_mean))
    gap_best = share_of(best[1], name_step) - share_of(best[1], name_mean)
    gap_top = share_of(rows[-1][1], name_step) - share_of(rows[-1][1], name_mean)
    gap_zero = share_of(rows[0][1], name_step) - share_of(rows[0][1], name_mean)

    print("\nчто видно:")
    if abs(gap_zero) < 1:
        print("   при σ = 0 разницы нет: 1/n — %.0f%%, шаг — %.0f%% — адаптивность в стоячем мире не нужна"
              % (share_of(rows[0][1], name_mean), share_of(rows[0][1], name_step)))
    elif gap_zero < 0:
        print("   при σ = 0 шаг проигрывает %.0f п.п. (%.0f%% против %.0f%%) — это цена адаптивности"
              % (-gap_zero, share_of(rows[0][1], name_step), share_of(rows[0][1], name_mean)))
    else:
        print("   при σ = 0 шаг выигрывает %+.0f п.п. — проверьте, что мир действительно стоит"
              % gap_zero)
    if cross is None:
        print("   на этой лестнице шаг так и не обогнал 1/n — попробуйте σ больше")
    else:
        print("   шаг обгоняет 1/n начиная с σ = %g" % cross)
    print("   самый большой разрыв — при σ = %g: %+.0f п.п. в пользу шага" % (best[0], gap_best))
    print("   при σ = %g разрыв %+.0f п.п. — %s"
          % (rows[-1][0], gap_top,
             "мир меняется быстрее, чем агент успевает учиться"
             if abs(gap_top) < abs(gap_best) else "шаг держится"))

    if args.csv:
        with open(args.csv, "w", encoding="utf-8") as fh:
            fh.write("sigma,strategy,metric,median,q1,q3\n")
            for sigma, cells in rows:
                for name, by_metric in cells.items():
                    for title, key in (("доход за спринт", "income"), ("доля лучшего", "share")):
                        stats = by_metric[title]
                        fh.write("%g,%s,%s,%.3f,%.3f,%.3f\n"
                                 % (sigma, name, key, stats["median"], stats["q1"], stats["q3"]))
        print("\nтаблица сохранена: %s" % args.csv)

    if args.log:
        command = "python3 %s --sigmas %s --seeds %d --steps %d --alpha %s" % (
            os.path.basename(__file__), ",".join("%g" % s for s in sigmas),
            args.seeds, args.steps, args.alpha)
        with open(args.log, "a", encoding="utf-8") as fh:
            for sigma, cells in rows:
                for name, by_metric in cells.items():
                    for title, unit, digits in METRICS:
                        stats = by_metric[title]
                        fh.write(json.dumps({
                            "n_runs": args.seeds,
                            "seed_from": 1,
                            "seed_to": args.seeds,
                            "sigma": sigma,
                            "metric": "%s (σ = %g): %s: медиана %s%s [%s–%s]" % (
                                name, sigma, title, fmt(stats["median"], digits), unit,
                                fmt(stats["q1"], digits), fmt(stats["q3"], digits)),
                            "strategy": name,
                            "metric_name": title,
                            "median": round(stats["median"], digits),
                            "q1": round(stats["q1"], digits),
                            "q3": round(stats["q3"], digits),
                            "unit": unit,
                            "command": command,
                        }, ensure_ascii=False) + "\n")
        print("\nстроки лога дописаны: %s" % args.log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
