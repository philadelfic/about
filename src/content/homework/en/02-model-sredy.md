---
title: Homework for lecture 3
summary: Describe an environment model for your task from the lecture 2 homework — two or three transitions with outcome probabilities.
due: '02.10.2026'
topic: 3
lecture: 3
---

**The problem.** Take your task from the homework for lecture 2 — the same process or system for
which you wrote out the agent, the states, the actions and the rewards.

**What to do.** Describe the **environment model** of that task — two or three transitions:

* from which state,
* which action,
* where we end up — in which state,
* which reward we get,
* what the probabilities of the outcomes are — so that they sum to one over the outcomes.

**What it looks like.** A 3 × 4 maze: the agent is in cell S6, the action “right” — with probability 0.8 it
moves to S7, with probability 0.1 it slips upward into S2, with probability 0.1 — downward into S10.
Reward: −1 per step, +10 for the exit. The sum of probabilities over the outcomes:

$$
0{,}8 + 0{,}1 + 0{,}1 = 1
$$

**A common mistake.** Probabilities describe the behaviour of the **environment** — what it will do in
response to an action. How the agent itself chooses is described by the policy; we do not touch it at this
step.

**How to submit:** on a sheet, by the lecture on 2 October. A couple or three transitions, no more than that.
