---
number: 4
title: "Iterative policy evaluation"
summary: "Evaluation of a given policy, the update rule and the passes, convergence as a consequence of contraction, the stopping criterion, two ways of sweeping, the action value, greedy improvement and the “evaluate — improve” loop."
date: '09.10.2026'
lectures:
  - number: 5
    date: '09.10.2026'
covered:
  - "We lean on lecture 4: the Bellman equations describe the answer but give no way to compute it"
  - "One state — three different numbers: 4.58 for a run without slips, −3.21 for the policy “always right”, 3.40 for the solution of the equations"
  - "Policy evaluation: v_π — what it costs to follow a given rule; the number belongs to the pair “environment + policy”"
  - "Why “always left” gives −10: a step into the wall is the loop v = −1 + 0.9v"
  - "Evaluation is a measurement, not a search for the best: v_π ≠ v*, they coincide only for the optimal policy"
  - "Why it cannot be computed head-on — the system is 11 × 11, and for a million states the matrix has 10¹² elements"
  - "Iterative evaluation: we substitute the previous pass into the right-hand side, v₀ = 0, v₀ → v₁ → v₂ → …"
  - "The first pass on numbers: v₁(S11) = 6.20, v₁(S8) = −0.10, the rest −1; one pass shifts information by one step"
  - "Why the iterations can be trusted: the Bellman operator contracts with coefficient γ = 0.9 — hence uniqueness, convergence from any start and geometric decay of the error"
  - "Passes on the maze: max|Δ| 6.20 → 4.28 → 2.92 → 0.73 → 0.48, on the 16th pass 0.09"
  - "When to stop: max|Δ| < θ; with θ = 0.1 that is 16 passes, with 0.01 — 32, with 0.001 — 48; the residual error is at most 9θ"
  - "Two ways of one pass: synchronously (two tables) and “in place” (one) — both converge to the same fixed point"
  - "Action value q: four numbers from S6 — ↑ −6.27, ↓ 1.12, ← −3.97, → −3.21; the maximum is down, and that is 4.33 better than what the policy does now"
  - "Policy improvement: greedily by q, on a tie — right; the improvement theorem says “no worse”"
  - "The “evaluate — improve” loop (GPI): round 0 — 159 passes and −3.21, round 1 — 39 and 3.23, round 2 — 35 and 3.40; the values never decrease"
