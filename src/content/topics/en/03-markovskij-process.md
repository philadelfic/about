---
number: 3
title: "The Markov decision process"
summary: "State and action value, the model of the world and transition probabilities, the Markov property, MDP, episodic and continuing tasks, discounting, the Bellman equations and the optimal policy."
date: '25.09.2026'
lectures:
  - number: 3
    date: '25.09.2026'
  - number: 4
    date: '02.10.2026'
simulator: l3
covered:
  - "We lean on topic 2: the return G, discounting γ, the policy π"
  - "How to break down a task: the agent loop — MDP → estimate the states → estimate the steps → move and start again"
  - State value v(s) — how good “here” is
  - Action value q(s, a) — how good this step is
  - The link between v and q — state value as the weighted average of action values
  - Transition probabilities p(s′, r | s, a) and the model of the environment
  - The Markov property — why the current state is enough
  - "MDP as a task made of four things: states, actions, probabilities, γ"
  - Episodic and continuing tasks — where γ = 1 is allowed
  - Discounting and the horizon 1/(1 − γ)
  - The Bellman equation — value now through value later
  - One step computed on the 3 × 4 maze
  - The optimal policy — the maximum over actions
  - "Pitfalls: the frequent mistakes — one run, two averages, discount on the reward, v and q as a pair"
qa:
  - q: "How does value differ from reward?"
    a: "A reward is an estimate of one step, “how much I got now”. Value is an estimate of the future, “how much I will get later if I act by the policy”. The environment hands out the reward, the agent computes the value: the reward for a step can be negative while the value of a cell is positive, because something good lies ahead."
  - q: "Why does value depend on the policy?"
    a: "Because value answers the question “how much will I get later”, and later depends on which actions I choose. The same cell is worth different things for a cautious and for a risky policy — that is why the index π is there in the notation. Only values computed under one and the same policy can be compared with each other."
  - q: "Why is the state value not enough and the action value needed as well?"
    a: "The state value is one number per state, it says “this place is good”, but it does not say which step exactly to take: there are several actions in a state. The action value is the price of each step, like a menu with prices. The choice then becomes simple: take the item with the highest value. Hence the letter Q in the name Q-learning."
  - q: "Why are transition probabilities needed if the environment is deterministic?"
    a: "Then there is only one probability and it equals one — that is not a different case but a special one. Probabilities are needed as a common language: the environment almost always answers in different ways — noise in the mechanics, random demand, random road load. Without knowing the consequences value cannot be computed in advance, and all that is left is experience, which can be expensive or outright inadmissible."
  - q: "How does a slip differ from ε-greedy?"
    a: "In who is being random. ε-greedy is the randomness of the agent: with probability ε it takes not the best action but a random one; this is a property of the policy π(a|s), and we set it ourselves. A slip is the randomness of the environment: the action is chosen, but it is carried out imprecisely (with probability p as intended, otherwise it pulls you sideways); this is a property of the world p(s′, r | s, a), and the agent has no influence on it. In the Bellman equation they sit in different sums: the outer one with weights π(a|s) is ε-greedy, the inner one with weights p(s′, r | s, a) is the slip. The check is simple: ask yourself whether this is about the agent's choice or about the environment's answer."
  - q: "Why is the sum of the probabilities over all outcomes equal to one?"
    a: "Because these are the probabilities of a complete set of events: one of the listed outcomes will certainly happen. A model either gives exactly one or it is incomplete — “roughly one” does not exist here."
  - q: "What to do if the Markov property does not hold for a state?"
    a: "Write the missing information into the state. This property is not so much of the world as of our description: one position is not enough for a ball (at one point it can roll left or right) — we added the velocity, and it became Markov. A good description of the state is one where the property holds; a bad one leaves the agent blind and learning from noise."
  - q: "Why can't γ = 1 in a continuing task?"
    a: "The sum is infinite and without damping it diverges: value turns into infinity and becomes the same for all states — there is nothing left to compare actions by. What breaks is not “the size of the numbers” but the comparison itself. That is why in continuing tasks γ is necessarily less than one, and γ = 1 is legitimate only where the task has an end."
  - q: "Why is there no sum over actions in the equation for the action value, while in the equation for the state value there is one?"
    a: "In the equation for q the action is already fixed — there is nothing to average over the policy, and one averaging remains: over the environment. In the equation for v we do not yet know which action the policy will choose, so an outer sum with weights π(a|s) is added. Two sums are two “on average”: over the policy and over the environment."
  - q: "Why is the reward not multiplied by γ in the Bellman equation?"
    a: "Because it arrives now, not in the future. Everything after the current reward is discounted: in the notation r + γ·v(s′) the factor γ stands only in front of the value of the next state. If you write γ·(r + v(s′)), the formula falls apart."
  - q: "Is the Bellman equation a ready answer?"
    a: "No. Value stands in it both on the left and on the right, because the future is also described by values, and they are unknown. It is a system of equations for all states at once, not a computation from left to right: to get the numbers you have to solve it — that is what we will do in lecture 5."
  - q: "What is an MDP in simple words?"
    a: "A task fully described by four things: a set of states, a set of actions, transition probabilities and the discount factor γ. If all of this is known, the return can be computed in advance, without trying. A useful habit: when breaking down a new task, write down these four things and check that the state describes everything needed for the future, and that the reward encourages exactly what we want."
  - q: "We do not know the transition probabilities. What do we do then?"
    a: "Then the model is obtained by experience: we act, we look at what happened, and we estimate from the facts. These are the next topics of the course — the multi-armed bandit, iterative evaluation, SARSA and Q-learning."
  - q: "Why does the computation of one step give 4.13, while the “value by distance” to the exit would be 4.58?"
    a: "Because these are two different cases. Without slips (p = 1) the step always goes as intended, and S6 is worth 4.58 — that number is on the map too. With slips (p = 0.8, the environment of lecture 3) with probability 0.2 the agent is pulled sideways, part of the estimate goes into a distant state, and we get 4.13. Both numbers are computed by the same chain from the exit (8.00 → 6.20 → 4.58 → 3.12) — 4.13 is a little lower, and that is the price of the slips."
  - q: "How to break down any task of the course?"
    a: "With the same loop of four steps: assemble the MDP (step 1) → estimate the states v(s) (step 2) → estimate the steps q(s, a) (step 3) → make a move and estimate again, now from the new state (step 4). Steps 2 and 3 are about value, step 1 is about the model of the world, step 4 is the move itself."
