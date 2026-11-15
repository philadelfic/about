#!/usr/bin/env python3
# Кафе-симулятор: бандит «где обедать» с группами рычагов.
#
# v3 · 08.11.2026
#
# Запуск:
  # python3 obed.py --play          # сам выбирай блюда каждый день
  # python3 obed.py --duel К1 К2    # две команды по четыре характера
#
# Характеры (один файл — одна стратегия, все файлы в одной папке):
  # завсегдатай (жадный), пятница (eps), любопытный (ucb), тянущийся (gradient), оптимист
# Шаг обновления после двоеточия: avg (честное среднее 1/n) или alpha.

import argparse
import re
import sys

from menu import GROUP_ORDER, GROUPS

# Windows console: do not crash on greek symbols.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors='replace')
    except Exception:
        pass


def normalize_args():
    # Разрешаем десятичную запятую: --sigma 0,05 0,01 ... -> 0.05 0.01 ...
    pattern = re.compile(r"(?<=\d),(?=\d)")
    sys.argv = [pattern.sub(".", arg) for arg in sys.argv]


def apply_knobs(args):
    import knobs
    knobs.EPSILON = args.epsilon
    knobs.ALPHA = args.alpha
    knobs.C_UCB = args.c
    knobs.ETA = args.eta
    knobs.Q0 = args.q0


def main():
    normalize_args()
    default_sigmas = [GROUPS[group]["sigma"] for group in GROUP_ORDER]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--play", action="store_true",
                        help="сам выбирай блюда каждый день")
    parser.add_argument("--vs", metavar="ХАРАКТЕР",
                        help="в --play: соперник-стратегия, например тянущийся")
    parser.add_argument("--duel", nargs=2, metavar=("КОМАНДА1", "КОМАНДА2"),
                        help="две команды по %d характеров через запятую"
                             % len(GROUP_ORDER))
    parser.add_argument("--days", type=int, default=200, help="дней (по умолчанию 200)")
    parser.add_argument("--seed", type=int, default=7, help="сид (по умолчанию 7)")
    parser.add_argument("--sigma", type=float, nargs="+", default=default_sigmas,
                        help="σ дрейфа по группам %s (по умолчанию: %s)"
                             % (", ".join(GROUP_ORDER), " ".join(map(str, default_sigmas))))
    parser.add_argument("--log", type=int, default=0,
                        help="печать прогресса каждые N дней")
    parser.add_argument("--selftest", action="store_true",
                        help="проверить, что все стратегии запускаются")
    parser.add_argument("--epsilon", type=float, default=0.1, help="ручка ε")
    parser.add_argument("--alpha", type=float, default=0.1, help="постоянный шаг α")
    parser.add_argument("--c", type=float, default=2.0, help="ручка c у UCB")
    parser.add_argument("--eta", type=float, default=0.1, help="шаг предпочтений η")
    parser.add_argument("--q0", type=float, default=5.0,
                        help="стартовая оценка оптимиста")
    args = parser.parse_args()
    if len(args.sigma) != len(GROUP_ORDER):
        sys.exit("нужно %d значений σ: %s"
                 % (len(GROUP_ORDER), ", ".join(GROUP_ORDER)))
    apply_knobs(args)

    from game import duel, play, selftest
    if args.selftest:
        selftest()
    elif args.play:
        play(args)
    else:
        duel(args) if args.duel else parser.print_help()


if __name__ == "__main__":
    main()
