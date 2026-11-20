---
number: 1
title: "Agent and Environment"
summary: "Where reinforcement learning applies: RL’s place among machine-learning paradigms, the five signs a task is a fit, one step of interaction between agent and environment, computing the return and choosing an action with an ε-greedy strategy. At the end — tasks to check you understood the material."
date: "22.09.2026 · 29.09.2026"
covered:
  - Went through where reinforcement learning applies, and RL’s place among machine-learning paradigms
  - Went through the five signs of a task that reinforcement learning fits
  - Practised telling supervised, unsupervised and reinforcement learning apart
  - "Went through one step of interaction: state → action → reward → new state"
  - Computed the return G and chose an action with an ε-greedy strategy
  - "Took progress test No. 1: 12 questions on lecture 2 and today’s theory"
tasks:
  - title: "Task 1. What type of learning"
    text: "The price of an apartment from its features; similar bank clients; a robot driving up to a charging station. Identify the type of learning in each case and explain why."
    answer: "Apartment price — supervised; similar clients — unsupervised; robot driving up to a charging station — reinforcement. Why: look at what the human gives the machine — ready correct answers, just objects without answers, or a single evaluation of actions; the agent collects the experience itself."
  - title: "Task 2. Does reinforcement learning apply"
    text: "A class timetable; a game with a score; a forecast of customer churn from history; the temperature in a data centre. Answer “yes” or “no” and explain why — the five signs from the theory will help."
    answer: "Class timetable — no; game with a score — yes; customer churn — no; temperature in a data centre — yes. Why: a timetable is solved with exact methods and not step by step, churn is a forecast from historical data, while a game with a score has step-by-step decisions and delayed reward, and a data centre has continuous control and safe trials. A separate trap: in a game with a score the rules of the moves are known, but the strategy is not — that is what we are looking for."
  - title: "Task 3. One step"
    text: "Take the courier example and write out one step: state, action, reward, new state. Separately answer why the reward has index t + 1."
    answer: "One step: sₜ → aₜ → rₜ₊₁, sₜ₊₁. State — where the courier is and which order he has in his hands; action — take route A or route B; reward — delivered on time +10, late −10; new state — the courier is in a new place, the order handed over. Why index t + 1: the result of the action arrives in the very next moment, so the reward and the new state belong to step t + 1, not to the action itself."
  - title: "Task 4. Find the mistake"
    text: "Three phrases: “the agent is the whole team”, “the state is the whole project”, “the action is a stage of the process”. What is wrong in each?"
    answer: "There is one agent, and it makes the decisions, the other roles are the environment; the state is only what is needed for the decision right now, otherwise it is infinitely large; the action is the agent’s decision, while a stage of the process is a time step. Why: in all three phrases the “agent — environment” boundary is erased — the team, the project and the stage of the process describe the environment, not the agent, the state and the action."
  - group: "A"
    title: "Task 5. Compute and choose"
    text: "Three rewards in a row: +10, −10, +10 with γ = 0.9 — what is the return? The average payoffs of the three actions are 6, 8 and 4, ε = 0.1 — which action will the ε-greedy strategy choose and with what probability?"
    answer: "Return: 10 + 0.9 · (−10) + 0.9² · 10 = 10 − 9 + 8.1 = 9.1. Why: the minus on the second step ate part of the return — that is exactly what discounting is for, the near reward weighs more than the far one. Choice: with probability 90 % — “route B” (the best known action, average payoff 8), with probability 10 % — a random action (exploration)."
  - group: "B"
    title: "Task 5. Compute and choose"
    text: "Three rewards in a row: 4, 4, 4 with γ = 0.5 — what is the return? How many steps ahead does the agent look with γ = 0.5? The average payoffs of the three actions are 6, 8 and 4, ε = 0.1 — which action will the ε-greedy strategy choose and with what probability?"
    answer: "Return: 4 + 0.5 · 4 + 0.25 · 4 = 4 + 2 + 1 = 7. Why: with γ = 0.5 each next step weighs half as much, so the effective horizon is about 2 steps (1/(1 − 0.5)) and beyond two steps the contribution hardly shows. Choice: with probability 90 % — “route B” (the best known action, average payoff 8), with probability 10 % — a random action (exploration)."