terms:
  - term: "agent loop"
    definition: "the four steps we break down any task with: assemble the MDP → estimate the states v(s) → estimate the steps q(s, a) → make a move and estimate again"
  - term: "state value v(s)"
    definition: "the expected return when starting from state s and acting by the policy from there on"
  - term: "action value q(s, a)"
    definition: "the expected return when taking action a in state s and acting by the policy from there on"
  - term: "expectation"
    definition: "the average over all outcomes — both over the randomness of the environment and over the randomness of the policy"
  - term: "π(a|s) — the probability of choosing an action"
    definition: "with what probability the policy chooses action a in state s"
  - term: "transition probability p(s′, r | s, a)"
    definition: "the probability of getting reward r and ending up in state s′ after action a in state s"
  - term: "model of the environment"
    definition: "knowledge of the transition probabilities for all states and actions"
  - term: "deterministic environment"
    definition: "the transition is known exactly — the probability of an outcome equals one"
  - term: "stochastic environment"
    definition: "the outcome is random: one action has several possible results"
  - term: "slip"
    definition: "the command did not work: the agent goes where it is led only with probability p, otherwise it is pulled sideways; slip probability = 1 − p"
  - term: "Markov property"
    definition: "the future depends only on the current state, not on how we got into it"
  - term: "MDP"
    definition: "a task made of four things: states, actions, transition probabilities and the discount factor"
  - term: "episodic task"
    definition: "a task with a natural end — there is a terminal state"
  - term: "continuing task"
    definition: "a task without an end: no terminal state exists"
  - term: "discounting"
    definition: "accounting for future rewards with a decreasing weight"
  - term: "discount factor γ"
    definition: "how much the agent takes the future into account; a number from 0 to 1"
  - term: "horizon 1/(1 − γ)"
    definition: "roughly how many steps ahead the agent really looks"
  - term: "Bellman equation for the state value"
    definition: "the link between the value of a state and the values of the following states"
  - term: "Bellman equation for the action value"
    definition: "the link between the value of one step and the values of the following states"
  - term: "optimal policy"
    definition: "a policy that in every state chooses the action with the highest value"
  - term: "greedy policy"
    definition: "choosing the action with the maximum action value"
lecture:
  - title: "Lecture 3 slides (PPTX)"
    href: "/files/course/rl/l3-markovskij-process.pptx"
  - title: "Lecture 4 slides (PPTX)"
    href: "/files/course/rl/l4-markovskij-process.pptx"
---

## How to break down a task: the agent loop

We break down any task of the course with the same loop of four steps. First we **assemble the MDP** — we write
down what the task is made of. Then we **estimate the states** v(s): what “here” is worth. Then we **estimate the
steps** q(s, a): what each move is worth. And finally we **make a move** — and, finding ourselves in a new state,
estimate it again.

![The agent loop: assemble the MDP, estimate the states, estimate the steps, make a move](/img/course/rl/l4-cycle.png)
*After the move the state is new — and the loop repeats.*

Further on the page we go by this loop: first about value (steps 2–3), then about the model of the world (step 1),
then the equations and one whole episode (step 4).

## State value: what “here” is worth

The reward answers the question “what did I get now”. You cannot choose by it: a cell with 0 in it right now may
lead straight to the exit, while a cell with +1 in it right now may lead into a dead end. We need a quantity that
squeezes the whole future into one number — the **state value**.

$$
v_\pi(s) = \mathbb{E}_\pi\left[\,G_t \mid S_t = s\,\right]
$$

*“If I am in state s now and act by the policy π from here on — how much will I get on average?”*

Let us take the symbols apart, as we will do with the other formulas too:

* $\mathbb{E}_\pi$ — the **expectation**, the “average”: the environment and the policy may answer in different ways, so we average over all the variants;
* $G_t$ — the **return** from topic 2: the sum of rewards with a decreasing weight;
* $\mid$ — read as “given”;
* $S_t = s$ — “given that we are in state s now”.

Putting it all together: “the average return if you start from s and play by π from there on”.

The **state value** v(s) is the average return when starting from state s. It is one number per state, and the
index π in the notation is not accidental: value is a property not only of the cell, but also of how we play in it.

![Value map of the 3 × 4 maze: one number in each cell, from 10.00 at the exit to 1.81 in the far corner](/img/course/rl/l3-v-map.png)
*The reward per step is the same (−1), yet the numbers differ: value is about the future, not about “now”. All the
numbers are for the case where the command always works; with slips the numbers will be lower.*

**How these numbers came about.** Take cell S6 and walk to the exit step by step — without formulas, just laying out
what we get and when.

