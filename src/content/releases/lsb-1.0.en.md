---
project: 'llm-second-brain'
version: '1.0'
lang: 'en'
date: '2026-09-02'
title: 'First release'
summary: 'A working release: a long-term memory service in one container — notes, search by meaning and by words, MCP tools and local embeddings.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v1.0'
---

**The gist: the assistant got memory that lives outside the chat.**

## 🧠 What it does

- notes: save, search, read, update, delete — through MCP;
- search by meaning (vector) and by words (full-text);
- embeddings computed locally through Ollama, no cloud;
- storage is one SQLite database next to the service, no external infrastructure;
- one container: download, run, connect to the assistant.

## 🎯 The search threshold is calibrated

The cut-off went from 0.35 to 0.50 following an experiment on 82 real queries: hits nobody would open stopped making it into the results.

## 📌 What comes next

Memory areas are still flat. A tree of areas arrives in 2.0.