quiz:
  - group: "A"
    title: "Question 1"
    text: "What is one step of interaction?"
    options:
      - "a) from the start of the episode to the terminal state"
      - "b) state → action → reward on the next step → new state"
      - "c) one action of the agent"
      - "d) the moment the reward is received"
    answer: "Correct: b) state → action → reward on the next step → new state. Why: one step is one action of the agent and the environment’s response to it; from the start of the episode to the terminal state is the whole episode."
  - group: "A"
    title: "Question 2"
    text: "Why is the reward after an action denoted rₜ₊₁?"
    options:
      - "a) the result of the action arrives already on the next step"
      - "b) to tell the reward from the return"
      - "c) because the state has index t"
      - "d) there is no separate meaning, that is the convention"
    answer: "Correct: a) the result of the action arrives already on the next step. Why: at moment t the agent acts, and the reward and the new state appear already at moment t + 1 — the index shows that the reward refers to the consequence of the action, not to the action itself."
  - group: "A"
    title: "Question 3"
    text: "An episodic task is a task…"
    options:
      - "a) in which γ < 1 without fail"
      - "b) with a natural end and a terminal state"
      - "c) in which the agent acts once"
      - "d) in which the reward comes only at the very end"
    answer: "Correct: b) with a natural end and a terminal state. Why: an episodic task has a natural end — a terminal state, after which a new episode begins (a game, a maze, a trip). Whereas γ < 1 is exactly about continuous tasks, where there is no end."
  - group: "A"
    title: "Question 4"
    text: "What does the agent maximise?"
    options:
      - "a) the reward of the current step"
      - "b) the number of steps in the episode"
      - "c) the return — the sum of future rewards with discounting"
      - "d) the average reward of the first two steps"
    answer: "Correct: c) the return — the sum of future rewards with discounting. Why: the reward is the signal for one step, while the agent’s goal is the total result over the whole time; that is exactly why the return G and the weight γ appear."
  - group: "A"
    title: "Question 5"
    text: "With γ = 0.9 the effective horizon is about 10 steps. What does that mean?"
    options:
      - "a) the agent takes about 10 steps ahead into account"
      - "b) the episode lasts no more than 10 steps"
      - "c) after 10 steps the return resets to zero"
      - "d) the agent makes 10 steps before the first reward"
    answer: "Correct: a) the agent takes about 10 steps ahead into account. Why: the effective horizon is 1/(1 − γ) and it shows how far ahead the agent really looks: 1/(1 − 0.9) = 10. The length of the episode and the moment of the first reward have nothing to do with it."
  - group: "A"
    title: "Question 6"
    text: "Where is γ = 1 allowed?"
    options:
      - "a) in a continuous task"
      - "b) in an episodic task"
      - "c) in any task"
      - "d) nowhere"
    answer: "Correct: b) in an episodic task. Why: γ = 1 can be taken only where the interaction ends — the sum is finite and converges; in a continuous task there is no end, so γ is necessarily less than one."
  - group: "A"
    title: "Question 7"
    text: "The agent received rewards 1, 1, 1, γ = 0.9. What is the return G_t?"
    options:
      - "a) 1.9"
      - "b) 2.71"
      - "c) 2.9"
      - "d) 3"
    answer: "Correct: b) 2.71. Why: the return is the sum of rewards with a decreasing weight: 1 + 0.9 · 1 + 0.81 · 1 = 2.71. Plain addition 1 + 1 + 1 = 3 does not take discounting into account."
  - group: "A"
    title: "Question 8"
    text: "How does reinforcement learning differ from supervised learning?"
    options:
      - "a) it does not, they are the same thing"
      - "b) in RL there are no ready correct answers — only an evaluation of actions"
      - "c) in RL there is always more data"
      - "d) in RL the machine does not learn at all"
    answer: "Correct: b) in RL there are no ready correct answers — only an evaluation of actions. Why: in supervised learning the human gives pairs “object — correct answer”, while in reinforcement learning he sets only the reward: the machine gets an evaluation “good or bad” and collects the data itself with its own actions."
  - group: "A"
    title: "Question 9"
    text: "Which task is NOT solved with reinforcement learning methods?"
    options:
      - "a) teach a robot to walk"
      - "b) control the cooling of a data centre"
      - "c) predict customer churn from historical data"
      - "d) teach an agent to play a game with a score"
    answer: "Correct: c) predict customer churn from historical data. Why: this is a forecast “what will happen?”, not a decision “what to do?” — there are no step-by-step decisions and you cannot experiment, you cannot remake the customers. The other three are step-by-step control, where you can try safely."
  - group: "A"
    title: "Question 10"
    text: "A strategy π is…"
    options:
      - "a) a list of actions performed during an episode"
      - "b) a rule for choosing actions: state → action"
      - "c) a sequence of visited states"
      - "d) the reward in the terminal state"
    answer: "Correct: b) a rule for choosing actions: state → action. Why: a strategy is a rule for all states, not one action and not a list of what has already been done; it is the strategy we are ultimately looking for."
  - group: "A"
    title: "Question 11"
    text: "Your own example: name the agent, the state, the action and the reward for any task (work, study, life) and say whether it is episodic or continuous"
    answer: "Sample: the agent is a student preparing for an exam; the state is how many topics are already covered and how many days are left; the action is to study the next topic or take a break; the reward is a practice problem solved, +1; the type of task is episodic, it ends with the exam passed. Scoring: 1 point if all five elements are named — agent, state, action, reward and the type of task; 0.5 — if 2–3 out of five."
  - group: "A"
    title: "Question 12"
    text: "Name three signs that show a task is meant for reinforcement learning"
    answer: "Sample: the task is solved step by step; the action affects what happens next; the reward does not come at once but after several steps. Scoring: 1 point for three signs out of five — steps, the action’s influence on the future, delayed reward, an unknown rule, the ability to interact with the environment; 0.5 — for two signs."
  - group: "B"
    title: "Question 1"
    text: "What is one step of interaction?"
    options:
      - "a) one action of the agent"
      - "b) state → action → reward on the next step → new state"
      - "c) from the start of the episode to the terminal state"
      - "d) the moment the reward is received"
    answer: "Correct: b) state → action → reward on the next step → new state. Why: one step is one action of the agent and the environment’s response to it; from the start of the episode to the terminal state is the whole episode."
  - group: "B"
    title: "Question 2"
    text: "Why is the reward after an action denoted rₜ₊₁?"
    options:
      - "a) to tell the reward from the return"
      - "b) because the state has index t"
      - "c) there is no separate meaning, that is the convention"
      - "d) the result of the action arrives already on the next step"
    answer: "Correct: d) the result of the action arrives already on the next step. Why: at moment t the agent acts, and the reward and the new state appear already at moment t + 1 — the index shows that the reward refers to the consequence of the action, not to the action itself."
  - group: "B"
    title: "Question 3"
    text: "An episodic task is a task…"
    options:
      - "a) with a natural end and a terminal state"
      - "b) in which γ < 1 without fail"
      - "c) in which the agent acts once"
      - "d) in which the reward comes only at the very end"
    answer: "Correct: a) with a natural end and a terminal state. Why: an episodic task has a natural end — a terminal state, after which a new episode begins (a game, a maze, a trip). Whereas γ < 1 is exactly about continuous tasks, where there is no end."
  - group: "B"
    title: "Question 4"
    text: "What does the agent maximise?"
    options:
      - "a) the reward of the current step"
      - "b) the average reward of the first two steps"
      - "c) the return — the sum of future rewards with discounting"
      - "d) the number of steps in the episode"
    answer: "Correct: c) the return — the sum of future rewards with discounting. Why: the reward is the signal for one step, while the agent’s goal is the total result over the whole time; that is exactly why the return G and the weight γ appear."
  - group: "B"
    title: "Question 5"
    text: "With γ = 0.5 the effective horizon is about 2 steps. What does that mean?"
    options:
      - "a) the episode lasts no more than 2 steps"
      - "b) the agent makes 2 steps before the first reward"
      - "c) after 2 steps the return resets to zero"
      - "d) the agent takes about the 2 nearest steps into account"
    answer: "Correct: d) the agent takes about the 2 nearest steps into account. Why: the effective horizon is 1/(1 − γ), with γ = 0.5 we get 1/(1 − 0.5) = 2; it is about how far ahead the agent looks, not about the length of the episode."
  - group: "B"
    title: "Question 6"
    text: "Where is γ = 1 allowed?"
    options:
      - "a) in a continuous task"
      - "b) in an episodic task"
      - "c) in any task"
      - "d) nowhere"
    answer: "Correct: b) in an episodic task. Why: γ = 1 can be taken only where the interaction ends — the sum is finite and converges; in a continuous task there is no end, so γ is necessarily less than one."
  - group: "B"
    title: "Question 7"
    text: "The agent received rewards 4, 4, 4, γ = 0.5. What is the return G_t?"
    options:
      - "a) 6"
      - "b) 8"
      - "c) 7"
      - "d) 12"
    answer: "Correct: c) 7. Why: the return is the sum of rewards with a decreasing weight: 4 + 0.5 · 4 + 0.25 · 4 = 4 + 2 + 1 = 7. Plain addition 4 + 4 + 4 = 12 does not take discounting into account."
  - group: "B"
    title: "Question 8"
    text: "How does reinforcement learning differ from supervised learning?"
    options:
      - "a) it does not, they are the same thing"
      - "b) in RL there are no ready correct answers — only an evaluation of actions"
      - "c) in RL there is always more data"
      - "d) in RL the machine does not learn at all"
    answer: "Correct: b) in RL there are no ready correct answers — only an evaluation of actions. Why: in supervised learning the human gives pairs “object — correct answer”, while in reinforcement learning he sets only the reward: the machine gets an evaluation “good or bad” and collects the data itself with its own actions."
  - group: "B"
    title: "Question 9"
    text: "Which task is NOT solved with reinforcement learning methods?"
    options:
      - "a) control the cooling of a data centre"
      - "b) teach a robot to walk"
      - "c) teach an agent to play a game with a score"
      - "d) predict customer churn from historical data"
    answer: "Correct: d) predict customer churn from historical data. Why: this is a forecast “what will happen?”, not a decision “what to do?” — there are no step-by-step decisions and you cannot experiment, you cannot remake the customers. The other three are step-by-step control, where you can try safely."
  - group: "B"
    title: "Question 10"
    text: "A strategy π is…"
    options:
      - "a) a rule for choosing actions: state → action"
      - "b) a list of actions performed during an episode"
      - "c) a sequence of visited states"
      - "d) the reward in the terminal state"
    answer: "Correct: a) a rule for choosing actions: state → action. Why: a strategy is a rule for all states, not one action and not a list of what has already been done; it is the strategy we are ultimately looking for."
  - group: "B"
    title: "Question 11"
    text: "Your own example: name the agent, the state, the action and the reward for any task (work, study, life) and say whether it is episodic or continuous"
    answer: "Sample: the agent is a student preparing for an exam; the state is how many topics are already covered and how many days are left; the action is to study the next topic or take a break; the reward is a practice problem solved, +1; the type of task is episodic, it ends with the exam passed. Scoring: 1 point if all five elements are named — agent, state, action, reward and the type of task; 0.5 — if 2–3 out of five."
  - group: "B"
    title: "Question 12"
    text: "Name three signs that show a task is meant for reinforcement learning"
    answer: "Sample: the task is solved step by step; the action affects what happens next; the reward does not come at once but after several steps. Scoring: 1 point for three signs out of five — steps, the action’s influence on the future, delayed reward, an unknown rule, the ability to interact with the environment; 0.5 — for two signs."
