---
number: 4
title: "The world has started moving: non-stationarity"
summary: "What changes when the payoffs of the levers stop standing still: a random walk of the averages, a Markov chain and a non-stationary bandit. Why the honest average 1/n drags the estimate into the past and how a constant step α saves it, how to read the gradient strategy in code, three gaps in the session code and the reference numbers — 53% for 1/n against 69% and 76% for α, 74–75% for UCB, 54% for the gradient one and a ceiling of 1.45 at the oracle."
date: "27.10.2026 · 30.10.2026"
covered:
  - "Recapped what the session stands on — the estimates q, two update rules (the honest 1/n and the constant step α) and three strategies"
  - "Went through what happens to the world when the averages start to wander — a random walk and a Markov chain whose state only the environment sees"
  - "Showed on the counterexample 1 → 0.5 → 1.25 why 1/n in a moving world drags the estimate into the past"
  - "Read the gradient strategy in code — preferences and the soft maximum"
  - "Filled in three gaps (the walk step, the update rule, the strategy) and ran our own numbers"
  - "Checked against the reference: 53% for ε with 1/n, 69% and 76% for ε with α, 74–75% for UCB, 54% for the gradient one, the oracle 1.45"
  - "Tested two hypotheses about the gradient one losing, on runs — the 1/t baseline and the preference step are not to blame"
  - "Went through three settings for “bandit or not a bandit”: where the bandit ends and the caveats begin"
tasks:
  - title: "Task 1. Why 1/n falls behind"
    text: "The rewards arrive one after another: 1, then 0.5, then 1.25. The average over the whole history (1/n) gives 1.0. What will the constant step α = 0.5 give, and what will α = 0.1? Which rule notices faster that the world has changed?"
    answer: "With α = 0.5: 0.5, then 1.25 — every new observation weighs half, so the estimate jumps after the fresh value almost at once. With α = 0.1: 0.9 and 1.01 — the step is small, the estimate crawls slowly. The one with the bigger step notices faster: the weight of an observation that was k steps ago is (1 − α)ᵏ, and with α = 0.5 the old observations are forgotten almost instantly, while with 1/n they never are. The price of freshness is the trembling of the estimate: the bigger α, the wider the spread."
  - title: "Task 2. Read a row of the table"
    text: "The greedy strategy chooses the current best 18% of the time, ε-greedy with 1/n — 53%. Yet a random choice out of three levers would give 33%. How is that to be understood: why is greedy worse than guessing?"
    answer: "Because greedy does not explore: once it convinces itself of a randomly lucky arm and pulls it until that arm stops being the best — and the world has moved by then. Its counter skew is 1000 (one arm is pulled a thousand times more often than another), and the estimates of the other arms freeze in the old era. A random choice, on the contrary, hits the current best every third of the time simply as a fact, without knowing anything. Hence the conclusion of the session: “explore less” does not mean “choose better” — what matters is that the estimates do not grow old."
  - title: "Task 3. Why UCB holds up with 1/n"
    text: "ε with 1/n has a share of the best of 53%, while UCB with the same 1/n has 74%. The update rule is the same. What makes the difference?"
    answer: "The bonus for uncertainty: it grows as the root of the logarithm of time and is large when n is small, so rarely pulled arms regularly get a chance and their estimates do not freeze at the old world. It shows in the skew: for ε with 1/n it is 20, for UCB with 1/n — 11, the averaging windows of the arms are comparable. With ε-greedy the losing arms are hardly ever touched, and they grow old in silence."
  - title: "Task 4. Why the ceiling is 1.45 and not 1.3"
    text: "The best starting average is 1.3. The oracle, which always pulls the current best, gets 1.45 [1.29–1.57]. Where do the extra 0.15 come from, if the averages only wander around the start?"
    answer: "The oracle pulls not “the arm with the best start” but the maximum of the three wandering averages at every moment. The maximum of three random variables is greater than each of them — that is why the average return of the oracle is above the best start. This is not a counting error but a property of the drift; the upper bound of 1.9 plays into it as well. The numbers are tied to our μ₀ and σ: with different starting averages the oracle is counted anew."
