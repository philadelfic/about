---
number: 2
title: "The concept of the agent–environment interaction"
summary: "The formal language of RL — the “agent — environment” scheme, the notation S, A, R, t, one step, trajectory and episode, return and discounting, policy."
date: '18.09.2026'
lectures:
  - number: 2
    date: '18.09.2026'
simulator: l2
covered:
  - "The main points of the last lecture — RL is about choosing actions, the basic four and the cycle of their interaction"
  - "The “agent — environment” scheme — the agent affects the environment but does not control it"
  - "The notation S, A, R, t and what counts as one step"
  - "Trajectory, episode and terminal state"
  - "“Reward is a signal, not a goal”"
  - "The return G and discounting γ — why a weight is needed and where the horizon 1/(1−γ) comes from"
  - "Episodic and continuing tasks — where you can take γ = 1"
  - "Policy and the ε-greedy policy"
qa:
  - q: "Why do we need a formal language if the idea is clear enough in words?"
    a: "In words you can explain an idea, but you cannot compute with it. A formal language sets precise notation (state, action, reward, time) and the rules for working with it — and it is from them that the formulas for values, the Bellman equations and the code are derived afterwards."
  - q: "Why is the reward written as R with the index t+1 and not t?"
    a: "Because the reward comes after the action. At moment t the agent acts, and the result and the new situation appear at moment t+1 — the index shows that the reward belongs to the consequence of the action, not to the action itself."
  - q: "Why can't we just maximise the reward of the next step?"
    a: "Because the goal is the total result over all the time, not “a plus right now”. Eating a pawn now or making a quiet move towards mate in ten moves — that is an example of how greed at one step keeps you from winning the game. That is why the return G appears — the sum of future rewards."
  - q: "Why discount at all, if you can simply add up all the rewards?"
    a: "Three reasons. The mathematical one — the infinite sum diverges, something has to compress it. The meaningful one — today's reward is worth more than a future one. The engineering one — the distant future is harder to predict, so it is reasonable to reduce its weight."
  - q: "When can you take γ = 1?"
    a: "Only in episodic tasks that have a natural end and a terminal state: there the sum is finite and converges. In continuing tasks there is no end, so γ is necessarily less than one — otherwise the sum will not converge and the horizon will become infinite."
  - q: "How does an episodic task differ from a continuing one?"
    a: "In whether the interaction has a natural end. In an episodic task the agent sooner or later reaches a terminal state, and after it a new episode begins — you can learn from episodes and restart the attempts (a game, a maze, a trip). In a continuing task there is no end: the environment runs all the time, there is no terminal state (the climate in a building, a trading algorithm, a data centre). Hence two consequences: in episodic tasks you can take γ = 1, because the sum is finite, while in continuing ones you cannot; and in episodic tasks you can safely try again, whereas a continuing process cannot be restarted — you have to learn on the go."
  - q: "What is a policy and how does it differ from a single action?"
    a: "A policy is a rule for choosing actions for every state, not one particular action. A deterministic policy always gives the same action in a state, a stochastic one chooses actions with probabilities. The policy is what we are looking for in the end."
  - q: "Why do we need an ε-greedy policy if we already know the best action?"
    a: "So as not to get stuck on the first solution found. If you always choose only what seems best by your current experience, you may never learn about another, more profitable action. The ε-greedy policy tries a random action with probability ε and only otherwise takes the best one known — that is the compromise between exploration and exploitation."
