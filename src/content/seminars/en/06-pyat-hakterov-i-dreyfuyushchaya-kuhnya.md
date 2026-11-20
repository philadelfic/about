---
number: 6
title: "Five characters and a drifting kitchen"
summary: "Lab 2 live in the cafe simulator “where to have lunch”: four groups of three dishes each, five character-strategies and a world that knows how to drift. We went through the letters α, σ, ε, c, η and γ, cross-checked one world and one seed (a return of 345.07 for the Regular against 409.01 for the Curious One), changed exactly one knob — and the world turned over: in a standing world the Optimist won (505.57 against 450.30), in a moving one the Curious One (411.14 at σ = 0.1), while the Regular lost in both. Plus the horizon sweep: over ten days the Optimist was the best, and over five million days ε-greedy with a constant step pulled away."
date: "10.11.2026 · 13.11.2026"
covered:
  - "Opened with a riddle: in a standing world one character wins, in a moving one another; the route to the answer was the cross-check, the knob, the world, the turning point"
  - "Went through the letters out loud — symbol, meaning, value, name in the code: α, σ, ε, c, η and γ, which is not in the bandit at all"
  - "Met the five characters — the Regular, Friday, the Curious One, the Drawn One and the Optimist — and argued in advance about who would find the best cafe"
  - "Got the archive of the cafe simulator and made sure it runs: selftest — ok, all five strategies with no errors"
  - "Cross-checked: one duel, one world, one seed — a return of 345.07 for the Regular against 409.01 for the Curious One, share of the best 35 / 4 / 0 / 30 against 45 / 50 / 38 / 54"
  - "Read the output of the program: return, share of the best per group separately, and regret — “team 2 won” is by return, not by regret"
  - "Changed exactly one thing — the rule for updating the estimate: the honest average against a constant step (372.65 against 376.09), and in a standing world the other way round (456.44 against 455.44)"
  - "Walked the ladder of drift: the champion changes before your eyes — the Optimist 505.57 against 450.30 at σ = 0 and 405.94 against 411.14 at σ = 0.1"
  - "Everybody ran their own character against the Regular, the room compared the table on the board and worked out the answer itself"
  - "Took apart the bet of the Drawn One: the soft maximum gives the first dish 58%, and the dishes not chosen are penalised"
  - "Swept the strategies over horizons — 10, 100, 5 000 and 5 000 000 days: at the start the Optimist is the best, over the distance ε-greedy with a constant step pulls away, and the greedy one always loses"
  - "Summed up and went through the criteria of lab 2: a hundred seeds of your own, median and interquartile range, the numbers in the report matching the log"
