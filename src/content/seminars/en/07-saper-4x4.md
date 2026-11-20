---
number: 7
title: "Saper 4 × 4: the room against a value table"
summary: "A match: the room against one value table. Board 4 × 4, two mines, the state is the picture of closed cells and open numbers, the reward arrives only at the end of a game, γ = 1. We assembled the Q table and the TD update, walked the ladder of games (ten — 1.2 %, a hundred — 1.5 %, a thousand — 16.4 %, ten thousand — 68.6 %, a hundred thousand — 96.8 % against 0.5 % for a random player) and hit the 97.1 % ceiling: saper is not Markov, one picture hides up to thirty-six mine placements. We played five main bets, compared Q-learning with SARSA (one line of difference: at ten thousand games 68.6 % against 24.4 %, at a hundred thousand 96.8 % against 96.9 %), turned the knobs α and ε — both edges are bad — and moved on to lab 1: in tic-tac-toe 19 683 positions collapse to 765."
date: "17.11.2026 · 20.11.2026"
covered:
  - "Opened with a match: the whole room against one value table, board 4 × 4, two mines, five main bets — five points, the score is kept in the open"
  - "Answered why not chess: there are ten to the forty-seventh positions, a table of that size fits into no memory — so we take a game where it fits"
  - "Went through the letters: state is what you see (closed cells and numbers), action is the number of a closed cell, reward is plus one for the whole field open and minus one for a mine, γ = 1"
  - "Said out loud what is missing from the state — the mines: that, and not the size of the table, is what breaks the ceiling on slide twenty-six"
  - "Assembled the Q table: a pair “state, cell” — one number, starting from zeros, “I know nothing about anything”"
  - "Read the TD update term by term and recomputed the micro-example: 0 + 0.1 × (1 − 0) = 0.1 — the bracket is the difference between what we expected and what we got"
  - "Handed out the code (eight files, the same first command for everyone: selftest → ok) and ran the first games: ten thousand — a table of 21 914 pairs, greedy play 68.6 %"
  - "Played two main bets on boards after four agent moves: the first — +1.000 against +0.257 and +0.001, the second — a two is visible, and the agent is right again"
  - "Walked the ladder of games: 10 — 1.2 %, 100 — 1.5 %, 1 000 — 16.4 %, 10 000 — 68.6 %, 100 000 — 96.8 %; a random player — 0.5 %"
  - "Compared the two strategies: Q-learning and SARSA differ by one line of the update; at ten thousand games 68.6 % against 24.4 %, at a hundred thousand 96.8 % against 96.9 %, while the SARSA table is twice as thick"
  - "Found the ceiling: a million games in the background gave 96.2 %, a re-measurement on a hundred thousand — 97.09 % against 97.07 %; an analysis of twenty thousand games showed that all losses live in ambiguous positions"
  - "Understood why saper is not Markov: 1 965 960 states, but 1 482 870 observations and 12 638 204 pairs “observation, action”; a demo board hides up to six placements, the control board — thirty-six"
  - "Turned the knobs: α 0.001 → 66.9 %, 0.1 → 96.8 %, 0.9 → 89.5 %; ε 0.01 → 97.8 %, 0.1 → 96.8 %, 0.3 → 88.2 % — both edges are bad for different reasons"
  - "Played three team attempts (66.9 / 91.8 / 96.8 %) and the final “human against the machine” on the projector"
  - "Moved on to lab 1: 19 683 positions in tic-tac-toe → 5 478 reachable → 765 with symmetries; the acceptance criteria and deadlines are on the lab page"