terms:
  - term: "state"
    definition: "a description of the current situation by which the agent makes its decision"
  - term: "S — the set of states"
    definition: "all the situations the agent can end up in"
  - term: "A — the set of actions"
    definition: "everything the agent can do"
  - term: "R — the set of rewards"
    definition: "the numbers by which we estimate the result"
  - term: "t — time"
    definition: "the number of the step"
  - term: "interaction step (timestep)"
    definition: "the transition “state → action → reward → new state”"
  - term: "trajectory"
    definition: "the sequence of “state, action, reward” from the beginning to the end"
  - term: "episode"
    definition: "one interaction of the agent with the environment, from the initial state to the terminal one"
  - term: "terminal state"
    definition: "the state in which the interaction stops"
  - term: "return G"
    definition: "the sum of future rewards with a decreasing weight"
  - term: "discount factor γ"
    definition: "how much the agent takes the future into account; a number from 0 to 1"
  - term: "discounting"
    definition: "counting future rewards with a decreasing weight"
  - term: "effective horizon"
    definition: "roughly 1/(1−γ) steps — how far ahead the agent really looks"
  - term: "episodic task"
    definition: "a task with a natural end — there is a terminal state"
  - term: "continuing task"
    definition: "a task without an end, there is no terminal state"
  - term: "policy (π)"
    definition: "the rule for choosing actions: a mapping from states to actions"
  - term: "deterministic policy"
    definition: "always the same action in a state"
  - term: "stochastic policy"
    definition: "actions are chosen with probabilities"
  - term: "ε-greedy policy"
    definition: "a random action with probability ε, otherwise the best one known"
  - term: "exploration and exploitation"
    definition: "to try something new or to take the proven one"
lecture:
  - title: "Presentation of lecture 2 (PPTX)"
    href: "/files/course/rl/l2-agent-i-sreda.pptx"
---

## Why a formal language

Intuition describes RL in words: a system acts, gets feedback and learns. That is enough to understand the idea,
but not enough to compute anything and write code. Formalisation is the task written down in precise notation
and in the rules by which you can do computations.

> **Why it matters:** without precise notation you will neither write the code nor explain yourself to colleagues and the teacher: “roughly like that” neither runs nor gets checked.

## The “agent — environment” cycle

* **The agent** — the one who makes the decisions.
* **The action** — what the agent can do.
* **The environment** — the world inside which the agent acts.
* **The reward** — a numeric signal for the result.

The agent sends an action into the environment, the environment returns a new state and a reward. What matters:
the agent **affects** the environment but does not **control** it — otherwise the task would be about plain
planning, not about learning.

> **Why it matters:** this is the only scheme by which all the tasks of the course are stated. If you do not draw the border “agent / environment”, you cannot define the state, the action or the reward further on.

## The notation S, A, R, t

* **S** — the set of states: all the situations the agent can end up in.
* **A** — the set of actions: everything the agent can do.
* **R** — the set of rewards: the numbers by which we estimate the result.
* **t** — time, the number of the step.

**A state** is a description of the current situation by which the agent makes its decision. **A reward** is a
numerical estimate of the result.

> **Why it matters:** all the rest of the mathematics of the course stands on these four symbols — transition probabilities, values, the Bellman equations. Without them the formulas further on read like hieroglyphs.

## One step in time

The action happens at moment t, the result at moment t+1:

![One step: from a state the agent acts, the environment returns a reward and a new state](/img/course/rl/step-chain.png)
*Time is the number of the step: the agent stands in s0 (step 0), took a step — and ended up in s1 (step 1). The action has the number 0, while the reward and the new state have 1: the reward comes on the transition.*

The reward comes after the action, hence its index t+1 as well. A step of interaction is the transition
“state → action → reward → new state”.

> **Why it matters:** this is where the order of computations in the code comes from: the reward belongs to the transition, not to the action. Getting that wrong means shifting the indices and getting the wrong return.

## Trajectory, episode, terminal state

* **A trajectory** — the full history of the interaction: the sequence of “state, action,
  reward” from the beginning to the end.
* **A terminal state** — the state in which the interaction stops.
* **An episode** — one interaction of the agent with the environment, from the initial state to the terminal one.

Examples of episodes: a maze, a game of chess, a taxi driver's trip.

$$
s_0 \to a_0 \to r_1 \to s_1 \to a_1 \to r_2 \to s_2 \to \dots
$$

