---
project: 'llm-second-brain'
version: '2.1.0'
lang: 'en'
date: '2026-09-05'
title: 'Per-slot LLM providers'
summary: 'The three slots — embeddings, summarization and the judge — got their own provider and model, a single client, a startup check, editable prompts and note titles.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v2.1.0'
---

**The gist: models are chosen separately for every slot.**

## 🧩 A provider per slot

The three external calls — embeddings, summarization, the judge — have their own provider and model. A local Ollama and a cloud API live side by side: nothing has to be bent to a single vendor.

## 🔌 A single client

One transport for every external call instead of homemade wrappers — errors, timeouts and retries are handled in one place.

## 🚦 A startup check

A lightweight request to every provider on boot: an unavailable model shows up immediately, not on the first queued job.

## ✍️ Editable prompts

The three system prompts live in files and are edited without touching code.

## 🏷 Note titles

A note got a title, mandatory for new notes. Title search grew out of it later (2.2.0).

## ⚙️ A worker loop per slot

Three independent loops instead of one: a slow slot no longer holds the others back.

## ♻️ Reindex on an embedding change

When the embedding model changes, the index is rebuilt — vectors from two different models are never silently mixed.

## 💥 Breaking changes

`OLLAMA_BASE_URL` became `EMBEDDING_BASE_URL`, and `keep_alive` was removed from request payloads.

## 🇬🇧 Documentation

A short README, `docs/INSTALL.md` and the rest of the public docs are in English.
