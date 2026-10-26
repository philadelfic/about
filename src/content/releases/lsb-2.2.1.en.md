---
project: 'llm-second-brain'
version: '2.2.1'
lang: 'en'
date: '2026-09-10'
title: 'Patch: upgrade break'
summary: 'A one-defect patch: upgrading from 2.1.x no longer ends in a restart loop because of old prompt files.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v2.2.1'
---

**The gist: upgrading from 2.1.x stopped breaking on prompts.**

## 🧩 Auto-migration of prompt seeds

After an upgrade the old prompt files did not match the new registry: the service failed on start and went into a restart loop. The registry now migrates files you have not edited by hand on its own — no manual step before the upgrade.

## 💬 A hint instead of a bare FATAL

The configuration error for the judge system prompt now says what to do, not just “FATAL”.

## 📌 Upgrade note

Prompt files you never touched need no attention: the migration handles them.
