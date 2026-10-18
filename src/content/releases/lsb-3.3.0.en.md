---
project: 'llm-second-brain'
version: '3.3.0'
lang: 'en'
date: '2026-10-16'
title: 'Job contour reliability'
summary: 'The first start over a database of a previous version no longer races its own job-table migration; the behaviour of a queue behind an unavailable model is pinned by a test.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v3.3.0'
---

**The gist: a start after an upgrade no longer argues with itself.**

## 🔁 A migration race on the first start

The job table migrates lazily, on first use. The “table is ready” flag was checked without a lock, and nothing guarded the window between inspecting the columns and `ALTER TABLE`: the judge and namespace loops both saw a missing column, both ran the change, and the second one failed with “duplicate column name” — taking the startup attention reset down with it. Found on the production deploy of 3.2.0 (2026-10-13). The whole block now runs under a lock with a double-checked flag, and a repeated schema change is tolerated: the lock covers the threads of one process only, a competing process is not its business. Regression test: two threads on a database without the attention columns — no exceptions, the schema comes out complete, the reset goes through.

## 🧪 A queue behind an unavailable model — verified, not assumed

With the slot down the work moves to waiting (nothing pending), nothing is lost and the counters stay honest; when the slot answers, the queue drains. The behaviour was correct before, but it rested on trust: a test now pins both a transient refusal and an auth break, draining in batches. No product code changed — the release makes the existing behaviour provable.

## 🏷 Small things

The version in `/health` matches the release tag.
