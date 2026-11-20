---
number: 5
title: "SARSA and Q-learning"
summary: "Learning from experience without an environment model — the step (s, a, r, s′), the return and Monte Carlo, a two-part target and the TD error, on-policy and off-policy, SARSA and Q-learning, the “cliff” variant, the three knobs α, γ, ε and what comes next."
date: '16.10.2026'
lectures:
  - number: 6
    date: '16.10.2026'
covered:
  - "We remove the model: until now the right-hand side of the Bellman equations relied on transition probabilities the agent does not have"
  - "Instead of a model — experience: the step (s, a, r, s′) and the tape of an episode; experience gives one outcome that happened, not all of them at once"
  - "We learn the table Q(s, a): eleven cells for four actions — forty-four numbers"
  - "What we need from the environment: start an episode, charge for a step, announce the end"
  - "Monte Carlo: wait for the end of the episode and shift the estimate towards the return — 8.00 · 6.20 · 4.58 · 3.12 · 1.81"
  - "The learning step α: the share of the difference “target − estimate”; with α = 0.1 a fresh episode weighs a tenth, and the estimate is the average over the last ten"
  - "Three limitations of Monte Carlo: until the episode is over there is nothing to learn from; in continuing tasks there is no end at all; the return wanders because of slips (0.64 on average against 1.81 in an ideal run)"
  - "Temporal differences: target = r + γ · Q(s′, ·), TD error = target − estimate, an update by the share α; the target is assembled from our own estimate — that is bootstrapping"
  - "Learning as we go: Monte Carlo updates once after an episode, TD — at every step"
  - "The bias–variance trade-off: Monte Carlo has an unbiased but noisy target, TD has a biased one but is steadier"
  - "The terminal: there is nothing behind the exit, target = r + γ · v(terminal), that is −1 + 0.9 × 10 = 8.00"
  - "Numbers: on a simple maze Monte Carlo and TD hardly differ — 0.89 against 0.94, so next we need a maze with a dangerous place"
  - "SARSA: the target is the estimate of the chosen pair (the step plus γ · Q(s′, a′)), we learn about the same policy we act by (on-policy)"
  - "Q-learning: the target is the maximum over actions, the behaviour policy and the learning policy are separated (off-policy)"
  - "The “cliff” variant: the short path along the edge is three steps, the safe detour on top is five; a fall costs −100, so a step down is estimated at −91.00"
  - "Two characters on one environment: SARSA goes around on top (59 falls, return of the greedy policy 0.16), Q-learning walks the edge (96 and 3.32)"
  - "Three knobs: α sets the learning speed, γ — the foresight (the horizon 1/(1 − γ) is ten steps), ε — how much we spend on exploration"
  - "The price of exploration: at ε = 0.2 / 0.1 / 0.02 that is 201 / 96 / 22 falls, while the return grows from −12.19 to +1.33"
  - "Pitfalls: a large α (the estimates jump), the optimism of the maximum in separate cells (S9 +0.83, S11 +0.04), expecting an end where there is none, updating after the terminal"
  - "Next: TD(λ), the actor-critic, approximating the table with a function, framework libraries — and the map of the whole course"
qa:
  - q: "How does the SARSA target differ from the Q-learning target?"
    a: "Only in what stands to the right of the plus. In SARSA it is the estimate of the pair (s′, a′) that the policy really chose — 3.91 in the transition we took apart; in Q-learning it is the maximum over actions in the next state, 5.46. That is why SARSA learns about the same policy it acts by (on-policy), and Q-learning about the greedy one, no matter how it behaves itself (off-policy)."
  - q: "Why does our ε-noise get into the SARSA target?"
    a: "Because a′ is the action our own policy chose, and with probability ε it chooses a random one. Over the four actions from S10 the targets are: right 3.91 (this action is chosen in nine cases out of ten), down −23.19 (in one) — and the average comes out 2.98. The Q-learning target takes the maximum 5.46 and knows nothing about our random moves. Hence the main conclusion: SARSA takes the price of its own exploration into account in advance, Q-learning does not."
  - q: "Why can Monte Carlo not learn in a continuing task?"
    a: "Its target is the return over the rest of the episode, and in a continuing task the episode never ends, so the return never accumulates and there is nothing to update. Cutting the process into arbitrary pieces means letting a truncated return into the target and learning from it as if it were complete. In the maze the episode is short and the wait is not long, but that luck does not hold everywhere."
  - q: "What is the TD error and why is it called bootstrapping?"
    a: "The TD error is the difference between the target r + γ · Q(s′, ·) and the current estimate Q(s, a); that is exactly what we drive, shifting the estimate by the share α. Bootstrapping — because the target is not taken wholly from fact: it is assembled from the real reward and from our own estimate of the next state (with zero estimates the target of an ordinary step equals −1.00, while a step into the exit gives 8.00)."
  - q: "Why is the rule different for a step into the exit?"
    a: "Nothing follows the terminal, so there is no “estimate further on”. The target of such a step is the reward plus the discounted value of the terminal itself: −1 + 0.9 × 10 = 8.00. If we keep asking what comes next, the target becomes −1 + 0.9 × 0 = −1.00, and the agent will learn to go around the exit."
  - q: "What happens at α = 1 and what at α close to zero?"
    a: "At α = 1 the estimate is simply replaced by the latest measurement: the target is the return of one episode, and the estimate starts jumping after the randomness of the environment. With a very small α the estimate stays almost in place: averaging goes over a very long tail of episodes, and learning takes long. Our working value is α = 0.1."
  - q: "Where does −91.00 come from and why do they walk along the cliff at all?"
    a: "−91.00 is the estimate of a step down from the cliff: −1 + 0.9 × (−100), where −100 is a fall. From the cell S9 itself (v* = 3.06) a step down is indeed bad, but further along the bottom row there is a short path to the exit: three steps against five for the detour on top. Q-learning estimates the maximum over actions and therefore walks the edge, paying for speed with falls; SARSA takes its own random steps into account and chooses the safe detour."
  - q: "Is it true that Q-learning is better than SARSA?"
    a: "Not “better”, but cheaper or more expensive — it depends on the task. On our cliff Q-learning has a lower error (1.69 against 2.85) and a higher return (3.32 against 0.16), but more falls (96 against 59), and with continued exploration it loses more (−5.08 against −4.41). The cautious policy pays less, the bold one earns more; what to choose depends on the price of a fall."
  - q: "Why is the Q table unsuitable for a robot that learns to walk?"
    a: "Because the states and actions cannot be counted: a state is a vector of angles, velocities and body tilts, the actions are continuous torques in the joints. A table for such sets cannot be set up. Instead of a table they take a function: state at the input, estimate at the output; it generalises to similar states, but the convergence guarantees that the contraction of the Bellman operator gave are lost."
  - q: "What does λ add in TD(λ)?"
    a: "It is a knob between two extremes: at λ = 0 the target is pure TD, “the step plus the estimate further on”, at λ closer to one the target leans more and more on the real return up to the end of the episode, that is it approaches Monte Carlo. One parameter mixes targets of different depth."
  - q: "Who are the actor and the critic?"
    a: "Two roles in one algorithm. The actor chooses an action by the current policy, the critic estimates the value and tells the actor how much better its step was than expected; the hint is the TD error. In the tabular version both jobs were done by one table Q — here they are separated, and that opens the way to approximation."