assignment:
  title: "Assignment: lab 2 — the multi-armed bandit in a moving world"
  text: "Lab 2 runs on its own kit: four channels, drift of the averages, four gaps in the code, five tables for its own seeds and twenty questions. The statement, the formulas and the order of work are on the lab page."
  homework:
    title: "Lab 2 — the statement, the files, the deadlines and a step-by-step guide"
    href: "students/mai/rl/labs/02-laboratornaya-2/"
  due: "13.11.2026, all groups"
materials:
  - title: "Session code — the environment environment.py"
    href: "/files/course/rl/sem4/environment.py"
  - title: "Session code — the agent agent.py (three gaps)"
    href: "/files/course/rl/sem4/agent.py"
  - title: "Session code — the run run.py"
    href: "/files/course/rl/sem4/run.py"
  - title: "The σ ladder — sigma_ladder.py"
    href: "/files/course/rl/sem4/sigma_ladder.py"
  - title: "Code pieces — snippets.py"
    href: "/files/course/rl/sem4/snippets.py"
  - title: "Reference numbers — for the cross-check (MD)"
    href: "/files/course/rl/sem4/etalon-numbers.md"
  - title: "Reference table — picture (PNG)"
    href: "/files/course/rl/sem4/etalon.png"
  - title: "Session presentation, group М80-203СВ-25 (27.10.2026) — PPTX"
    href: "/files/course/rl/sem4/s4-mir-poshel-nestacionarnost-gr-m80-203.pptx"
  - title: "Session presentation, group М80-202СВ-25 (30.10.2026) — PPTX"
    href: "/files/course/rl/sem4/s4-mir-poshel-nestacionarnost-gr-m80-202.pptx"
---

## What we did in this session

For three sessions the world had stood still: the averages of the levers were set once and for all, and the whole struggle was
about estimating them more precisely. This session is about what happens when the world starts to move.
The levers are the same, the payoffs are different: every average shifts a little in a random direction every sprint.
That is **non-stationarity**, and because of it a rule that was the best in a standing world becomes
the worst in a moving one.

The order of work was this: first we went through how the drift is arranged and why it breaks the honest average,
then we read the gradient strategy in code, then filled in three gaps and checked our numbers
against the reference.

## Random walk of the averages

Every sprint every average shifts by a random value:

**μ(t + 1) = μ(t) + σ · noise**, where σ = 0.05, the noise is normal with mean 0, and going beyond the bounds
0.1 and 1.9 is clipped (a clip, not a reflection — it is cheaper in code, and with σ = 0.05 the average
reaches the bound rarely).

The starting averages are the same as in the previous practical: **0.3 / 0.8 / 1.3**.

Two properties that have to be taken away:

* **the next value depends only on the current one**, not on the whole history — this is a Markov chain,
  and its state is a vector of three averages;
* **only the environment sees the state**: the agent, as before, has access only to the reward. Therefore for the agent
  it is still one state — we work as with a bandit, only the world under it moves.

## Why 1/n gives way

The update rule from the previous practical: the estimate shifts by a step multiplied by the difference between the reward
and the estimate. The step is of two kinds — the honest **1/n** and the constant **α**.

In a standing world 1/n is king: the estimate equals the exact average over the whole history, and the longer, the more precise.
In a moving world the same property becomes a misfortune: with 1/n the estimate is the average **over all time**, so
an observation that was a hundred sprints ago still drags it into the past. With a constant step the weight
of an observation that was k steps ago is **(1 − α)ᵏ**: the old is forgotten exponentially, and the estimate
runs after the fresh world. The price is trembling: the bigger α, the wider the spread.

The counterexample we went through in class: the rewards 1 → 0.5 → 1.25. The average over the whole history is 1.0,
with α = 0.5 — 0.5 and 1.25, with α = 0.1 — 0.9 and 1.01. One and the same rule, three different ideas
of where the world is now.

## Three strategies in a moving world: the numbers

The reference — 240 seeds of 1000 sprints each, σ = 0.05, starting averages 0.3 / 0.8 / 1.3. The main metric is
**the share of the current best**: what part of the sprints the agent pulled the arm that had at that moment
the maximum average. The second metric is the return per sprint.