tasks:
  - title: "Task 1. What α is, and why it is not the “learning rate”"
    text: "Yesterday's estimate of a dish is 1.0, today's reward is 1.4. What will the estimate show at α = 0.1 and at α = 0.9? What is α called in the code and what flag does it have?"
    answer: "At α = 0.1: 1.0 + 0.1 × 0.4 = 1.04 — the estimate has barely moved. At α = 0.9: 1.0 + 0.9 × 0.4 = 1.36 — the estimate jumped to today's result. α is the forgetting rate, not the learning rate: a small α remembers almost everything, a large one lives on the last lunch. In the code — knobs.ALPHA, the flag `--alpha`."
  - title: "Task 2. Why there is no γ in the bandit code"
    text: "γ is the discount factor from lectures 3 and 4. Does it take part in the bandit?"
    answer: "No. There is no episode in the bandit: the reward comes right after lunch, there is nothing to discount, and γ from the lectures is about the horizon of the return. That is why γ is absent from the code — and that is honest: we did not add an extra knob to the simulator, and nobody fell into the trap of “γ = 0.9”."
  - title: "Task 3. The cross-check: why your neighbour has the same numbers"
    text: "In the duel of the Regular against the Curious One everybody got 345.07 and 409.01. Your neighbour has other numbers. Which of you changed something?"
    answer: "The world and the seed are hard-wired into the program: the same `--seed 7` gives the same world, so the numbers are bound to match to the last kopeck. A discrepancy means that someone has another seed, another number of days, another σ or another strategy in the team — that is, it is already another experiment. That is what the cross-check is built on: first we make sure we are counting the same thing, and only then do we compare."
  - title: "Task 4. The share of the best by groups"
    text: "The shares of the best for the teams: 35 / 4 / 0 / 30 against 45 / 50 / 38 / 54 (first course, second course, dessert, drink). The Regular's dessert is 0%. How do you read that, if the corridors of the averages differ: first courses 0.8–1.3, second courses 0.95–1.8, dessert 0.6–0.8, drink 0.1–1.2?"
    answer: "The shares are counted per group separately, because the corridors differ, and “the share of the best” is the share of days when the team took the best dish of its own group. The Regular's dessert is 0%: his estimate of the dessert froze at the first measurement, while the dessert corridor is the narrowest (0.6–0.8) — there it is worse by definition, and there was no reason to go there. The drink, 30% against 54% for the Curious One, is explained by the width of the corridor: the drink has the widest spread (0.1–1.2), “the average over the corridor” means almost nothing there, and the only way to win was by checking — and the bonus for the unfamiliar (c) is exactly what drags the Curious One into the most unpredictable group."
  - title: "Task 5. The knob: why the world turns the update rule over"
    text: "Friday with the honest average against Friday with a constant step: 372.65 against 376.09 at σ = 0.05 and 456.44 against 455.44 at σ = 0. One rule, another world. What does that mean?"
    answer: "In a standing world the honest average is more accurate: every measurement weighs the same, 1/n loses nothing. In a moving world old measurements go stale, and 1/n drags the estimate into the past — there the constant step wins, because it forgets fast. So the choice of the update rule is not a matter of taste but a property of the world: the world changes — you need a step. You can check it with one command: the same duel with `--sigma 0 0 0 0`."
  - title: "Task 6. Where the turning point is on the ladder of drift"
    text: "The Optimist against the Curious One: at σ = 0 — 505.57 against 450.30, at σ = 0.05 — 429.46 against 414.32, at σ = 0.1 — 405.94 against 411.14, at σ = 0.2 — 391.98 against 409.62. Where did the champion change, and how do you check it yourself?"
    answer: "The turning point is between σ = 0.05 and σ = 0.1: the world began to change faster than the Optimist's memory can update, and forward comes the Curious One, who actively picks up the unfamiliar. You check it with two runs at intermediate values — `--sigma 0.09 0.09 0.09 0.09` and `--sigma 0.095 0.095 0.095 0.095`: at whichever of them the returns swap places, that is the turning point."
  - title: "Task 7. Why softmax gives 58%, not 50%"
    text: "The Drawn One has preferences H = (1, 0, 0): how many per cent will the first dish get, and why not 50%?"
    answer: "The soft maximum weighs not the preferences themselves but their exponentials: π_i = e^{H_i} / Σ_j e^{H_j}. At H = (1, 0, 0) you get 0.58 · 0.21 · 0.21. The first dish gets a weight above one, and the others share what is left equally — hence 58%, not 50%. With equal preferences it is ⅓ each. The probabilities always sum to one — that is a property of softmax."
  - title: "Task 8. Why ε-greedy is at the tail over ten days and far ahead over five million"
    text: "Friday with a constant step gives 29.79 of return and 17.26 of regret over 10 days — next to last place. Over 5 000 000 days the same Friday gives 20 594 200 of return and 1 968 129 of regret — first place by a wide margin. Not a single knob changed, only the length of the run. How do you explain that?"
    answer: "A short horizon is a world that has not moved yet: all the measurements are fresh, so the honest average 1/n loses nothing, while ten per cent of random days (ε = 0.1) is pure payment for exploration that has no time to pay off. Over a long horizon the world does move, and old measurements turn into ballast: 1/n drags the past along, while the constant step α forgets fast. On top of that, over a long horizon the error of overestimation accumulates: over a million days a small lag costs millions. Hence the rule of the session: the longer the horizon, the more important it is to forget rather than to remember."
  - title: "Task 9. The Optimist: why he is the best at the start and merges with the others over the distance"
    text: "Over 10 days the Optimist is the best (a return of 40.35, a regret of 6.70), over 100 days he is still among the leaders (409.41 / 47.10), and over 5 000 000 days he lags behind Friday with α by almost two million of return. What changes in him over time, and why does Q0 = 5 help on a short horizon and get in the way on a long one?"
    answer: "Q0 = 5 is a starting estimate above the ceiling of the reward: until a dish has been checked, the Optimist considers it the best and tries everything in turn. On a short horizon that pays: the world has not moved yet, a lucky dish is found quickly, hence 40.35 and 6.70. On a long horizon the same inflated estimate makes him try new things where everything has already been checked, while the world keeps changing: he pays for exploration nobody asked for and slides into the common heap (a regret of 3 673 784 against 1 968 129 for Friday with α)."
