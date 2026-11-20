---
number: 5
title: "Tournament of strategies"
summary: "The whole session is about how to measure a result: one run proves nothing, so we compare medians and corridors, change exactly one thing and put a number on the uncertainty. Plus the game itself: a draft of ten configurations, runs on a shared world, a leaderboard and a rematch on another world, where everybody ran the winner's configurations together — two champions and 75% for config 5 on world 1 against 71% for config 6 on world 2."
date: "06.11.2026"
covered:
  - "We formed the teams and played the tournament: a draft of ten configurations, runs on a shared world, a leaderboard and a rematch on another world"
  - "We worked out why one run proves nothing: the distribution of returns is not Gaussian, the middle is dense and the tails are long"
  - "We introduced the corridor — the central 50% of runs — and agreed when to write “hint” and when “difference”"
  - "We read the output of tournament.py and the spread() function: three percentiles and no magic"
  - "We went through the knobs of the strategies: ε, α, c and η — a strategy with knobs is a family, not a single strategy"
  - "We went through calibration: how to put a number on uncertainty — the penalty as the distance from the bet to the outcome, and 50% as a legal “I don’t know”"
  - "We played two worlds: the first was won by config 5, the second by config 6; in the rematch the team with the best return named the configurations and everybody ran them together"
  - "We summed up the four skills we take away from the session"
tasks:
  - title: "Task 1. What IQR is, in your own words"
    text: "This was in the independent work. What is that range — the interquartile range — why is it about the middle and not about the edges, and why do we take it instead of the ordinary range?"
    answer: "It is the corridor from the 25th to the 75th percentile: half of the runs lie inside it, and the tails do not pull it. Those are exactly the brackets you see in the output of the script: “67% [66–68]”. We need it instead of the range because the range is counted from the minimum to the maximum and rests on the two outermost runs: for a good strategy and for a bad one it comes out equally wide and says almost nothing about the typical result."
  - title: "Task 2. What the brackets in the output mean"
    text: "The script prints the line “config 6 (UCB c2 · 1/n) | share of the best 67% [66–68]”. One and the same number, but in one place with brackets, in another without. What exactly does the corridor give, and why does the number read differently without it?"
    answer: "Without brackets the number reads as “exactly that much”: one measurement, one random story. With brackets — as “that much, give or take the corridor”: the median is 67%, and the central 50% of runs landed between 66% and 68%. For config 6 the corridor is narrow — it holds from run to run; for the greedy one on world 2 the corridor is [24–38] — that is 14 points at a median of 38, and there a single number without brackets misleads more than anywhere else."
  - title: "Task 3. A neighbour caught a run above his corridor"
    text: "You ran a config and got a median with a corridor, and your neighbour on the same config and the same world got one run noticeably better than the upper edge of the corridor. Did he make a mistake, rig it, or does that happen?"
    answer: "It happens: that is the right tail of the distribution. The corridor covers exactly half of the runs, so the other half lies beyond its edges — part above, part below. The conclusion “the neighbour has found a better strategy” would be a mistake: a strategy is judged by its distribution, not by a single run. If, though, the numbers did not match at all between you and your neighbour on the same config and world — that is already a reason to look at his script: the world and the seed are hard-wired, the numbers are bound to match."
  - title: "Task 4. The penalty for three bets"
    text: "Three events, three of your bets: 70, 80 and 60 percent. The outcomes: happened, did not happen, happened. What is your penalty, and what does it say about your calibration?"
    answer: "The penalty is the distance from the bet to the outcome, and the outcome is 100 or 0. First event: 100 − 70 = 30. Second: 80 − 0 = 80. Third: 100 − 60 = 40. The sum is 150. The smaller the sum, the better the calibration: someone who bet 50 on everything would get 50 + 50 + 50 = 150, that is exactly as much as you with your confidence. A confident bet pays off only if it hits more often than it promises."
  - title: "Task 5. “Hint” or “difference”"
    text: "On world 1 the configs gave 75% [74–78], 67% [66–68] and 67% [64–69]. About which pairs can you write “difference”, and about which only “direction”?"
    answer: "75% [74–78] against 67% [66–68] — the corridors do not overlap, that is a difference, write it boldly. 67% [66–68] against 67% [64–69] — the medians coincide, the corridors overlap almost completely, by these numbers the configurations are indistinguishable: the honest wording is “hint”, “in that direction”. The rule is one and the same in every report: there is an overlap — “hint”, there is no overlap — “difference”."
  - title: "Task 6. Which of the two champions is the real one"
    text: "World 1 was won by config 5 (75%), world 2 by config 6 (71%). Different configs, different worlds, both victories obtained on one and the same script. Which of them is really the stronger one?"
    answer: "One world cannot tell you: the configurations win in different realisations of one and the same drift, and the difference between them is a question of the luck of a particular world. The answer comes not from a single world but from the median and the corridor over many worlds and seeds: if the corridors diverge — a difference, if they overlap — a hint. That is why the rule sounded at the session: we draw the conclusion from the distribution, not from whoever came first in the table."