| Strategy | Return per sprint: median [IQR] | Share of the current best: median [IQR] | Skew of n (max/min) |
| --- | --- | --- | --- |
| greedy | 0.74 [0.53–1.01] | 18% [5–33] | 1000 |
| ε-greedy 0.1 · 1/n | 1.17 [0.99–1.36] | 53% [41–67] | 20 |
| ε-greedy 0.1 · α 0.1 | 1.31 [1.16–1.44] | 69% [62–76] | 9 |
| ε-greedy 0.1 · α 0.3 | 1.34 [1.18–1.47] | 76% [69–81] | 6 |
| UCB c = 2 · 1/n | 1.35 [1.19–1.48] | 74% [64–81] | 11 |
| UCB c = 2 · α 0.1 | 1.36 [1.21–1.49] | 75% [67–81] | 5 |
| gradient h = 0.1 | 1.18 [1.01–1.38] | 54% [44–68] | 21 |
| oracle (always the current best) | 1.45 [1.29–1.57] | 100% | 9 |

What to read in the table:

* **the zero of the scale is 33%**: that is a random choice out of three arms. Greedy (18%) is worse than guessing: it gets stuck
  on a randomly lucky arm and does not notice that the world has moved;
* **the spread of 1/n is twice as large**: by IQR 26 against 14, by the minimum 14 against 28 (by the maximum there is
  no difference — 90 and 91). That is why we compare distributions: the median and the IQR, not a single average;
* **UCB holds up with 1/n too** (74%): the bonus evens out the frequencies, the averaging windows of the arms are comparable
  (a skew of 11 against 20 for ε-greedy);
* **the ceiling floats**: the oracle gives 1.45, not 1.3 — it pulls the maximum of three wandering averages,
  and the maximum of three random variables is greater than each of them.

The same picture in another scale — **regret**, the average reward not received relative to the current
best: 0.62 for greedy, 0.24 for ε with 1/n, 0.10 for ε with α = 0.3, 0.08 for UCB with α = 0.1, 0.22 for the gradient one.
The order is the same, but the upper part reads differently: by the share of the best UCB and ε with α = 0.3 are almost equal,
while by regret UCB misses more often but more cheaply — it takes the second arm, not the worst one.

## Median and IQR: how to read these numbers

### Why one number is not enough

Every run of a strategy is one sample from the distribution of results, and it depends on the seed. A run in which ε with 1/n scored 90% of the share of the best does not say the strategy is good: it says this seed played along with it. Judging a strategy by one run is like judging a coffee shop by one visit on a Friday evening.

That is why we do many runs (in the reference — 240 seeds of 1000 sprints each) and look at the distribution, not at a random point of it.

### The median and the IQR — and how to compute them

**The median** is the middle of the distribution: half the runs gave less than it, half more. The entry “53%” reads like this: in a typical run the strategy pulled the current best in 53% of the sprints, and half the runs were worse than that number, half better. The arithmetic mean does not work like that: our metrics have a long right tail (for ε with α = 0.1 there were runs up to 91%), and rare lucky runs pull the mean up, to where a typical run does not live. That is why the median comes first and the mean next to it, but not instead of it.

**The IQR** (interquartile range) is the corridor from the 25th to the 75th percentile: where the middle half of the runs lives. Reading the entry **53% [41–67]**:

* 53% — the median;
* [41–67] — the first and the third quartiles: a quarter of the runs below 41%, a quarter above 67%, half inside;
* the width of the corridor is 67 − 41 = **26 points** — that is the spread of the strategy in this metric.

Two things people trip over most often:

* **the IQR is not symmetric**, and you cannot write “53 ± 26”: [41–67] is not “53 plus or minus 26”. The symmetric measure is the standard deviation; the report has it, but not instead of the IQR;
* **this is not the min–max range.** The full range for ε with 1/n is 14–90, but it rests on two extreme runs and wanders with the range of seeds, while the IQR leans on the middle half and is therefore stable. We still state the range of seeds in the report: without it the corridor cannot be reproduced.

Computing it yourself — with the standard library (this is how `sigma_ladder.py` counts too, then the quartiles will match the output of the run):

