---
number: 3
title: "The multi-armed bandit: choosing without a model of the world"
summary: "The first method in the course with neither a model of the environment nor states: one choice per sprint, the reward arrives at once, and the world has to be learned by trial. What a bandit is and how its step works, why ε is needed, why optimistic initialisation collects a hundred per cent of hits and how UCB evens out the arms with a bonus for uncertainty. Five strategies, the reference numbers and three gaps in the session code."
date: "20.10.2026 · 23.10.2026"
covered:
  - "Went through what a multi-armed bandit is: one choice per sprint, the reward at once, no state, no model of the world"
  - "Went through the one-armed bandit — there is no choice, only estimation is left — and where that lives: slot machines, an A/B test, medicine doses, recommendations"
  - "Went through five strategies: greedy, ε-greedy, optimistic initialisation, UCB and gradient"
  - "Went through how the estimate moves: q and a counter instead of a history, the step 1/n against a constant step α"
  - "Assembled the reference: greedy 0.31 and 0 %, ε 1.12 and 76 %, optimistic 1.26 and 100 %, UCB 1.22 and 93 %, gradient 1.24 and 94 %, ceiling 1.3"
  - "Put the numbers of the pairs into a table and checked them against the reference, went through the discrepancies"
  - "Filled in two gaps in the code — the update rule and the ε-greedy choice — and ran our own numbers"
  - "Gave the homework: fill in two places, run it and put together a report with three conclusions"
tasks:
  - title: "Task 1. Why ε and not greedily"
    text: "The greedy strategy pulls the arm with the best estimate and gets 0 % of the choices for arm C, an average return of 0.31 against 1.12 for ε-greedy. It does update its estimates with the 1/n rule. So why does it not find the best arm?"
    answer: "Because it does not try: the very first arm that happened to pay a lot stays “the best” forever — the other estimates do not move, there is nothing to compare. ε-greedy spends a share of the steps on random trials, and that pays off: 76 % of the choices for arm C against zero. Exploration is not a loss, it is the price of getting any estimates at all."
  - title: "Task 2. Why optimistic initialisation gives 100 %"
    text: "The optimistic strategy starts from an inflated estimate Q₀ = 5 and gets 100 % of the choices for arm C — more than ε-greedy. What does it do instead of random trials?"
    answer: "It makes the trials systematically: any untouched arm looks better than an already checked one, because its estimate has not yet come down from 5 to the real value. So the agent checks all the arms in turn, and after the first series the estimates pull the best one. This is exploration “through greed”: ε is not needed, but the right start is — and the same start is a mistake if Q₀ is guessed wrong."
  - title: "Task 3. What UCB does"
    text: "UCB gives 93 % and needs neither ε nor a lucky start: it adds a bonus for uncertainty to the estimate. How is that bonus tied to the arm’s counter, and why does it even out the choices?"
    answer: "The bonus grows when the arm has been pulled little: it is the larger the smaller n is for that arm, and the smaller the more sprints have passed. So a rarely tried arm gets a chance even if its estimate is not the best right now — and the counters of the arms even out. The price is c: too large a bonus turns the agent into an explorer, too small returns it to greedy."
  - title: "Task 4. Where the ceiling of 1.3 comes from"
    text: "The best average of the three levers is 1.3. No strategy overtakes that number, although the gradient one comes right up to it — 1.24. Why is 1.3 the ceiling, and what should a strategy do to reach it?"
    answer: "The ceiling is the return of the arm with the maximum average: 0·0.1 + 1·0.5 + 2·0.4 = 1.3 for arm C. You can reach it only by always choosing C. None of the strategies in our set does that: ε spends 10 % on trials, UCB — on challenges, the gradient one — on the soft maximum. Hence 93–94 % and a return just below the ceiling: the rest is the price of exploration, without which you cannot learn that C is the best."
assignment:
  title: "Assignment: fill in two places, run it and put together a report"
  text: "Two empty places are left in agent.py. All the assignments are in task-and-report.md: eight of them in order, from two lines of code to three conclusions with numbers, each with its own “Answer:”. That same file is handed in, there is no separate report."
  files:
    - title: "The environment — environment.py"
      href: "/files/course/rl/sem3/environment.py"
    - title: "The agent — agent.py (two gaps)"
      href: "/files/course/rl/sem3/agent.py"
    - title: "The run — run.py (--png, --exp)"
      href: "/files/course/rl/sem3/run.py"
    - title: "Assignments and report — task-and-report.md"
      href: "/files/course/rl/sem3/task-and-report.md"
  homework:
    title: "Homework for seminar 3 — what to fill in, what to run and what to send"
    href: "students/mai/rl/homework/06-domashnee-zadanie-po-seminaru-3/"
