#!/usr/bin/env python3
# Entry point: python3 saper.py <mode>.
# Modes and details — in README.md next to this file.

import sys

import knobs
import play
from qagent import QAgent
from sarsa import SarsaAgent

AGENT_CLS = SarsaAgent

USAGE = """Saper 4 x 4, tabular Q-learning. Modes:
  --selftest                    check that everything runs
  --random --games 2000         lower bound: a random cell, no table
  --train --episodes 10000      learning + greedy evaluation (Q-learning)
  --sarsa --episodes 10000      the same, but on-policy (SARSA)
  --ladder --episodes 100000    ladder 10 -> ... -> 100000 games
  --sarsa --ladder              the same ladder for SARSA
  --show --seed 7 --after 4     board after agent moves and its cell estimates
  --vs                          human against the machine

You can add --sarsa to --show and --vs: then SARSA plays and shows the board.

Knobs: --alpha --epsilon --seed. Amount of learning — --episodes (for --show and --vs
the same can be written as --train-episodes). Details — README.md."""


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
            print("flag %s needs a value, for example %s 1000" % (name, name))
            raise SystemExit(2)
        try:
            return type(default)(rest[i + 1])
        except ValueError:
            print("cannot read the value of flag %s: %r" % (name, rest[i + 1]))
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
                title="SARSA, ladder (alpha 0.1, epsilon 0.1):",
            )
        else:
            play.cmd_train(
                episodes=opt("--episodes", 10000),
                alpha=opt("--alpha", knobs.ALPHA),
                epsilon=opt("--epsilon", knobs.EPSILON),
                seed=opt("--seed", knobs.SEED),
                eval_games=opt("--eval", 2000),
                agent_cls=SarsaAgent,
                title="SARSA: on-policy TD, bootstrap on the action actually taken.",
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
        print(f"unknown mode {mode!r}; see README.md")
        sys.exit(2)


if __name__ == "__main__":
    main()