tasks:
  - title: "Task 1. Why γ = 1 is not a mistake"
    text: "In the lectures γ discounted the future and was almost always below one. Here γ = 1. Why is that honest and not a simplification?"
    answer: "Because the task is episodic: a game is finite (at most fourteen moves), the sum of rewards is finite, there is no looping — there is nothing to discount. Discounting is needed where the horizon is infinite or where “sooner beats later”. Here the reward is single and arrives at the end, so γ = 1 only fixes that all moves of the chain are equally valuable. And this is an important difference from the cafe: there γ did not take part at all, because there was no episode."
  - title: "Task 2. What is missing from the state"
    text: "The state in the code is a tuple of sixteen numbers: −1 closed, 0…8 how many mines are among the neighbours. There are no mines in the state. Why is that the main property of the game and not an implementation detail?"
    answer: "Because the agent sees a picture, not a placement: the same picture is compatible with several mine placements (on the demo boards from two to six, on the control board 39 — thirty-six). So the transition “observation → next observation” is not uniquely defined, the Markov property is violated, and a table that averages incompatible continuations physically cannot reach one hundred percent. Hence the 97.1 % ceiling — not because of the size of the table."
  - title: "Task 3. The TD update on your fingers"
    text: "The estimate of a cell was 0, we opened it and the game ended in a win (reward +1), α = 0.1. What is the new estimate? And if we had hit a mine with α = 0.9?"
    answer: "A win: 0 + 0.1 × (1 − 0) = 0.1. A mine: 0 + 0.9 × (−1 − 0) = −0.9. The bracket is the TD error: the difference between what we expected (0) and what we got (+1 or −1). A small α moves the estimate by a step, a large one almost rewrites it with the last episode. In the code that is knobs.ALPHA and the flag --alpha."
  - title: "Task 4. Why ten games give only 1.2 %"
    text: "After ten training games greedy play wins 1.2 %, after a hundred — 1.5 %, after a thousand — 16.4 %. A game lasts eight or nine moves, so in ten games the agent saw about eighty moves. What does the number 39 pairs in the table tell us?"
    answer: "That the table is almost empty: thirty-nine records are not “learned badly” but “has not seen the board yet”. The first games almost all end on a mine after the second or third move, so only the initial observations get into the table, and the positions with numbers are never reached. The growth from 1.2 % to 96.8 % is not the strategy improving by itself, it is the table filling up: 2 575 pairs at a thousand games, 21 914 at ten thousand, 64 923 at a hundred thousand. Hence the rule: judging a method by ten games is meaningless."
  - title: "Task 5. SARSA caught up — and what did it pay?"
    text: "At a hundred thousand games Q-learning gives 96.8 %, SARSA — 96.9 %. At the same time the tables hold 64 923 and 110 558 pairs. Why does on-policy keep almost twice as much, and why does that not make it better?"
    answer: "SARSA learns the estimate of the move the agent will really make — together with random probes. So exploration moves, which greedy play will never choose, also get into the table: hence 110 558 pairs against 64 923. It adds no wins: in greedy play a thousandth of a percent is noise, while memory is spent twice over. At small volumes something else is visible: ten thousand games — 68.6 % against 24.4 %, because on-policy is more cautious and leaves exploration more slowly. The lesson of the session: “smarter” does not mean “more profitable”."
  - title: "Task 6. Why a million games did not help"
    text: "A hundred thousand games — 96.8 %, a million — 96.2 %. Growth stopped and even rolled back. How do you know this is noise and not degradation?"
    answer: "The evaluation runs on two thousand greedy games, and the standard deviation at 96.8 % is about 0.4 percentage points; so 96.2 % and 96.8 % are indistinguishable. A re-measurement on a hundred thousand games gave 97.09 % (a hundred thousand training games) and 97.07 % (a million), the difference is +0.013 p.p. with an error of 0.075 — zero. There is nothing more to learn: the point is not the number of games, but that some positions are fundamentally ambiguous."
  - title: "Task 7. Why the control board gives 0.994 and not 1.000"
    text: "On the demo boards the best estimate is always +1.000, on board 39 it is +0.994. There are thirty-six compatible placements, and the best cell is safe in thirty-three of them. Where does 0.994 come from, and why is it not a bug?"
    answer: "The machine takes the maximum over cells: the share of safe moves in a position is the maximum over compatible placements, not the average. 33 out of 36 is 0.917 of a “true” chance, while the table shows 0.994, because the maximum overestimates: it picks the placement where the cell is safe and does not pay for the others. That is the honest uncertainty of a POMDP, not a code error: in twenty thousand games all 580 losses happened exactly in such positions, and none on a cell with an estimate of +1.000."
  - title: "Task 8. Teams: why α 0.5 and ε 0.01 gave 91.8 %, not 96.8 %"
    text: "Three attempts against the machine: α 0.001 / ε 0.1 — 66.9 %, α 0.5 / ε 0.01 — 91.8 %, α 0.1 / ε 0.1 — 96.8 %. The second attempt “forgets fast and almost does not explore”. Why did it lose to the baseline?"
    answer: "Because the two knobs pull in different directions and one good knob does not save the other bad one. α = 0.5 is rapid memory loss: the table lives almost entirely on the last games, that is, on noisy estimates. ε = 0.01 is almost no exploration: new positions are not found, and the table fills one-sidedly (35 699 pairs against 64 923 for the baseline). The result 91.8 % is better than the almost non-learning agent (66.9 %), but worse than the baseline: the parameters only work together."
  - title: "Task 9. The bridge: 19 683, 5 478 and 765"
    text: "In tic-tac-toe 3 × 3 there are 19 683 positions if you write the board as it is — three to the ninth. Reachable ones — 5 478. And the table in the lab should come out at about 765. What happened at each step, and what matters more than the size of the table in the lab?"
    answer: "19 683 = 3^9: every cell is either empty, a cross or a nought. 5 478 — the unreachable ones are dropped (for example, where there are two more crosses than noughts). 765 — the board is symmetric: eight symmetries (four rotations times two reflections) collapse into one canonical record, and the table is kept only for it. In the lab the size matters less than the opponent: the agent plays against itself, and every position is recorded from the point of view of the side to move — those are the hardest parts of the assignment, and they are covered in the step-by-step guide."
