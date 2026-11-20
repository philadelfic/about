---
number: 1
title: "Where reinforcement learning applies"
summary: "What RL is, how it differs from other approaches, and when a task really needs it."
date: '11.09.2026'
lectures:
  - number: 1
    date: '11.09.2026'
covered:
  - "What reinforcement learning is and how it differs from supervised learning"
  - "The three paradigms of learning and where RL sits among them"
  - "The signs of a task that really needs RL"
  - "The dilemma “explore or exploit” (explore/exploit)"
  - "Sparse reward and the price of a mistake"
qa:
  - q: "How does reinforcement learning differ fundamentally from supervised learning?"
    a: "In supervised learning there are labelled examples with the right answers, and the model learns to reproduce them. In reinforcement learning there are no right answers — there is only a reward for the consequences of your own actions. The agent collects the data itself, by its own behaviour, and its actions determine which data it will get next."
  - q: "Do you have to use a neural network?"
    a: "No. The basic methods of the course are tabular: the policy and the value estimates can be kept in a table of states and actions. Neural networks are needed when there are too many states to list them in a table."
  - q: "I have a simulator and I know the rules — why RL, if I can just enumerate the options?"
    a: "Enumeration works while there are few states and the horizons are short. As soon as there are many options (say, 10 actions over 50 steps), a full enumeration is impossible, and you need a method that learns from experience instead of trying everything."
  - q: "What do I do if the reward comes rarely?"
    a: "That is the main difficulty of RL: with a sparse reward there is almost no signal to learn from. The usual tricks are to make the signal denser (intermediate rewards), to simplify the task, or to start with a simpler version of the environment."
  - q: "How do I tell that a task is not for reinforcement learning?"
    a: "If there are ready-made right answers and labels — that is supervised learning. If you need structure in the data without sequential decisions — that is unsupervised learning. RL is justified when there is a sequence of decisions, a delayed result and a chance to gain experience in an environment."
terms:
  - term: "reinforcement learning (RL)"
    definition: "a method of machine learning in which the system learns to choose actions by their consequences — by the reward it gets"
  - term: "agent"
    definition: "the one who makes the decisions"
  - term: "environment"
    definition: "the world the agent acts on and that returns a result"
  - term: "action"
    definition: "what the agent can do"
  - term: "reward"
    definition: "a numerical estimate of the result"
  - term: "supervised learning"
    definition: "an approach where there are examples with right answers"
  - term: "unsupervised learning"
    definition: "an approach without labels: it looks for structure in the data"
  - term: "exploration"
    definition: "trying new actions to learn more"
  - term: "exploitation"
    definition: "choosing the action that already seems the best"
  - term: "sparse reward"
    definition: "the signal comes rarely, there is almost nothing to learn from"
lecture: []
---

## What reinforcement learning is

An agent acts in an environment and learns from its own experience: for its actions it gets a **reward** and
over time builds a **policy** that brings more reward over the long run. Nobody gives it ready-made “right
answers” — there are only the consequences of its actions.

> **Why it matters:** if you do not see this difference, it is easy to take on RL where ordinary labelling would have been enough — and to spend months instead of days.

Three consequences follow, and they set RL apart from the other approaches:

* **No labels.** Instead of a right answer — a reward signal, often rare and delayed.
* **The agent collects the data itself.** Nobody hands it over in advance: by its own behaviour the agent determines what it will see.
* **The goal is delayed in time.** What matters is not the action that got a reward right now, but the total result
  over many steps.

## The three paradigms of learning

| Paradigm | What is given | What it learns |
|-----------|----------|-------------|
| Supervised | Labelled examples | To reproduce the right answer |
| Unsupervised | Data without labels | To find structure, groups, anomalies |
| Reinforcement | Environment, actions, reward | To choose actions that maximise the total reward |

The border is not rigid: inside RL people often use models trained with supervision — for example, a neural
network as an approximation of the value function.

> **Why it matters:** the choice of paradigm is the first practical question when you set up a task: it determines which data you need and what even counts as a result.

## When RL is really needed

The signs of a task:

1. There is a **sequence of decisions**, not a single answer.
2. The result is **delayed**: the effect of an action is not visible at once.
3. There is an **environment** where you can gain experience — real or a simulator.
4. There is a **scalar signal**: what exactly we want to maximise is expressed as a number.

Red flags: the reward cannot be formulated as a number; experience cannot be gained safely and cheaply; the task
can be solved by enumeration or ordinary optimisation; a mistake in the environment costs too much.

> **Why it matters:** these four signs are a quick filter. If at least one of them is missing (no environment, no experience, no numeric signal), RL will not work, and it is better to find that out before development, not after.

## Explore or exploit

The main dilemma of RL: **exploit** the best action known or **explore** a new one in order to learn more.
Little exploration — the agent gets stuck in a mediocre policy. Too much — it loses reward on constant
experiments.

The matter is made harder by a **sparse reward**: when the reward comes rarely, there is almost no signal,
and nothing to learn from.

> **Why it matters:** this is the main conflict of RL. Any decision “try something new or take the proven one” is about it, and further along the course it never goes away.

## The price of RL

RL is not a free way to solve tasks. It requires a lot of experience (sometimes millions of steps), it tolerates
mistakes only in a simulator, and it is noticeably harder to tune than supervised learning. Before taking on
RL, it is worth honestly checking whether there is a simpler path to the result.

> **Why it matters:** an honest estimate of the price saves you from disappointment: RL is an expensive tool, and it is worth taking on only where the simple paths really do not work.
