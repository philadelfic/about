---
# ПРОДУКТ: LLM Second Brain — единственный источник карточки на витрине и страницы продукта.
title: 'LLM Second Brain'
slug: 'llm-second-brain'
kind: 'repo'
repo: 'https://github.com/philadelfic/llm-second-brain'
status: 'в проде'
statusEn: 'in production'
stack: ['Python', 'MCP (Open WebUI, Claude Desktop и другие MCP-клиенты)', 'SQLite + sqlite-vec + FTS5', 'Ollama', 'Docker']
stackEn: ['Python', 'MCP (Open WebUI, Claude Desktop and other MCP clients)', 'SQLite + sqlite-vec + FTS5', 'Ollama', 'Docker']
order: 10
idea: 'Память для ИИ-ассистента: чтобы он помнил факты, договорённости и контекст, а не начинал каждый разговор с нуля.'
ideaEn: 'Memory for an AI assistant: so it remembers facts, agreements and context instead of starting every conversation from scratch.'
why: 'Ассистент без памяти каждый день забывает, кто вы, о чём вы договорились и как у вас принято делать дела. Приходится повторять одно и то же в каждом разговоре и заново объяснять контекст.'
whyEn: 'An assistant without memory forgets who you are, what you agreed on and how you like things done. You end up repeating yourself in every conversation and explaining the context again.'
how: 'Знания хранятся отдельно от модели: заметки, термины, факты о вас и процедуры «как делать». Ассистент сам достаёт нужное к текущей задаче, а решения и договорённости остаются между разговорами, а не исчезают вместе с чатом.'
howEn: 'Knowledge lives separately from the model: notes, terms, facts about you and “how to do things” procedures. The assistant pulls what it needs for the task at hand, and decisions stay between conversations instead of disappearing with the chat.'
links:
  - { title: 'Репозиторий', titleEn: 'Repository', href: 'https://github.com/philadelfic/llm-second-brain' }
  - { title: 'Релизы на GitHub', titleEn: 'Releases on GitHub', href: 'https://github.com/philadelfic/llm-second-brain/releases' }
  - { title: 'Как поставить: инструкция', titleEn: 'How to install', href: 'https://github.com/philadelfic/llm-second-brain/blob/main/docs/INSTALL.md' }
  - { title: 'Пост о релизе 3.2.0 в канале', titleEn: 'Post about release 3.2.0 (RU)', href: 'https://t.me/HobbyOdnogoITishnika' }
sections:
  - title: 'Модели и слоты'
    titleEn: 'Models and slots'
    items:
      - { text: 'Система не привязана к одной модели: провайдер и модель задаются отдельно для каждого слота — эмбеддинги, суммаризация, судья, решения.', textEn: 'Not tied to a single model: the provider and the model are set per slot — embeddings, summarization, judge, decisions.' }
      - { text: 'Тип модели у слота указывается явно: генеративная, эмбеддинг-модель или решающая — та, что отдаёт вместо текста вероятности.', textEn: 'The model type of a slot is explicit: generative, embedding, or decision — the one that returns probabilities instead of text.' }
      - { text: 'Если модель не умеет нужный режим, слот сам уходит на генеративный путь и работу не теряет.', textEn: 'If a model does not support the mode, the slot falls back to the generative path and never loses a job.' }
      - { text: 'На практике рядом живут разные модели: эмбеддинги — на своём сервере через Ollama, генерация и решения — через любой OpenAI-совместимый API.', textEn: 'In practice different models live side by side: embeddings on a local server via Ollama, generation and decisions through any OpenAI-compatible API.' }
      - { text: 'В журнале видно, чем закончился вызов: причина остановки ответа и «мысли», которые модель потратила на него.', textEn: 'The journal shows how a call ended: the stop reason of the answer and the thinking tokens the model spent on it.' }
---
