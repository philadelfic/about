---
project: 'llm-second-brain'
version: '3.9.0'
lang: 'en'
date: '2026-11-15'
title: 'A slot per operation: the operation as the primary entity'
summary: 'The unit of the system is an operation, not a group of processes: each of the ten processes has its own model, pause, breaker and answer contract; a failure of one no longer silences its neighbours, and split and merge understand free text instead of JSON.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v3.9.0'
post: 'https://t.me/HobbyOdnogoITishnika'
---

**The main thing: the unit of the system is an operation, not a group of processes.**

The model used to be configured by slot - a group of processes: summarization, judge, embedding, decisions. A group shared one pause, one safeguard and one job queue. The price: when merge stumbled, the whole summarization stalled together with the headings and the summaries.

## 🧩 An operation instead of a slot

There are ten processes: summarization, headings, merge, split, classification, node description, the dedup judge, the structure judge, embedding, decisions. Each has its own model, timeout, pause, backoff, failure counter and its own set of environment variables - `SUMMARIZE_*`, `MERGE_*`, `EMBED_*`, `DECISION_*` and so on. The operation registry became the single source of truth: names, answer contracts, pause thresholds. Switching between the old and the new order is one flag, the rollback is the reverse switch.

## 🛡️ A failure of one operation does not silence its neighbours

The breaker, the pause and the failure counter are keyed by the operation name. Merge slows down - headings, summaries and embeddings keep going. An unavailable decision maker stops only the processes whose path goes through it. Merge, split and headings got their own queues, each with its own events and its own gate.

## ✍️ The answer contract is the code's business, not the model's

Split and merge take free text with a delimiter instead of JSON: the model used to be expected to return strict JSON while it wrote prose, and a pair of notes went to the back of the queue with a failure. A part shorter than the code threshold is not written and the call is repeated: the crumb parts are gone. The heading of every split part is a separate call, and it is counted toward the split, not toward the headings.

## 🧭 Every process is visible

The health panel returns a snapshot per operation, while the four old keys stay as aggregates so nothing that reads them breaks. Two fields are new: the mode of the slot layer and how many jobs still wait to move to the new scheme.

## 🔁 Migration and the embedding model

The slot values in the job queue move to operation names - idempotently, with a journal and without losing hanging jobs: an unknown combination is not dropped but marked for attention. The embedding model is now tracked per operation: a model change no longer passes the automatic reindex, the backup check and the manual reindex by.

## ➕ Also in the release

- a warning about the old environment names: the service does not fail, it names the equivalent new ones;
- the acceptance hooks take operation names, the old names answer with a hint;
- the false red of the "age of the oldest task" scenario is gone;
- 22 tasks and 14 steps, a full run of 2756 tests with zero failures; acceptance on the test contour: 176 checks green, two failures, both pre-existing.

## 📦 Upgrade

The database schema does not change and the data is untouched: the queue values are migrated in the new mode only. The previous mode keeps working as it did; the switch is one flag, the rollback is the reverse. The new environment names repeat the values of the slot groups; the old names stop working in 3.10.0.

Ten processes in order instead of four groups 🧠✨
