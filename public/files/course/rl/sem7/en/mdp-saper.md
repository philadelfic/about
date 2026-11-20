# MDP of saper 4 × 4

The formal statement for the game from seminar 7: board 4 × 4, two mines, the first opened
cell is safe. The numbers are computed by `tools/mdp_saper.py` (full enumeration, no sampling).

## Statement

| Element | What it is in saper |
|---|---|
| **S** — state | the pair "mine placement + set of opened cells". Mines are hidden, so only the environment knows the state |
| **A** — action | the number of a closed cell (1…16); the number of legal actions equals the number of closed cells |
| **P** — transition | deterministic: a cell without a mine opens and shows a number — the count of mines among its neighbours; a mine ends the game |
| **R** — reward | −1 for a mine, +1 when all safe cells are open, otherwise 0 |
| **γ** | 1: the episode is finite (at most 14 moves), there is nothing to discount |

## How many of everything

```
mine placements on the board:                        120
placements after the first click (a cell without a mine):  105
true MDP states (placement + opened cells):      1 965 960
the same with the "first click is safe" rule:    13 762 560
distinguishable observations (what the agent sees): 1 482 870
pairs (observation, action) in principle:       12 638 204
```

## Why this is a POMDP for the agent, not an MDP

The agent does not see where the mines are. It sees an **observation**: which cells are
closed and which numbers are open. The same picture corresponds to several placements —
on the demo boards of the seminar there are 4 / 2 / 2 / 4 / 6 of them, and on the control
example (board 39) thirty-six. That is why the transition "observation → next observation"
is not uniquely defined: the same picture can turn into a win and into a mine.

Two things follow, and both are said in class:

* the agent's table is keyed on the observation, not on the state — that is exactly what
  "saper is not Markov" means;
* the ceiling of greedy play (97.1 %, slide 26) is not about the size of the table but
  about the positions where the picture does not determine the mines. The exact share of
  safe moves in such a position is the maximum over cells of the number of compatible
  placements.

## How full the table is

Out of 12 638 204 possible pairs "observation, action", after 100 000 games:

| Strategy | pairs in the table | share |
|---|---|---|
| Q-learning | 64 923 | 0.5 % |
| SARSA | 110 558 | 0.9 % |

Half a percent — and 96.8 % of wins: most observations simply never occur in greedy play.
The same explains why SARSA (0.9 %) is not better: it honestly keeps more, exploration
moves included.

## Where this is in the materials

* slides 13–14 — this statement in the deck: "MDP: what to assemble" and "Our MDP: saper 4 × 4";
* slide 24 — two strategies on one table;
* slides 25–26 — the ceiling and "why it is not Markov";
* the run protocol (Russian) — all the numbers the slides refer to.
