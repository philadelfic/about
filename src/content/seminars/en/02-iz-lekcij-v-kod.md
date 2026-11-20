---
number: 2
title: "The maze: from lectures to code"
summary: "How the MDP of a 3 × 4 maze becomes code: states, actions, probabilities and rewards — in words and in lines of a file, the three files of the work (environment, agent, run), the numbers from lecture 4 (4.13 and 4.58, the episode from S1 at seed = 7 — 3.12) and the readiness sign — eight [ok] lines. At the end — tasks and a progress test on the material of the session."
date: "06.10.2026 · 13.10.2026"
covered:
  - "How the session is organised: the order of work — from the 3 × 4 maze to an assembled MDP and code"
  - "Assembled the MDP of the 3 × 4 maze: states, actions, transition probabilities and rewards, the discount — and agreed on the start"
  - "Went through which files are needed and why there is no way without them: environment, agent, run"
  - "Went through the environment: the rules of the game and the model of the world, what it gives the agent"
  - "Went through the agent: first discussed four questions to the agent, then showed the code"
  - "Went through the run: the episode from S1 at seed = 7 — return 3.12; average return over 200 episodes — greedy 1.72 against ε-greedy 1.18; the experience table fills up run by run, 44 out of 44"
  - "Wrote progress test No. 2 on the material of the seminar: 12 questions, 12 points, 12 minutes"
  - "Summed up and handed out the assignment"
tasks:
  - title: "Question 1. How to evaluate a move"
    text: "The discussion starts with a question: how does the agent evaluate a move? Say in your own words what the value of a step is and in which function of the agent it lives."
    answer: "The value of a step is the reward plus the discounted future: the reward for the step plus γ times the average value of what comes after. In the code that is the function `q_value`."
  - title: "Question 2. How to get the row"
    text: "One estimate is one number. And how do you get the q row for a cell — all four numbers by moves? Which function of the agent is responsible for that?"
    answer: "Run the estimate over all four actions and collect them into a row. In the code that is `row`: the q row for a cell — four numbers by moves."
  - title: "Question 3. How to choose a move"
    text: "How does the agent choose a move? How does the greedy way differ from the ε-greedy one and why do we need exploration?"
    answer: "Greedy — the maximum over the row; ε-greedy — sometimes at random. Random trials are exploration: we pay for them by sometimes losing."
  - title: "Question 4. How to run an episode"
    text: "How does the agent go through an episode from the start to the exit and how is the return counted along the way?"
    answer: "A move → the environment’s response → the return with weight γ, and so on until the exit. We accumulate the return with its own weight at every step."
  - title: "The “think it over” spot No. 1: q_value"
    text: "In the homework `agent.py` the function `q_value` has no body — only a stub with a message. What do you need to put into it?"
    answer: "The value of a step by the model: the reward for the step plus γ times the average value of what comes after. The transition row — “where and with what probability” — is given by the environment through `transitions`."
  - title: "The “think it over” spot No. 2: learn"
    text: "In the homework `agent.py` the function `learn` has no body either. Which update rule from experience do you need to put in?"
    answer: "The estimate is pulled towards “the reward plus γ times the best known estimate of the next cell”. At the end of an episode there is no next step — then we simply take the reward."
assignment:
  title: "Assignment: assemble the work from three files"
  text: "The portal has the same three files, but with gaps — and deliberately clean code, without hints: the mechanics and the checks in them are ready, while the numbers of the game and the two “think it over” spots are missing. What to put in — nine numbers of the environment, four numbers of the run, the functions q_value and learn — and which numbers should come out in the report, is written in the full statement; download the files into one folder."
  files:
    - title: "Environment — environment.py"
      href: "/files/course/rl/environment.py"
    - title: "Agent — agent.py"
      href: "/files/course/rl/agent.py"
    - title: "Run — run.py"
      href: "/files/course/rl/run.py"
  homework:
    title: "Homework for seminar 2 — statement, files and deadline"
    href: "students/mai/rl/homework/04-sobrat-rabotu-iz-blokov/"
materials:
  - title: "Slides of the session, group М80-203СВ-25 (06.10.2026) — PPTX, in Russian"
    href: "/files/course/rl/sem2/s2-labirint-iz-lekcij-v-kod-gr-m80-203-06.10.2026.pptx"
  - title: "Slides of the session, group М80-202СВ-25 (13.10.2026) — PPTX, in Russian"
    href: "/files/course/rl/sem2/s2-labirint-iz-lekcij-v-kod-gr-m80-202-13.10.2026.pptx"
---

## What we did in this session

The session is about code, and not about new formulas. The material of lectures 3 and 4 (MDP, transition probabilities, value,
Bellman equations) we assembled into one small working project: the 3 × 4 maze turned into three files —
the environment, the agent and the run. There are no service files in the work: everything you need lies in these three.

