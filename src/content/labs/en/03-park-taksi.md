---
number: 3
title: "Lab 3: the optimal strategy for managing a fleet of vehicles"
summary: "Stating control as an MDP and solving it by learning from experience: SARSA and Q-learning on one scene, a comparison of a single and a split strategy. A mandatory piece of the course: a report, two plots, a strategy table, a checklist and a log."
issued: false
due: "25.12.2026 (group 1) · 29.12.2026 (group 2)"
---

**What the work is about.** Learn to state a control problem as an MDP and solve it by learning from experience,
without a model of the transitions: implement SARSA and Q-learning on one scene, compare a single and a split
strategy, and explain the difference between the learned strategies through the price of a mistake.

**Variant.** The two groups have different variants of the statement — yours is given in the assignment and at
session 10.
**Variant A** — group М80-203СВ-25, practical session 08.12. **Variant B** — group М80-202СВ-25, practical session
11.12.

**When it is handed out.** The skeleton with gaps — at the tenth practical session (08.12 / 11.12); the files go to
the chat after the class.

**Deadline.** Report, code, checklist and log — before the twelfth practical session starts: group М80-203СВ-25 — by
25.12.2026, group М80-202СВ-25 — by 29.12.2026. There is no oral defence: the work is accepted by the report, the
code and the log, the code is read selectively and on suspicion, the formal requirements are checked by a script.
Typical mistakes get their walkthrough at the eleventh and twelfth practical sessions.

**Retake** — one, within two weeks after that walkthrough, before the exam day: a corrected report, the log and
three to five lines on what was fixed under which checklist item.

**What is submitted.** Code (the fleet environment, both methods, a run with the metrics from the log) — pure
python3, no numpy. Two plots: the learning curves of SARSA against Q and income (or the share of demand served) over
time. A table of the learned strategy “state → action” for both methods. `REPORT.md`: the MDP statement, methods
and settings, result tables, conclusions — at least three, each with a number, two mandatory paragraphs (questions
22 and 23), a section “what will change in another statement”, reproducibility. A checklist of criteria with
references to the report sections — without it the work is not accepted. `run_log.jsonl`.

**Criteria.** Variant A: the statement is episodic (S, A, p, R, γ = 0.9, T = 100) plus a paragraph on the
difference from the lectures; the metric is income per shift. Variant B: the statement is continuing (γ < 1
mandatory, γ = 0.95) plus a phrase about the divergence of the sum; the metric is the mean income per step, window
2000; the wording “income per episode” must not appear in the report. Common to both variants: both methods are
implemented and compared (curves plus the strategy table), all three mandatory studies are done, the two mandatory
paragraphs are filled in, ≥ 100 runs per point, median + IQR, every conclusion with a number from your own runs,
the code is reproduced by the command from the report, borrowed code — in the format of lab 1.

**The full assignment** — in the file: [technical specification of lab 3](/about/files/course/rl/lab3/lab3-spec.md).