terms:
  - term: "learning from experience (without a model)"
    definition: "a way of learning in which the agent does not know the transition probabilities and learns from what really happened"
  - term: "experience (a step)"
    definition: "the four-tuple (s, a, r, s′): where the agent was, what it did, how much it got, where it ended up"
  - term: "Monte Carlo"
    definition: "a method that waits for the end of the episode and shifts the estimate towards the full return over the rest of the episode"
  - term: "return G"
    definition: "the sum of discounted rewards over the rest of the episode: G = r + γ · G_next"
  - term: "update target"
    definition: "the number the estimate is shifted towards: for Monte Carlo the return, for temporal differences the step plus the discounted estimate further on"
  - term: "TD error"
    definition: "the difference between the target r + γ · Q(s′, ·) and the current estimate Q(s, a); that is exactly what the update drives"
  - term: "bootstrapping"
    definition: "assembling the target from our own estimate, not only from facts: the target relies on the estimate of the next state"
  - term: "bias and variance"
    definition: "the trade-off between targets: the Monte Carlo target is unbiased but noisy, the TD one is biased yet steadier"
  - term: "terminal state"
    definition: "the state in which the episode ends; nothing lies beyond it, so the target of a step into the terminal is r + γ · v(terminal)"
  - term: "on-policy"
    definition: "learning about the same policy the agent acts by; the exploration noise enters the learning target"
  - term: "off-policy"
    definition: "the behaviour policy and the learning policy are separated: we learn about the greedy one while acting with exploration"
  - term: "SARSA"
    definition: "a TD method with an on-policy target: the target is r + γ · Q(s′, a′), where a′ is chosen by the same policy; the name is made of the letters s, a, r, s′, a′"
  - term: "Q-learning"
    definition: "a TD method with an off-policy target: the target is r + γ · max_a Q(s′, a)"
  - term: "α — the learning step"
    definition: "the share of the difference “target − estimate” that we take into the estimate in one step; with α = 0.1 that is the average over the last ten episodes"
  - term: "γ — the discount"
    definition: "the weight of a future reward; it sets the foresight, the horizon 1/(1 − γ) — with 0.9 that is ten steps"
  - term: "exploration ε"
    definition: "the share of random actions in the ε-greedy policy: how much we pay for not missing the unexplored"
  - term: "the “cliff” variant"
    definition: "our example: the start S9, the bottom row S9–S11 is the dangerous place, a step down off the cliff breaks the episode at a cost of −100; the short path along the cliff is three steps"
  - term: "cliff and fall"
    definition: "the cliff is the dangerous place and the name of the variant, a fall is dropping into it; an episode break is the end of the episode, a different word"
  - term: "approximation of the value function"
    definition: "replacing the table with a function: state at the input, estimate at the output; it generalises to similar states but loses the convergence guarantees"
  - term: "actor-critic"
    definition: "a scheme of two roles: the actor chooses actions, the critic estimates values and hints through the TD error"
lecture:
  - title: "Lecture 6 presentation (PPTX)"
    href: "/files/course/rl/l6-sarsa-i-q-obuchenie.pptx"
---

## Where we came from: the model stood on the right

The maze is the same as in lectures 4 and 5: a 3 × 4 grid, the cells S1…S11, the exit S12. The numbers are the same too: a step **−1**, entering the exit **+10**, the discount **γ = 0.9**, the slip **0.8 / 0.1 / 0.1**.