materials:
  - title: "Session code — the tournament of strategies tournament.py"
    href: "/files/course/rl/sem5/tournament.py"
  - title: "Walkthrough of the tournament code — what is written and why (MD)"
    href: "/files/course/rl/sem5/tournament-razbor.md"
  - title: "Session slides, both groups (06.11.2026) — PPTX"
    href: "/files/course/rl/sem5/s5-turnir-strategiy-gr-m80-203-i-202.pptx"
---

## What we did in this session

The previous sessions answered the question “which strategy to choose”. This session answered another one:
**how to know that the choice was right**. So instead of new theory there was a game — a tournament of strategies,
in which four teams drafted configurations, ran them on a shared world, put percentages on the outcomes
and played a rematch on another world. All the new theory grew out of what was happening on the screens:
first “why does everybody get the same numbers”, then “what do the brackets mean”, then “why are there
different champions in the two worlds”.

The order was this: a short mini-lecture on three points and two new pieces (the knobs of the strategies and calibration),
then everybody ran `tournament.py` themselves and read its output, then the draft, the runs, the leaderboard and the rematch,
and at the end — a summary with two champions and the rule of corridors.

## One run proves nothing

**A run** is one game played: a thousand sprints, one random story. Inside a run the agent
learns, makes mistakes, finds a good arm or does not, and all of it depends on how the first
rewards fell and where the drift had managed to go.

The distribution of returns is **not Gaussian**: the middle is dense, the tails are long. There are rare runs
noticeably better than the typical one, and rare ones noticeably worse, — and from one such run you cannot
say anything about a strategy. Hence the rule that worked all day: we speak not about a run,
but about the distribution — **the median and the corridor**.

**The median** is the middle of the list: half of the runs gave less, half more. One outlier will not move it,
and that is exactly why it suits distributions with long tails, while the arithmetic mean does not:
rare lucky runs pull the mean up, to where the typical run does not live.

## A fair comparison

**A configuration** is a strategy plus the values of its knobs. In a comparison we change exactly one thing —
the configuration — and keep everything else the same: the same world, the same number of sprints, the same set
of agent seeds. Change two things at once and the effect cannot be attributed to either of them.

**A world** is a concrete realisation of the drift. The script has three worlds, and the drift path is computed
from the seed of the world (`777 + world number`) and **does not depend on the configuration**: one and the same
array of increments is fed to all ten configurations and to all teams. Hence the answer to the question that
sounded first at the session: everybody gets the same numbers, because the world is one and the script is
deterministic. That is a fair comparison in action.

An important caveat, said out loud separately: fairness of comparison does not promise a fair outcome.
It is about one world — in it everybody was on equal terms, but the world itself could play into the hands
of one configuration.

## Three metrics of one run

The script prints three numbers per configuration, and all three are a median with a corridor:

* **return per sprint** — how much the agent earned on average per step;
* **share of the current best** — what part of the sprints it pulled the arm that had at that moment
  the maximum average. This is the main metric of the session;
* **regret** — how much on average it fell short of the current best.

The key detail: the share of the best and the regret are counted **by the true averages `mu`, not by the rewards**.
The environment knows which lever is the best at that moment; the agent does not see those averages — it sees only
the reward with noise. So the metric answers the question “did the agent guess the best one at that moment”, not
“how much did it earn”: the agent can earn decently on the second arm and still fail to guess the best one.

Here is what one line of the output looks like — configuration 6 on world 1:

```
world 1 · 30 agent seeds × 1000 sprints
config  6 (    UCB c2 · 1/n) | share of the best    67% [  66– 68]
                             | return  1.53 [1.52–1.54] | regret  0.12 [0.12–0.13]
```

## Corridor: median and quartiles

**The corridor** is the central 50% of runs. It is counted like this: sorted the runs by the metric, cut off
a quarter from each end, and the half that is left is the corridor. Its edges are the 25th and the 75th percentiles,
it is the interquartile range, IQR; at the session we agreed to say simply “corridor”.