materials:
  - title: "Session presentation, group М80-203СВ-25 — PPTX"
    href: "/files/course/rl/s1-agent-i-sreda-gr-m80-203.pptx"
  - title: "Session presentation, group М80-202СВ-25 — PPTX"
    href: "/files/course/rl/s1-agent-i-sreda-gr-m80-202.pptx"
---

## What reinforcement learning is

**Reinforcement learning (RL)** is a machine-learning method in which the system learns to choose
actions by the consequences of those actions. The agent acts, the environment answers: a new state
arrives and a number — the reward. We set the goal not with a correct answer but with a reward; the
agent learns from the consequences: what brought benefit it repeats, what did not it drops.

## Three ways to teach a machine

* **Supervised** — the human gives pairs “object — correct answer”. Example: the price of an apartment from its features.
* **Unsupervised** — there are no correct answers, the machine looks for structure in the data. Example: finding similar
  bank clients.
* **Reinforcement** — the human sets only the reward, the agent collects the data itself with its own
  actions. Example: a system keeps the temperature in a data centre.

The difference is exactly one thing: in the first two cases we say what is correct, in the third we only evaluate
the result.

> **Why this matters:** in an interview and at an exam the first question about RL is “how does it differ from
> ordinary machine learning”. The answer is short: RL does not predict, it chooses actions.