materials:
  - title: "Class code — archive saper-en.zip (eight files, English)"
    href: "/files/course/rl/sem7/en/saper-en.zip"
  - title: "Instructions and hints — how to run it and what we do in class (MD)"
    href: "/files/course/rl/sem7/en/instructions-and-hints.md"
  - title: "Entry point: flags and modes (saper.py)"
    href: "/files/course/rl/sem7/en/saper.py"
  - title: "Run modes: selftest, random, train, ladder, show, vs (play.py)"
    href: "/files/course/rl/sem7/en/play.py"
  - title: "Environment: mines, opening cells, end of the game (game.py)"
    href: "/files/course/rl/sem7/en/game.py"
  - title: "The Q table and ε-greedy choice (base.py)"
    href: "/files/course/rl/sem7/en/base.py"
  - title: "TD update, Q-learning — off-policy (qagent.py)"
    href: "/files/course/rl/sem7/en/qagent.py"
  - title: "TD update, SARSA — on-policy (sarsa.py)"
    href: "/files/course/rl/sem7/en/sarsa.py"
  - title: "Simulator knobs: FIELD, MINES, GAMMA, ALPHA, EPSILON (knobs.py)"
    href: "/files/course/rl/sem7/en/knobs.py"
  - title: "MDP of saper 4 × 4 — the formal statement and the sizes of spaces (MD)"
    href: "/files/course/rl/sem7/en/mdp-saper.md"
  - title: "Slides of the session, group М80-203СВ-25 (17.11.2026) — PPTX, in Russian"
    href: "/files/course/rl/sem7/s7-saper-4x4-gr-m80-203-17.11.2026.pptx"
  - title: "Slides of the session, group М80-202СВ-25 (20.11.2026) — PPTX, in Russian"
    href: "/files/course/rl/sem7/s7-saper-4x4-gr-m80-202-20.11.2026.pptx"
---

## What we did in this class

