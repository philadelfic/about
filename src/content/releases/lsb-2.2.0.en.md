---
project: 'llm-second-brain'
version: '2.2.0'
lang: 'en'
date: '2026-09-09'
title: 'Making life easier for models'
summary: 'Notes are found by title, search and listing became one tool with modes, a note is read in chunks, and lifetimes and three-level areas appeared.'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v2.2.0'
---

**The gist: easier to find, easier to read, harder to confuse.**

## 🔎 Search by title

The note title joined the vector index (title and text are vectorized together) and the full-text index: a note is now found by its title, not only by meaning.

## 🧭 One search, one listing

Search is one tool with a mode — by meaning or by title; listing is one tool, detailed as titles only or with summaries. The area path shows up in every output, so it is clear where a record lives.

## 📖 Reading in chunks

A note can be read in full or only the needed fragment — by a semantic query or by index with continuation. Long texts stop eating the context.

## ✏️ Metadata edits and lifetimes

Title, summary and area are edited without rewriting the text, and the summary is not regenerated. A note may carry a lifetime: expired ones are removed by background cleanup.

## 🌳 Deeper areas

Area depth went from two levels to three; models create nodes themselves — with a mandatory description and an anti-synonymy check, so no twins appear.

## 🇬🇧 Model-facing texts in English

Prompts, hints and tool descriptions moved to an English canon and were rewritten for clarity.

## 🐛 Defects

Five of them: JSON parsing from “thinking” models, two flaky live tests, the E2E script after the hint translation, structure-judge non-determinism (up to three attempts) and an MCP session drop under background load (timeouts in E2E).
