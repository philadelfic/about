---
title: Homework for seminar 2
summary: Assemble the work from three files with gaps — fill in nine environment numbers and four run numbers, complete q_value and learn and get eight lines [ok].
topic: 3
seminar: 2
---

**The problem.** At seminar 2 we assembled the work from three files: `environment.py` — the environment,
`agent.py` — the agent, `run.py` — the run. Now we assemble the same thing ourselves. The portal has the same
three files, but with gaps: the mechanics and the checks inside are ready, while the numbers of the game and
two spots “to think about” are missing. The files are deliberately left as clean code, without hints: what to
fill in is here, in the statement.

**What is already done.** Cell numbers and transitions, the world model, the choice of move (greedy and
ε-greedy), running an episode, filling the experience table with runs, and the checks at the end of every file.
Actions are numbers: 0 up, 1 down, 2 left, 3 right; when the estimates tie, the agent goes right, as we agreed
in lecture 4.

**The environment — `environment.py`, the block “MAZE PARAMETERS”: nine numbers.**

| Parameter | What it is | Value |
| --- | --- | --- |
| `ROWS` | rows in the grid | 3 |
| `COLS` | columns | 4 |
| `EXIT` | number of the exit cell | 12 |
| `START` | start cell | 1 |
| `GAMMA` | discount γ | 0.9 |
| `STEP_R` | reward for an ordinary step | −1 |
| `EXIT_R` | reward for entering the exit | +10 |
| `P_OK` | probability that the command worked | 0.8 |
| `P_SLIP` | probability of a sideways slip | 0.1 |

In words, the same thing: a grid three by four, the start is always S1, the exit S12 in the bottom right corner,
the command works in eight cases out of ten, in one case out of ten it slips sideways one way and in one case
the other way, beyond the grid the agent stays in place and still pays for the step, a step costs −1, entering
the exit gives +10, and the episode ends there.
`CELLS` does not need filling in — it is computed by itself, as `ROWS × COLS`.

**The run — `run.py`, the block “RUN PARAMETERS”: four numbers.**

| Parameter | What it is | Value |
| --- | --- | --- |
| `EPISODES` | how many episodes in a series and in the experience set | 200 |
| `SEED` | the seed of randomness: one seed — one and the same episode | 7 |
| `EPSILON` | the share of random probes, ε-greedy | 0.1 |
| `MAX_STEPS` | the limit of steps per episode | 200 |

**The agent — `agent.py`: two spots “to think about”.** Both bodies currently raise `NotImplementedError` — write
the formulas into them:

* `q_value(state, action)` — **the value of a step by the model**: the reward for the step plus γ times the
  average value of what comes next. The row of transitions (“where to and with what probability”) is handed
  out by the environment: `self.env.transitions(state, action)`.
* `learn(state, action, reward, next_state, done)` — **the update rule from experience**: the estimate is pulled
  towards “the reward plus γ times the best known estimate of the next cell”. At the end of an episode (`done`)
  there is no next step — then we take just the reward. Write the result into `self.q[state][action]`, and mark
  the pair in `self.seen`.

**How to check it step by step.** Every file checks itself, so you can go one at a time:

1. `python3 environment.py` — four checks of the environment;
2. `python3 agent.py` — two checks of the agent (the numbers of the environment must be filled in first);
3. `python3 run.py` — a summary of the whole work.

As long as something is not filled in, the files do not crash but say what is missing.

**How you know it is done.** `python3 run.py` prints eight lines `[ok]` and “summary: all checks agree”.
Specifically we expect:

* `environment: the probability sums in every row give 1 (44 rows)`;
* `environment: beyond the grid the agent stays in place (S1 → up → S1)`;
* `environment: the return of the route from the lecture = 4,58`;
* `environment: the return of the optimal route from S1 = 3,12`;
* `agent: the q-row for S6: ↑1,97 · ↓4,13 · ←1,97 · →4,13`;
* `agent: the q-row for S7: ↑3,77 · ↓5,93 · ←3,77 · →5,93`;
* `run: an episode from S1 (seed = 7): S1 → S2 → S3 → S4 → S8 → S12 — 5 steps, return 3,12`;
* `run: the experience table 44 of 44, greedy from S1 — reached the exit`.

**Where to get the files.** [environment.py](/about/files/course/rl/environment.py) (the environment),
[agent.py](/about/files/course/rl/agent.py) (the agent) and [run.py](/about/files/course/rl/run.py) (the run) —
download them into one folder and run from there.

**How to submit:** the files are sent to the teacher in person (as before on this course).
