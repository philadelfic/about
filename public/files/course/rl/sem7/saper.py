#!/usr/bin/env python3
# Точка входа: python3 saper.py <режим>.
# Режимы и подробности — в README.md рядом с этим файлом.

import sys

import knobs
import play
from qagent import QAgent
from sarsa import SarsaAgent

AGENT_CLS = SarsaAgent

USAGE = """Сапёр 4 x 4, табличное Q-обучение. Режимы:
  --selftest                    проверка, что всё запускается
  --random --games 2000         нижняя граница: клетка наугад, таблицы нет
  --train --episodes 10000      обучение + жадная оценка (Q-обучение)
  --sarsa --episodes 10000      то же самое, но on-policy (SARSA)
  --ladder --episodes 100000    лестница 10 -> ... -> 100000 партий
  --sarsa --ladder              та же лестница для SARSA
  --show --seed 7 --after 4     доска после ходов агента и его оценки клеток
  --vs                          человек против машины

К --show и --vs можно добавить --sarsa: играть и смотреть будет SARSA.

Ручки: --alpha --epsilon --seed. Объём обучения — --episodes (у --show и --vs
то же самое можно писать --train-episodes). Подробности — README.md."""


def main():
    args = sys.argv[1:]
    if not args:
        print(USAGE)
        return
    mode = args[0]
    rest = args[1:]

    def opt(name, default):
        if name not in rest:
            return default
        i = rest.index(name)
        if i + 1 >= len(rest):
            print("флагу %s нужно значение, например %s 1000" % (name, name))
            raise SystemExit(2)
        try:
            return type(default)(rest[i + 1])
        except ValueError:
            print("не понял значение флага %s: %r" % (name, rest[i + 1]))
            raise SystemExit(2)

    if mode == "--selftest":
        play.cmd_selftest()
    elif mode == "--random":
        play.cmd_random(
            games=opt("--games", 2000),
            seed=opt("--seed", 7),
        )
    elif mode == "--sarsa":
        if "--ladder" in rest:
            play.cmd_ladder(
                top=opt("--episodes", 100000),
                alpha=opt("--alpha", knobs.ALPHA),
                epsilon=opt("--epsilon", knobs.EPSILON),
                seed=opt("--seed", knobs.SEED),
                eval_games=opt("--eval", 2000),
                agent_cls=SarsaAgent,
                title="SARSA, лестница (alpha 0.1, epsilon 0.1):",
            )
        else:
            play.cmd_train(
                episodes=opt("--episodes", 10000),
                alpha=opt("--alpha", knobs.ALPHA),
                epsilon=opt("--epsilon", knobs.EPSILON),
                seed=opt("--seed", knobs.SEED),
                eval_games=opt("--eval", 2000),
                agent_cls=SarsaAgent,
                title="SARSA: on-policy TD, оценка у своего хода.",
            )
    elif mode == "--train":
        play.cmd_train(
            episodes=opt("--episodes", 10000),
            alpha=opt("--alpha", knobs.ALPHA),
            epsilon=opt("--epsilon", knobs.EPSILON),
            seed=opt("--seed", knobs.SEED),
            eval_games=opt("--eval", 2000),
        )
    elif mode == "--ladder":
        play.cmd_ladder(
            top=opt("--episodes", 100000),
            alpha=opt("--alpha", knobs.ALPHA),
            epsilon=opt("--epsilon", knobs.EPSILON),
            seed=opt("--seed", knobs.SEED),
            eval_games=opt("--eval", 2000),
        )
    elif mode == "--show":
        play.cmd_show(
            seed=opt("--seed", 7),
            after=opt("--after", 4),
            episodes=opt("--train-episodes", opt("--episodes", 100000)),
            alpha=opt("--alpha", knobs.ALPHA),
            epsilon=opt("--epsilon", knobs.EPSILON),
            agent_cls=AGENT_CLS if "--sarsa" in rest else QAgent,
        )
    elif mode == "--vs":
        play.cmd_vs(
            episodes=opt("--train-episodes", opt("--episodes", 100000)),
            alpha=opt("--alpha", knobs.ALPHA),
            epsilon=opt("--epsilon", knobs.EPSILON),
            seed=opt("--seed", 99),
            agent_cls=AGENT_CLS if "--sarsa" in rest else QAgent,
        )
    else:
        print(f"не знаю режима {mode!r}; см. README.md")
        sys.exit(2)


if __name__ == "__main__":
    main()