qa:
  - q: "How does policy evaluation differ from the search for the best policy?"
    a: "These are two different questions. Evaluation answers “what does a given rule cost”: v with the index π is the expected return if you go by π from then on. The search for the best one is the maximum over all policies, v with a star. For any policy v_π is not greater than v*, and they coincide exactly for the optimal one: in S6 “always right” gives −3.21, while the honest answer of the equations is 3.40. Evaluation corrects nothing and suggests nothing: it honestly measures the current rule, while a good action is found by improvement — the greedy choice by the action value."
  - q: "Why does the policy “always left” give −10 in almost all cells?"
    a: "Because at the left wall the chosen action hits the boundary: the agent stays in place but still pays minus one for the step. The Bellman equation for such a cell turns into a loop: v = −1 + 0.9v, whence 0.1v = −1 and v = −10. The sum of the infinite progression −1 − 0.9 − 0.81 − … = −1/(1 − γ) = −10 gives exactly the same. The exceptions are the cells where the slip sometimes pulls you down: S4 = −9.82, S8 = −8.18."
  - q: "Why can't the Bellman system of equations simply be solved head-on?"
    a: "It can be solved — by inverting the transition matrix; for our maze that is an 11 × 11 system. But the cost grows as the square of the number of states: a million states is a matrix of 10¹² elements, that is terabytes for memory alone, and such a thing does not exist. And all of it anew for every new policy, while in the loop there are dozens of them: there are 4¹¹ variants of “an action in a cell”, that is more than four million. So we need a method that counts the numbers step by step without writing out the matrix."
  - q: "Why does the iteration converge, and where is the guarantee that the limit is always the same?"
    a: "Because the Bellman operator is a contraction. Make one pass with any two tables of estimates, and the distance between them will shrink by at least a factor of γ: the multiplier in front of the old estimates in the update rule is exactly γ, and the sums over actions and over outcomes are weighted averages, and an average does not stretch a difference. Hence three consequences at once: the fixed point is unique, convergence goes from any initial approximation, the error decays geometrically. With γ = 1 the multiplier equals one — and the whole guarantee disappears."
  - q: "Why is the stopping threshold θ = 0.1, and what does the residual error 9θ mean?"
    a: "The threshold is taken in the scale of the reward: a step costs −1, so 0.1 is “a tenth of a step”. The stop fires when the largest change over the cells has become smaller than the threshold, but that does not mean we have obtained exact numbers: the distance to the limit is at most γ/(1 − γ) · θ, with γ = 0.9 that is 9θ, that is up to 0.9 — almost the price of a step. Want it more precise — lower the threshold: with 0.01 there are twice as many passes (32), and the error is ten times smaller. Stopping after a fixed number of passes is stopping at random: in a task with a longer horizon the same number will give a noticeably worse map."
  - q: "How does a synchronous pass differ from a pass “in place”?"
    a: "In where the numbers on the right-hand side come from. Synchronously all the values are taken from the previous pass, so the new one cannot be written over the old one — you need two tables, twice the memory. “In place” the value is updated at once and immediately used by the neighbours — one table. This does not affect the answer: both converge to one fixed point; in the maze 16 passes against 15–16, because the slip mixes everything up and the order almost does not matter. When stopping by the threshold the maps still differ (−2.85 against −2.92), after full convergence both give −3.21."
  - q: "Why do we need the action value if we already have the state value?"
    a: "Because from the map v you cannot see what a step is worth. The state value is the average over the actions the policy chooses, that is different steps are already mixed into one number: in S6 it is −3.21, and what a step down is worth — you cannot make out from the map. The action value q answers about a particular step: in S6 under “always right” it is ↑ −6.27, ↓ 1.12, ← −3.97, → −3.21. And there is no need to compute it anew: q is one step by the model from the already computed map v."
  - q: "How does q_π differ from q*?"
    a: "In which policy we follow after the first step. In q_π the first step is fixed, and then we continue by our current policy — that is why it equals −1 + 0.9 · Σ p(s′|s,a) · v_π(s′). In q* after the first step there is already the best policy. To confuse them means to compute someone else's numbers: q_π is used for improvement (we compare what would happen if we made this step), q* describes already optimal behaviour. A useful check: q_π for an action that the policy does anyway always equals v_π — in S6 “right” gives −3.21 in both places."
  - q: "Why is it greedily better down from S6, although the policy goes right?"
    a: "Because down from S6 leads to the exit through S10 and S11, and the slip pushes you in the right direction in advance: 1.12 against −3.21 for “right”. The difference of 4.33 is exactly the gain at one step, the hook for improvement. At the same time one can see a sign: if q in a cell is above its v, the policy in that cell is not optimal, and the bigger the gap, the more there is to gain. At one step the gain does not turn into a ready policy: in the first round the cells S1–S8 went down greedily, in S9–S11 “right” remained, and only the second round gave the optimum."
  - q: "Why does the “evaluate — improve” loop necessarily terminate?"
    a: "For two reasons at once. The number of policies is finite: 4¹¹, four actions in each of the eleven cells. And the improvement theorem forbids getting worse: the value of the new policy is not less than that of the old one in every cell. So while the policy changes, the values strictly grow, and a strictly growing sequence on a finite set breaks off. The sign of stopping is not “it has become good” but “the greedy step does not change the policy in any cell”; in S6 the path is: −3.21 → 3.23 → 3.40."
  - q: "Why are the q numbers from S6 different in the table of passes?"
    a: "Because they are computed from a map that has not converged yet. When stopping by the threshold θ = 0.1, S6 holds −2.85, while the limit is −3.21; if you take q from such a map, you get ↑ −5.80, ↓ 1.24, ← −3.64, → −2.90 — different numbers, but the same maximum, down. This is the meaning of the caveat: before convergence the intermediate estimates are an approximation, not v_π, and by them you can make wrong decisions, although the direction of improvement is usually guessed."
  - q: "How does value iteration differ from the “evaluate — improve” loop?"
    a: "By one symbol on the right-hand side: instead of the average over the actions of the policy the maximum is taken. The result is “evaluation and improvement in one step” — there is no need to bring the evaluation of the current rule to the end. On the maze that is 10 passes at the threshold θ = 0.1 against 233 for the full loop, and the same answer: v*(S6) = 3.40. It is legitimate because the maximum contracts the difference between estimates just like the average, so convergence and uniqueness of the limit are preserved."