Everything before relied on the **model of transitions** $p(s'\mid s,a)$: in lecture 4 we assembled the Bellman equations from it, in lecture 5 we solved them by substitution:

$$v(s) = \sum_a \pi(a\mid s)\sum_{s'} p(s'\mid s,a)\left[\,-1 + 0{,}9\,v(s')\,\right]$$

and for one step:

$$q(s,a) = -1 + 0{,}9\sum_{s'} p(s'\mid s,a)\,v(s')$$

$\pi(a\mid s)$ is the policy, the agent chooses it; $p(s'\mid s,a)$ are the transitions of the environment: the agent does not choose them, it **knows** them, which is why the right-hand side could be computed.

![On the left a maze with arrows, on the right the block “model p(s′|s,a)” crossed out](/img/course/rl/l6-model-crossed.png)
<!-- FIG source: s_model_crossed.png -->
*Everything we solved in lectures 4 and 5 stood on this model — today there will be none.*

The checkpoints of the course come from the model: $v^*(S6) = 3{,}40$, $v^*(S7) = 5{,}25$, $v^*(S2) = 1{,}93$, $q^*(S6, \text{down}) = 3{,}26$ — any other answer here is a sign of a mistake.

The method of lecture 5 required known transition probabilities, and nobody hands them out: the environment has the model, but it is not available to the agent, and the environment is learned by itself. That is what is called learning from experience. **What will remain on the right-hand side if there is no model?** Experience — what actually happened — and it is enough to learn the same numbers.

## Instead of a model — experience: a step of four quantities

The numbers are taken from what happened: every step the environment returns a four-tuple $(s,\ a,\ r,\ s')$.

* **$s$** — the state the agent was in;
* **$a$** — the action it chose;
* **$r$** — the reward for this step;
* **$s'$** — the state it ended up in.

The four-tuples add up into the **tape of the episode** — nothing else comes from the environment.

The model speaks at once about **all** outcomes (“make $a$ — and with such and such probabilities you will end up in such and such states”), experience is about **one** that happened. The slip pulled the agent sideways, and in the four-tuple it will write only $s'$: that there was a slip is visible from the result.

From the four-tuple you can see which pair $(s,a)$ the episode touched — that is the one that gets the correction; $s'$ is needed to understand what stands further on: the old scheme went through all $s'$ with weights, here there is only one.

In experience the agent **never sees value**: the reward is a fact from the environment, while $Q(s,a)$ is what we want to learn to compute. A step costs **−1** (the convention of lectures 3–5); the **+10** does not “drip” along the way — it is brought by the last step into the terminal.

## What exactly we learn: the table Q(s,a)

We will learn about the **table** $Q(s,a)$: a row is a state, a column is an action, a cell holds an estimate.

$$Q(s,a) \approx \text{how much on average you can get if in state } s \text{ you take action } a, \text{ and then act reasonably}$$

![A maze of 11 cells and the exit on the left, an empty 11 × 4 table with the arrows ↑ ↓ ← → on the right](/img/course/rl/l6-q-table-empty.png)
<!-- FIG source: s_q_table_empty.png -->
*The table is empty: 44 cells are waiting for experience.*

The size of the table comes from the task: there are eleven playable cells (S1…S11), the exit S12 is not included (a terminal, no action is chosen after it), there are four actions — ↑ ↓ ← →, hence $11 \times 4 = 44$; not a single number can be computed in advance — the agent starts with zeros and shifts them towards the truth.

A cell is a promise of a number, not a fact: the zero at the start is too high, and the table converges gradually. One number per row is not enough: $v(s)$ is the average over the actions of the policy, and S6 holds 3.40, but what a step down is worth cannot be made out.

The reference points are the checkpoint numbers of lecture 5: $Q(S6, \downarrow)$ will come to **3.26**, the maximum of row S6 — to **3.40**. The price of a step down is less than the price of the best action, that is in S6 it is more profitable not to go down; the table suggests the policy itself — take the column with the largest number ($\pi(s) = \arg\max_a Q(s,a)$, on a tie — right, as in lecture 4). Previously the numbers came from the model, now from experience.

What gets filled is the **pair** “cell plus step”, and only when the step has really been made: in one pass the agent touches several pairs out of 44. It is the table that will not let the method go beyond the maze; all methods of learning from experience fill one table and differ only in the update target.

## What we need from the environment

Since the model is gone, the environment has to report exactly three things about itself: how to start an episode (a reset to S1), how much to pay for a step (**−1**) and whether the episode is over (the flag `done`).

The agent gives away an action $a$, the environment returns the state, the reward and the end flag: $a \;\longrightarrow\; (s',\ r,\ \text{done})$.

There are **no** transition probabilities in the exchange: the environment does not say why the agent ended up in this $s'$ — it answers with facts only. The command “left” at a wall gives $s' = s$ and $r = -1$: it is as if there was no step, yet the unit is charged — hence the loops and “always left” for −10 in lecture 5.

The end flag is needed to know what stands in the update target: an ordinary cell has an estimate and the path continues, while nothing follows the exit — its value is given by the number **+10**. Without the end flag the learning will compute something for a state that does not exist.

We already have such an environment: `environment.py` from seminar 2 (in the libraries — `reset`, `step`).

## Monte Carlo: wait until the end of the episode

The simplest answer: wait for the end of the episode and count how much has accumulated in total. A run without slips — $S1 \to S2 \to S3 \to S4 \to S8 \to S12$: five steps of −1 and entering the exit. The quantity we need is the **return** over the rest of the episode, all the remaining rewards with the discount:

$$G_t = r_{t+1} + \gamma\, r_{t+2} + \gamma^2 r_{t+3} + \dots$$

In the maze every reward equals −1, so it is convenient to count from the end: $G = -1 + 0{,}9 \cdot G_{\text{next}}$, where “next” is the return of the following step, and for a step into the exit — the value of the terminal, 10.

![The route 1→2→3→4→8→12, under the steps the returns 1.81 · 3.12 · 4.58 · 6.20 · 8.00, under the exit +10](/img/course/rl/l6-mc-route.png)
<!-- FIG source: s_mc_route.png -->
*Monte Carlo learns from the return over the rest of the episode: every step has its own.*

| Step | Substitution | Return |
| --- | --- | --- |
| S8 → S12 (into the exit) | $-1 + 0{,}9 \cdot 10$ | **8.00** |
| S4 → S8 | $-1 + 0{,}9 \cdot 8{,}00$ | **6.20** |
| S3 → S4 | $-1 + 0{,}9 \cdot 6{,}20$ | **4.58** |
| S2 → S3 | $-1 + 0{,}9 \cdot 4{,}58$ | **3.12** |
| S1 → S2 | $-1 + 0{,}9 \cdot 3{,}12$ | **1.81** |

The closer to the exit, the bigger the return; in the first cell — 1.81. With 4.58 be careful: the same number was in lecture 4 (“value by distance”), while 6.20 and 3.40 come from lecture 5.

Let us check the return of a step in S3 directly: three steps of −1 and entering the exit:

$$G(S3) = -1 - 0{,}9 - 0{,}81 + 0{,}9^3 \cdot 10 = -1 - 0{,}9 - 0{,}81 + 7{,}29 = 4{,}58$$

the same as in the table: the recursion “from the end” and the sum “from the beginning” give one return.

The return turns into an estimate by the rule

$$Q(s,a) \leftarrow Q(s,a) + \alpha\bigl(G - Q(s,a)\bigr)$$

the estimate of the pair $(s,a)$ shifts towards the target not wholly, but by the share $\alpha$; exactly the pair that occurred in the episode is updated. The episode is played to the end and then we walk back through the list of rewards.

The weak spot is visible at once: while the episode is not over, the return $G$ is unknown and there is nothing to update; the letter $\alpha$ is new — let us take it apart right away.

## The learning step α: the share of the difference

$\alpha$ is the **share of the difference** that we take into the estimate in one step: the share of the path from the old estimate to the target.

The last step of the route: the estimate is empty ($Q = 0$), the target is known ($G = 8{,}00$), the difference $G - Q = 8{,}00 - 0 = 8{,}00$. Then $Q_{\text{new}} = Q + \alpha\,(G - Q) = 0 + \alpha \cdot 8{,}00$:

| α | Estimate from $Q = 0$, target $G = 8{,}00$ |
| --- | --- |
| **0** | $0 + 0 \cdot 8{,}00 = 0$ |
| **0.1** | $0 + 0{,}1 \cdot 8{,}00 = 0{,}80$ |
| **1** | $0 + 1 \cdot 8{,}00 = 8{,}00$ |

Zero is a deaf estimate, one is a credulous one, a tenth is the working middle (that is the default in the course): with $\alpha = 0{,}1$ the target 8.00 does not turn into the estimate at once — it comes out 0.80.

The shift works the same downwards: it holds 8.00, a new measurement gave 6.20 (the path is a step longer) — $Q = 8{,}00 + 0{,}1 \cdot (6{,}20 - 8{,}00) = 8{,}00 - 0{,}18 = 7{,}82$.

The middle was chosen because of the noise: the return $G$ wanders, the same route pays off differently. A small share is averaging: a fresh episode weighs 0.1, the previous one 0.09, the next 0.081, in total one:

$$0{,}1 + 0{,}1 \cdot 0{,}9 + 0{,}1 \cdot 0{,}9^2 + \dots = \frac{0{,}1}{1 - 0{,}9} = 1$$

An estimate with $\alpha = 0{,}1$ is the average over the last ten episodes ($1/0{,}1 = 10$); with $\alpha = 1$ — exactly the last measurement.

Let the target 8.00 repeat from episode to episode:

$$Q_1 = 0 + 0{,}1 \cdot 8{,}00 = 0{,}80$$
$$Q_2 = 0{,}80 + 0{,}1 \cdot (8{,}00 - 0{,}80) = 0{,}80 + 0{,}72 = 1{,}52$$
$$Q_3 = 1{,}52 + 0{,}1 \cdot (8{,}00 - 1{,}52) = 1{,}52 + 0{,}65 = 2{,}17$$

The remainder of the difference melts away by a tenth: 0.80 → 1.52 → 2.17 → …, converging to 8.00.

$\alpha$ does not decide where the estimates converge — only the speed and the smoothness. $\gamma$ is set by the statement of the task, $\alpha$ is a knob of the algorithm itself.

## What Monte Carlo cannot do

The rule $Q(s,a) \leftarrow Q(s,a) + \alpha\,(G-Q(s,a))$ is honest: $G$ is the real return over the rest of the episode. But honesty has a price, and there are three limitations.

**First: until the episode is over there is nothing to update.** The return 1.81 in the first cell is made of five steps that have not happened yet; in the maze the wait is short, but the longer the path, the longer the method stays silent.

**Second: in continuing tasks there is no episode at all.** An episodic task has a beginning and an end, a continuing one has none by its statement: controlling a plant, regulating a flow. Waiting for the outcome is pointless, and cutting the process into pieces means letting a truncated return into the rule.

**Third: the return is noisy.** The plan of the route is carried out differently every time: with probability 0.8 the command works as intended, with 0.1 each the agent is pulled sideways. The same greedy policy, two thousand runs:

| What we measure | Number |
| --- | --- |
| An ideal run without slips | **1.81** |
| Average return | **0.64** |
| Minimum return | **−6.29** |
| Maximum return | **1.81** |
| Runs that came more than one short of the average | **642 out of 2000** |

The average return of the same policy is 0.64: the slips eat more than half, while the best of two thousand runs again gave 1.81. Every third run (642 out of 2000, about 32 %) went below −0.36.

The slip accumulates over all the steps: an episode a step longer — a loss of 0.9, two steps longer — 0.9 + 0.81; at a wall the agent pays for a step without moving (hence the loops and “always left” for −10). The noise is a property of the target itself: $\alpha$ smooths it by averaging, but a single measurement stays noisy.

## Temporal differences: a target of two parts

Two things about a step are known for certain: how much was paid and where we landed — $r$ and $s'$ are facts, the rest is unknown; but the table $Q$ already holds a rough estimate of that very $s'$:

$$\text{target} = r + \gamma \cdot Q(s', \cdot)$$

| | Monte Carlo target | Temporal-difference target |
| --- | --- | --- |
| What it is made of | the whole return over the rest of the episode | one step plus the estimate further on |
| When it is known | after the end of the episode | right after the step |
| What it relies on | fact | our own guess |

The difference between the target and the estimate is called the **TD error** (*temporal difference*):

$$\text{TD error} = \bigl(r + \gamma \cdot Q(s',\cdot)\bigr) - Q(s,a)$$

The update rule keeps its old form, only the target changes: $Q(s,a) \leftarrow Q(s,a) + \alpha \cdot \text{TD error}$.

At the start of learning the table is zeroed:

| Case | Substitution | Target |
| --- | --- | --- |
| An ordinary step | $-1 + 0{,}9 \cdot 0$ | **−1.00** |
| A step into the exit | $-1 + 0{,}9 \cdot 10$ | **8.00** |

An ordinary step gives exactly −1.00: the next node is estimated at zero, so the target is only the price of the step; temporal differences are “blind” to the future, but it will be pulled in by itself when the estimate of one cell goes into the target for the previous one. A step into the exit gives 8.00: the “estimate further on” there is not zero but the value of the terminal, **+10**.

The construction is called **bootstrapping** (“pull yourself up by your bootstraps”): the target is built from our own estimate and not from fact. It is legitimate because the Bellman equation links the value of a pair with the value of the next step: in lectures 4 and 5 the right-hand side was computed by the model, while here the sum over outcomes is replaced by the single one that happened. TD is the same Bellman equation, but for estimates.

The symbol $Q(s',\cdot)$ is still general: behind it there will be either the estimate of the pair $(s',a')$ chosen by the policy, or the maximum over actions.

![One step: on the left a cell, on the right the next one, above the arrow r = −1; on the right the table of estimates of the next state, below “the target equals r plus 0.9 times Q(s′, ·)”](/img/course/rl/l6-td-step.png)
<!-- FIG source: s_td_step.png -->
*The temporal-difference target is glued from two parts: the fact for the step plus the estimate further on.*

## Learning as we go

The difference is visible also in **when** the update arrives: in Monte Carlo the corrections are shifted to the end of the tape, in temporal differences an update stands under every step.

* **The corrections start at once:** a step that has been made already has a target — there are as many updates, one per step, but they come as we go.
* **No need to store the episode:** Monte Carlo accumulates the rewards in a list and walks back through it; TD corrects on the spot and forgets the step at once.
* **It works where there is no end:** learning goes on while the agent acts — hence the second name of the mode, learning “on the go”, online.

Now the price: the TD target relies on **immature estimates** — at the start the target of an ordinary step equals −1.00, and the error of the estimate of the neighbouring cell does not disappear but is copied into the target: TD believes itself. After the first successful step into the exit the estimate $Q(S8,\downarrow)$ shifts towards 0.80, and the target for a step from S4 (it leads to S8) is no longer −1.00 but $-1 + 0{,}9 \cdot 0{,}80 = -0{,}28$; then the “news” spreads cell by cell.

Hence the main risk: a quick correction fixes the error — a wrong estimate further on becomes part of the target, the target pulls the estimate towards itself, and so on in a circle. Monte Carlo is protected: its target is a fact.

## Bias and variance: what we pay with

**Bias** is a systematic miss: where the estimate goes on average. **Variance** is the spread of the random deviations around that average.

The Monte Carlo target is the full return over an episode, a fact and not a guess: averaging over many episodes brings us to the true value, so the estimate is **unbiased**; on the other hand the variance grows with the length of the episode. The TD target is the step plus our own estimate further on: its error does not vanish under averaging, so the estimate is **biased**; on the other hand only one random quantity enters the target, the reward for the step — and the variance is smaller.

![Two bells: a wide one centred on the truth (the Monte Carlo target) and a narrow one with a shifted centre (the TD target); the labels “variance” and “bias”](/img/course/rl/l6-two-bells.png)
<!-- FIG source: s_two_bells.png -->
*The bias–variance trade-off: an unbiased but noisy target against a steady but shifted one.*

A long episode makes the Monte Carlo target noisy — a steady, even if biased, TD target is more profitable; a short one leaves Monte Carlo almost exact. The trade-off has no common winner: the only question is what is more expensive in the task.

Between the extremes there is a smooth transition: the parameter $\lambda$ mixes targets of different depth — with $\lambda = 0$ it is pure one-step TD, with $\lambda \to 1$ — almost Monte Carlo (TD($\lambda$)).

## The terminal: there is nothing behind the exit

So far we assumed that after a step there is an $s'$ with an estimate — but for the exit that is not so: S12 is a terminal, the episode ends there, and it has no row in the table $Q$ (the table is 11 × 4, without S12). There is nobody to ask “what comes next”, so the rule for the target is separate:

$$\text{target} = r + \gamma \cdot v(\text{terminal})$$

where $v(\text{terminal})$ is the value of the exit from the statement of the task: with us it is **+10**. For the last step of the route: $-1 + 0{,}9 \cdot 10 = 8{,}00$.

| Case | What stands on the right | Substitution | Target |
| --- | --- | --- | --- |
| An ordinary step | the estimate of the next state from the table | $-1 + 0{,}9 \cdot Q(s',\cdot)$ | depends on the estimate |
| A step into the exit | the value of the terminal given by the task | $-1 + 0{,}9 \cdot 10$ | **8.00** |

8.00 is the same number that Monte Carlo has on the last step: the rest of the episode there consists of one entry into the exit. Monte Carlo learns it by playing the episode out; TD knows it at once, because the value of the terminal is given in advance — the only number not from experience.

**A typical mistake is “asking what comes next”.** If the program does not tell the terminal from an ordinary cell and substitutes $Q(s',\cdot)$ on a step into the exit — zeros, for instance — the target of the last step will be $-1 + 0{,}9 \cdot 0 = -1{,}00$ instead of 8.00. Then entering the exit, which pays +10, will be estimated as an expensive and useless step, and the agent will learn that going to the exit is bad: it will start circling the maze, paying −1 each time. The end flag (`done`) is what the algorithm uses to understand that on the right stands the value of the terminal and not an estimate from the table.

## Numbers: Monte Carlo and TD on the maze

Besides Monte Carlo, the table holds two temporal-difference targets — SARSA and Q-learning; they are discussed further on, and for now we look at the Monte Carlo row.

The setup: the base 3 × 4 maze, learning from zeros, $\alpha = 0{,}1$, $\varepsilon = 0{,}1$, a thousand episodes, seed 7. We measure the **error** $|Q - q^*|$ — the difference of the table from the right answer — averaging over all 44 pairs $(s,a)$; the answer $q^*$ is known from lectures 4 and 5, so this is not an exercise but a check.

| Method | Error after episode 1 | Error after episode 1000 | Threshold 2.00 | Threshold 1.00 | Correct greedy actions |
| --- | --- | --- | --- | --- | --- |
| Monte Carlo | 2.54 | **0.89** | episode 53 | episode 754 | 10/11 |
| SARSA | 2.55 | **1.30** | episode 266 | not reached | 8/11 |
| Q-learning | 2.52 | **0.94** | episode 132 | episode 886 | 10/11 |

The comparison is honest: the settings are identical, only the method changed; all start from the same place (2.54 / 2.55 / 2.52 — the table is zeroed). After that the curves go down: Monte Carlo at episode 10 — 2.26, at 50 — 2.03, at 200 — 1.53; SARSA — 2.67, 2.59, 2.12; Q-learning — 2.69, 2.47, 1.82.

![Error curves |Q − q*| by episode: Monte Carlo crosses the threshold 2.00 at episode 53, Q-learning at episode 132](/img/course/rl/l6-learning-curves.png)
<!-- FIG source: s_learning_curves.png -->
*Both curves fall towards one; the marks show where each crosses the threshold 2.00.*

The greedy routes converge to the exit: SARSA learns the path 1 → 2 → 3 → 7 → 11 → 12, Q-learning — 1 → 2 → 3 → 7 → 8 → 12; Monte Carlo has 10 correct greedy actions out of 11.

The conclusion, and here care is needed: the claim “Monte Carlo is slower and noisier” **is not confirmed by these numbers** — it crosses the threshold 2.00 earlier than Q-learning (episode 53 against 132), and its final error is no bigger: 0.89 against 0.94.

Something else is confirmed: **on a simple maze the curves are close, the methods have nowhere to diverge** — there are no dangerous places, the episode is short, and any sensible method will bring the error below one.

The difference starts to matter where **the episodes are long and there are dangerous places**: the price of one careless step sharply changes the target, and the different properties of the targets become visible in numbers. We will take such an environment apart — a maze with a cliff and a fall behind it — in the next part, together with SARSA and Q-learning.

## On-policy: learning about our own

In the second part the right-hand side of the target was left general:

$$\text{target} = r + \gamma \cdot Q(s', \cdot)$$

The symbol “$\cdot$” is an open question: the step is made, $r$ is received, $s'$ is known, but what exactly to take from the row $s'$ is not visible. The methods have two answers.

The first: take the estimate of the pair that the policy has already chosen. The agent reaches $s'$ and by the usual rule picks the next action $a'$ — its estimate becomes the second half of the target:

$$\text{target} = r + \gamma \cdot Q(s', a')$$

The action $a'$ was chosen by the same policy the agent walked by. The name of the method is a gluing of five letters: $s$, $a$, $r$, $s'$, $a'$ (State, Action, Reward, State, Action) — **SARSA**. The update rule is as before, only the target changes:

$$Q(s,a) \leftarrow Q(s,a) + \alpha\bigl[\, r + \gamma \cdot Q(s', a') - Q(s,a) \,\bigr]$$

with $\gamma = 0{,}9$. One cell is corrected — the pair $(s,a)$ whose step has just happened; $a'$ is not an object of learning but part of the target.

A method that learns about the same policy it acts by is called **on-policy**: the policy chooses the steps, and we learn estimates about that same policy. We act $\varepsilon$-greedily — which means $a'$ was chosen by the same rule, with all its randomness. Hence: our $\varepsilon$-noise enters the target directly.

## Our ε-noise enters the target

$Q(s',a')$ in the target is a **random quantity**: its value depends on what the policy chooses. More often it is the best pair, sometimes a badly estimated one; the “bad” case pulls the target down no weaker than a real step.

A snapshot of the “cliff” variant after **100 episodes**, the cell S10 by the dangerous place:

| Action | Estimate |
| --- | --- |
| ↑ up | **−0.35** |
| ↓ down | **−24.66** |
| ← left | **0.13** |
| → right | **5.46** |
| average over the four | **−4.86** |

The target of the transition S9 → S10, where $r = -1{,}00$, $\alpha = 0{,}10$, $\gamma = 0{,}90$, $\varepsilon = 0{,}10$:

* nine times out of ten the policy takes the best action:
  $$\text{target} = -1{,}00 + 0{,}9 \cdot 5{,}46 = \mathbf{3{,}91}$$
* one time out of ten — a random one; if it is “down”, the target collapses:
  $$\text{target} = -1{,}00 + 0{,}9 \cdot (-24{,}66) = \mathbf{-23{,}19}$$

SARSA substitutes neither one case nor the other, but the **average over what the policy will choose**: with probability 0.9 the best action, with 0.1 — any of the four, on average −4.86:

$$\text{target} = -1{,}00 + 0{,}9 \cdot \bigl[\,0{,}9 \cdot 5{,}46 + 0{,}1 \cdot (-4{,}86)\,\bigr] = \mathbf{2{,}98}$$

![Cell S10 with four estimates; two branches of the target — “9 out of 10 → right” gives 3.91 and “1 out of 10 → down” gives −23.19, below the average target 2.98](/img/course/rl/l6-s10-noise.png)
<!-- FIG source: s_s10_noise.png -->
*One branch follows the best action, the other a random one; SARSA takes the average and is therefore cautious.*

The SARSA target **takes into account in advance that the agent will sometimes stumble by itself**: the maximum of the row would give 3.91, the average target with noise — 2.98, 0.93 less. These 0.93 are the risk premium that the method writes in for itself; its size depends on one thing: how expensive a random step is.

The snapshot was taken in a Q-learning run, while the target is computed from it for SARSA — and that is legitimate: the target is not a property of the method.

## Off-policy: Q-learning

The second answer: take not the estimate of the chosen pair, but the **best of what is possible** — not “how I will play” but “how one could have played”:

$$\text{target} = r + \gamma \cdot \max_a Q(s', a)$$

The maximum is not a random quantity but the highest figure of the row; exploration does not enter such a target. The same transition S9 → S10, the same snapshot after 100 episodes:

$$\text{target} = -1{,}00 + 0{,}9 \cdot \max(-0{,}35;\ -24{,}66;\ 0{,}13;\ 5{,}46) = -1{,}00 + 0{,}9 \cdot 5{,}46 = \mathbf{3{,}91}$$

SARSA had **2.98** on the same transition on average: one step, one four-tuple, identical $\alpha$, $\gamma$ and $\varepsilon$ — different targets.

![The same transition S9 → S10 and two targets: the estimate of the chosen pair against the maximum over actions](/img/course/rl/l6-two-targets.png)
<!-- FIG source: s_two_targets.png -->
*One and the same transition, two targets — the estimate of the chosen pair against the maximum over actions.*

A method whose learning policy is separated from the behaviour policy is **off-policy**. There are two policies: the **behaviour** one, by which the agent collects experience ($\varepsilon$-greedy with exploration), and the **learning** one, about which we learn estimates (the greedy one, “always play the best action”). Experience comes from the first, the table learns about the second: that is why one can also learn from someone else's experience — demonstrations and past runs will do.

| | SARSA — on-policy | Q-learning — off-policy |
| --- | --- | --- |
| What we take from $s'$ | the estimate of the chosen pair $Q(s',a')$ | the maximum over actions $\max_a Q(s',a)$ |
| Whom we teach | the same policy we act by | “as if from here on we played the best” |
| Where the $\varepsilon$-noise goes | enters the target directly | does not enter the target |
| Target on the transition S9 → S10 (snapshot 100) | **2.98** (on average) | **3.91** |

The update rule and everything else is as before; only the content of the right-hand side is new. The name of the second method is **Q-learning**.

The asymmetry: for SARSA a random step “down” was part of the target and dropped it to −23.19, for Q-learning it does not get into the target at all. So Q-learning learns estimates that are honest **with exploration switched off**; for the methods to diverge we need an environment where a wrong step is really expensive.

## The “cliff” variant: the short path and the detour

We made such an environment ourselves. The start is S9, the bottom row S9, S10, S11 is the **cliff**: behind it there is an abyss, and the action “down” from any cell of the cliff means a fall with the value **−100**. We do not touch the main maze of lecture 4. The terms: the **cliff** is the dangerous place and the name of the variant, a **fall** is dropping into it, an **episode break** is the end of the episode, as it is named in the course program.

![A 3 × 4 grid: the bottom row S9–S11 is the cliff, under it the band “fall −100”, along the cliff a short path and on top a safe detour to the exit](/img/course/rl/l6-cliff-plan.png)
<!-- FIG source: s_cliff_plan.png -->
*The cliff is the bottom row S9–S11; down from it — a fall with the value −100.*

The start is S9 in the bottom left corner, the exit is the bottom right: the last two steps go down from S8 and right from S11. The bottom row is dangerous — a step down from it means a fall — while the cells of the row above always have either a cell or the exit under their feet. The start stands on the most dangerous line: the decision is made at once.

There are two roads to the exit: **along the cliff, 3 steps** — S9 → S10 → S11 → exit; **on top, 5 steps** — S9 → S5 → S6 → S7 → S8 → exit. The difference is two steps, but one road goes along the very cliff, where the price of a mistake is exceptional. A step “down” from S9:

$$q^*(S9, \text{down}) = -1 + 0{,}9 \cdot (-100) = \mathbf{-91{,}00}$$

We pay −1, and right behind the cliff — a fall at −100, discounted by 0.9. The value of the cell itself is meanwhile **3.06**:

$$v^*(S9) = \mathbf{3{,}06}$$

The number is positive: in the optimal policy “down” on the cliff is never chosen, and the value of the cell is set by the detour, not by the fall; the same cell with the same step turns from +3.06 into −91.00. Next to it S10 with the value **5.04** — and the same abyss is right beside it.

On the safe path a wrong step costs one or two units, on the cliff — ninety-odd: here the cautious correction of SARSA finally gets its weight. The checkpoints of the course are in place: $v^*(S6) = 3{,}40$, $v^*(S7) = 5{,}25$, $v^*(S2) = 1{,}93$.

## Two characters on one environment

We train both methods on the “cliff” from zeros, under identical conditions: $\alpha = 0{,}1$, $\varepsilon = 0{,}1$, a thousand episodes, seed 7. The environment, the rewards and the settings are the same — yet the policies are not alike.

![On the left the SARSA map: the detour on top S9 → S5 → S6 → S7 → S8 → exit; on the right the Q-learning map: along the cliff S9 → S10 → S11 → exit](/img/course/rl/l6-two-maps.png)
<!-- FIG source: s_two_maps.png -->
*One cliff, two learned policies: the cautious one walks away from the risk, the bold one walks along it.*

**SARSA goes around the cliff on top** — 9 → 5 → 6 → 7 → 8 → 12, five steps; **Q-learning walks the cliff** — 9 → 10 → 11 → 12, three steps. What frightens the cautious one is not the extra step but −91.00 for one wrong one; the bold one gives the risk no weight: its target is the maximum, and the maximum does not notice a random step.

Before looking at the numbers, let us separate two metrics. The **estimation error** averages the difference from $q^*$ over all 44 pairs $(s,a)$; the **correct greedy action** looks only at the order inside a row — which of the four numbers is the largest — and is therefore stricter: a row can be close in numbers but with the order mixed up. Hence “the error is lower” and “fewer correct actions” do not contradict each other.

| | SARSA | Q-learning |
| --- | --- | --- |
| Falls during training | **59** | **96** |
| Return of the greedy policy | **0.16** | **3.32** |
| Return with continued exploration, $\varepsilon = 0{,}1$ | **−4.41** | **−5.08** |
| Error $\lvert Q - q^*\rvert$: from the start to the 1000th | 8.00 → **2.85** | 8.01 → **1.69** |
| Correct greedy actions | 7 out of 11 | 4 out of 11 |

Q-learning has fewer correct actions (4 out of 11 against 7), but also a lower error (1.69 against 2.85), yet more falls (96 against 59). The lower error of the bold one is explainable: $q^*$ are the values of the **greedy** policy, Q-learning learns about exactly the greedy one, while SARSA learns about its own $\varepsilon$-greedy one, cautious at the cliff, and therefore stands further from $q^*$.

SARSA puts into the target the average over its $\varepsilon$-greedy behaviour — together with the random step, which at the cliff costs a fall. The estimate for the cliff comes out low, and the method voluntarily chooses the detour. Q-learning takes the maximum of the row: the cliff is as profitable for it as it would be without exploration — three steps against five — hence the 96 falls against 59.

Why the cautious one **pays less and the bold one earns more**: a greedy run gives 0.00 falls for both, while the routes differ — three steps against five. Hence the return 3.32 against 0.16: the difference is the price of a safety margin, since every extra step costs minus one. But during training the insurance pays off: 59 falls against 96.

“Better” depends on the task:

* if a fall is lost points and the goal is to earn more, the bold one is right: the return 3.32 against 0.16, the estimate is more accurate — 1.69 against 2.85;
* if a fall is expensive or irreversible, what matters more is not the return but the number of catastrophes: 59 against 96 in favour of SARSA;
* if exploration **continues**, both are in the red, but the bold one loses more — −5.08 against −4.41.

It is not a seed accident: over six runs SARSA falls less often than Q-learning in **all six** (59–76 against 93–108), and Q-learning goes along the cliff also in **all six**; only the detour of SARSA changes, but it never chooses the cliff.

The argument between these methods is not about the right answer but about which behaviour to consider right. The caution of SARSA is insurance against its own exploration, and by definition it costs return; the boldness of Q-learning is a bet that exploration will be switched off and the play will be greedy. While a mistake is cheap the insurance is unnoticeable — that is why on a simple maze the methods had nowhere to diverge; at the price of a mistake of −91.00 it becomes the main thing that tells them apart.

## Three knobs: α, γ, ε

**α is the share of the difference** that we take into the estimate in one step (in detail — in the section “The learning step α: the share of the difference”):

$$Q(s,a) \leftarrow Q(s,a) + \alpha \cdot (\text{target} - Q(s,a))$$

**γ is the foresight**: how much the future is discounted and how far ahead the agent looks (lectures 3 and 5). The scale is the horizon $1/(1-\gamma)$: with γ = 0.9 that is **ten steps**, with 0.99 — a hundred. Ten is more than enough for our maze; γ = 1 would zero out both the discounting and the guarantees.

**ε is how much we explore.** The share of steps given to randomness: nine out of ten — the best action, one — any of the four. This is a knob not of the estimates but of behaviour; its price is further on.

The roles: **γ is set by the statement of the task, while α and ε are chosen by us.** Change γ and it is not the speed that changes but the task itself: the price of the future becomes different.

| Knob | What it is responsible for | Who sets it | Dangerous edge |
| --- | --- | --- | --- |
| **α** | the share of the difference we take into the estimate | the algorithm, we | large — the estimates jump; small — learning takes long |
| **γ** | foresight, the horizon $1/(1-\gamma)$ | the statement of the task | at one — no guarantees |
| **ε** | the share of steps given to exploration | the algorithm, we | at one — pure chance; at zero — we will not meet the danger |

* **α too large** — the estimate jumps after the latest random outcome; too small — smooth, but long.
* **ε = 1** — pure chance, the agent wanders at random; **ε = 0** — the dangerous place may never be met.
* **γ near one** — the horizon stretches, learning requires far more steps; with γ = 1 there are no convergence guarantees.

![Three sliders α, γ and ε; under α — two route maps: a hook with α = 0.5 and a clean detour with α = 0.1](/img/course/rl/l6-three-knobs.png)
<!-- FIG source: s_alpha_slider.png -->
*Three knobs of learning: speed, foresight, exploration.*

## How much exploration costs

The “cliff” variant, a thousand episodes, seed 7, both methods at ε: 0.20, 0.10, 0.02. The row shows: falls **during training**, the return of the learned **greedy** policy and the return of the same policy **with exploration**.

| ε | Falls during training | Return of the greedy policy | Return with exploration |
| --- | --- | --- | --- |
| **Q-learning** | | | |
| 0.20 | **201** | 3.30 | **−12.19** |
| 0.10 | **96** | 3.32 | **−5.08** |
| 0.02 | **22** | 3.32 | **+1.33** |
| **SARSA** | | | |
| 0.20 | **101** | −1.12 | **−11.24** |
| 0.10 | **59** | 0.16 | **−4.41** |
| 0.02 | **22** | 3.30 | **+1.35** |

In Q-learning the falls follow the decrease of ε strictly: **0.20 → 201, 0.10 → 96, 0.02 → 22**, while the return with exploration goes −12.19 → −5.08 → +1.33, from minus into plus: every extra random step at the cliff is an extra chance to fall, and a fall breaks the episode early. The less we explore, the less we pay.

The return of the **greedy** policy hardly moves together with ε: 3.30 → 3.32 → 3.32 — with exploration switched off ε does not affect such a game. The whole effect sits in the last column: at ε = 0.10 the policy promises 3.32, while with exploration it comes out −5.08; the rows 96 and 59 are from the table of the previous block.

SARSA has fewer falls — 101 against 201 at ε = 0.20 — but with a lot of exploration even the learned greedy policy brings −1.12: the cautious estimate leads it onto the long detour. At ε = 0.02 the two policies almost coincided: 22 falls each, the returns 3.30 and 3.32 (SARSA and Q-learning), with exploration +1.35 and +1.33. The difference between the characters is proportional to ε.

And the rule: **with no exploration at all the danger may simply not be met**, and the method will not learn to go around the cliff. That is why ε is not brought down to zero in one step — this is the “explore — exploit” trade-off.

![Two rows of bars by ε: the falls during training decrease, the return with exploration grows; in each row Q-learning and SARSA side by side](/img/course/rl/l6-eps-price.png)
<!-- FIG source: s_eps_price.png -->
*The less we explore, the less we pay; but ε must not be brought to zero.*

## Pitfalls

**A large α: the estimates jump.** The target is always assembled from chance: a large α tells the estimate to follow the noisy target almost wholly. At α = 0.5 SARSA gets stuck on a hook (9 → 5 → 1 → 2 → 3 → 7 → 8 → 12) with a return of −1.23 and 58 falls, Q-learning goes astray: 0.67 with 84 falls; at α = 0.2 SARSA is still on the same hook (−1.38, 43 falls), while Q-learning already walks the cliff (3.31, 75 falls); the clean picture is at α = 0.1: SARSA 9 → 5 → 6 → 7 → 8 → 12 (0.16), Q-learning 9 → 10 → 11 → 12 (3.32).

**The optimism of the maximum.** The maximum over a row of noisy estimates looks upwards: a randomly inflated number is exactly what it will take. According to the report (“cliff”, a thousand episodes, α = 0.1, seed 7) the average “promise minus truth” over the eleven cells is **negative** for both: −1.02 for Q-learning, −1.21 for SARSA — on average there is no overestimation, but in separate cells there is: Q-learning is worst in S9, **+0.83**, SARSA in S11, **+0.04**, on the most dangerous line. The lesson: **overestimation lives in separate cells, not on average** — averaging will not show it.

**“So Q-learning is better” is a hasty conclusion.** By the return of the greedy policy and the accuracy of the estimate the bold one is ahead, by the number of catastrophes and by robustness to continued exploration — the cautious one. “Better” here depends on what is more expensive in the task.

**Expecting the end of an episode where there is none.** Monte Carlo learns from the return over the rest of the episode, and that is defined only for a finished one — in a task without a finale there is nothing to wait for (in detail — in the section “What Monte Carlo cannot do”).

**Updating after the terminal.** The exit has no row in the table, so the target for a step into the exit is special, and the end flag `done` is the place where the algorithm chooses the right target (the computation — in the section “The terminal: there is nothing behind the exit”).

**The cliff, a fall and an episode break are not the same thing.** In the report file the variant itself is labelled “break” — a historical name, not to be confused with the end of an episode (the definitions of the terms are in the section about the “cliff” variant).

## A bridge: the table does not scale

Everything in this block rested on the **table** $Q(s,a)$ — eleven rows, four columns, forty-four numbers. That is possible only while the number of states and actions is finite and small: the table is enumerated in full and a cell is stored for every pair — and as soon as the pairs cannot be counted, the cells run out. What comes in place of the table, we will take apart in this same block.

## TD(λ): a knob between two extremes

The update target is chosen by depth: either the whole return up to the end of the episode (Monte Carlo), or one step plus our own discounted estimate further on (temporal differences). Between the extremes there is a smooth knob — the parameter **λ**. At **λ = 0** it is pure one-step TD, at **λ close to one** — almost Monte Carlo, with an eye on the whole episode. That is how TD(λ) works.

![A scale from TD (one step) to Monte Carlo (the whole episode), the λ slider stands in the middle](/img/course/rl/l6-td-lambda.png)
<!-- FIG source: s_td_lambda.png -->
*λ is a knob between two extremes: 0 — pure TD, closer to 1 — almost Monte Carlo.*

## Actor-critic: two roles

The tabular $Q(s,a)$ had one object doing two jobs: actions were chosen by it (ε-greedily) and it also corrected itself. The actor-critic (*actor-critic*) separates these roles.

**The actor** is the policy: it chooses an action and behaves. **The critic** is the value: it estimates how well the actor plays and gives it a hint. The hint is the same TD error: the difference between the target and the current estimate. The estimate grew — the action is reinforced, it fell — the actor moves away from it.

Here there are two separate learnable objects: one stores *what to do*, the other *how well it is going*; in the table both jobs were done by one row.

![Two boxes “actor (policy)” and “critic (value)”, between them the arrows “action” and “hint”](/img/course/rl/l6-actor-critic.png)
<!-- FIG source: s_actor_critic.png -->
*Two roles: the actor acts, the critic estimates and hints.*

## Approximation: table → function

A table requires a cell for every pair $(s,a)$; when the pairs cannot be counted, the cells run out. The task “teach a robot to walk”: a skeleton with muscles, each driven by its own signal; there are not four actions but one per combination of torques, and the states cannot be counted — the pose, the angles in the joints, the velocities, the tilt of the body change continuously. In games it is similar: the positions are immense in number, the available moves differ, there is no grid. To fill the table “state × action” is impossible: there are infinitely many rows, and the agent gets into each only in passing; the loop stays the same — state, action, reward, next state — while the table disappears.

Instead of a table we need a **function**: instead of a number for every pair — a small set of weights by which the estimate is **computed**:

$$Q(s,a) \approx f(s,a;\,w)$$

The state and the action are fed to the input, the estimate is read from the output. There are few weights, they are shared by all states, and the memory needed is as much as the function weighs. Along the way **generalisation** appears: similar states get similar estimates, so experience from one place works in the neighbouring ones, which the table could not do. That is what is called the **approximation of the value function**.

The state here is a vector of numbers: the angles in the joints, the velocities, the tilt of the body, sometimes the brightness of pixels. A neural network is one of such functions, a universal one: hence the name of the field — deep reinforcement learning.

![On the left the 11 × 4 table, on the right the scheme “state → function → estimate”](/img/course/rl/l6-table-to-function.png)
<!-- FIG source: s_table_to_function.png -->
*A function replaces the table: state at the input, estimate at the output.*

The price of freedom is familiar: **scale is paid for with guarantees**. With a table a correction touched exactly one cell, and convergence followed from the contraction of the Bellman operator (lecture 5). With a function the weights are shared: a correction because of one state changes the estimates of many others, and the promise of convergence becomes conditional. The update rule does not change — the estimate is shifted towards “the step plus the discounted estimate further on” — only the object of the correction changes: not a cell but the weights.

## Frameworks: Gymnasium and the rest

**Gymnasium** is the environment and the interface: `reset()` starts an episode and returns the initial state, `step(...)` makes a step and returns the next state, the reward and the end flag — the same three things that were required from the environment in the first part. The interface is one for all environments: the algorithm does not know what it is dealing with — changing the environment requires no edits in the learning. Ready-made sets: control classics, Atari, MuJoCo; the same environment as in block 1 is arranged in the same way and written by hand.

**Stable-Baselines3** — ready-made implementations of algorithms (DQN, PPO and others) on PyTorch. **CleanRL** — one file per algorithm: short code is convenient to check line by line against the formula. **RLlib** — when there are many environments at once and training is distributed over machines. In one line: **the environment is Gymnasium, the learning is the rest**.

![Four tiles: Gymnasium, Stable-Baselines3, CleanRL, RLlib; under each one line of purpose; the first is the environment, the rest are learning](/img/course/rl/l6-frameworks.png)
<!-- FIG source: s_frameworks.png -->
*What each library takes on: the environment — Gymnasium, the learning — the rest.*

## The map of the course and five thoughts

Three stations of the course: **lecture 4** — the Bellman formulas (value is the reward plus the discounted value further on); **lecture 5** — solving the equations by the model; **lecture 6** — the model is removed, the right-hand side holds one real step. Each station drops one requirement of the previous one; the discount and the table stay for now.

If the course is compressed into five sentences:

1. **Reinforcement learning is about the goal, not about the rule.** The agent acts for the total reward, and the methods of the course are different ways of assembling that goal.
2. **Everything rests on one rule:** the value now is the reward plus γ times the value later.
3. **The solution is built iteratively:** estimate — improve — estimate again.
4. **When there is no model, one learns from experience:** the target is the step plus γ times the estimate further on; that is temporal differences and the TD error.
5. **Caution and boldness.** SARSA learns about the same policy it acts by and is therefore cautious; Q-learning takes the maximum over actions and is therefore bold.

**Progress test 3** — at seminar 4, on 27 and 30 October; **lab 3** “a fleet of vehicles” — at seminars 10–12.

What tells the methods apart is not the update rule — that is common — but the target: one line to the right of the plus sets the character of the agent.

## What to take away

1. **Without a model the number is taken from experience.** Instead of transition probabilities the environment gives a tape of four-tuples $(s, a, r, s')$ — what actually happened.
2. **The update target is chosen by us.** Either the whole return up to the end of the episode, or the step plus the discounted estimate further on; the shift rule is the same, the right-hand side tells the methods apart.
3. **The TD error is the difference between the target and the current estimate.** In the terminal the target is special: $r + \gamma \cdot v(\text{terminal}) = 8{,}00$.
4. **One line of formula — two characters.** SARSA is on-policy: it learns about the same policy it acts by, together with its ε-noise, and is therefore cautious. Q-learning is off-policy: it takes the maximum over actions and is therefore bold.
5. **Three knobs: α, γ and ε.** α is the share of the difference we take into the estimate (speed); γ is the foresight, the horizon $1/(1-\gamma)$; ε is the share of random steps (the price of exploration).
6. **The table does not scale:** a cell for every pair $(s,a)$ cannot be filled in for a robot and a game. A function comes in its place, $Q(s,a) \approx f(s,a;\,w)$ — scale is paid for with guarantees.
7. **Next — four directions:** TD(λ), the actor-critic, approximation, frameworks.

## Check yourself

A short check on the lecture. The answers are hidden — answer by yourself first.

<div class="qa">
<details>
<summary>1. Why can Monte Carlo not learn in a continuing task?</summary>
<p>Its target is the return over the rest of the episode, and in a continuing task there is no episode: the process lasts as long as the system works. While there is no outcome there is no target and nothing to update; the process cannot be cut into pieces — a truncated return would get into the target.</p>
</details>
<details>
<summary>2. How does the SARSA target differ from the Q-learning target?</summary>
<p>SARSA takes the estimate of the pair $Q(s', a')$ that our own policy chose — together with its ε-noise (on-policy). Q-learning takes the maximum over the actions of the next state, “as if from here on we played greedily” (off-policy). The difference between the methods is to the right of the plus.</p>
</details>
<details>
<summary>3. Why is the rule different for a step into the exit?</summary>
<p>The exit S12 has no row in the table — the episode ends there. That is why the target = −1 + 0.9 · 10 = 8.00, where 10 is the value of the terminal. If an estimate from the table (or a zero) is substituted here, the step becomes −1.00, and the agent will learn to go around the exit.</p>
</details>
<details>
<summary>4. What will happen at α = 1?</summary>
<p>The estimate will become equal to the latest target: the accumulated memory is wiped, the estimates will jump after the latest random outcome. At α = 0.5 this is visible in numbers: SARSA gets stuck on the hook 9 → 5 → 1 → 2 → 3 → 7 → 8 → 12 with a return of −1.23 and 58 falls. A clean picture comes out at α = 0.1.</p>
</details>
<details>
<summary>5. Where does −91.00 come from?</summary>
<p>It is the price of a step “down” from the cell of the cliff S9: −1 + 0.9 · (−100) = −91.00, where −100 is the value of a fall. The value of the cell itself is positive meanwhile, $v^*(S9) = 3{,}06$: in the optimal policy “down” on the cliff is never chosen. One wrong step turns +3.06 into −91.00.</p>
</details>
<details>
<summary>6. Why is the table unsuitable for a robot?</summary>
<p>A skeleton with muscles has many actions — one per combination of torques — and the states cannot be counted: the table “state × action” is infinite. A function saves the day: state at the input, estimate at the output, shared weights and generalisation to the neighbouring states. But scale is paid for with convergence guarantees.</p>
</details>
<details>
<summary>7. What does λ add in TD(λ)?</summary>
<p>λ is a smooth knob between the two extremes of the target: at λ = 0 it is pure one-step TD, at λ close to one — almost Monte Carlo. It mixes targets of different depth, so there is no need to choose one of the extremes.</p>
</details>
<details>
<summary>8. What are the two roles in the actor-critic?</summary>
<p>The actor is the policy: it chooses actions and behaves. The critic is the value: it estimates how well the actor plays and gives a hint by which the actor reinforces successful actions. It is the tabular Q split into two roles: what to do and how well it is going.</p>
</details>
</div>