assignment:
  title: "Assignment: lab 2 — the multi-armed bandit in a moving world"
  text: "In the session we went through the rules by which the work is assessed: a hundred seeds of your own, median and interquartile range, a conclusion with a number, the numbers in the report matching the log, and a link to a section that does not exist meaning an unfilled checklist. The work itself was handed out earlier, at seminar 4: the statement, four gaps in the code, five tables over your own seeds and a step-by-step guide — on the lab page. It is submitted as a file to the group chat, there is no oral defence."
  homework:
    title: "Lab 2 — statement, files, deadlines and the step-by-step guide"
    href: "students/mai/rl/labs/02-laboratornaya-2/"
  due: "13.11.2026, all groups"
materials:
  - title: "Session code — the archive of the cafe simulator obed.zip"
    href: "/files/course/rl/sem6/obed.zip"
  - title: "Instructions and hints — how to run it and what to do in class (MD)"
    href: "/files/course/rl/sem6/instrukciya-i-podskazki.md"
  - title: "Session code — launching obed.py: flags, modes, a walkthrough of the commands"
    href: "/files/course/rl/sem6/obed.py"
  - title: "Knobs of the strategies — knobs.py"
    href: "/files/course/rl/sem6/knobs.py"
  - title: "The Regular — the greedy strategy (greedy.py)"
    href: "/files/course/rl/sem6/greedy.py"
  - title: "Friday — the ε-greedy strategy (epsilon.py)"
    href: "/files/course/rl/sem6/epsilon.py"
  - title: "The Curious One — UCB (ucb.py)"
    href: "/files/course/rl/sem6/ucb.py"
  - title: "The Drawn One — the gradient strategy (gradient.py)"
    href: "/files/course/rl/sem6/gradient.py"
  - title: "The Optimist — the optimistic strategy (optimistic.py)"
    href: "/files/course/rl/sem6/optimistic.py"
  - title: "Registry of characters and synonyms (agents.py)"
    href: "/files/course/rl/sem6/agents.py"
  - title: "Slides of the session, group М80-203СВ-25 (10.11.2026) — PPTX"
    href: "/files/course/rl/sem6/s6-pyat-hakterov-gr-m80-203-10.11.2026.pptx"
  - title: "Slides of the session, group М80-202СВ-25 (13.11.2026) — PPTX"
    href: "/files/course/rl/sem6/s6-pyat-hakterov-gr-m80-202-13.11.2026.pptx"
---

## What we did in this session

This session was lab 2 live: not a review of what was sent in, but a world of your own where you can make
mistakes and check. The world is a cafe: every day you choose one of twelve dishes, and the kitchen wanders
between days. Five characters are five ways of choosing, from the greedy one to the one who trusts too much.
The session ran as a riddle: in a standing world one character wins, in a moving one another, and the only
way to find that out was a run.