terms:
  - term: "policy evaluation"
    definition: "a prediction of how much it costs on average to follow a given rule for choosing actions"
  - term: "state value v_π(s)"
    definition: "the expected return when starting from state s, if you act by the policy π from then on"
  - term: "iterative evaluation"
    definition: "obtaining a policy evaluation by successive approximations: the previous pass is substituted into the right-hand side, pass after pass"
  - term: "update rule"
    definition: "the formula of one pass: the new estimate of a cell = the price of a step + γ × (the average estimate of the next cell by the model)"
  - term: "Bellman operator T"
    definition: "the transformation that does exactly one pass with the table of estimates: v_{k+1} = T v_k"
  - term: "contraction"
    definition: "the property of the Bellman operator to reduce the difference between any two estimates by at least a factor of γ"
  - term: "fixed point"
    definition: "a table of estimates that does not change after a pass; for the Bellman operator it is unique and equals v_π"
  - term: "pass (iteration)"
    definition: "one recomputation of the whole table of estimates; a pass shifts information no further than one step from the exit"
  - term: "movement measure max|Δ|"
    definition: "the largest change of an estimate over the cells in one pass; by it one judges whether the count is moving"
  - term: "stopping threshold θ"
    definition: "the bound for max|Δ|: the count is stopped when the change per pass has become smaller than the threshold"
  - term: "residual error"
    definition: "how far the stopped estimate can be from the limit; at most γ/(1 − γ) · θ, with γ = 0.9 that is 9θ"
  - term: "synchronous pass"
    definition: "a pass in which all the right-hand values are taken from the previous table; two tables are needed"
  - term: "pass “in place”"
    definition: "a pass in which the new value is written at once and used by the neighbours; one table"
  - term: "action value q_π(s, a)"
    definition: "the expected return if exactly this action is made and then the policy π is followed"
  - term: "greedy improvement"
    definition: "replacing the policy by the choice of the action with the maximum action value in every cell; on a tie — right"
  - term: "improvement theorem"
    definition: "the policy greedy by q_π is not worse than π in any cell"
  - term: "GPI — generalised policy iteration"
    definition: "the loop “evaluate the policy → improve greedily → evaluate again”, until the greedy step changes the policy"
  - term: "value iteration"
    definition: "the same substitution, but with the maximum over actions instead of the average: evaluation and improvement in one step; converges to v*"
  - term: "horizon 1/(1 − γ)"
    definition: "roughly how many steps ahead the discount really looks: with γ = 0.9 that is ten steps, with 0.99 — a hundred"
lecture:
  - title: "Lecture 5 presentation (PPTX)"
    href: "/files/course/rl/l5-iterativnoe-ocenivanie.pptx"
  - title: "Addendum to lecture 5 — read at the start of lecture 6 (slides 27–34)"
    href: "/files/course/rl/l5-hvost-27-34.pptx"
---

## One state — three different numbers

The maze is the same as in lecture 4: a 3 × 4 grid, eleven playable cells and the exit S12. Entering the exit gives
**+10**, every step costs **−1**, the discount is **γ = 0.9**, and the slip: with probability 0.8 the command works as
intended, with 0.1 each the agent is pushed sideways, at the boundary it stays in place and still pays for the step.

In the last lecture we derived the Bellman equation. It has one unpleasant detail: the unknown value stands both on
the left and on the right, so there is simply nowhere to put numbers into it — it is a description of the answer,
not a way of getting it. Today's lecture is about the way.