This class was a match, not a lecture and not a review of submitted work. The room played
against one value table: board 4 × 4, two mines, everybody knows the rules from childhood.
Whoever opens all safe cells wins. Five main bets — five points: guessed — a point for the
room, missed — a point for the agent. Everything else was a warm-up.

The order was: why not chess, then the four letters (state, action, reward, discount), then
the table and the TD update, then the code handout and a workshop with two bets, then the
ladder of games, the ceiling and the knobs, and finally a volunteer against the machine on
the projector.

The main idea of the class: the 97 % ceiling is not about the size of the table and not
about the number of games. It is about saper not being Markov: the agent sees a picture,
and the picture does not determine where the mines are. That is exactly why the next piece
of work is tic-tac-toe, where the environment is Markov and the table is more honest.

## Why not chess, but saper

In chess there are about $10^{47}$ positions — a table of that size fits into no memory, and
no “let us simply learn everything” works. So we take a game where the table does fit:
a 4 × 4 board with two mines. The rules are the same as in real minesweeper: the number in
an open cell is the count of mines among its neighbours.

In tic-tac-toe 3 × 3, which we return to in the lab, there are $3^9 = 19\,683$ positions if
you write the board as it is; 5 478 of them are reachable, and 765 with symmetries taken
into account. That comes at the end of the class, in the bridge to the lab.

## Four letters: state, action, reward, discount

From here on everything is as in the lectures, only on a small board. Let us agree on the
letters once, so that we can talk about numbers afterwards.

### The state is what you see — and what it does not contain

The state is everything that is visible: which cells are closed and which numbers are open.
In the code it is a tuple of sixteen numbers: $-1$ — the cell is closed, $0 \ldots 8$ — how
many mines are among its neighbours.

The main point: **mines are not in the state**. They are somewhere under the cells, and this
is not an implementation detail but a property of the game from which the whole ceiling grows.
The same picture can hide different mine placements — and then the same state ends both in
a win and in a mine.

### The action is the number of a closed cell

The action is the number of a closed cell. Not a move in the chess sense, no tactics: you
point with your finger. If eleven cells are closed, there are eleven actions. The fewer cells
are closed, the smaller the choice — the game shrinks towards the end by itself.

### The reward lives at the end

The reward: $+1$ — everything safe is open, $-1$ — you stepped on a mine, $0$ — an ordinary
cell is open. Everything is decided at the end of the episode, intermediate moves are zeros.

Just as in the cafe γ was “resting” because the reward came right after lunch, here the reward
travels back along the chain of moves: to understand the value of the first cell you have to
know how the game ended five moves later.

### γ = 1 is not a mistake

In the lectures γ discounted the future. Here $\gamma = 1$. This is not a simplification: the
game is finite (at most fourteen moves), the sum of rewards is finite, there is no looping.
There is nothing to discount — the task is episodic. Gamma exists but equals one, and that is
honest.

## The Q table and the TD update

What is learned? A table: the pair “state, cell” → one number, the chance to win if this cell
is opened. The table starts at zeros: “I know nothing about anything”.

The table is corrected by the temporal-difference (TD) error. We compute it in one line and
update in another:

