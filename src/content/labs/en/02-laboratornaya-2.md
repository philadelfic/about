---
number: 2
title: "Lab 2: the multi-armed bandit in a moving world"
summary: "Four channels with drifting means: the 1/n and α update rules, UCB, the gradient strategy, the role of ε. Your own environment included, four gaps in the code, five tables on your own seeds and twenty questions."
seminar: 4
issued: true
due: "13.11.2026, all groups"
---

Lab 2 is about choice in a world that does not stand still. The environment is small and entirely ours:
four channels, the mean rewards drift slowly, the reward is 0–2. You have to finish four places in the code,
take five tables on your own seeds and answer the questions — each about its own mechanism.

**What to submit:** `agent.py`, `environment.py` and a filled-in `tasks-and-report.md`. Nothing else:
`metrics.py`, `run.py` and `check.py` are measuring instruments, they are not edited and are not sent back.

**Deadline:** 13.11.2026, the same for all groups. One retake — at the eighth practical session (24.11 / 27.11).

## The assignment

Four channels `A`, `B`, `C`, `D` with means μ: 0.4 · 0.9 · 1.2 · 1.6. The reward is 0, 1 or 2, the probabilities
depend on μ piecewise linearly:

| μ | P(0) | P(1) | P(2) |
|---|---|---|---|
| μ < 1 | 1 − μ | μ | 0 |
| μ = 1 | 0 | 1 | 0 |
| μ > 1 | 0 | 2 − μ | μ − 1 |

The mean income of a channel equals μ, but the spread does not: it is zero at μ = 0, 1, 2 and maximal at μ = 0.5
and 1.5. At the edges the reward is deterministic, and at μ = 1 the channel always gives one and tells you nothing
about itself.

After every move the means of all four channels shift independently:

```
μ_c ← clip( μ_c + N(0, σ), 0, 2 )
```

where σ is the standard deviation of the step (0.1 by default), `clip` cuts to the bounds 0.0–2.0. The randomness
comes from `self.rng`: reproducibility by seed depends on it.

A run is 1000 steps: choose a channel → reward → update the estimate. The estimates start from zero, a tie is
settled by the first channel in alphabetical order. That is why the greedy strategy sticks to the very first channel
that gave a positive reward — and that is the main story of task 5.

Three metrics are counted per step: **income** (the mean reward), **share of the best** (how often the channel with
the maximal μ at the moment of the move was chosen, before the shift) and **regret** (the mean difference between
the best μ and the μ of the chosen channel).

## The statement

The agent here is a rule for choosing a channel; the environment is four drifting reward distributions; the action
is the choice of a channel; the reward is 0, 1 or 2; the strategy is ε-greedy, UCB or gradient. **There is no
state:** the situation does not change from the agent's actions, the agent does not affect the world, and it sees
only the reward of the chosen channel.

What makes this different from a full reinforcement learning problem is the absence of both a transition to the next
state and a horizon: every move is an independent trial. The knowledge of μ is not available to the agent, only to us
— and it is exactly what sets the ceiling: a share of the best of 100 % and a regret of 0 are unattainable in a
drifting world in principle, not because of a bad strategy.

## Files

| File | What it is |
|---|---|
| [agent.py](/about/files/course/rl/lab2/agent.py) | the agent: greedy, ε-greedy, UCB, gradient |
| [environment.py](/about/files/course/rl/lab2/environment.py) | the environment: channels, rewards, drift |
| [metrics.py](/about/files/course/rl/lab2/metrics.py) | metrics: income, share of the best, regret, IQR |
| [run.py](/about/files/course/rl/lab2/run.py) | runs, tables, studies, log |
| [check.py](/about/files/course/rl/lab2/check.py) | self-check: 18 items |
| [tasks-and-report.md](/about/files/course/rl/lab2/tasks-and-report.md) | questions and room for the answers |
| [lab-2-bandit.zip](/about/files/course/rl/lab2/lab-2-bandit.zip) | everything at once, in one archive |

## What to fill in

Four places, marked `raise NotImplementedError`. There are no ready formulas here on purpose: all of this was
discussed in class, and you write the code — otherwise `check.py` would have nothing to check.

**1. `Bandit.drift`** — every mean takes its own independent Gaussian step with spread σ and stays within the
segment 0…2 (the shift formula is above, in the description of the world).

**2. `Agent.update`, the `else` branch** — the estimate of a channel is pulled towards the reward that arrived:
with a constant step α, if one is set, and with a step of 1/n_c, if not. The line `if n == 1: q = r` is already
written — work out for which of the two step rules it is mandatory and what breaks if you remove it.

**3. `Agent.preferences`** — preferences are turned into probabilities by a soft maximum. Think about why the
maximum is subtracted from the score and what happens to the numbers if you do not do it.

**4. `Agent.ucb_score`** — the estimate of a channel plus a bonus for uncertainty: it grows with the number of the
move and falls with the number of visits to the channel. The case `n_c = 0` never reaches the formula — it is cut
off by `ucb_choice`; check that this is so.

What exactly to return and in what form — the text in `check.py` will tell you: it names the place and the broken
property.

## The order of work

Download the archive, unpack it, go into the folder and finish the code. Then step by step — every step gives the
material for one task.

```bash
cd lab-2-bandit
python3 check.py                                  # 18 self-checks; until it is green there is no point going on
python3 run.py --seeds 100 --offset 300 --log run_log.jsonl     # task 5: six strategies
python3 run.py --study rules --seeds 100 --offset 300           # task 6: 1/n against α; σ is swept by the script itself
python3 run.py --study eps --sigma 0.0 --seeds 100 --offset 300 # task 7: ε in a still world
python3 run.py --study eps --sigma 0.2 --seeds 100 --offset 300 # task 7: ε in a drifting world
python3 run.py --study ucb --seeds 100 --offset 300             # task 8: the price of trust c
python3 run.py --study eta --seeds 100 --offset 300             # task 8: the preference step η
python3 run.py --strategy greedy                                # task 5.3: the distribution of choices
```

**Each of you has their own seeds.** The number 300 in the commands is an example for the fourth person on the list
(numbering from one: `--offset 0`). Put `100 × (your number − 1)` and write the window down under the table.

Then your medians will not match anybody else's, and the conclusions must match — that is the check that you
understood the mechanism and did not fit the numbers.

Every table is a median and an IQR corridor over 100 seeds, not a single run. The cell format is copied from the
screen: income and regret as `1.41 [1.32–1.46]`, share of the best as `52% [45–57]`.

## How it is checked

Code: `python3 check.py` — eighteen `[ok]`. The checks catch not “looks about right” but concrete substitutions:
UCB without the estimate `q`, uniform “probabilities” instead of softmax, a step of `1/turn` instead of `1/n`,
σ squared, the drift of one channel instead of four, clipping on one side only.

Tables: five at 6 points each, cross-checked against a run on your seed window. Answers: 20 questions, 10 simple
at 1 point each and 10 key ones at 2 — 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 7.1, 7.2, 8.1, 9.2. Submission: 10 points for
the two code files and the filled-in answer file. A pass from 70 with a green `check.py`. An answer of “I don’t
know” — zero with no penalty; an answer without a number where a number is required — half a point.

## If it does not add up

* `check.py` prints `[no]` — read the text of the line: it says which place is empty and which property is broken.
* The table is there but the questions cannot be answered — almost always it means a “similar” rule was
  implemented. Cross-check against the formulas above.
* The numbers do not match the format example above — that is as it should be: it was taken without `--offset`.