Let's start with one cell, S6. There are three numbers about it, and all three are correct:

![Three numbers about cell S6: a run without slips 4.58, the evaluation of the policy “always right” −3.21, the solution of the equations 3.40](/img/course/rl/l5-three-numbers.png)
*The difference is not in the maze but in what we compute: a lucky run, the evaluation of a given rule, or the honest answer of the equations.*

* **4.58** — the return of one lucky run: three steps of −1 and entering the exit, without a single slip. This is the
  same number that was “value by distance” in lecture 4.
* **−3.21** — what the rule “always right” costs. This is policy evaluation, and it will appear in the first half of
  the lecture.
* **3.40** — the honest answer of the equations: that is what the cell is really worth once the slips are taken into
  account.

Then we go step by step: first we measure, then from the measurements we get the solution.

## Policy evaluation: what a rule costs

**A policy** π is a rule for choosing an action in every cell: “always right”, “always left”, “in S1–S8 down, then
right”. The policy belongs to the agent. The cells, the transitions and the slip probabilities are the environment,
that is the task.

Policy evaluation answers one question: how much will the agent get on average if it starts from state s and from
then on acts by the rule π:

$$
v_\pi(s) = \mathbb{E}_\pi\left[\,G_t \mid S_t = s\,\right]
$$

*“The average return if you start here and play by π from then on”*. The expectation is taken over two kinds of
randomness at once: over the choice of action (if the policy is stochastic) and over the transitions of the
environment — the slip is random too. In formulas we write $v_\pi$, in text — briefly v.

The main thing here is that the number has two owners. The same cell is worth differently under different rules,
because the rule decides which transitions the agent actually lives through:

![Two maps of one maze: under “always right” the values are around −3, under “always left” almost everywhere −10](/img/course/rl/l5-two-policies.png)
*The cells, the transitions and the probabilities are the same in both maps — only the rule gives different numbers.*

* “Always right”: $v(S6) = -3{,}21$, $v(S1) = -6{,}62$, $v(S11) = 6{,}54$ — the very numbers we will arrive at
  with the passes.
* “Always left”: −10 in almost every cell. The reason is the loop: a step left at the left wall hits the boundary,
  the agent stays in place but pays −1. The Bellman equation turns into $v = -1 + 0{,}9v$, whence
  $0{,}1v = -1$ and $v = -10$ — the same as the sum of the infinite progression $-1/(1-\gamma)$. The exceptions are the
  cells where the slip sometimes pulls you to the exit: $S4 = -9{,}82$, $S8 = -8{,}18$.

Hence the first thing worth taking away: **evaluation is a measurement, not a search for the best**. $v_\pi$ honestly
computes what the current rule costs and corrects nothing. A good action is not visible from the evaluation: to
notice it you need the action value. The maximum over all policies is $v^*$, and it coincides with the evaluation of
a particular rule only for the optimal one. In S6: 3.40 against −3.21.

## Why it cannot be computed head-on

The system is linear, and it really can be solved directly — by inverting the transition matrix. For our maze that is
11 equations in 11 unknowns: about 1331 operations and 121 numbers. A trifle.

The problem starts when there are many states:

![The price of a head-on solution: 11 equations in the maze and a matrix of 10¹² elements for a million states](/img/course/rl/l5-cost.png)
*The Bellman equation proves that the answer exists. Computing by it is a dead end.*

* The matrix grows as the square of the number of states: a million states is 10¹² elements, terabytes for memory
  alone. Such a thing does not exist.
* And all of it anew for every new policy, and in the loop there are dozens of them. There are exactly 4¹¹ ≈ 4.2 million
  different rules “an action in every cell”.

So we need a method that reuses the previous evaluations and does not store the whole matrix. There is a formula —
there is no method; today the method appears.

## Iterative evaluation: substituting the past

The idea is one: into the right-hand side of the equation we substitute the **previous** pass and repeat. We solve
nothing — we simply compute a new table from the old one:

$$
v_{k+1}(s) = \sum_a \pi(a\mid s) \sum_{s',r} p(s',r\mid s,a)\left[\,r + \gamma\, v_k(s')\,\right]
$$

For our deterministic policy the outer sum is one action, and the rule reduces to

$$
v_{k+1}(s) = -1 + 0{,}9 \cdot \sum_{s'} p(s'\mid s,a)\, v_k(s')
$$

*the price of a step plus the discounted average estimate of the next cell.*

The start is zeros in all the cells: $v_0 = 0$. In the exit there is already 10 — this is the terminal value, the
episode ends there, there is nothing to count. A bad initial guess costs extra passes but does not change the answer.

![Substituting the previous pass into the right-hand side: v₀ → v₁ → v₂, the information shifts by one step](/img/course/rl/l5-idea-subst.png)
*One pass shifts information no further than one step from the exit: the numbers seem to seep backwards through the maze.*

The first pass on numbers, the policy “always right”:

* **S11** — the neighbour of the exit. The intended step leads into the exit (probability 0.8), the slip down hits the
  boundary and returns the agent to S11: $v_1(S11) = -1 + 0{,}9\cdot(0{,}8\cdot 10) = 6{,}20$.
* **S8** — the neighbour of the exit from above, and it comes alive quietly: the intended step right hits the wall,
  but the slip down with probability 0.1 leads straight into the exit: $v_1(S8) = -1 + 0{,}9\cdot(0{,}1\cdot 10) = -0{,}10$.
* The other cells: $-1$, because all their neighbours in the previous pass are zeros, and the price of a step is
  charged always, even when the step hits the wall.

![What one pass shifted: zeros on the left, on the right two neighbours of the exit came alive — 6.20 and −0.10](/img/course/rl/l5-first-pass.png)
*In one pass exactly two cells changed; the movement measure max|Δ| = 6.20 is the change in S11.*

It is important that the numbers on the intermediate passes are **not yet** $v_\pi$ but an approximation: 6.20 is the
first step towards the limit 6.54.

## Why the iterations can be trusted

A pass is the application of one and the same transformation to the table of estimates. Formally $v_{k+1} = T v_k$,
where $T$ is the Bellman operator. The main thing known about it: **T contracts**.

![Contraction: any two tables of estimates move closer after a pass by at least a factor of γ](/img/course/rl/l5-contraction.png)
*With γ = 0.9 the difference between any two estimates is multiplied by no more than 0.9 — hence all the guarantees.*

Why so: the multiplier in front of the old estimates in the update rule is exactly γ, and the sums over actions and
over the outcomes of a step are weighted averages, and an average does not stretch a difference. So any two tables
after a pass are closer by at least a factor of γ (we measure the distance by the largest difference over the cells):
$\lVert Tv - Tu \rVert_\infty \le 0{,}9\,\lVert v - u \rVert_\infty$.

Hence three consequences at once:

1. **The fixed point is unique** — and it is exactly the solution of the equation, that is $v_\pi$.
2. **Convergence from any start** — the distance to the limit decays as $\gamma^k$.
3. **The error decays geometrically** — predictably, not anyhow.

A caveat: with $\gamma = 1$ the multiplier equals one, there is no contraction — and there are no guarantees
either. The discount in the task plays two roles at once: it is both the rate of forgetting the future and the rate
of convergence.

## Passes on the maze

We count “always right” synchronously from zeros and watch not the map but the movement measure — the largest change
over the cells in a pass:

| Pass | 1 | 2 | 3 | 4 | 5 | … | 16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| max\|Δ\| | 6.20 | 4.28 | 2.92 | 0.73 | 0.48 | … | 0.09 |

The change melts geometrically — no slower than by a factor of 0.9 per pass (0.9 is the contraction bound; on the
first passes it goes faster, because some of the cells have not yet been connected to the exit). On the 16th pass it
becomes smaller than 0.1 for the first time — that is our threshold. The cell S1 meanwhile crawls to the end: −1 →
−1.90 → −2.71 → … → −6.05, because the information comes from the exit and reaches the far corner later than
everything else.

![Table of passes: the column max|Δ| and the values of S1, S6, S11 by passes](/img/course/rl/l5-passes-table.png)
*The table shows both the convergence and the stopping criterion: the “right” limit is v(S6) = −3.21, v(S11) = 6.54, v(S1) = −6.62.*

![Convergence on a logarithmic scale: the points lie almost on a straight line, the threshold 0.1 is crossed on the 16th pass](/img/course/rl/l5-convergence.png)
*A straight line in the logarithm is exactly the geometric decay; its slope in the tail is set by γ.*

And one more number that links convergence with the task: the horizon $1/(1-\gamma)$. With γ = 0.9 that is ten steps,
and 16 passes are enough for us. With γ = 0.99 the horizon is ten times longer, and the same evaluation requires 42
passes.

## When to stop

The stopping rule: the largest change over the cells has become smaller than the threshold θ.

![The stopping rule and the residual error: with θ = 0.1 that is 16 passes and an error up to 9θ](/img/course/rl/l5-stop-rule.png)
*“It has converged” does not mean “we got the exact answer”: the stopped estimate still differs from the limit.*

* θ = 0.1 → **16 passes**, θ = 0.01 → 32, θ = 0.001 → 48. Ten times more precise — twice as many passes: the price
  of precision is logarithmic.
* The residual error is at most $\gamma/(1-\gamma)\cdot\theta$, with γ = 0.9 that is $9\theta$ = 0.9 — almost the price of
  a step. Want it more precise — lower the threshold.
* A fact: when stopping at θ = 0.1, S6 holds −2.85 against the limit −3.21, that is an error of 0.36 — inside the bound.
  The estimate $9\theta$ is a guarantee from above, the worst case.

That is why a fixed number of passes is stopping at random: in another task the same number will give anything. And
the threshold is worth taking in the scale of the reward: 0.1 is comparable with the price of a step (−1).

## Two ways of one pass

The right-hand side takes the values from the previous table, but the table itself can be swept in different ways:

* **Synchronously**: all the numbers from the previous pass, the new one is written into a separate table — twice the
  memory.
* **“In place”**: the new value is written over the old one and used at once — one table.

![Synchronous pass and pass “in place”: two tables against one, 16 passes against 15–16](/img/course/rl/l5-sync-inplace.png)
*The answer is the same: both ways are the same operator applied in a different order.*

On our maze: synchronously 16 passes, “in place” — 15–16. The order of sweeping almost does not matter, because the
slip mixes everything up and a cell still looks at its neighbours. In an acyclic task (a simple corridor without
returns) sweeping backwards from the exit would give the answer noticeably faster — there every cell learns its
number at once. An important detail: when stopping by the threshold the maps still differ (synchronously −2.85, “in
place” −2.92), and after full convergence both give −3.21.

## The action value: a step is visible from the cell

The policy evaluation is ready, but you cannot use it for choosing: $v$ is one number per cell, and there are four
actions. In S6 it is −3.21 and does not say what a step down is worth.

![In S6 one number and four question marks: what each step is worth is not visible from the value map](/img/course/rl/l5-v-vs-q.png)
*The state value is the average over the actions of the policy: different steps are already mixed in it.*

We need the **action value** — the price of a particular step:

$$
q_\pi(s,a) = -1 + 0{,}9 \cdot \sum_{s'} p(s'\mid s,a)\, v_\pi(s')
$$

We fix the first step — we make exactly this action — and then again go by the policy. There is no need to count
anything anew: this is one step by the model from the already computed map $v_\pi$. The feedback link is familiar
too:

$$
v_\pi(s) = \sum_a \pi(a\mid s)\, q_\pi(s,a)
$$

*the value of a cell is the weighted average value of the actions, the weights are given by the policy.*

Four numbers from S6 under the rule “always right”:

![Four values of q from S6: up −6.27, down 1.12, left −3.97, right −3.21; the maximum is down](/img/course/rl/l5-q-s6.png)
*The policy goes right, while the best action is down: 1.12 against −3.21, a gain of 4.33.*

| Action | ↑ | ↓ | ← | → |
| --- | --- | --- | --- | --- |
| q(S6, a) | −6.27 | **1.12** | −3.97 | −3.21 |

A sign is visible too: $q$ can be noticeably higher than the value of the cell itself — such places are the
interesting ones, that is where the policy loses. Note: $q(S6, \text{right}) = -3{,}21$ coincides with $v(S6)$ — as it
should be, because the policy in S6 goes right anyway. This is a handy check of the code.

Do not confuse $q_\pi$ with $q^*$: in $q_\pi$ after the first step there is our current policy, in $q^*$ — the best one.

## Policy improvement: greedy over q

From the four numbers the choice is made in one line:

$$
\pi'(s) = \arg\max_a\, q_\pi(s,a)
$$

In every cell we take the action with the maximum value, on a tie — right, as we agreed in lecture 4.

![Greedy improvement: the best step in every cell is chosen from the map of values](/img/course/rl/l5-improve-stairs.png)
*Improvement learns nothing new about the environment — it computes by the model we already have.*

**The improvement theorem**: the new policy is not worse than the old one in any cell. The meaning without a proof:
in $v_\pi(s)$ there is the value of what the policy does in s, and we replace it with the best of what is available —
it cannot get worse from such a replacement. And if the greedy step does not change the policy in any cell, it means
the policy is already optimal.

## The “evaluate — improve” loop

Then these two steps simply repeat: evaluated the policy → made it greedy → evaluated again → improved again. This is
**GPI**, generalised policy iteration, — the template of all our algorithms.

![Three rounds of the loop: −3.21 → 3.23 → 3.40 in cell S6](/img/course/rl/l5-gpi.png)
*While the policy changes, the values strictly grow — the improvement theorem on numbers.*

| Round | Rule | Passes per evaluation | v(S6) |
| --- | --- | --- | --- |
| 0 | “always right” | 159 | −3.21 |
| 1 | greedily down in S1–S8, right in S9–S11 | 39 | 3.23 |
| 2 | optimal | 35 | 3.40 |

Three rounds — 233 passes, and the values never decreased. Why the loop necessarily ends: the number of policies is
finite (4¹¹), and improvement forbids getting worse — so while the policy changes, the values strictly grow, and such
a sequence breaks off. The sign of stopping is not “it has become good” but “the greedy step changes nothing”. And one
more thing: 233 is three evaluations almost down to zero; with the criterion “by the threshold” the first round would
have closed in ten passes — 10 against 233 is about different stopping criteria, not about one being twenty times
smarter.

## The fast form: max instead of the average

The loop has a fast variant, and the difference in it is exactly one symbol: instead of the average over the
actions of the policy the right-hand side has the **maximum**.

$$
v_{k+1}(s) = \max_a \left[\,-1 + \gamma \sum_{s'} p(s' \mid s, a)\, v_k(s')\,\right]
$$

This is “evaluation and improvement in one step”: we do not bring the evaluation of the current rule to the end, but
immediately take the best action by the estimates we have. On the maze such a substitution converges in **10 passes**
at the threshold θ = 0.1 (at θ = 0.01 — in 12) against 233 passes for the full “evaluate — improve” loop, where every
policy was driven almost to zero. The answer is the same: $v^*(S_6) = 3{,}40$.

Why this is allowed: the maximum contracts the difference between estimates just like the average — the difference of
maxima is not greater than the difference of the numbers themselves — so the operator remains contracting, the fixed
point is still unique, and it is now $v^*$, not the evaluation of one rule. And a caveat about the honesty of the
comparison: 10 against 233 are different stopping criteria, not “twenty times smarter”; if the loop converged by the
same threshold, its first round would have closed in ten passes.

This section was added later: it was read on 16.10.2026 at the start of lecture 6, together with the following
“Pitfalls”. Slides 27–34 are in the files of the topic.

## Pitfalls

* **The numbers halfway through the count are not $v_\pi$ but an approximation.** On the 16th pass S6 holds −2.85, while
  the limit is −3.21; the q values from such a map are different too: ↑ −5.80, ↓ 1.24, ← −3.64, → −2.90. The direction of
  improvement is usually guessed (the maximum is down again), but the numbers are not yet the answer.
* **“Stopped” does not mean “exact”.** The threshold checks the movement, not the error: with θ = 0.1 the residual
  error can reach 0.9.
* **$v_\pi$ and $v^*$ are different things**, and so are $q_\pi$ and $q^*$. The evaluation describes a given rule, the
  star — the best of the possible.
* **Greed by immature values gives arbitrary actions.** An intermediate policy is not obliged to be a good one: in the
  first round S1–S8 went down, while in the optimum S1, S2, S3, S5, S6, S7 go right again.
* **A fixed number of passes is stopping at random.** The criterion is max|Δ| < θ, and the threshold is taken in the
  scale of the reward.
* **With γ = 1 there are no guarantees.** The contraction multiplier equals one, the difference does not shrink, the
  error can accumulate; γ = 1 is legitimate only where the task has an end.

## What to take away

1. **Evaluation measures, it does not search.** What a given rule costs is $v_\pi$; the best of the possible is $v^*$.
2. **Iteration solves the equation by substitution.** The previous pass goes into the right-hand side: 6.20 → … → −3.21.
3. **Convergence is a consequence of contraction**, not luck: the multiplier γ gives both uniqueness and the geometric
   decay of the error.
4. **Do not confuse stopping with precision**: the criterion is on the values, not on the policy.
5. **From the evaluations comes the solution:** greedily by q — and the “evaluate — improve” loop leads to −3.21 → 3.23 → 3.40.

Further on in the course the limitation of today's method is lifted: the method has three requirements — a model
is needed (the transition probabilities), a table is needed for every state, and a discount less than one is needed.
Lecture 6 removes the first: instead of the sum over the model the right-hand side will have one real step —
experience, the TD update, SARSA and Q-learning. The “evaluate — improve” loop will not go anywhere.

## Check yourself

A short check on the lecture. The answers are hidden — answer by yourself first.

<div class="qa">
<details>
<summary>1. “Always right” gives −3.21 in S6, while the honest answer of the equations is 3.40. Is that a contradiction?</summary>
<p>No, these are answers to different questions. −3.21 is what it costs to follow a given rule, 3.40 is the maximum over all policies, that is the price of optimal behaviour. Evaluation corrects nothing, which is why it is smaller.</p>
</details>
<details>
<summary>2. Why do almost all cells at the left wall cost −10?</summary>
<p>A step into the wall does not move the agent, but −1 is charged always. The equation turns into the loop v = −1 + 0.9v, whence v = −1/0.1 = −10.</p>
</details>
<details>
<summary>3. Start from zeros: what is v₁(S11) and why did the slip down not come into the answer?</summary>
<p>6.20 = −1 + 0.9 · (0.8 · 10). The slip down hits the boundary and returns the agent to S11, and in the previous pass there was a zero there — the term is multiplied by zero and disappears.</p>
</details>
<details>
<summary>4. From S6 the four steps give ↑ −6.27, ↓ 1.12, ← −3.97, → −3.21. Which one to choose and how much better is it than the current one?</summary>
<p>Down: 1.12 is the maximum. The current rule goes right (−3.21), so the gain is 4.33. When two maxima are equal we take right, as in lecture 4.</p>
</details>
<details>
<summary>5. Why does the “evaluate — improve” loop necessarily terminate?</summary>
<p>The number of policies is finite, and improvement forbids getting worse: while the policy changes, the values strictly grow. A strictly growing sequence on a finite set breaks off.</p>
</details>
<details>
<summary>6. The movement measure has become smaller than the threshold. So the values are computed exactly?</summary>
<p>No. The threshold checks the movement, not the error: the residual error can reach γ/(1 − γ) · θ, with γ = 0.9 that is 9θ. With θ = 0.1 it actually came out as −2.85 against the limit −3.21.</p>
</details>
</div>