The order was this: first the letters (each out loud: symbol, meaning, value, name in the code), then the five
suspects with a vote, then we handed out the archive and spent half an hour working with our hands: the
cross-check, the walkthrough of the output, one edit, the ladder of drift, “everyone against the Regular” and
the table on the board. Then the bet of the Drawn One, the answer, and the closing number “human against the
machine”.

## The cafe world: four groups of three dishes

| Group | Corridor of the averages | Dishes |
| --- | --- | --- |
| first course | 0.8 – 1.3 | borscht · noodle soup · solyanka |
| second course | 0.95 – 1.8 | cutlet · pelmeni · grill |
| dessert | 0.6 – 0.8 | kompot · cake · ice cream |
| drink | 0.1 – 1.2 | water · kvass · juice |

The corridor is the range inside which the average of a dish wanders. The width of the corridor is different:
the dessert has the narrowest (0.6–0.8), the drink the widest (0.1–1.2). There are $3^4 = 81$ different
lunches in the cafe: three dishes in each of the four groups. Twelve is the number of dishes, not of lunches.

## The letters out loud

| Letter | What it means | Our value | In the code |
| --- | --- | --- | --- |
| α | the forgetting rate of the estimate | 0.1 | knobs.ALPHA, the flag `--alpha` |
| σ | how much the average of a dish wanders per day | 0.05 · 0.05 · 0.01 · 0.20 by group | the flag `--sigma` |
| ε | the share of random probes | 0.1 | knobs.EPSILON, the flag `--epsilon` |
| c | the price of curiosity: a bonus for an unfamiliar dish | 2.0 | knobs.C_UCB, the flag `--c` |
| η | how much one lunch reshapes the probabilities | 0.1 | knobs.ETA, the flag `--eta` |
| γ | the horizon of the return from lectures 3–4 | — | not in the bandit: there is no episode |

**α is the forgetting rate, not the “learning rate”.** Yesterday's estimate of a dish is 1.0, today's
reward is 1.4. At α = 0.1 the estimate becomes 1.0 + 0.1 × 0.4 = 1.04 — it has barely moved; at α = 0.9 it will
be 1.0 + 0.9 × 0.4 = 1.36 — it jumped to today's result. A small α remembers almost everything, a large one
lives on the last lunch.

**σ is not the nervousness of the agent but the nervousness of the kitchen.** At σ = 0.05 over twenty days the
best dish can drift by about 0.2. In the code σ is set by group: first 0.05, second 0.05, dessert 0.01, drink
0.20 — the dessert almost stands still, the drink is the most nervous of all.

**ε is the share of random probes.** At 0.1, out of a hundred lunches about ten are random; at zero all
hundred are your own, at one all hundred are a gamble. Both edges are bad: at zero we get stuck, at one we
learn nothing.

**c is the price greed pays for unfamiliarity.** On day one hundred a dish tried once gets a bonus of ≈ 4.3,
one tried a hundred times — ≈ 0.4: the unfamiliar is ten times dearer. In everyday terms: you are pulled more
strongly to the counter in the canteen where you have never stood, even if the food there is worse.

**η is the rate of the preferences.** There were 33 % for each dish; the lunch went well, the reward above
average — at η = 0.1 it became 34 / 33 / 33, at η = 1 — 40 / 30 / 30. A small η is a smooth drift, a large one
is jumps after every lunch.

**γ takes a rest in the bandit.** The reward comes right after lunch, there is no episode, there is nothing to
discount. That is why there is no γ in the code — and that is honest.

## Five characters

