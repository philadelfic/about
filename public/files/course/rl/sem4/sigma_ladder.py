# sigma_ladder.py — опыт «где 1/n сдаётся»: лестница σ, две стратегии, точка перелома.
# python3 sigma_ladder.py [--sigmas 0,0.01,0.05,0.2,1.0] [--seeds 30] [--steps 1000] [--alpha 0.1] [--csv ladder.csv]
#
# Зачем: в стоячем мире (σ = 0) честное среднее 1/n точнее постоянного шага α,
# а в движущемся — наоборот. Здесь мы не верим эталону, а ищем перелом сами:
# где по σ стратегии меняются местами и почему при большом σ α уже не спасает.

import argparse
import statistics
import sys

from run import one_run, update_is_stub, env_is_stub

LADDER = (0.0, 0.01, 0.05, 0.2, 1.0)                                   # σ: от стоячего мира к скачущему
NAME_MEAN = "ε 0,1 · 1/n"                                              # честное среднее
NAME_STEP = "ε 0,1 · α{alpha}"                                        # постоянный шаг (α подставляется)


def measure(kwargs, sigma, seeds, steps):                              # медиана и квартили по сидам
    shares, incomes = [], []
    for seed in range(1, seeds + 1):
        run = one_run(kwargs, steps=steps, seed=seed, sigma=sigma)
        shares.append(100.0 * run["share"])
        incomes.append(run["income"])
    q1, _, q3 = statistics.quantiles(shares, n=4)
    return statistics.median(incomes), statistics.median(shares), q1, q3


def main(argv=None):
    parser = argparse.ArgumentParser(description="лестница σ: где 1/n и α меняются местами")
    parser.add_argument("--sigmas", default=",".join("%g" % s for s in LADDER),
                        help="значения σ через запятую (по умолчанию 0,0.01,0.05,0.2,1.0)")
    parser.add_argument("--seeds", type=int, default=30, help="сидов на точку (по умолчанию 30)")
    parser.add_argument("--steps", type=int, default=1000, help="спринтов в прогоне (по умолчанию 1000)")
    parser.add_argument("--alpha", type=float, default=0.1, help="постоянный шаг α (по умолчанию 0,1)")
    parser.add_argument("--csv", default=None, help="куда сохранить таблицу")
    args = parser.parse_args(argv)
    if env_is_stub() or update_is_stub():
        print("\nЛестница пока не имеет смысла: не заполнены пропуски.")
        if env_is_stub():
            print("   ПРОПУСК 1 — среда стоит: σ не влияет ни на что (environment.py).")
        if update_is_stub():
            print("   ПРОПУСК 2 — оценки q не двигаются: строки с α совпадают с 1/n (agent.py).")
        print("   Куски — snippets.py, группы 1 и 2; проверка — environment.py и agent.py.\n")
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
        inc_m, med_m, q1_m, q3_m = cells[name_mean]
        inc_s, med_s, q1_s, q3_s = cells[name_step]
        gap = med_s - med_m
        print("   %8g  %5.0f%% [%3.0f-%3.0f] %5.2f   %5.0f%% [%3.0f-%3.0f] %5.2f  %+7.0f"
              % (sigma, med_m, q1_m, q3_m, inc_m, med_s, q1_s, q3_s, inc_s, gap))

    # где шаг обгоняет честное среднее и где разрыв самый большой
    cross = next((s for s, c in rows if s > 0 and c[name_step][1] > c[name_mean][1]), None)
    best = max(rows, key=lambda item: item[1][name_step][1] - item[1][name_mean][1])
    at_zero = rows[0][1]
    gap_best = best[1][name_step][1] - best[1][name_mean][1]
    gap_top = rows[-1][1][name_step][1] - rows[-1][1][name_mean][1]

    gap_zero = at_zero[name_step][1] - at_zero[name_mean][1]
    print("\nчто видно:")
    if abs(gap_zero) < 1:
        print("   при σ = 0 разницы нет: 1/n — %.0f%%, шаг — %.0f%% — адаптивность в стоячем мире не нужна"
              % (at_zero[name_mean][1], at_zero[name_step][1]))
    elif gap_zero < 0:
        print("   при σ = 0 шаг проигрывает %.0f п.п. (%.0f%% против %.0f%%) — это цена адаптивности"
              % (-gap_zero, at_zero[name_step][1], at_zero[name_mean][1]))
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
            fh.write("sigma,strategy,income,share_median,share_q1,share_q3\n")
            for sigma, cells in rows:
                for name, (inc, med, q1, q3) in cells.items():
                    fh.write("%g,%s,%.3f,%.1f,%.1f,%.1f\n" % (sigma, name, inc, med, q1, q3))
        print("\nтаблица сохранена: %s" % args.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