$$
\begin{aligned}
\delta &= r + \gamma \max_{b} Q(s',b) - Q(s,a) \\
Q(s,a) &\leftarrow Q(s,a) + \alpha\,\delta
\end{aligned}
$$

Read it term by term: δ holds the reward plus γ times the best estimate of the next position,
minus the old estimate. That difference is the TD error: what we expected against what we got.
The update is simple: the old estimate plus α times that error.

The maximum over future cells is an important detail: Q-learning learns from the best possible
continuation, not from the one the agent will actually take. This is off-policy; the
alternative comes below.

### A micro-example on your fingers

The estimate of a cell was $0$, we opened it, reached a win, $\alpha = 0.1$:

$$
0 + 0.1 \cdot (1 - 0) = 0.1
$$

If we had hit a mine with $\alpha = 0.9$: $0 + 0.9 \cdot (-1 - 0) = -0.9$. A small α moves the
estimate by a step, a large one almost rewrites it with the last episode.

## The ladder of games

Next comes the main experiment: the ladder. One run, steps 10 → 100 → 1 000 → 10 000 →
100 000 training games; after each step the agent plays greedily, without random probes, and
we measure what it has learned ($\alpha = 0.1$, $\varepsilon = 0.1$, evaluation on 2 000
greedy games, learning seed 42):

| Training games | Wins | Pairs in the table |
|---|---|---|
| 0 (random player) | 0.5 % | — |
| 10 | 1.2 % | 39 |
| 100 | 1.5 % | 342 |
| 1 000 | 16.4 % | 2 575 |
| 10 000 | 68.6 % | 21 914 |
| 100 000 | 96.8 % | 64 923 |

It reads like a story: thirty-nine records in the table are not a strategy yet, just first
impressions; a thousand games give 16.4 %, ten thousand — 68.6 %, a hundred thousand — 96.8 %.
A random player gives 0.5 %: the board forgives almost everything, because there are only two
mines out of sixteen.

### Two strategies, one line

Next to Q-learning lives SARSA: the same table, the same step α, the same exploration ε. The
difference is one line of the update:

$$
\begin{aligned}
\text{Q-learning:}\quad \delta &= r + \gamma \max_{b} Q(s',b) - Q(s,a) \\
\text{SARSA:}\quad \delta &= r + \gamma\, Q(s',a') - Q(s,a)
\end{aligned}
$$

After that both strategies update the table in the same way: $Q(s,a) \leftarrow Q(s,a) + \alpha\,\delta$.

SARSA takes the estimate of the move the agent will really make from $s'$ — together with its
random probes. That is why it is called on-policy: it teaches to value the line of behaviour
the agent follows.

On the ladder this is visible: ten thousand games — 68.6 % against 24.4 %, a hundred thousand —
96.8 % against 96.9 %. At small volumes on-policy lags behind, by a hundred thousand it has
caught up. The price is a table twice as thick: 110 558 pairs against 64 923, because
exploration moves live in it too. It caught up, but did not win: a thousandth of a percent is
noise, while the memory is spent.

## The ceiling: why 97 %, not 100 %

At first it seemed that the number of games was the issue. A million games in the background
gave 96.2 % — less than a hundred thousand (96.8 %). But the evaluation runs on two thousand
games, where the noise is about 0.4 percentage points — the numbers are indistinguishable.
A re-measurement on a hundred thousand games: 97.09 % (a hundred thousand training games)
against 97.07 % (a million), the difference is $+0.013$ p.p. with an error of $0.075$. There
is no growth.

So the ceiling is not in the number of games. It is in the game itself.

### How many states there are

The formal statement (full enumeration, we do not pick the numbers):

```
mine placements on the board:                        120
placements after the first click (a cell without a mine):  105
true MDP states (placement + opened cells):      1 965 960
the same with the “first click is safe” rule:    13 762 560
distinguishable observations (what the agent sees): 1 482 870
pairs (observation, action) in principle:       12 638 204
```

There are almost two million states, but only 1 482 870 distinguishable pictures: the same
picture corresponds to several placements. Formally this is a POMDP, and a table keyed on the
picture averages incompatible continuations. There is nowhere further to go — not because
there are few games, but because information is lost.

The demo boards: board 9 hides four placements, board 3 — four, board 7 — two, board 8 — two,
board 15 — six. On all these boards the best cell is safe in all compatible placements, and the
table honestly says $+1.000$. But that is not always so: on the control board 39 there are
thirty-six compatible placements, the best cell is safe in thirty-three, and the table says
$+0.994$ — the maximum over cells overestimates, because it picks the placement where the cell
is safe and does not pay for the others.

### Where the losses come from

A run with every decision recorded — twenty thousand games:

- 97.10 % wins, 580 losses;
- in 66 % of the games all decisions after the first move were exact ($Q = 1.000$), and in such
  games the agent won 100 %;
- in the remaining 34 % of games an ambiguous position occurred, the table said $0.994$, and
  there it won 91.5 % — all the losses are exactly here.

Not a single loss on a cell the agent considered safe. The ceiling is not in the size of the
table but in the positions where the picture does not determine the mines. A million games
will not remove them.

In the lab the environment will be Markov — and there the table is more honest. That word will
come back at the acceptance.

## The knobs: α and ε

### α — the forgetting rate

| α (with ε = 0.1) | Wins |
|---|---|
| 0.001 | 66.9 % |
| 0.1 (baseline) | 96.8 % |
| 0.9 | 89.5 % |

Both edges are bad, but for different reasons: at 0.001 the table does not have time to learn —
old mistakes sit in it; at 0.9 it trembles, the last game erases what was learned. For
reference, not read aloud in class: 0.01 gives 97.2 %, and 0.5 — 97.1 %, so the middle works
no worse than the baseline.

### ε — the share of random probes

| ε (with α = 0.1) | Wins |
|---|---|
| 0.01 | 97.8 % |
| 0.1 (baseline) | 96.8 % |
| 0.3 | 88.2 % |

Few probes — the board is not covered, the agent is stuck in its habits; many probes — a third
of the games goes at random, and the table learns randomness. Why is 0.01 not a failure?
Because there are only two mines out of sixteen: a random move is rarely fatal here. A small
environment forgives — a large one will not.

## Teams against the machine

| Attempt | α | ε | Wins | Pairs in the table |
|---|---|---|---|---|
| 1 | 0.001 | 0.1 | 66.9 % | 111 562 |
| 2 | 0.5 | 0.01 | 91.8 % | 35 699 |
| 3 | 0.1 | 0.1 | 96.8 % | 64 923 |

The second attempt is telling: it forgets fast and almost does not explore — 91.8 %. The knobs
only work together: one good knob does not save the other bad one.

## The bridge to lab 1

The first bet of the class was about tic-tac-toe: how many different positions are there?
The answer: $3^9 = 19\,683$ if you write the board as it is; reachable — 5 478; and the board
is symmetric — rotate it, reflect it, the same position, eight symmetries collapse into one
canonical record, and 765 remain. It fits into an Excel sheet.

But the main difference of the lab is not the size of the table. There an opponent appears:
the agent plays against itself (self-play), and every position is recorded from the point of
view of the side to move. Those are the hardest parts of the assignment; they are covered in
the step-by-step guide.

The acceptance criteria are five points, without which the work is not accepted: a formal
statement (state, action, reward, γ = 1 with justification), a hundred independent runs per
point, the median and the interquartile range, at least three conclusions — each with a number
from your own runs, and a log file that the numbers in the report must match.

## What to take away

Five phrases from the class:

1. The state is what you see, and in saper that is not enough: mines are not in it.
2. The reward lives at the end of the episode and flows back along the chain of moves — that is
   why γ = 1 is honest here.
3. The table learns on tens of thousands of games, not on five: 39 records are not a strategy yet.
4. Both edges of α are bad — remembering forever and forgetting instantly; for ε only the upper
   edge is bad in this small environment.
5. The ceiling is not in the size of the table but in the positions where the picture does not
   determine the mines. Saper is not Markov.

## How to repeat it at home

The code is eight files side by side, nothing to install. The first command is the same for
everyone:

```
python3 saper.py --selftest
```

Then:

```
python3 saper.py --train --episodes 10000
python3 saper.py --ladder --episodes 100000
python3 saper.py --sarsa --ladder --episodes 100000
python3 saper.py --show --seed 9 --after 4
python3 saper.py --vs
```

The knobs `--alpha --epsilon --seed` work in any mode. Details, the order of the games,
reference numbers and pitfalls are in the file “Instructions and hints”.
