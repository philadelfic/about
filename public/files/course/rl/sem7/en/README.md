# Saper 4 × 4 — seminar 7 code

Tabular Q-learning on a tiny minesweeper. Pure Python 3, nothing to install.
Board 4 × 4, two mines, the first opened cell is always safe.

All files sit in one folder — eight of them, no nested directories.
Put them into one folder (for example `saper/`) and run from there.

## The first command (the same for everyone)

```
python3 saper.py --selftest
```

It prints `selftest: ok` — everything runs.
On Windows the interpreter is called `python` (or `py`): `python saper.py --selftest`.
Run the command from the folder itself: `knobs.py`, `game.py`, `base.py`, `qagent.py`,
`sarsa.py`, `play.py` must be next to it.

## Modes

| Command | What it does |
|---|---|
| `python3 saper.py --random --games 2000` | lower bound: a random cell, no table |
| `python3 saper.py --train --episodes 10000` | Q-learning + greedy evaluation on 2000 games |
| `python3 saper.py --sarsa --episodes 10000` | the same, but on-policy (SARSA) |
| `python3 saper.py --ladder --episodes 100000` | ladder 10 → 100 → … → 100 000 games |
| `python3 saper.py --sarsa --ladder --episodes 100000` | the same ladder for SARSA |
| `python3 saper.py --show --seed 7 --after 4` | board after 4 agent moves and its cell estimates — the audience bet |
| `python3 saper.py --vs` | human against the machine (the agent learns for ~10 seconds) |

Knobs: `--alpha --epsilon --seed` — in any mode; the amount of learning is `--episodes`
(in `--show` and `--vs` the same can be written as `--train-episodes`).

You can add `--sarsa` to `--show` and `--vs`: then SARSA plays and shows the board
instead of Q-learning: `python3 saper.py --vs --sarsa`.

**About `--seed`:** in `--show` and `--vs` it is the seed of the *board*, not of
learning — learning always runs on `--train-episodes` games with seed 42. That way
the bet boards reproduce exactly every time.

## Two strategies: how SARSA differs from Q-learning

The table, the step α, the exploration ε — all shared. The difference is one line:

```
Q-learning:  target = R + gamma * max Q(s', b)   # estimate of the best possible move
SARSA:       target = R + gamma * Q(s', a')      # estimate of its own move
```

Q-learning looks at the maximum over future cells, so it learns from the "ideal"
continuation; SARSA takes the move the agent will really make from s', together with
its random probes. The ladder shows where this leads: at ten thousand games SARSA
lags behind, at one hundred thousand it catches up, but its table is thicker — it
keeps estimates of the moves that were exploration too.

## Structure

| File | What is inside |
|---|---|
| `knobs.py` | all the letters in one list: FIELD, MINES, GAMMA, ALPHA, EPSILON |
| `game.py` | environment: mines, opening cells, end of the game |
| `base.py` | the Q table, ε-greedy choice |
| `qagent.py` | TD update of the table, Q-learning (off-policy) |
| `sarsa.py` | TD update, SARSA (on-policy) |
| `play.py` | run modes |
| `saper.py` | entry point: parsing flags and calling a mode |

## Game rules

- board 4 × 4, two mines; a cell is entered as "row column", for example `2 3`;
- reward: +1 everything open, −1 hit a mine, otherwise 0; γ = 1 (episodic task);
- state is what you see: closed cells and numbers. Mines hide behind closed cells —
  that is why the same picture can end both in a win and in a mine.

## Relation to lab 1

Here it is one player against the board; in the lab (tic-tac-toe) there is an opponent,
self-play and board symmetries. The recipe is the same: state → action → reward →
table → TD update.