Hence the reading of the entry **67% [66–68]**: in a typical run the strategy pulled the current best in 67%
of the sprints; a quarter of the runs was below 66%, a quarter above 68%, half — inside. The width of the corridor
68 − 66 = **2 points** is exactly the spread of the strategy in this metric.

Two things people stumble over most often:

* **the corridor is not symmetric**, and “median ± half-width” does not come out of it: for [66–68] the half-width is
  1 point, while for the greedy one on world 2 [24–38] at a median of 38 it is 14 points down and 0 up. The symmetric
  measure is the standard deviation, it is in the report, but not instead of the corridor;
* **it is not the min–max range**. For the greedy one on world 2 the corridor is [24–38], and beyond its edges live runs
  that have nothing to do with the typical result.

### Where the brackets come from: spread()

All the “magic” of the corridor is three lines. The function from the script in full:

```python
def spread(values):
    # median and corridor: sorting and quartiles
    m = float(np.percentile(values, 50))
    a = float(np.percentile(values, 25))
    b = float(np.percentile(values, 75))
    return (m, a, b)
```

Three percentiles, nothing more: the 50th is the median, the 25th and the 75th are the edges of the corridor. Everything else in the output
of the script is decoration.

### Why not the range

The range — from the minimum to the maximum — sees only the tails. For a good strategy and for a bad one it comes out
equally wide, because it is determined by the two outermost runs out of thirty, and it says nothing about the typical
result. The corridor shows the dense middle, that is why the tables carry only it.

From this it also follows that **a single run does not count as a result** — neither a high one nor a low one.
A run above its corridor is neither a mistake nor a cheat: the corridor covers exactly 50%, and the second half
of the runs lies beyond its edges by definition.

### The rule of corridors

One rule for all reports and all conversations:

* the corridors **overlap** — we write “hint”, “direction”, “in that direction”;
* the corridors **have diverged** — we write “difference”, and we write it boldly.

The words “hint” and “difference” were introduced officially at the session: before that we only recorded the fact
of the overlap itself, and the interpretation came later, in the summary.

## The knobs of the strategies

The second new piece — that the strategy in our hands is not one, but one with knobs. Four knobs, and each
means exactly one thing:

| Knob | What it is | A large value | A small value |
| --- | --- | --- | --- |
| **ε** (epsilon) | share of sprints at random | more tries | stuck on the favourite |
| **α** (alpha) | forgetting rate | we believe the fresh | we remember the old |
| **c** | greed for buying uncertainty | frequent tries | exploitation |
| **η** (eta) | rate of preferences | sharply | smoothly |

Hence the main idea: **a strategy with knobs is a family, not a single strategy**. The phrase
“UCB wins” without the values of the knobs is a phrase without meaning: the same UCB with `c = 1` and with `c = 4` behaves
differently.

### The update rule — a separate axis

Inside a strategy there is one more fork that we passed on the previous sessions, and here it became
an axis of comparison: **how the estimate is updated**. The `1/n` rule is the honest average over the whole history of the arm.
The `α` rule is a constant step: the old is forgotten, the weight of the fresh observation does not fall, and the memory window
is roughly `1/α` sprints.

One and the same strategy with a different rule gives different numbers, so one should look not at the name of the
strategy but at the configuration as a whole. The menu has pairs where exactly one thing changes: 3 and 8 —
the rate of preferences `η`, 4 and 10 — the share of tries `ε` under one and the same `1/n` rule. The other pairs
change along two axes at once: 5 and 6 differ both in `c` and in the rule, 1 and 9 — both in `ε` and in `α`. Such pairs
read as “configuration against configuration”, not as “the influence of one knob”: the difference cannot be attributed
to a single parameter here.

## Calibration

The third new piece — about how to talk honestly about uncertainty.

**Calibration** is the honesty of an estimate expressed as a number. A good forecast is not the one that guessed right, but the one whose
stated frequency comes true: out of ten events with an estimate of 70%, seven happen. A bad forecast is a
guessing one: it says “it will certainly happen” and is sometimes right.

You can count it like this. **The penalty** is the distance from the bet to the outcome: you bet 70 and it happened — the penalty is 30;
you bet 70 and it did not happen — 70. The sum over several events is the number: the smaller the sum, the better
the calibration.

**Fifty percent is a legal but expensive “I don’t know”**: it never gives a big penalty and never
gives a small one. Boldness is not accuracy: a confident bet pays off only when it hits
more often than it promises.

And the main thing: **a forecast and a win are different skills**. A calibrated estimate does not make a configuration
stronger, and it does not make the one who gave it a champion: one we trust, the other is lucky.