| Character | How he behaves | Strategy | File |
| --- | --- | --- | --- |
| the Regular | found the first cafe — and goes only there | greedy | greedy.py |
| Friday | nine days I eat at home, on the tenth I go out | ε-greedy | epsilon.py |
| the Curious One | wherever I have not looked for a long time — that is where I am pulled | UCB | ucb.py |
| the Drawn One | wherever they helped me more often — that is where I reach | gradient | gradient.py |
| the Optimist | everything new is excellent until proven otherwise | optimistic, Q0 = 5 | optimistic.py |

Before the code was handed out the room voted: who will find the best cafe. The answer in class turned out
to be not “the smartest” but “the one that suits the world” — and that was the answer to the riddle.

## How it was in a standing world

The dossier from session 3 — a thousand sprints, one seed, a ceiling of 1.3. There the return was counted per
sprint, here we count it over a hundred days, the scale is different:

| Strategy | Return | Share of the best |
| --- | --- | --- |
| greedy | 0.31 | 0 % |
| ε-greedy 0.1 | 1.12 | 76 % |
| optimistic Q0 = 5 | 1.26 | 100 % |
| UCB c = 2 | 1.22 | 93 % |
| gradient | 1.24 | 94 % |

There was one question for the room: who will win here, where the kitchen wanders?

## Cross-check: one world — one number

The first duel is the same for everyone: the Regular against the Curious One, a hundred days, seed seven.

```
python3 obed/obed.py --days 100 --seed 7 --duel \
  'greedy,greedy,greedy,greedy' \
  'ucb,ucb,ucb,ucb'
```

You should get 345.07 against 409.01. Your neighbour gets the same: one world, one seed. Before the duel the
program asks for a bet; if you are not betting — just press Enter.

## What the program prints

```
group                   team 1                 team 2
share of the best:
first course                  35%                    45%
second course                  4%                    50%
dessert                        0%                    38%
drink                         30%                    54%
return                     345.07                 409.01
regret                     111.44                 47.50

Team 2 won.
```

* **return** — how much the team collected over all the days; the more the better;
* **share of the best** — per group separately, in two columns: how often the team took the best dish of its own group;
* **regret** — how much it fell short of the best dish;
* “Team 2 won” — that is **by return**, not by regret. Return and regret can diverge: a team with a small
  return usually has a big regret, but not always.

## The knob: one edit — another result

Friday with the honest average (`eps:avg`) against Friday with a constant step (`eps:alpha`):

| World | Honest average | Constant step | Who is ahead |
| --- | --- | --- | --- |
| σ = 0.05 (the working one) | 372.65 | 376.09 | the constant step |
| σ = 0 (standing) | 456.44 | 455.44 | the honest average |

In a standing world the honest average is more accurate: every measurement weighs the same, 1/n loses nothing.
In a moving world old measurements go stale, and 1/n drags the past along — there the constant step wins, because it
forgets fast. The choice of the update rule is not taste but a property of the world.

## The ladder of σ: where the champion loses

One and the same world, only the drift of the kitchen changes — the rivals are the Optimist and the Curious One:

| σ | the Optimist | the Curious One | Who is ahead |
| --- | --- | --- | --- |
| 0 | 505.57 | 450.30 | the Optimist |
| 0.05 | 429.46 | 414.32 | the Optimist |
| 0.1 | 405.94 | 411.14 | the Curious One |
| 0.2 | 391.98 | 409.62 | the Curious One |

The turning point is between 0.05 and 0.1: the world began to change faster than the Optimist's memory can
update. Check the intermediate values: `--sigma 0.09 0.09 0.09 0.09` and `--sigma 0.095 0.095 0.095 0.095` —
at whichever of them the returns swap places, that is the turning point.

## The Drawn One: how he chooses and how he learns

The Drawn One keeps not an “average over the estimates” but preferences, and takes a softmax of them:

$$
\pi_i = \frac{e^{H_i}}{\sum_j e^{H_j}}
$$

