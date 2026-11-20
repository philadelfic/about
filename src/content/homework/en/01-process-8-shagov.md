---
title: Homework for lecture 2
summary: Give definitions for an eight-step development process — agent, actions, steps, state, rewards.
due: '25.09.2026'
topic: 2
lecture: 2
---

**The problem.** Here is a development process in eight steps:

backlog → requirements gathering → requirements analysis → handover to the architect → task specs → development →
testing → release to prod

**What to do.** Give definitions for this process — one phrase for each:

* who the agent is,
* which actions are available,
* what the steps are (what counts as one step),
* what a state is,
* what the rewards can be.

A definition is not “naming” but defining and drawing the border: where the agent is and where the
environment is.

**Levels:**

* **Level 1** — all five definitions.
* **Level 2** — add the task type (episodic or continuing) and γ with a justification.
* **Level 3** — add a policy: a rule for choosing actions for your agent; show
  the trajectory of one task and compute the return G_t with γ = 0.9.

**A plus:** what an ε-greedy strategy would look like in your process — what counts as a random
action here, what as the best known one, and which ε you would take.

**How to submit:** 5–9 lines of “term — definition”, by hand, on a sheet with your surname, no more
than one page. Bring it to the lecture.
