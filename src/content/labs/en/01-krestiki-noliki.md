---
number: 1
title: "Lab 1: tic-tac-toe — algorithms and hyperparameters"
summary: "Self-play in tic-tac-toe: a value table of positions, the TD update from experience, tuning the step α and exploring with ε. A mandatory piece of the course: a report, two plots, a checklist and a run log."
issued: false
draft: true
due: "01.12.2026 (group 1) · 04.12.2026 (group 2)"
---

**What the work is about.** Tic-tac-toe 3 × 3, the agent learns by playing against itself (self-play). State values
are estimated by the tabular TD method from experience, without an environment model; the move is chosen
ε-greedily. Show with numbers how α and ε affect the quality of the learned strategy.

**When it is handed out.** The skeleton with gaps — at the seventh practical session (17.11 / 20.11); the files go
to the chat after the class.

**Deadline.** Report, code, checklist and log — before the ninth practical session starts: group М80-203СВ-25 — by
01.12.2026, group М80-202СВ-25 — by 04.12.2026. There is no oral defence: the work is accepted by the report, the
code and the log, the code is read selectively and on suspicion, the formal requirements are checked by a script.
Typical mistakes get their walkthrough at the eighth and ninth practical sessions.

**Retake** — one, within two weeks after that walkthrough, before the eleventh practical session (08.12 / 11.12):
a corrected report, the log and three to five lines on what was fixed under which checklist item. The record sheet
gets the latest version; a retake without the walkthrough in class is not accepted.

**What is submitted.** Code (environment: a game, lines, a draw; canonisation; agent: a value table, ε-greedy
choice, TD update; a self-play run; evaluation) — pure python3, no numpy. Two plots: learning curves by α and by
ε. `REPORT.md`: statement, methods and settings, result tables, conclusions — at least three, each with a number
from your own runs, reproducibility (seeds and commands). A checklist of criteria with references to the report
sections — without it the work is not accepted. `run_log.jsonl` from the run.

**Criteria.** The statement is formalised (state, action, rewards, γ = 1 with a justification). Both mandatory
studies (α — two values, ε — two values) and a curve for each. Quality is evaluated against both named opponents
**in both roles**, ≥ 100 independent runs per point, median + IQR. The size of the table after canonisation is
reported — and it matches 765. Every conclusion is backed by a number from your own runs. The code is reproduced
by the command from the report, the log contains all mandatory fields. Borrowed code — as a list of fragments in
the report, each with a two-sentence comment in the code.

**The full assignment** — in the file: [technical specification of lab 1](/about/files/course/rl/lab1/lab1-spec.md).