## How the game went

The rules were arranged as the design of a game, not as prohibitions:

* **we do not edit the script** — it is deterministic, the seed of the world is hard-wired, any edit is immediately visible from the numbers
  that did not match your neighbour’s;
* **in the rematch the winner names the configurations** — the team with the best return on world 1 says which configurations
  it has, and everybody runs them together: the numbers are the same for all, there is nothing to rig;
* **nobody hints at a strong configuration** — the draft is blind, as in sport.

The game itself went like this. The draft: a menu of ten configurations, the choice in a snake (1-2-3-4-4-3-2-1), two configurations
per team — insurance and tactics, five minutes to choose, the picks into the chat. Then the runs of your two configurations
on world 1 and the result line into the chat in full, by copy-paste. From those lines we built the leaderboard of world 1
and found the team with the highest return. Then the rematch: world 2, and here you ran not your own configurations
but theirs — all together, everybody getting the same numbers. The winner was named by the common run, not by anyone's
word: hence the two champions — different configurations won different worlds.

The draft menu (the order is not by strength — that is the point):

| No. | Strategy | Knobs |
| --- | --- | --- |
| 1 | ε-greedy | ε 0.05 · α 0.1 |
| 2 | UCB | c 4.0 · 1/n |
| 3 | gradient | η 0.05 |
| 4 | ε-greedy | ε 0.2 · 1/n |
| 5 | UCB | c 1.0 · α 0.1 |
| 6 | UCB | c 2.0 · 1/n — the honest average |
| 7 | greedy | — |
| 8 | gradient | η 0.2 |
| 9 | ε-greedy | ε 0.1 · α 0.3 |
| 10 | ε-greedy | ε 0.02 · 1/n |

## What the tournament showed

The design of the world in the script: five levers, starting averages 0.3 / 0.7 / 1.1 / 1.5 / 1.9, drift step
σ = 0.05, the averages live within the bounds 0.1–1.9, 1000 sprints per run, 30 agent seeds per pair “configuration × world”,
reward noise 0.3.

Share of the current best, median [corridor]:

| Configuration | World 1 | World 2 |
| --- | --- | --- |
| 5 — UCB c 1 · α 0.1 | **75% [74–78]** | 66% [61–69] |
| 6 — UCB c 2 · 1/n | 67% [66–68] | **71% [70–73]** |
| 9 — ε 0.1 · α 0.3 | 67% [64–69] | — |
| 7 — greedy | 0% | 38% [24–38], sixth place |

What reads here:

* **different worlds — different champions**. On world 1 the best is configuration 5 (75%), on world 2 — configuration 6
  (71%), and both victories are honest: the configurations swapped places not because someone made a mistake, but because
  their luck differs in different realisations of the drift;
* **the corridors of 6 and 9 on world 1 overlap** (67% [66–68] against 67% [64–69]) — by these numbers
  the configurations are indistinguishable, the honest word here is “hint”. While 5 against 6 — 75% [74–78] against
  67% [66–68] — is already a difference;
* **the greedy one on world 1 is zero percent**: it does not explore at all, once it convinces itself of a randomly
  lucky arm and never lets it go;
* **on world 2 the greedy one rose to sixth place** — 38% [24–38], overtaking configurations 4 (22%),
  8 (20%), 3 (19%) and 10 (16%). Its corridor is wide, though: this is exactly the case of
  “the greedy one got lucky”, and that is why a single world proves nothing.

## Four skills

* **one run proves nothing**: it is the median that is stable, not the mean, and a result is a median
  with a corridor;
* **a fair comparison**: we change one thing, we keep the same world and the same number of sprints — otherwise the effect
  cannot be attributed to either of them;
* **corridors**: an overlap — “hint”, they diverge — “difference”;
* **calibration**: putting a number on uncertainty, fifty is a legal “I don’t know”, boldness is not
  accuracy.

It is these four that are worth keeping in mind when you run your configurations at home: without them any number in a table is just a number.

## How to repeat it at home

You need Python 3.8+ and numpy; everything else is the script itself.

```bash
# one config on one world
python3 tournament.py --config 6 --world 1

# all ten configurations in a row, 3–4 seconds
python3 tournament.py --config all --world 2
```

Three worlds are three realisations of one and the same drift. Run any configurations on any world,
compare not the numbers but the corridors, and check that your neighbour on the same config and world has the same numbers:
if not — the file was edited. We do not edit the script itself: any edit breaks both the comparison and the trust
in the result. Your own experiments — with your own scripts, the tournament script remains the reference.