Start: $H = (0, 0, 0)$ → ⅓ for each dish. After one lunch, when the first dish was chosen:
$H = (1, 0, 0)$ → 0.58 · 0.21 · 0.21. The first dish gets a weight above one, the others share
what is left equally — hence 58 %, not 50 %. The probabilities always sum to one — that is a property of softmax.

Then the update. We chose dish A: reward 1.3, average 1.0, step η = 0.1, the probability was ⅓.
The shifts: +0.02 for the chosen one, −0.01 for the others. **The dishes not chosen are penalised — that is not a typo:** the distribution
flows from the losers to the winner, otherwise the preferences would never change.

## Why the Drawn One gives up in the drift

The teacher's reference — 240 seeds, three knobs, σ = 0.05:

| Strategy | Share of the best | Skew (max/min) |
| --- | --- | --- |
| ε-greedy, α = 0.1 | 69 % | 9 |
| UCB c = 2, α = 0.1 | 75 % | 5 |
| gradient, η = 0.1 | 54 % | 21 — the worst of the three |

Your own hundred seeds will give other numbers — compare the order, not the digit. The conclusion: the soft maximum changes
its choice more often, and a fast world needs speed.

## The answer

The only one who loses in both worlds is **the Regular**: in the standing one he gave 246.84 — last place, in the rough one
(σ = 0.2) — 365.78, again last (Friday 370.54, the Drawn One 374.49, the Optimist 391.98, the Curious One
409.62). The reason is one: he does not check the alternatives, and a world cannot be known without checking.

There is no best character at all — there is one that suits the world: in a standing world the Optimist wins, in a moving one
the Curious One. “Yesterday's champion is not today's champion”.

## The window of free runs: who wins at the start and who over the distance

Instead of ready-made duels the room turned the knob of the run length and watched who behaves how in a short and in a long
world. Every strategy worked the same world on its own — four identical characters, one per
group of dishes (seed 7, the standard drift) — and we watched what happens when the run is stretched
from ten days to five million.

**Return** — how much it collected over all the days:

| Strategy | 10 days | 100 days | 5 000 days | 5 000 000 days |
| --- | --- | --- | --- | --- |
| the Regular (greedy) | 25.77 | 345.07 | 18 765.02 | 18 870 368 |
| the Curious One (UCB) | 38.18 | 409.01 | 20 243.87 | 18 893 484 |
| Friday, 1/n | 29.79 | 372.65 | 18 918.66 | 18 878 599 |
| Friday, α = 0.1 | 29.79 | 376.09 | **20 440.94** | **20 594 200** |
| the Drawn One (gradient) | 34.23 | 380.42 | 19 072.75 | 18 874 965 |
| the Optimist (Q0 = 5) | **40.35** | **409.41** | 19 283.19 | 18 888 545 |

**Regret** — how much it fell short of the best dish; the smaller the better.

The values are exactly what the program prints; in the 5 000 000 days column the fractional part is dropped.

| Strategy | 10 days | 100 days | 5 000 days | 5 000 000 days |
| --- | --- | --- | --- | --- |
| the Regular | 21.28 | 111.44 | 3 687.29 | 3 691 962 |
| the Curious One | 8.87 | 47.50 | 2 208.44 | 3 668 846 |
| Friday, 1/n | 17.26 | 83.85 | 3 533.65 | 3 683 731 |
| Friday, α = 0.1 | 17.26 | 80.41 | **2 011.37** | **1 968 129** |
| the Drawn One | 12.82 | 76.08 | 3 379.56 | 3 687 365 |
| the Optimist | **6.70** | **47.10** | 3 169.12 | 3 673 784 |

**What this shows**

* **The one who wins at the start is not the one who wins later.** Over ten days the best is the Optimist (40.35 of return and
  6.70 of regret), second is the Curious One (38.18 / 8.87), and ε-greedy Friday is next to last (29.79 / 17.26): ten
  per cent of the days go on random lunches, and on a short horizon that is the price of exploration that has not
  paid off yet. Over five million days the order turns over: Friday with the constant step pulls away,
  while the Optimist and the Drawn One — the best at the start — slide into the common heap and share third and fifth places.
