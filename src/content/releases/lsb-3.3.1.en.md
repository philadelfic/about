---
project: 'llm-second-brain'
version: '3.3.1'
lang: 'en'
date: '2026-10-17'
title: 'Contour hotfix: history and observability'
summary: 'A note erased for good takes its history with it; the waiting counter counts the jobs that wait; the full test run drops from 150 to 30 seconds.'
cover: 'img/projects/llm-second-brain/3.3.1.webp'
github: 'https://github.com/philadelfic/llm-second-brain/releases/tag/v3.3.1'
post: 'https://t.me/HobbyOdnogoITishnika'
---

**The main thing: two quiet bugs in the memory — and checks that run five times faster.**

## 🧹 What is gone for good is gone whole

A note can be moved to the trash, or erased for good — by hand or when its lifetime runs out. In the second case the note disappeared while its version history stayed behind. Note ids are reused, so the freed id went to the next note and that note's very first version could not be written: saving failed until the leftover rows were removed by hand. The delete and its history now go in one operation.

The trash behaves as before: it keeps the history and gives the note back together with it.

## 🕒 The queue counts its waiting honestly

Every queue has a counter for “how long the oldest job has been waiting”. It went blank exactly in the state it exists for: with the model down all the work moves to waiting, and instead of an age the counter showed nothing. The age is now computed over everything waiting to run, and disappears only when there is truly nothing left to wait for. An empty queue still invents nothing.

## ⏱ The full test run: 150 → 30 seconds

The suite of 2147 checks now runs across several workers: ~30 seconds instead of ~150 on the same machine. The set of checks was compared name by name across three runs — it is unchanged, and the sequential run stays the default. One snag surfaced on the way: test servers held fixed ports and collided with each other — a port is now handed out per worker.

## 📦 Upgrading

The data schema is unchanged and there are no migrations — upgrading is replacing the container.

A memory that tidies up after itself 🧹
