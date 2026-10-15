---
project: 'llm-second-brain'
version: '3.2.0'
lang: 'en'
date: '2026-10-13'
title: 'Hygiene, contour and slots'
summary: 'Version history with rollback, an assistant log, warnings, a decision slot, and “as much as fits” instead of a fixed cap.'
cover: 'img/projects/llm-second-brain/3.2.0.webp'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v3.2.0'
post: 'https://t.me/HobbyOdnogoITishnika'
---

**The main thing: the memory can now be checked and rolled back.**

## 🗂 Version history

Every change — a note, a skill, a term, a fact about you — is kept as a version. For long texts you can see line by line what actually changed. Any version can be rolled back, and the rollback becomes a new version itself: history is never rewritten. The assistant can look into the history and answer why something became what it is.

## 📓 Assistant log (LOGS)

A new area of the memory: the assistant records what it did and why — what it changed, with what result, what it verified. Not notes and not tasks, but a separate layer of “why it turned out this way”.

## 🔍 Warnings

If a note looks like it belongs elsewhere, the system does not silently shuffle the memory: it opens a warning and waits for a decision.

## 🧩 Skills, terms and facts about you (SKILLS / TERMS / USER)

Each area can be switched on and off separately — the data itself stays in place.

## 🔗 Terms

The contexts of one term are brought to a single form: matching ones merge, different ones honestly stay different.

## 🧠 Slots: “broken” is not “thinking”

A slow model and a failed call used to look the same. Now a slot tells a failure from an auth refusal, an empty answer and a truncated one, pauses and makes a cheap probe instead of knocking on a closed door. Jobs wait with a growing back-off instead of spinning idle.

## ⚖️ Decision slot

A separate slot type: the model returns probabilities instead of text. Deduplication and picking a home for a note run on it — faster, cheaper, with no redundant calls. When there is nothing to choose from, the call is not made at all.

## 🧩 Different model types

Slots no longer sort models into “good” and “bad”: the type is explicit — generative, embedding, or decision, the one that returns probabilities instead of text. The provider and the model are chosen per slot, so local embeddings and cloud generation live side by side. If a model does not support the mode, the slot falls back to the generative path and never loses a job, and an inconsistent configuration is flagged with a startup warning. The journal now shows the stop reason of an answer and the thinking tokens the model spent.

## 💾 A memory that is easier to keep

- at save time — a hint about which area the note fits;
- you can ask “what changed after this date”;
- a “similar notes” hint without a model call;
- a note now has a comment: it never leaks into the note text or the semantic search, but comments have their own search;
- a note with a lifetime is no longer merged with others.

## 📦 Backups and the contour

The “contour” is the whole running system: the service itself, the database, background jobs and the model slots. Every snapshot is verified by opening it: a bad one is marked and never silently deleted. A verified copy can be shipped off the box. One call reports the state of the whole contour: what is alive, what is queued, what needs attention.

## ✂️ Less text for the agent

The text the server injects into the agent at connection time is shorter and now measured: instructions 640 → 525 tokens, descriptions of 31 tools 2702 → 2170 (−19.7%).

## 🐛 Small fixes

Empty answers of “thinking” models are fixed (no longer confused with a breakdown), and the idle loop of the terms background job is gone. Skill form limits were raised — real procedures finally fit.

A memory you can check and roll back 🧠