materials:
  - title: "The environment — environment.py"
    href: "/files/course/rl/sem3/environment.py"
  - title: "The agent — agent.py (with the gaps, as it was handed out in class)"
    href: "/files/course/rl/sem3/agent.py"
  - title: "The run — run.py (-png and -exp)"
    href: "/files/course/rl/sem3/run.py"
  - title: "Session presentation, group М80-203СВ-25 (20.10.2026) — PPTX"
    href: "/files/course/rl/sem3/s3-mnogorukij-bandit-gr-m80-203.pptx"
  - title: "Session presentation, group М80-202СВ-25 (23.10.2026) — PPTX"
    href: "/files/course/rl/sem3/s3-mnogorukij-bandit-gr-m80-202.pptx"
---

## What we did in this session

Up to now the course always had a model of the world: we knew where an action leads and with what probability.
The bandit is the first method in the course with **neither a model nor states**: there are several arms with unknown
averages, **one choice** is made per sprint, and the reward arrives at once. The world has to be learned
only by trial — and the whole struggle is about how to divide the sprints between exploration and exploitation.

The order of work was this: we went through what a bandit is and how its step works, went through five strategies,
looked at how the estimate moves, then ran our own numbers and checked them against the reference.

## The bandit: how the step works

Four features by which the setting is recognised:

* **one choice** — per sprint we pull exactly one arm;
* **the reward at once** — there is no delayed reward and no horizon;
* **there is no state** — what happened before does not change the rules of the game (in the non-stationary version
  the payoffs themselves change, but not the state);
* **there is no model of the world** — the probabilities of the outcomes are unknown, there is nobody to ask.

Hence the working unit of measurement — a **sprint**: choice → reward → update of the estimate. And the first conclusion
of the session: if there is no choice at all (a one-armed bandit), the task reduces to estimating an average, and the whole difficulty
of the multi-armed one is that several arms have to be estimated while the sprint is one.

## Five strategies

| Strategy | How it chooses | What it pays with |
| --- | --- | --- |
| greedy | the maximum over the current estimates | does not try: gets stuck on the first lucky arm |
| ε-greedy | with probability ε — at random, otherwise greedily | a fixed share of trials even at the cost of a good arm |
| optimistic | greedily, but the start of the estimates is inflated (Q₀ = 5) | you have to guess the scale of Q₀ |
| UCB | the estimate plus a bonus for uncertainty | the constant c: large — an explorer, small — greedy |
| gradient | a soft maximum over the preferences | a small step and a non-zero probability of a bad arm |

## How the estimate moves

The estimate is a number and a counter, not a history of observations: `q` and `n` per arm. The update rule
shifts the estimate by a step multiplied by the difference between the reward and the estimate. The step can be **1/n** — an honest
average over the whole history, or **α** — a constant step that forgets the old. In this session the world still
stands, and both work; in a moving world 1/n will start to lose — that is the next session.

## Reference numbers

One run of 1000 sprints, seed = 7. The first number is the average return per sprint, the second is the share of choices
for arm C, whose true average is the maximum (1.3).

| Strategy | Return per sprint | Share of choices for arm C |
| --- | --- | --- |
| greedy | 0.31 | 0% |
| ε-greedy, ε = 0.1 | 1.12 | 76% |
| optimistic, Q₀ = 5 | 1.26 | 100% |
| UCB, c = 2 | 1.22 | 93% |
| gradient | 1.24 | 94% |
| ceiling (always C) | 1.30 | 100% |

What to read in the table:

* **greedy is worse than guessing**: it never chose C even once — its estimates of the other arms did not move;
* **nobody gets above 94 % except the optimistic one**: ε spends 10 % on trials, UCB and the gradient one —
  on challenges and the soft maximum. That is the price of exploration;
* **100 % for the optimistic one** is not magic: the inflated start forces it to check all the arms one after another,
  after which greed pulls C at once.

## What to take from the session

* **a bandit is a setting without a model and without states**: what matters is not the name but the four features;
* **every strategy is a trade-off** between exploration and exploitation, and each has its own knob:
  ε, Q₀, c or the step;
* **strategies have to be compared by two numbers at once**: the return says “how much we got”, the share of the best —
  “whether we chose right”; one without the other lies;
* **the code is the same formulas**: the two gaps in `agent.py` — the update rule and the choice of action —
  are the whole strategy.