```python
import statistics
q1, _, q3 = statistics.quantiles(values, n=4)   # values — one number per seed
print(f"{statistics.median(values) * 100:.0f}% [{q1 * 100:.0f}–{q3 * 100:.0f}]")
```

`statistics.quantiles` interpolates with the *exclusive* method, `numpy.percentile` — linearly: the numbers may
part by half a point. That is not an error, but the report has to be checked against the log in one and the same manner.

One point — one seed. Count from the numbers of the runs, not from the averages inside a run.

### How to compare two strategies

We look at two things at once: the shift of the medians and the overlap of the corridors.

* 69% [62–76] against 76% [69–81]: the corridors overlap on the stretch 69–76, but the medians are 7 points apart, and the overlap is narrow — the difference reads;
* 74% [64–81] against 76% [69–81]: the medians are two points apart, the overlap is almost complete — by these numbers the strategies are indistinguishable, and an honest wording sounds like “a hint”, not “one is better than the other”.

The comparison works strongest on **the same range of seeds** for both strategies: the noise of the environment is then common to them and does not mask the difference.

The IQR shows the main thing: the honest average has a corridor twice as wide — 26 points against 14. That is why “1/n gives way in drift” is a conclusion about distributions, not about the pair 53 against 69. By the return the gap is more modest (IQR 0.37 against 0.28), and that is exactly why the table has two metrics, not one.

### Tails and the requirements of the lab

Beyond the IQR there are the tails: up to 90% for ε with 1/n and up to 91% for ε with α = 0.1. A run with 90% is neither an error nor a merit: it is the long tail of the distribution. Hence the rule for the report:

* **at least 100 seeds per point** of the table, with the median and the IQR for every metric, and the mean and the standard deviation next to them;
* **the range of seeds and the launch command** for every table — otherwise the numbers cannot be reproduced;
* **the conclusion — by the medians and the overlap of the corridors**, always with a figure from your own table.

The tables for this stand in the answer file of lab 2 — there are five of them, 100 seeds per point; the requirements and the deadlines are on the lab page.

### About σ = 0.05 and the 68–95–99.7 rule

Separately, so as not to confuse two different things. σ = 0.05 is the **standard deviation of the step of the walk** of the averages, not the spread of results between runs. Normal noise with such a σ gives roughly 68% of the steps inside ±0.05 and 95% inside ±0.1 — hence “the world crawls, it does not jump”.

The accumulated shift grows as the root of time: over 100 sprints its standard deviation is ≈ 0.5, over 1000 — ≈ 1.6 with the whole range of the averages 0.1–1.9. So the clip at the bounds really does work, and on a long horizon the walk is no longer Gaussian. From the same place it is clear why a short window (α) keeps up with the average, while the window “all the time” (1/n) does not.

**The 68–95–99.7 rule does not apply to the IQR**: the distribution of the metrics is not Gaussian, and ±0.05 is about the step of the world, not about the spread of the runs. In the lab you run three regimes — σ = 0.01, 0.05 and 0.2 — and watch how both the IQR and the gap between 1/n and α change together with σ.


## What we checked about the gradient one

The gradient one is worse under drift: 54% [44–68] against 76% for ε with α = 0.3. We tested two versions with runs
of 240 seeds:

* **the baseline**. Inside the gradient one the average return is counted as 1/t — the same inertial estimate
  we scolded throughout the seminar. We replaced it with a constant step: 53% with α = 0.1, 52% with α = 0.3 —
  against 54%, no difference;
* **the preference step**. We increased it tenfold: 56% — two points out of twenty-two, that does not explain it either.

The third version remains: **the soft maximum does not zero out the probability of a bad arm**, and that exploration
under drift costs more than ε with forgetting. We did not test it — this is an open question, and it can be taken up.

## What to take from the session

* **non-stationarity** is when the payoff depends on time, and then “the exact average over the whole history”
  stops being a virtue;
* **the step α** is the knob “how much to remember”: the weight of an old observation is (1 − α)ᵏ, and in a moving world that
  matters more than precision;
* **compare distributions, not runs**: the spread of 1/n is twice as large, and one launch will not show it;
* **every metric has its own truth**: the share of the current best and regret give one order, but different conclusions
  about who is second.