The order of work was this: **first we discuss — then we show**. For every file we first
said out loud what should be in it and why there is no way without it, and only then looked at the ready code. New
numbers we did not derive in the session: the maze is the same as in lecture 4, and all its numbers come from there.

Three things to take away from the session:

* how a statement of the task in words turns into lines of a file — that is exactly what “to comb a task into code” means;
* what the work of three files consists of and why it cannot be cut down to one;
* by which numbers you see that the code is right: eight `[ok]` lines and the familiar numbers from lecture 4 — 4.13 and 4.58.

## The 3 × 4 maze: the world we describe

The stage is a grid three by four, twelve cells:

* **numbering** — left to right, top to bottom: the top row S1 … S4, the bottom one — S9 … S12;
* **start** — always S1, the top left corner: that is the agreement, it is part of the statement;
* **exit** — S12, the bottom right corner;
* **moves** — up, down, left, right; in the code these are the numbers 0, 1, 2, 3, and arrows are printed only for the eyes;
* **a command does not always work**: in eight cases out of ten the agent goes where it was asked, once out of
  ten it is carried sideways;
* **beyond the grid** the agent stays in place;
* **a step costs −1**, entering the exit gives **+10**, and the episode ends there;
* **discount γ = 0.9** — the rewards of distant steps weigh less in the return.

Eleven cells out of twelve are playing; the exit is a terminal state: once in it, the agent no longer
moves, it only takes +10 and ends the episode.

**Why this matters:** every number here is not an ornament but part of the task. The slip turns the maze from a
puzzle into a stochastic task: from one and the same cell one and the same move may lead to different
places. That is why “go along the shortest path” does not work here — you have to count on average.

## Four things of an MDP — in words and in lines of a file

An MDP is not a formula but four things written down in words. On the left is what we said, on the right is what it
becomes in the files.

| In words | In the code |
| --- | --- |
| **S** — states: twelve cells, eleven playing and the exit | `ROWS, COLS, EXIT = 3, 4, 12`, `START = 1`, `CELLS = ROWS * COLS` |
| **A** — actions: four moves | `UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3` |
| **p** — transition probabilities: 0.8 “as intended” and 0.1 of a slip sideways each | `P_OK, P_SLIP = 0.8, 0.1` and the model-of-the-world row `transitions()` |
| **R** — reward: −1 per step, +10 for entering the exit | `STEP_R, EXIT_R = -1.0, 10.0` |
| **γ** — discount: distant rewards weigh less | `GAMMA = 0.9` |

Separately — the agreement about the start: an episode always begins from S1. In the code it is one line, but without it
everyone’s run will go its own way.

**Why this matters:** the table above is exactly the answer to the question “what does it mean to comb a task into code”. Not a single
number is taken “just like that”: the grid — from the picture, the probabilities and the rewards — from the fix, the discount — from
lecture 2.

## The numbers — from lecture 4, we do not count them again

There was nothing to count: all the numbers of the maze were already counted in lecture 4, it is enough to recognise them in the output
of the program. Here they are:

* **the value map “by distance”**: 10 → 8 → 6.2 → 4.58 → 3.12 → 1.81 — by the number of steps to the exit;
* **the return of the route from the lecture** S6 → S7 → S8 → slip → S12: **4.58**;
* **the q row for S7**: ↑ 3.77 · ↓ 5.93 · ← 3.77 · → 5.93;
* **the q row for S6** under the strategy “always to the right”: ↑ 1.97 · ↓ 4.13 · ← 1.97 · → 4.13.

The last number is worth counting by hand — that shows where it comes from. A step to the right from S6: the intended
move (probability 0.8) leads to S7, the slip sideways — to two more cells, 0.1 each. The values in the map are rounded to
whole numbers (6, 5, 3), so by hand you get exactly the same as in the code:

$$
q(S_6, \text{right}) = -1 + 0{,}9 \cdot (0{,}8 \cdot 6 + 0{,}1 \cdot 3 + 0{,}1 \cdot 6) = 4{,}13
$$

The same thing in the code — with one sum:

$$
q_\pi(s, a) = -1 + \gamma \sum_{s'} p(s' \mid s, a)\, v(s')
$$

**Why this matters:** numbers are the only way to check that the code is right. If the output of the program agrees
with the lecture, then both the model and the count are assembled correctly. If it does not agree — look for the error, and not for an “approximately
right result”.

## Three files: environment, agent, run

The work is assembled from three files — and not a single service one.

* **Environment — `environment.py`.** The rules of the game and the model of the world: `reset` (start an episode), `step` (make a step),
  `transitions` (the model-of-the-world row). It gives the agent the new state, the reward and the end-of-episode flag.
* **Agent — `agent.py`.** Chooses a move and evaluates it: `act`, `row` and the table of estimates `q`. It does not know the rules of
  the game — it asks the environment.
* **Run — `run.py`.** Connects the environment and the agent: an episode, a series of episodes, the report. It decides nothing itself.

Remove a file — the work falls apart: without the environment the rules have nowhere to live, without the agent there is no one to choose, without the run
the result is not visible.

The agreement between the files (in code it is called a contract) is simple: **the environment must be able to `reset`, `step` and
`transitions`, the agent — `act`, `row` and the table `q`**. These are the same names as in Gymnasium: `reset` and `step`
exist in any reinforcement-learning environment, so the habit is transferable.

**Why this matters:** splitting into three files is not bureaucracy but a way to change one part without breaking
the others. In the labs it will be the same: the environment there is different, while the agent and the run are almost the same.

## The environment: from the maze — to code

The environment is the file where the rules live. We started with the constants, and each one was born from a picture or a fix:

* `ROWS, COLS = 3, 4` — counted from the picture: three rows, four columns;
* `EXIT = 12` — the exit is in the bottom right corner, that is cell number twelve;
* `START = 1` — an episode always begins from S1;
* `P_OK, P_SLIP = 0.8, 0.1` — from the fix: a command works 8 times out of 10, a slip sideways — 1 out of 10;
* `STEP_R, EXIT_R = -1.0, 10.0` — from the rules of the game: −1 per step, +10 for entering the exit;
* `GAMMA = 0.9` — the discount from lecture 2.

Then the mechanics, that is turning “where I am and where I step” into cell numbers:

* `rc()` and `num()` translate a cell number into the pair “column, row” and back;
* `target(cell, delta)` answers the question “where will I end up”; beyond the grid it returns the same cell —
  the agent stays in place, but the step is paid for anyway;
* `perp(delta)` gives two directions perpendicular to the command: that is the slip sideways.

The model of the world is the function `transitions`: a cell and a move on the input, a row “where and with what probability” on the output.
The intended step goes with probability 0.8, the two slips — 0.1 each. If several outcomes lead into one and the same
cell (that happens at a wall), the probabilities add up, and the sum over the row is always equal to one — that is the first thing
the environment checks in itself.

A step (`step`) is the drawing of an outcome: the environment draws one of the options by the probabilities of the row and gives the agent the new
state, the reward and the end-of-episode flag. An important detail: **the reward depends on the new state, and not on the
old one** — +10 comes on the step that led into the exit, and before that every step costs −1.

**Why this matters:** the rules of the game do not leak into the agent. The agent knows neither the size of the field nor the probabilities of a
slip — it asks the environment. That is exactly why the same environment can later be replaced with another task
without rewriting the agent.

## The agent: four questions — four functions

Before showing the code we discussed what the agent is obliged to be able to do. There are exactly four questions, and each of them
has its own function in the file.

1. **How to evaluate a move** — the value of a step: the reward plus the discounted future.

$$
q_\pi(s,a) = r + \gamma \sum_{s'} p(s' \mid s, a)\, v(s')
$$

In the code that is `q_value`: the agent gets the transition row from the environment, and takes the values of the next cells from the map
`self.v`.

2. **How to get the row** — run the estimate over all four actions and collect them together: that is `row`.
The q row for S6: ↑ 1.97 · ↓ 4.13 · ← 1.97 · → 4.13; for S7: ↑ 3.77 · ↓ 5.93 · ← 3.77 · → 5.93.

3. **How to choose a move** — greedily (the maximum over the row) or ε-greedily (sometimes at random): that is `act`. When the estimates
are equal we agreed to go **to the right** — otherwise two identical agents will take different routes.

4. **How to run an episode** — a move → the environment’s response → the return with weight γ, and so on until the exit: that is `run_episode`.

$$
G = r_1 + \gamma r_2 + \gamma^2 r_3 + \ldots
$$

Separately there is `learn` — the update rule **from experience**, for the case when there is no model. The estimate is pulled
towards “the reward plus γ times the best known estimate of the next cell”; at the end of an episode there is no next step,
and then we simply take the reward.

**Why this matters:** the four questions are not a classroom formality but the frame of any agent of the course. In
lab 1 (tic-tac-toe) the questions are the same, only the content of the answers changes.

## The run: what the code prints

`run.py` decides nothing — it spins episodes and counts the return. You have to look at the numbers.

* **The episode from S1 at seed = 7:** the route S1 → S2 → S3 → S4 → S8 → S12, five steps, return **3.12**. That is
  the optimal route from the start: −1 − 0.9 − 0.81 − 0.729 + 0.6561 · 10 = 3.12.
* **A series of 200 episodes:** the greedy strategy — **1.72**, the ε-greedy one (ε = 0.1) — **1.18**. Greedy takes the maximum over
  the row and checks nothing; ε-greedy makes a tenth of the steps at random — that is exploration, and you
  pay for it. One run proves nothing, you have to look at the average.
* **The experience table:** a pair “cell, move” has its own cell, 44 in total (eleven playing cells × four moves).
  The table lives between episodes: at first it is almost empty, so the agent tries at random more often, then it fills up
  completely — and the agent goes greedily. We got 44 out of 44, and the greedy move from S1 reached the exit.

**What a seed is.** The environment draws outcomes at random, so one and the same code may take different
routes every time. To make the result checkable and comparable, randomness is pinned to a number — a seed.
One and the same seed gives one and the same episode: seed = 7 is the route S1 → S2 → S3 → S4 → S8 → S12 and the return
3.12 both for us and for you.

## How to tell that everything works

The readiness sign is one: `python3 run.py` prints eight `[ok]` lines and “result: all checks agree”.
The lines are like this:

* `environment: the sums of probabilities in every row give 1 (44 rows)`;
* `environment: beyond the grid the agent stays in place (S1 → up → S1)`;
* `environment: the return of the route from the lecture = 4.58`;
* `environment: the return of the optimal route from S1 = 3.12`;
* `agent: q row for S6: ↑1.97 · ↓4.13 · ←1.97 · →4.13`;
* `agent: q row for S7: ↑3.77 · ↓5.93 · ←3.77 · →5.93`;
* `run: episode from S1 (seed = 7): S1 → S2 → S3 → S4 → S8 → S12 — 5 steps, return 3.12`;
* `run: experience table 44 out of 44, greedily from S1 — reached the exit`.

The checks live at the end of every file, and not as a separate file of checks: that way a check lies next to what
it checks. Therefore a file can be run on its own too — `python3 environment.py` will show four checks of the
environment, `python3 agent.py` — two checks of the agent, — while one command `python3 run.py` gives a summary over the whole
work, and you see at once which file did not agree.

**Why this matters:** “somehow it works” does not count as work. We hand in when all eight lines are `[ok]`.

## What it means to “comb a task into code”

This is the main skill of the session, and it fits into four steps.

1. **The fix → constants.** First in words: the grid, the start, the exit, the probabilities, the rewards, γ. Then every
   line of the fix becomes a line of code — nothing is taken “just like that”.
2. **The rules → a class.** The rules of the game live in one place — in the environment, and the agent does not know them: it asks
   questions through `reset`, `step` and `transitions`.
3. **The agreement → functions.** The agent has exactly the functions that are needed to answer the four questions.
4. **The check → a self-check.** Every file at the end checks itself on the numbers from the lecture.

## Pitfalls

* **4.13 and 4.58 are not a contradiction.** 4.58 is the return of the route from the lecture, where the slip did not get in the way; 4.13 is the estimate of a step
  to the right from S6 by the model with slips. Different questions — different numbers.
* **Without a seed a run cannot be compared.** One episode proves nothing: look either at a seed that can be
  repeated, or at the average over a series.
* **The experience table lives between episodes.** You cannot reset it at every episode — otherwise the agent will keep
  going at random.
* **When the estimates are equal — to the right.** The agreement is needed so that the routes coincide for everyone.
* **One `[no]` line — the work is not handed in**, even if the other numbers “look similar”.

## The same task in different clothes

The same frame fits a completely different task — for example, a taxi fleet. The state — where the car is and
how long the order has been waiting; the action — where to drive; the reward — the money for the ride minus petrol and time; the goal — the takings for
the shift. A shift ends, so the task is episodic, and here γ = 1 is acceptable (but people take less). The model of the world
is unknown: the agent learns demand and traffic jams from experience. The reward lives inside the probabilities: it is part of
the model, and not a separate entity. The cycle is the same: assemble the MDP → evaluate states and steps → make a move → evaluate
again.

## Progress test No. 2

Twelve questions, 12 points, 12 minutes, on the material of the session: the MDP of the maze, the environment, the agent, the run.
Ten multiple-choice and two — in your own words. The variant is by your group.

Both variants are assembled from the same questions, that is why the questions, the answers and the presentations with them appear
here only after both groups have written the progress test — that is, after 13.10.2026. It cannot be posted earlier: it is the same set of questions.

## Key points from the session

* The work is **three files**: the environment, the agent, the run. There is no service layer.
* **Every number in the code came from somewhere**: the grid — from the picture, the probabilities and the rewards — from the fix, γ — from
  lecture 2.
* The agent answers **four questions**: how to evaluate a move, how to get the row, how to choose a move, how to run
  an episode.
* The numbers — from lecture 4: the q rows 4.13 and 5.93, the episode from S1 at seed = 7 — 3.12, the route from the lecture — 4.58,
  the average return of 200 episodes — 1.72 against 1.18.
* The work is handed in when `python3 run.py` prints **all the `[ok]` lines**.
