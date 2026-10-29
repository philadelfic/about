---
project: 'llm-second-brain'
version: '3.4.1'
lang: 'en'
date: '2026-10-29'
title: 'One number for the note limit, a background that degrades politely'
summary: 'The note limit is one configuration value and the database moves itself; searches and listings return headers instead of full texts; merging without truncation; the background stops grinding through a broken provider and loses nothing.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v3.4.1'
post: 'https://t.me/HobbyOdnogoITishnika'
---

**The main thing: the note limit is one number, reading is headers first, and the background stops grinding through a broken provider.**

## 🧩 The note limit is one number

`MAX_NOTE_CHARS` (default 2000) feeds everything at once: save/update validation, merge and split part limits, hints, tool descriptions and `/health`. Change the limit and a live database moves by itself: upward as a 1:1 pour with no model calls at all, downward as a careful split. No limit constants are left in the code.

## 🔎 Reading got cheaper

`memory_search` and `memory_list` return headers capped by a character budget by default; full text is read point-wise — `memory_get` by id, up to eight records per call. A single id (and chunk mode) still returns the whole text. Elements that do not fit the budget degrade to a header marked `truncated` — the extra text never arrives.

## ✂️ Merging without loss

Merging returns self-contained parts with titles of their own and checks completeness strictly: one retry in the same context, and if the parts still do not add up the pair is deferred with both notes alive. Silent truncation of long notes is gone. The default limit of 2000 keeps ordinary notes whole: the “one note, one cluster of facts” band holds.

## 🛡️ The background degrades politely

When a model is unavailable, background jobs abandon the batch after the first failure instead of grinding through up to 32 positions of 900-second timeouts for hours. Processed positions count, the tail stays in the queue and drains when the slot returns — nothing is lost. The gate is now shared by every job of a slot, external ones included; work moves to `waiting` honestly, and `/health` shows what exactly is waiting and why. A freshly saved note no longer waits up to 15 minutes for vectorization while models are healthy: the embedding job rechecks its queue before going to sleep.

## ➕ Also in the release

- saving an array: `memory_save` takes up to 20 notes per call with per-element validation;
- ranking boosts: exact title match, 30-day freshness, linked notes;
- an operations registry: nine operations with their own env overrides, visible in `/health.operations` without addresses or keys;
- a repeated migration no longer deletes the chain base holding the only copy of split parts, and migration progress is visible in `/health` per call and phase;
- comment search without ghosts of deleted notes;
- a live integration tier: 13 checks against real models, host addresses never enter the repository.

## 📦 Upgrading

The note limit is governed by one env, `MAX_NOTE_CHARS` (default 2000): over an existing database a higher value pours 1:1 in minutes with no model work, a lower value splits notes. New optional envs: `MIGRATION_BATCH` (5) and `MIGRATION_PAUSE_SEC` (600 seconds). If you relied on full texts in list responses — switch to point-wise reads by id or pass an explicit budget.

On GitHub, 3.4.0 and 3.4.1 ship as one release — the link holds the full notes of both versions.

Remembers more, stays politely quiet 🧠✨
