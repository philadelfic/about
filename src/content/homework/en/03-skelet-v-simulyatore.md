---
title: Homework for lecture 4
summary: Eight questions about the skeleton in the simulator — what the environment and the agent are, s and a, a reward of three terms, how to measure improvement and why you cannot write out a q-row.
due: '09.10.2026'
topic: 3
lecture: 4
---

**The problem.** In the lecture we watched three short clips from a physics simulator: there an agent learns
to walk. Nobody drew a single frame — every movement was chosen by a program. The eight questions below are
about that task. They test not memory but the ability to write out an MDP in your own words: the same four —
state, action, reward, γ — only instead of a cell there are angles and joint velocities.

The clips (YouTube, the Goatstream channel):

* 46 s — [“Trying to teach my new model to run using reinforcement learning”](https://www.youtube.com/watch?v=c3R3-QXlL4s)
* 11 s — [“This agent was optimized for maximum happiness”](https://www.youtube.com/watch?v=wvQ1D7hI2rE)
* 8.3 s — [“Stair climbing simulation”](https://www.youtube.com/watch?v=DRnjQT2b0us)

**What to do.** Answer the eight questions — briefly, one or two phrases each.

1. What is the environment here and what is the agent? Is the environment the video recording itself?
2. What does the agent get as input and what does it output? Write it in one line: s = …, a = … — three or four
   quantities are enough.
3. Assemble the reward from three terms — with signs, in one formula.
4. What happens if you leave only “how far forward it got” in the reward?
5. Is this an episodic or a continuing task? Justify. What γ will you set and what horizon does it give?
6. How is a step chosen under an ε-greedy strategy? What ε would you set at the start of learning and what at the
   end — and why?
7. How will you know that the agent has started walking better? Name exactly what you will measure.
8. In the maze a q-row is four numbers: ↑1.97 ↓4.13 ←1.97 →4.13. For our skeleton such a row cannot be written
   out. Why?

**A common mistake.** “Because there are too many states” — that is an answer about states, while the eighth
question asks about actions: in the skeleton they are continuous and multidimensional, there are infinitely many
of them.

**Where to look.** The first three questions are about the problem statement: what the state is here, what the
action is, what the reward is. It is covered in the section
[“Where and how this is used”](/about/students/mai/rl/topics/03-markovskij-process/#где-и-как-это-используется).
On γ and the horizon — in the section
[“Discounting: why the future has weight”](/about/students/mai/rl/topics/03-markovskij-process/#дисконтирование-зачем-у-будущего-вес),
on ε-greedy choice — in topic 2,
[“ε-greedy strategy”](/about/students/mai/rl/topics/02-agent-i-sreda/#ε-жадная-стратегия).

**How to submit:** on a sheet, by the lecture on 9 October. We go through the answers on 9 October.