From S6 to the exit there are three steps: S6 → S7 → S8 → exit. Each step costs −1, and the exit gives +10. The
return is all the rewards in a row, but each next one arrives a step later, so it enters with a smaller weight (γ to
the power of the number of steps — the same discounting as in topic 2; γ is the discount factor: what the future is
worth in today's units, more in the “Discounting” section):

| Reward | When it arrives | Weight | Contribution |
| --- | --- | --- | --- |
| −1 | step S6 → S7 | γ⁰ = 1 | −1.00 |
| −1 | step S7 → S8 | γ¹ = 0.9 | −0.90 |
| −1 | step S8 → exit | γ² = 0.81 | −0.81 |
| +10 | the exit itself | γ³ = 0.729 | +7.29 |

We add up the last column: −1.00 − 0.90 − 0.81 + 7.29 = **4.58**. That is the value of S6: how much the agent will
get on average, starting from this cell.

The same count is briefly written with one formula — not because it is clearer that way, but because it is shorter:

$$
G = -1 + 0{,}9 \cdot (-1) + 0{,}81 \cdot (-1) + 0{,}729 \cdot 10 = 4{,}58
$$
*Both records are about the same thing: three rewards of −1, then +10 for the exit, and their weights are 1, 0.9, 0.81 and 0.729.*

Counting the other cells that way takes long — path after path. The short count is the same in meaning, and it is
exactly what gives the numbers on the map for the cells on the way to the exit; for the rest the rule is the same,
only the path is shorter. We go back from the exit, and each step is “−1 plus the discounted value of what has
already been counted”:

* $v(S_{12}) = 10{,}00$ — the exit gives $+10$;
* $v(S_8) = -1 + 0{,}9 \cdot 10{,}00 = 8{,}00$;
* $v(S_7) = -1 + 0{,}9 \cdot 8{,}00 = 6{,}20$;
* $v(S_6) = -1 + 0{,}9 \cdot 6{,}20 = 4{,}58$;
* $v(S_5) = -1 + 0{,}9 \cdot 4{,}58 = 3{,}12$;
* $v(S_1) = -1 + 0{,}9 \cdot 3{,}12 = 1{,}81$.

Both counts agree: “head-on” and “back from the exit” give the same 4.58 for S6. And in both it is visible that
the reward “now” is the same (−1) while the values differ — all the difference is in the future. If the exit could
not be reached, the rewards would go on without end, and the value of such a cell would be
$-1 - 0{,}9 - 0{,}81 - \ldots = -1/(1 - 0{,}9) = -10$. ($-1 - 0{,}9 - 0{,}81 - \ldots$ is an infinite
geometric progression: $-1 \cdot (1 + \gamma + \gamma^2 + \ldots) = -1/(1 - \gamma)$.)

> **Why this matters:** without value we would have to compare the trees of all continuations — deep down to the end
> of the episode, and in a continuing task to infinity. Value turns the tree into one number, and from there we simply
> compare numbers.

## Action value: what “this step” is worth

The state value says “this place is good”, but it does not say which of several steps to take. To choose, we need
the price of each action.

$$
q_\pi(s, a) = \mathbb{E}_\pi\left[\,G_t \mid S_t = s,\ A_t = a\,\right]
$$
*The same question, but the first step is fixed: “if I am in s, make exactly a, and act by π from there on — how much will I get?”*

The symbols are the same as for the state value: 𝔼 is the average, $G_t$ is the return, “|” is “given”. Only
$A_t = a$ is added: “given that the first action is exactly a”.

**Action value** q(s, a) — you get a “menu with prices” instead of one average estimate. Having q for all the
actions, the choice reduces to comparing numbers and taking the maximum — hence the letter Q in the name
Q-learning.

An example on the maze: the agent is in S6, a step costs $-1$, $\gamma = 0{,}9$. Left — S5, four steps to the
exit, $v(S_5) = 3{,}12$; right — S7, two steps to the exit, $v(S_7) = 6{,}20$.

![Agent in S6: left is S5 with value 3.12, right is S7 with value 6.20, and the value of each step being counted](/img/course/rl/l3-q-actions.png)
*The reward per step is the same (−1), yet the values differ: what comes next decides everything. The cells hold the “by distance” value to the exit.*

Both values are taken from the chain from the exit — it is written out in full in the “State value” section.

$$
\begin{aligned}
q(\text{left}) &= -1 + 0{,}9 \cdot 3{,}12 = 1{,}81, \\
q(\text{right}) &= -1 + 0{,}9 \cdot 6{,}20 = 4{,}58
\end{aligned}
$$

The choice is right: 4.58 is greater than 1.81. Down from S6 gives exactly the same 4.58 — both paths to the exit
are three steps long — so here the policy dictates the choice, not the gain. For now we assume the step always
lands where it is led; slips and probabilities are in the “Transition probability” section.

> **Why this matters:** every time the agent chooses something, it compares action values. Any “policy improvement”
> in this course is taking the maximum over q, not going through the options anew.

## How state value and action value relate

$$
v_\pi(s) = \sum_a \pi(a \mid s)\, q_\pi(s, a)
$$

The state value is the **weighted average** of the action values: the weights are the probabilities with which the
policy chooses each action. If the action values are 10 and 2, then the policy “always the first” gives v = 10, and
“half and half” — v = 6.

**Where these numbers come from.** We substitute into the formula above:

| How we play in the cell | Count | v |
| --- | --- | --- |
| always the first | 1 · 10 + 0 · 2 | 10 |
| half and half | 0.5 · 10 + 0.5 · 2 | 6 |
| always the second | 0 · 10 + 1 · 2 | 2 |

Policy improvement grows from this: the weighted average always lies between 2 and 10 and does not exceed 10 —
that is, it cannot be greater than the maximum. So if you move the weight onto the action with the highest value,
things get no worse — we simply shifted the weight onto the most expensive item on the menu.

> **Why this matters:** the gap between “how we play” and “how we could play” is measured by exactly this average.
> This is the mechanism on which all the further algorithms of the course stand.

## Transition probability: p(s′, r | s, a)

We can compute the return, but we do not know the main thing: what will happen after an action. We need a number
answering the question “having taken action a in state s, where will we end up and how much will we get”. There are
many such answers — so we need probabilities, not one outcome.

$$
p(s', r \mid s, a) = \Pr\left\{\,S_{t+1} = s',\ R_{t+1} = r \mid S_t = s,\ A_t = a\,\right\}
$$
*“The probability that from state s after action a we get reward r and end up in s′.”*

Left to right: s and a are what we know; s′ and r are what we will get. The reward and the transition are written
together not by accident: the reward arrives together with the transition, separately they cannot be tied.

The sum of the probabilities over all pairs $(s', r)$ equals one — one of these outcomes will certainly happen.
The **model of the environment** is knowledge of such probabilities for all states and actions.

> **Why this matters:** with a model the task can be solved “in the head”, by planning. Without it only experience
> remains, and it can be expensive or outright inadmissible — in medicine, power engineering, finance you cannot set
> up an experiment.

## An example in numbers: the 3 × 4 maze

![The 3 × 4 maze: an action to the right is picked out in a cell, with a row of outcome probabilities](/img/course/rl/l3-grid.png)
*A row of probabilities for one action: 0.8 — went as wanted, 0.1 — pushed up, 0.1 — pushed down. Rewards: −1 per step, +10 for the exit.*

The world does not have to be predictable: the same action has several outcomes. And if there is only one
probability and it equals one, that is not a different case but a special one — a **deterministic environment**;
an environment with several outcomes is called **stochastic**.

In numbers it looks like this: to the right from S6 — with probability 0.8 we get into S7, with 0.1 each it pulls
us into S2 and S10 (the same row as in the figure).

**What a slip is.** The command does not always work: with probability $p = 0{,}8$ the agent goes where it is
led, and in the remaining 0.2 cases it is pulled sideways — 0.1 up and 0.1 down (if we went left or right).
That is why an action has not one outcome but three, and the sum of their probabilities equals one. This behaviour
of the environment is what we call a **slip**. Further in the text we name two situations briefly: **without
slips** — the command always works ($p = 1$), this is a deterministic environment; **with slips** — the
environment of lecture 3, where $p = 0{,}8$. In the simulator at the bottom of the page $p$ can be changed with a
slider: at $p = 1$ there are no slips.

**Do not confuse:** ε-greedy is randomness in the agent's choice (the policy), a slip is randomness in the
environment's answer. Two different randomnesses, and in the Bellman equation they will end up in different sums.

> **Why this matters:** “the environment answered differently” is not a failure but the norm, and it is built into
> the model. Forgetting about slips means computing the value wrongly.

## The Markov property: why the current state is enough

![Different histories lead into one cell — and from there everything is the same](/img/course/rl/l3-history.png)

The future depends only on the current state, not on how we got into it. The check is simple: two agents in the
same cell — the past is indifferent to them, from there everything is the same for both.

An important correction: this property is not so much of the world as of **our description**. If the information in
the state is not enough — it is written into the state: the speed of a car, the temperature, the time of day, the
history of the last orders. One position is not enough for a ball (at one point it can roll left or right) — we
added the velocity, and it became Markov. In chess the position is enough, past moves are not needed.

> **Why this matters:** without this property the same cell would give two different answers to “how good is this
> place” — depending on how we came there — and you cannot rely on such a number.

## What an MDP is

**A Markov decision process (MDP)** is a task fully described by four things:

* a set of states S,
* a set of actions A,
* transition probabilities p(s′, r | s, a),
* the discount factor γ.

If all of this is known, the return can be computed in advance, without trials. In practice the model is either
given or obtained by experience — that is what we will do in the lectures about the bandit and Q-learning.

An MDP is the **first step of the loop**: assemble the task. Then the loop moves on to the estimation of states and
steps — as in the section “How to break down a task: the agent loop”.

> **Why this matters:** an MDP is the common language of the course. If a task is described this way, the equations
> and algorithms apply to it; if not — we are just “trying something” and do not understand what exactly we are
> optimising.

## Case: a taxi fleet, formally

The maze is already an MDP. Let us check on a live task: the dispatcher of a taxi fleet decides in which district to
look for the next order. The four things are written out like this:

* **states** — where the car is (the district) and what time of day it is; nothing else is needed: the Markov property;
* **actions** — in which district to go and look for an order (including “stay here”);
* **probabilities** — from district A an order with different chances will lead to B, C or D, and the chances depend on
  the time of day;
* **γ** — 0.9: an order today matters more than an order in an hour.

The reward is not a fifth item but part of the probabilities: $p(s', r \mid s, a)$ answers at once both “where we
will end up” and “how much we will get”. In a taxi that is the price of the ride minus fuel and idle time; an empty
ride is a minus.

A shift is an episode: drove out, worked, came back to the base; the count is finite, so γ = 1 is admissible here
(more in the “Episodic task” section below).

What this gives: as soon as the task is written out like this, a “greedy” driver, an “experienced” driver and an
algorithm are compared on the same numbers — and it is visible which policy is better.

## Episodic task: the task has an end

The interaction ends: there is a terminal state. Examples — the maze, a game of chess, a taxi driver's ride, a
shift of a car fleet. Here $\gamma = 1$ is admissible: the sum is finite and converges.

## Continuing task: there is no end

The interaction goes on without end, no terminal state exists: the climate in a building, a data centre, a
trading algorithm, fleet management. Here $\gamma$ is necessarily less than one — with $\gamma = 1$ the sum
diverges and the value becomes infinite.

![Episodic task: episode after episode, a finite number of rewards. Continuing: no end, the sum diverges](/img/course/rl/l3-infinite.png)

The same system can learn in episodes and work without stopping. A shift of a car fleet is an episode for learning,
while the fleet itself drives every day without end. So the “type of task” is about **how we set it**, not about how
the system works.

> **Why this matters:** an episode is a convenient tool, not a compromise. It lets you sum up, compare options on the
> same data and retrain. To treat “episodicity” as a property of the system means giving up the main way of learning
> in practice.

## Discounting: why the future has a weight

**γ** is the discount factor from 0 to 1. The main reason it exists is technical: without γ the return flies off to
infinity, the values of all states become infinite, and comparing infinity with infinity is meaningless. It is exactly
$\gamma < 1$ that makes the sum finite, and hence a number appears that can be compared.

Two reasons side by side: the meaningful one — a reward today is worth more than one in the future; the engineering
one — the distant future is predicted worse. The horizon is ≈ $1/(1-\gamma)$: with $\gamma = 0{,}9$ — about ten
steps, with $0{,}99$ — about a hundred.

**How γ changes our numbers.** The same map, but computed with different γ — for cells 1, 3 and 5 steps from
the exit:

| γ | v(S8) — 1 step | v(S6) — 3 steps | v(S1) — 5 steps |
| --- | --- | --- | --- |
| 0.5 | 4.00 | −0.50 | −1.63 |
| 0.9 | 8.00 | 4.58 | 1.81 |
| 0.99 | 8.90 | 6.73 | 4.61 |

**Where the numbers in the table come from.** The same count back from the exit as above — only the rewards are
discounted faster or slower. The row γ = 0.5: $v(S_8) = -1 + 0{,}5 \cdot 10{,}00 = 4{,}00$, then
$v(S_7) = -1 + 0{,}5 \cdot 4{,}00 = 1{,}00$, $v(S_6) = -1 + 0{,}5 \cdot 1{,}00 = -0{,}50$, then
$v(S_5) = -1{,}25$ and $v(S_1) = -1{,}63$. The row γ = 0.99: $v(S_8) = -1 + 0{,}99 \cdot 10{,}00 = 8{,}90$, and
further almost without losses — 6.73 and 4.61.

With $\gamma = 0{,}5$ the agent lives for one day: the exit is far, its $+10$ hardly affects the count, and the
cells three and five steps from the exit turn out simply bad (−0.50 and −1.63) — the agent will not want to go
there. With $\gamma = 0{,}99$ the opposite: all cells look decent, the agent is ready to wait a long time. That is
exactly the meaning of the γ knob.

γ is a knob that we set: not a property of the world, but a parameter of the formulation. A small γ — a short
horizon, γ close to 1 — playing the long game.

> **Why this matters:** γ is not the learning rate (that is another knob, α, it will appear in lecture 6). γ is about
> farsightedness: how far the agent looks and whether it is ready to wait for the result.

## Value now through value later

Counting an infinite sum directly is impossible, but if we take out the first term, the tail of the sum looks
exactly like the sum itself: $G_t = R_{t+1} + \gamma\, G_{t+1}$.

![Now → step → later, and a bracket closing the infinite tail](/img/course/rl/l3-idea.png)

Hence the main thought: **value now = reward now + γ × value later**. The infinite tail is rolled up into one
quantity — and that turns the sum into a short equation.

## The equation for state value

$$
v_\pi(s) = \sum_a \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[\,r + \gamma\, v_\pi(s')\,\right]
$$

It reads like this: we go through the actions by the policy, for each we go through the outcomes and add
“reward + discounted value of the next state”.

Piece by piece:

* the outer sum with weights $\pi(a \mid s)$ — “on average over the policy”: which action we choose now;
* the inner sum with weights $p(s', r \mid s, a)$ — “on average over the environment”: what it will answer;
* $r$ stands without $\gamma$ — we get the reward now, there is nothing to discount;
* $\gamma\, v_\pi(s')$ — the discounted “later”, and it is exactly here that the infinite tail is rolled up into one quantity;
* v stands both on the left and on the right — which means this is not an answer but a link.

> **Why this matters:** this equation is the heart of the course. All the further algorithms either solve it or
> go around it; and it is also a convenient check: the values found must satisfy it, otherwise there is a mistake
> somewhere.

## The equation for action value

$$
q_\pi(s, a) = \sum_{s', r} p(s', r \mid s, a) \left[\,r + \gamma\, v_\pi(s')\,\right]
$$

The difference from the previous equation is one thing: the action is already fixed, so the outer sum over the
actions disappears. One averaging remains — over the environment.

Inside stands the value of the next state under our policy, and that, in turn, is the weighted average value of the
actions. So v and q refer to each other — and this is not a flaw but a source of strength: all the further methods
work on this pair.

> **Why this matters:** inside there is exactly v under the policy, not the maximum. The maximum will appear only for
> the optimal quantities — that is the border between this lecture and the following ones.

## Computing by hand: one step through the maze

![One step from S6 to the right: three outcomes with their probabilities and values](/img/course/rl/l3-one-step.png)

We substitute the numbers into the equation for the action value from the previous section. The data is from the
example with the maze above: from S6 to the right with probability 0.8 we get into S7, with 0.1 — into S2 (pulled
up), with 0.1 — into S10 (pulled down); the reward is −1 per step, γ = 0.9.

**Where the values 6, 3 and 6 come from.** Each outcome leads into its own cell, and its value comes from the same
chain “how many steps to the exit” as on the map. From S7 and S10 to the exit there are two steps each, from S2 —
four: that is why $v(S_7) = v(S_{10}) = 6{,}20 \approx 6$, and $v(S_2) = 3{,}12 \approx 3$. For counting by hand we
round to whole numbers — the arithmetic is simpler that way; the exact values with slips will be in lecture 5.

**Where 5.7 comes from.** Now we average the “later” over the environment: each “later” enters with its own
weight, and the weight is the probability of the outcome:

| Outcome of the step right from S6 | Probability | Where we end up | Value of the cell | Contribution |
| --- | --- | --- | --- | --- |
| as intended | 0.8 | S7 — two steps to the exit | 6 | 0.8 · 6 = 4.8 |
| pulled up | 0.1 | S2 — four steps to the exit | 3 | 0.1 · 3 = 0.3 |
| pulled down | 0.1 | S10 — two steps to the exit | 6 | 0.1 · 6 = 0.6 |
| **average value later** | 1.0 | | | 4.8 + 0.3 + 0.6 = **5.7** |

**Where 4.13 comes from.** It remains to add two things: the reward for the step and the discounted “later”:

| Term | What it is | Number |
| --- | --- | --- |
| −1 | reward for the step: it arrives now, γ does not touch it | −1 |
| 0.9 · 5.7 | “later” with a discount: 10 % for one step | 5.13 |
| **total** | value of the step right from S6 | −1 + 5.13 = **4.13** |

Briefly the same is written in one line:

$$
0{,}8 \cdot 6 + 0{,}1 \cdot 3 + 0{,}1 \cdot 6 = 5{,}7, \qquad -1 + 0{,}9 \cdot 5{,}7 = 4{,}13
$$

> **4.13 against 4.58.** The same cell S6, two cases. **Without slips** ($p = 1$: the step always lands where it
> is led) the value is 4.58 — the one on the map. **With slips** ($p = 0{,}8$, the environment of lecture 3) part
> of the estimate goes sideways, and it comes out 4.13 — 0.45 less. We count the exact values with slips in
> lecture 5.

What is visible here:

* the reward for the step arrives without discounting, and the whole future — with a weight of 0.9;
* the reward for the step is negative while the value of the cell is positive — because something good lies ahead;
* without discounting it would be $-1 + 5{,}7 = 4{,}7$; the difference $0{,}57$ is exactly the “price of discounting”;
* rare inconvenient outcomes (0.1 instead of 0.8) noticeably pull the estimate down.

> **Why this matters:** we substituted the numbers — and got a number that can be compared with the value of
> another action in the same cell and then chosen. That is exactly what the agent does at every step.

## The best policy: the maximum over actions

$$
v_*(s) = \max_a q_*(s, a)
$$
*The star in the notation means “optimal”: $v_*$ and $q_*$ are the values of the best policy, they are computed from the model of the environment, not from the current estimates.*

The final goal is not numbers but a policy: what to do. The greedy choice by the action value gives it at once,
without inventing anything: in every state we take the action with the highest value. Such a policy is called
greedy by the action value.

**How it looks in numbers.** The q row for S6: up 1.97 · left 1.97 · right 4.13 · down 4.13. The maximum is 4.13,
and the choice falls on “right” or “down”. When two actions are equal, the choice between them is dictated by the
policy. The numbers 4.13 and 1.97 are computed with slips; without slips on the same step it would be 4.58 and 1.81.

The optimal values, meanwhile, are a property of the task: they do not depend on which policy we followed before
and how long we learned. So one can start from any policy and improve step by step.

> **Why this matters:** greediness by q is the mechanism that turns estimates into a decision. Everything else in
> the course is needed to obtain these estimates when the model of the environment is unknown.

## One episode step by step

The agent loop on the maze: **estimate → compare → take the maximum → make a move → estimate again** — now
from the new cell. Let us walk one episode this way from beginning to end and see where the return comes from.

![Episode step by step: where we stand, what we chose, what the environment answered and what return has accumulated](/img/course/rl/l4-episode-demo.png)

The route: S6 → S7 → S8, in S8 there was a slip (the agent stayed in place), then the exit. Rewards: −1, −1,
−1 and +10 for the step with which the agent entered the exit; four steps — because of the slip:

$$
-1 - 0{,}9 - 0{,}81 + 0{,}729 \cdot 10 = 4{,}58
$$

**What is visible here.** Without slips the same route would take three steps and bring 6.2. One slip costs an
extra step — and the return drops to 4.58, exactly to the value of S6 “by distance”. Hence the main thought: value
is an **average over many runs**, not a guarantee of one episode.

The same average over 200 runs: the greedy policy gives 4.98 at 3.8 steps, the ε-greedy one — 4.11 at 4.5. The
difference is the price of exploration: the ε-greedy one pays with return, but it finds out what happens on “bad”
steps. Next to it there is also the number 4.02 — that is the value of the ε-greedy policy in S6, computed from the
model: $0{,}9 \cdot 4{,}13 + 0{,}1 \cdot 3{,}05$. Do not confuse it with 4.11: 4.02 is obtained by the formula,
4.11 — by experience, from runs.

## Why this is an equation, not a ready answer

We computed one number by hand — 4.13. But where does the formula itself come from? Value is the expected
return, the return is the sum of rewards over the steps, and where we land on the next step is decided by the
environment. So the value of one cell depends on the values of other cells: the record we obtained above
($G_t = R_{t+1} + \gamma\, G_{t+1}$) refers to itself. That is exactly why this is an equation, not a ready
answer.

Four naive ways to compute the value of a cell — and the place where each one breaks:

| Naive way | Where it breaks |
| --- | --- |
| compute from a single attempt | the environment is random: one run is a lottery, while value is about the average |
| wait for the end of the episode and add up all the rewards | there may be no end: in a continuing task the episode does not end |
| cut the horizon: “count only N steps” | the tail of the return is lost, and the estimate becomes arbitrary |
| drag the whole history of steps along | the past does not influence the future: the current state is enough |

> **Why this matters:** all four dead ends are about one thing. Value cannot be obtained “in one pass”: neither
> from a single run, nor from the end of the episode, nor from a cut horizon, nor from the whole history. It can
> only be solved as an equation. Both Bellman equations are already on this page, and the ways to solve them are
> in lecture 5.

## Pitfalls

Four mistakes one stumbles over most often:

* judging by a single run: the environment is random, while value is about the average;
* confusing averaging over the environment (over outcomes) and over the policy (over actions);
* discounting the reward for the step itself: the reward for a step weighs 1, the discount applies to the future;
* treating v and q as independent numbers: in the equation they are a pair.

> **Why this matters:** if any of this has surfaced — go back to the section where the equations were derived.

## Where and how this is used

The 3 × 4 maze is a test bench on which we took the mechanics apart, not the task itself: the same four things —
**where I am, what I do, what I get and how much the future matters** — stand behind very different affairs:
behind a development plan, behind the steps of a robot, behind what to show a user. Only what the state is
written with changes, and how expensive a mistake is; the equations and the way of choosing an action stay the
same.

| Area | State — “where I am” | Action — “what I do” | Reward — “what I get” |
| --- | --- | --- | --- |
| software development process | the stage of the task: requirements → development → testing → prod | break down, write, run, ship | tasks above plan per week: 0, 1, 2 |
| robot locomotion | joint angles and velocities, contact with the ground | torques in the joints | for moving forward and balance, minus the effort spent |
| recommendation feed | the user's interests and context | what to show next | the reaction: watched, clicked, left |
| servers and cooling | load, queue, temperature | where to send the task, how much to cool | minus latency and cost, a penalty for overheating |
| treatment | the patient's readings, the history of observations | the dose and the moment of the next step | the patient feels better minus side effects |

The fourth thing — how much the future matters (γ) — is its own in every area: in the development process 0.9 —
a task today weighs more than the same task in a week; for the robot and for the feed it is less than one; for
servers it is necessarily less than one, otherwise the sum diverges; for treatment it is also less than one.

### Software development process

Take the eight-step process we went through: backlog → gathering requirements → analysing requirements →
handing over to the architect → specifications → development → testing → release to prod. The state is which
stage the candidate task is at, what has already been done and what is in the way. The action is what exactly you
do at the step: break down, write, run, ship. The reward is how many tasks above plan were closed in a week:
0, 1 or 2. γ = 0.9: a task today weighs more than the same task in a week.

**What makes this task hard.** The environment's answer comes with a delay: what is done this week will echo
back after several steps, and it can be tied to today's choice only through the discounted “later”. The average
payoff is hidden — as the average payoff of a slot machine is hidden; only what has already happened is visible.
Actions are tied to each other: today's analysis of requirements changes what can be shipped tomorrow. That is why
a step cannot be chosen “by the reward now” — the link **reward now + γ × value later** is needed, that is, the
Bellman equation, not a table of gains for a week.

> **Why this matters:** here you work with the same four things as in the maze — only instead of a cell there is a
> stage, and instead of four moves there is what you do at the step. Write them out for your process — and “do it
> this way or that way” turns into numbers that can be compared.

### Robot and character locomotion

The state is not a cell but the angles and velocities of the joints, the position of the body, contact with the
ground. The action is the torques in the joints. The reward is assembled from several terms with signs: a plus for
moving forward, a plus for the time spent upright, a minus for the effort spent. The task is episodic: the episode
ends with a fall or with the allotted time running out, so γ is less than one.

**What makes this task hard.** Both the state and the action here are continuous and multidimensional. A q row of
four numbers cannot be written out: there are infinitely many actions, the table does not fit, and the value has to
be given by a function $q(s, a)$ and approximated. At the same time it is visible why the reward is made of
terms: if only “how far I moved forward” is left, it becomes profitable to fall forward.

### A look: how it looks live

The three short clips below are an illustration, not a separate topic: this is a physics simulator, nobody drew a
single frame, every movement was chosen by a program. All three are from the Goatstream channel, the link under
each one leads to YouTube.

<div class="video">
  <iframe src="https://www.youtube.com/embed/c3R3-QXlL4s" title="Teaching a model to run with reinforcement learning" loading="lazy" allowfullscreen></iframe>
  <p class="muted">46 s · <a href="https://www.youtube.com/watch?v=c3R3-QXlL4s">“Trying to teach my new model to run using reinforcement learning”</a> — running, jumping, falling</p>
</div>

<div class="video">
  <iframe src="https://www.youtube.com/embed/wvQ1D7hI2rE" title="An agent optimised for maximum happiness" loading="lazy" allowfullscreen></iframe>
  <p class="muted">11 s · <a href="https://www.youtube.com/watch?v=wvQ1D7hI2rE">“This agent was optimized for maximum happiness”</a> — the same task, a different reward</p>
</div>

<div class="video">
  <iframe src="https://www.youtube.com/embed/DRnjQT2b0us" title="Stair climbing: a simulation" loading="lazy" allowfullscreen></iframe>
  <p class="muted">8.3 s · <a href="https://www.youtube.com/watch?v=DRnjQT2b0us">“Stair climbing simulation”</a> — steps over uneven ground</p>
</div>

### The recommendation feed

The state is the user's interests and context: what they watched, what they clicked on, what time of day it is
now. The action is what to show next. The reward is the reaction: watched, clicked, left. The task is continuing:
the feed does not end, the episode has no end, so γ is strictly less than one.

**What makes this task hard.** The reward arrives rarely and with a delay: “clicked” will happen several steps
after the show, and “left” is a cumulative result over many steps. The main trap is greediness: if you always show
only what is already liked, something new will never be shown and we will not find out that it is better. That is
exactly the exploration the ε-greedy policy pays for. Plus there are infinitely many states: they have to be
described by features, not by a table.

### Servers and cooling

The state is load, queue length, temperature. The action is where to send the task and how much to cool. The reward
is minus latency and minus cost, with overheating as a separate penalty. This is a continuing task without an end:
here γ is not “just in case” but a mandatory condition, otherwise the sum diverges.

**What makes this task hard.** A mistaken action does not just cost money — it runs into a constraint (overheating,
a power limit), and constraints in an MDP do not live separately but inside the reward. And the environment changes
by itself: the load depends on the time of day and on what someone else has launched. Here it is visible why one
should know the probabilities at all: you cannot go through the options on a live system, while a model allows you
to compute the value in advance.

### Treatment: where you cannot afford mistakes

The state is the patient's readings and the history of observations. The action is the dose and the moment of the
next step. The reward is the patient feeling better, minus side effects. If the state is short, the Markov property
starts to work: the future is determined by the current readings, not by how the patient came to them.

**What makes this task hard.** A mistaken action cannot be “replayed” here: you cannot experiment on a patient, so
the model is obtained not by an experiment on a living being but from accumulated records. And another difficulty
is what exactly we compare: “the best treatment on average over patients” is not the same as “the best for this
patient”. This has to be sorted out before counting.

### What all five have in common

Everywhere the same four things and two averagings: over the environment — that is q, over the actions of the
policy — that is v. What differs is this. In the maze there are eleven states, and the q row can be printed; in the
other cases that will not work — the states and actions are continuous or there are too many of them. That is
exactly why equations are needed: they link the value of a state with the values of neighbouring states without
requiring all the options to be enumerated. And the agent always chooses in the same way — it compares numbers.

## Five thoughts

The summary of the lecture is five thoughts:

1. **State value** — how much the agent will get on average from here, acting by the policy; **action
   value** — the same for one particular step.
2. **State value is the weighted average of action values**; policy improvement stands on this.
3. **The model of the world** — probabilities: what will happen after an action; the sum of the probabilities over
   the outcomes equals one.
4. **The Markov property** — the current state is enough; whatever is missing we write into the state.
5. **Value now = reward now + γ × value later.** If you remember only one thought — let it be the fifth.

The same summary in action — the agent loop above: assemble the MDP → estimate the states and steps → make a move →
repeat.

## Check yourself

A short check on the lecture. The answers are hidden — answer yourself first.

<div class="qa">
<details>
<summary>1. The agent is in S6, a step costs −1, γ = 0.9. What is v(S6)?</summary>
<p>4.58. From S6 to the exit there are three steps, the weights of the rewards are 1, 0.9, 0.81 and 0.729: −1.00 − 0.90 − 0.81 + 7.29 = 4.58.</p>
</details>
<details>
<summary>2. The reward per step is the same for all cells (−1). Why are the values different?</summary>
<p>Because value is about the future, not about “now”. For a cell next to the exit the future is short and good, for a distant one it is long and expensive: the steps manage to discount the reward for the exit.</p>
</details>
<details>
<summary>3. In cell S8 there are four actions. What is missing to choose a step?</summary>
<p>The value of each action — q(S8, a) for all four. The state value says “this place is good”, but does not say which step is better: to choose you have to compare four numbers and take the maximum.</p>
</details>
<details>
<summary>4. From S6 to the right: 0.8 → S7, 0.1 → S2, 0.1 → S10. What is the sum of the probabilities and what does it mean?</summary>
<p>1.0 — this is a complete set of events: one of the listed things will certainly happen. If the sum is not equal to one, the model is incomplete, and you cannot count by it.</p>
</details>
<details>
<summary>5. In the episode with slips the return came out 4.58, while without slips the same route would give 6.2. Why?</summary>
<p>With slips one step did not work as intended: in S8 the agent was knocked off course and stayed in place — there were four steps to the exit instead of three. An extra step is one more reward of −1 and extra discounting, so the return drops from 6.2 to 4.58.</p>
</details>
<details>
<summary>6. The q row for S6: up 1.97 · left 1.97 · right 4.13 · down 4.13. Which action to choose?</summary>
<p>“Right” or “down” — they have the maximum, 4.13. When two actions are equal, the policy chooses the particular one. The numbers 4.13 and 1.97 are with slips; without slips it would be 4.58 and 1.81.</p>
</details>
</div>