## How reinforcement learning differs

1. **There is no correct answer for every step** — only an evaluation: good or bad.
2. **The agent creates the data itself** — its actions change what it will see next, you cannot collect a dataset in advance.
3. **The reward is delayed** — a correct step may be paid for ten steps later. In chess a quiet move
   decides the game, but a captured pawn does not.
4. **A mistake costs time and money** — a wrong step cannot be undone.

> **Why this matters:** everything else grows out of these four differences: since we create the data ourselves, we need
> exploration and exploitation; since the reward is delayed, we need the return and discounting.

## Where it is used

* **Games and simulators** — from chess to control simulators.
* **Robots and control** — walking, manipulators, cooling a data centre.
* **Recommendations and content** — what to show next so the person does not leave.
* **Energy and logistics** — load distribution, fleet management.

They all have one thing in common: there is an environment, and decisions are made step by step.

## A task that reinforcement learning does not solve

* **The transportation problem** — how to deliver goods more cheaply. There is an exact optimisation method, no experience needed.
* **Predicting customer churn** from history. There are no step-by-step decisions, and you cannot experiment: you cannot
  remake the customers.

The rule is simple: if there is an exact method or you cannot interact with the environment, you do not need
reinforcement learning.

## Five signs: worth trying if…

1. The task is **solved step by step**.
2. Your action **affects what happens next**.
3. The reward comes **not at once**, but after several steps.
4. The rule of actions is **unknown** or too complicated.
5. You **can interact with the environment** — there is a simulator or a safe way to try.

> **Why this matters:** the fifth sign is the most practical. If you cannot experiment, reinforcement learning
> will not start, however fitting the rest of the list looks.

## A forecast is not a decision

**A forecast** answers the question “what will happen?” — a price, churn, demand. **A decision** answers the question “what
to do?” — whom to deliver an order to, what to put in a release. Reinforcement learning is always about the second.

## Key points from the session

* Reinforcement learning is about **choosing actions**, not about a forecast.
* A task fits if decisions are made **step by step**, there is **influence** on the future, the reward is
  **delayed**, the rules are **unknown** and you **can experiment** with the environment.
* One step is $s_t \to a_t \to r_{t+1},\ s_{t+1}$: the action at moment t, the result at moment t + 1.
* The return G is the sum of rewards with a decreasing weight; γ is farsightedness, ε is the share of random trials.
