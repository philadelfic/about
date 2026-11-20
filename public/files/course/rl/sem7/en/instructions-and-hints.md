# Instructions and hints — saper 4 × 4 (seminar 7 code)

The code of seminar 7 in reinforcement learning. A tiny minesweeper: board 4 × 4, two
mines, the first opened cell is safe. Tabular Q-learning and SARSA — two strategies,
the difference is one line of the update.

## 1. How to run it

Eight files sit flat, there is no nested folder. Put them into one folder (for example
`saper`) and go there:

```
python3 saper.py --selftest
```

You expect the line `selftest: ok` — everything runs. If not, raise your hand.

Only Python 3 is needed, no third-party libraries.

**Windows:** the interpreter is called `python` (or `py`), there is no `3` suffix:
`python saper.py --selftest`. If PowerShell answers "Python was not found", that is the
Microsoft Store stub — install Python from python.org.

## 2. What is in the files

| File | What is inside |
|---|---|
| `saper.py` | entry point: parsing flags and calling a mode |
| `play.py` | run modes: selftest, random, train, ladder, show, vs |
| `game.py` | environment: mines, opening cells, end of the game |
| `base.py` | the Q table and ε-greedy choice |
| `qagent.py` | TD update, Q-learning (off-policy, maximum over future cells) |
| `sarsa.py` | TD update, SARSA (on-policy, estimate of its own move) |
| `knobs.py` | knobs: `FIELD`, `MINES`, `GAMMA`, `ALPHA`, `EPSILON`, `SEED` |

## 3. Modes

| Command | What it does |
|---|---|
| `python3 saper.py --random --games 2000` | lower bound: a random cell, no table |
| `python3 saper.py --train --episodes 10000` | learning + greedy evaluation on 2000 games |
| `python3 saper.py --sarsa --episodes 10000` | the same, but on-policy (SARSA) |
| `python3 saper.py --ladder --episodes 100000` | ladder 10 → 100 → … → 100 000 games |
| `python3 saper.py --sarsa --ladder --episodes 100000` | the same ladder for SARSA |
| `python3 saper.py --show --seed 7 --after 4` | board after four agent moves and its cell estimates |
| `python3 saper.py --vs` | human against the machine (the agent learns for about ten seconds) |

The knobs `--alpha --epsilon --seed` work in any mode. You can add `--sarsa` to
`--show` and `--vs`: then SARSA plays and shows the board instead of Q-learning.

An important note about `--seed` in `--show` and `--vs`: it is the seed of the *board*,
not of learning. Learning always uses seed 42, so the bet boards reproduce every time.

## 4. What we do in class

Selftest for everyone, then `--train --episodes 10000`, then two boards with a vote
(`--show --seed 9 --after 4` and `--show --seed 15 --after 4`), then the ladder
`--ladder --episodes 100000`, the comparison with `--sarsa --ladder`, the knobs α and ε,
and `--vs` if there is time left.

## 5. Numbers you should get

Ladder (α = 0.1, ε = 0.1, evaluation on 2000 greedy games):

| Training games | Wins | Pairs in the table |
|---|---|---|
| 10 | 1.2 % | 39 |
| 100 | 1.5 % | 342 |
| 1 000 | 16.4 % | 2 575 |
| 10 000 | 68.6 % | 21 914 |
| 100 000 | 96.8 % | 64 923 |

A random player — 0.5 %. SARSA on the same ladder: 1.2 / 2.0 / 6.9 / 24.4 / 96.9 %,
pairs in the table at one hundred thousand — 110 558.

The α knob (one hundred thousand games): 0.001 → 66.9 %, 0.1 → 96.8 %, 0.9 → 89.5 %.
The ε knob: 0.01 → 97.8 %, 0.1 → 96.8 %, 0.3 → 88.2 %.

The numbers were produced by a script and are not edited by hand; the seminar slides and
the session page show the same values. If you get something else, one of the inputs
changed: the learning seed, the number of games, α, ε or the strategy itself.

## 6. Hints and pitfalls

- The table holds a "state, cell" pair, and the state is the picture: closed cells and
  open numbers. Mines are not in the state — that is not a bug, it is the reason for
  the ceiling.
- The greedy evaluation runs without random probes: ε works during learning and is off
  during evaluation. That is why "training wins" is always lower than "greedy play".
- The ladder starts at ten games: `--episodes 5` prints nothing.
- `--episodes` for `--show` and `--vs` is the amount of learning for the agent; the same
  can be written as `--train-episodes`.
- The one line of difference between Q-learning and SARSA lives in `qagent.py` and
  `sarsa.py`; compare them by eye — it is the fastest way to get on-policy vs off-policy.

## 7. You do not hand this in

The class code is a demonstration, not a lab. Laboratory 1 is tic-tac-toe: the
assignment, criteria and deadlines are on the lab page.