*The trajectory is the whole chain, from the initial state to the terminal one.*

> **Why it matters:** the episode is the unit of experience the agent and the code work with: it is the transitions of one episode that are fed to learning.

## Reward is a signal, not a goal

The reward is a signal of “here and now”, an estimate for one step. The goal of the agent is the **total**
reward over all the time of interaction, not the maximum of the next step. Examples: eating a pawn now or
making a quiet move towards mate in ten moves; spending your salary in a day or putting it aside for a flat.

![On the left — the signal for one step, on the right — the goal: the sum of all estimates over all the time](/img/course/rl/signal-vs-goal.png)
*One estimate per step against the sum of all estimates.*

> **Why it matters:** if you optimise the signal instead of the goal, the agent will win the step and lose the task. That is the most frequent mistake when setting up a reward.

## Return and discounting

The **return** G is the sum of future rewards, each with its own weight:

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

**γ (gamma)** is the discount factor from 0 to 1: how much the agent takes the future into account. $\gamma = 0$ —
we look only at the next step, $\gamma \to 1$ — we look far ahead.

Why discount:

1. **Mathematics** — the infinite sum diverges, it has to be compressed.
2. **Meaning** — today's reward is worth more than a future one.
3. **Engineering** — the distant future is harder to predict.

$$
1/(1-\gamma)
$$

The effective horizon is ≈ $1/(1-\gamma)$. Where that comes from: denote the sum by $S$; then
$S = 1 + \gamma S$ (everything after the first unit is the same sum multiplied by $\gamma$), hence
$S = 1/(1-\gamma)$.

| γ | Horizon | Looks ahead roughly |
|---|----------|---------------------------|
| 0 | 1 | 0 steps |
| 0.5 | 2 | 2 steps |
| 0.9 | 10 | 10 steps |
| 0.99 | 100 | 100 steps |

γ is a setting that we choose.

> **Why it matters:** γ is the knob that tunes the behaviour of the agent: how ready it is to wait for the result. A wrong γ gives learning that formally works but does not solve the task.

## Where γ = 1 is allowed

* **Episodic tasks** — a game, a maze, a trip: there is a natural end and a terminal state, so $\gamma = 1$ is
  allowed.
* **Continuing tasks** — the climate in a building, a trading algorithm, a data centre: there is no end, so
  $\gamma$ is necessarily less than one.

![Episodic task: episode after episode, a finite number of rewards — you can take γ = 1. Continuing: there is no end, the sum diverges — γ is necessarily less than one](/img/course/rl/episodic-vs-continuous.png)

> **Why it matters:** a mistake here breaks the whole computation: $\gamma = 1$ in a continuing task means a diverging sum and an infinite horizon.

The rule is simple: $\gamma = 1$ only where the task ends.

## Policy: the rule for choosing actions

**A policy (π)** is a rule for choosing actions, a mapping from states to actions. Not one action but a rule for
all states; it is convenient to picture it as a table “states × actions” with the probabilities of choice in the
cells.

* **Deterministic** — always the same action in a state.
* **Stochastic** — the actions are chosen with probabilities.

The policy is what we are looking for.

> **Why it matters:** the policy is what we are looking for in the end; everything else in the course (values, estimates, algorithms) exists to find it.

## The ε-greedy policy

* **Exploration** — trying new actions.
* **Exploitation** — choosing what already seems the best.

**The ε-greedy policy**: with probability ε a random action is chosen, otherwise — the best one known.
**ε** is the probability of a random action, one more setting that we choose.

![ε-greedy: the share ε — random actions, 1 − ε — the best one known](/img/course/rl/eps-greedy.png)
*Small ε — we rarely try something new, large ε — often.*

> **Why it matters:** this is the first working answer to the question “how do I search while I do not know yet”: without exploration the agent gets stuck on the first solution found and never reaches the better one.