* **The difference between “started well” and “finished well” is not luck but the update rule.** Friday with 1/n and
  Friday with α are almost indistinguishable over a hundred days (372.65 / 83.85 against 376.09 / 80.41), diverge over five thousand
  (18 918.66 against 20 440.94), and over five million the gap is 9 % in return (20 594 200 against 18 878 599) and almost
  twofold in regret (1 968 129 against 3 683 731). A short world has not moved yet, and the honest average 1/n loses
  not a single measurement; a long world moves, and the one who forgets fast wins.
* **Optimism pays off over the short horizon and does not over the long one.** Q0 = 5 is an estimate above the ceiling of the
  reward: until a dish has been checked, the Optimist considers it the best and tries everything in turn. Over ten days
  that is a win; over a long horizon the same inflated estimate makes him try new things where everything has already been
  checked — and over five million days his regret is 3 673 784 against 1 968 129 for Friday with α.
* **The Drawn One finds quickly but does not hold.** The soft maximum flows to the lucky dish (34.23 over ten
  days — third place), but then constantly reshapes the probabilities and does not let the estimates settle: over a long
  horizon 3 687 365 of regret — almost like the greedy one, and at the tail of the table.
* **The greedy one always loses.** The only strategy that is at the tail by regret on every horizon:
  21.28 → 111.44 → 3 687.29 → 3 691 962. He does not check the alternatives, and a world cannot be known without checking.
* **This is one trajectory, not statistics.** One world, one seed — so we compare the order, not the digit.
  We did not count 50 000 000 days: such a run would not fit into a class.

## How to repeat it at home

```
unzip obed.zip
cd obed
python3 obed.py --selftest
```

We expect `selftest: ok — all 5 strategies × 2 update rules, 20 days, no errors`. Then:

```
# cross-check: the Regular against the Curious One
python3 obed.py --days 100 --seed 7 --duel \
  'greedy,greedy,greedy,greedy' \
  'ucb,ucb,ucb,ucb'

# the knob: the honest average against the constant step
python3 obed.py --days 100 --seed 7 --duel \
  'eps:avg,eps:avg,eps:avg,eps:avg' \
  'eps:alpha,eps:alpha,eps:alpha,eps:alpha'

# the ladder of drift
python3 obed.py --days 100 --seed 7 --sigma 0.2 0.2 0.2 0.2 --duel \
  'optimistic,optimistic,optimistic,optimistic' \
  'ucb,ucb,ucb,ucb'

# the horizon sweep: 10, 100, 5 000 and 5 000 000 days
# (five million days takes about ten minutes)
python3 obed.py --days 100000 --seed 7 --duel \
  'eps:alpha,eps:alpha,eps:alpha,eps:alpha' \
  'optimistic,optimistic,optimistic,optimistic'

# the game against the machine
python3 obed.py --play --vs gradient --days 30
```

Hints: the names of the characters in the commands go in quotes, otherwise the shell may cut the commas;
the archive also accepts the Latin synonyms `greedy`, `eps`, `ucb`, `gradient`, `optimistic` (see agents.py), and the commands
above use them; a decimal comma works (`--sigma 0,05` is the same as `0.05`); on Windows `python3` is a Microsoft Store stub, run
`py obed.py` or `python obed.py`; the σ symbol in the output may turn into “?” — that is not an error.

## Deadlines and submission

* Lab 2 — the deadline is **13.11.2026**, both groups; there is one retake, at the eighth session (24.11 / 27.11).
* It is submitted as a file to the group chat, there is no oral defence. Questions about submission — straight away, not at the deadline.
* There is no homework for the seventh session. Further, from the seventh session — lab 1, tic-tac-toe.
* Questions about the session and about the lab — to the group chat, not in a private message.
