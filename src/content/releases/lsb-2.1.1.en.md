---
project: 'llm-second-brain'
version: '2.1.1'
lang: 'en'
date: '2026-09-05'
title: 'Background pipeline restart and hardening'
summary: 'The pipeline fully restarts after an edit; a code audit produced 13 refactor pools, 828 tests and a save into a large area at 0.34 s instead of 4–12.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v2.1.1'
---

**The gist: background processing restarts as a whole, and reliability is fixed by audit.**

## 🔄 Full restart after an edit

Classification marks are reset in the same record update: rewritten notes are classified again and may move again, and stale hints stop feeding the area-promotion trigger.

## 🛠 Worker reliability

Vector writes are guarded against a mid-flight edit; unexpected errors no longer kill background loops (supervisor and lost-wakeup fixes); grooming, moves and duplicate merges are atomic; the job queue got indexes and a seven-day retention.

## ✅ Correctness

Literal dedup runs inside the save transaction — no more “between check and write” duplicates; an edit drops the stale full-text vector; a namespace rename race returns 409 instead of 500.

## ⚡ Performance

Dedup query plans were fixed under an area filter: at 50,000 notes a save into a large area took 4–12+ seconds, now p95 is about 0.34 s.

## 🔐 Security and logging

Token comparison is safe on non-ASCII headers (401 instead of 500), query strings in the access log are truncated to 80 characters, and failed tool calls show up in the log with their latency.

## 🧪 Tests

828 tests (up from 790); a full run on live slots — 13 integration tests, no skips — plus E2E on the test container with zero errors.
