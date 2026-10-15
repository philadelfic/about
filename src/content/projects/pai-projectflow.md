---
# ПРОДУКТ: анонс системы ведения проектов. Версий нет — показываем, что планируется.
# Ссылок нет: проектная документация публично не показывается (решение О. 15.10.2026).
# ИМЯ: 'PAI ProjectFlow' — предложение Олега (15.10.2026), ждём подтверждения. В трекере продукт
# живёт как LLMProjectManager (префикс задач LPM), поэтому переименование стоит делать осознанно.
title: 'PAI ProjectFlow'
slug: 'pai-projectflow'
kind: 'announcement'
status: 'в активной разработке'
statusEn: 'in active development'
stack: ['Python', 'MCP', 'REST + веб-интерфейс', 'SQLite', 'Docker']
stackEn: ['Python', 'MCP', 'REST + web interface', 'SQLite', 'Docker']
order: 30
idea: 'Система ведения проектов, которой управляет ИИ-ассистент: задачи, связи, сроки и критический путь — через агента, а не мышкой в интерфейсе.'
ideaEn: 'A project-management system run by an AI assistant: tasks, links, dates and the critical path — through an agent, not by clicking around a UI.'
why: 'Планы живут в таблицах и в головах: чтобы увидеть, что от чего зависит и где горит, приходится руками сводить задачи, оценки и сроки. Отдать эту работу ассистенту нечем: у него нет ни списка задач, ни связей, ни дат — только переписка, которая забывается.'
whyEn: 'Plans live in spreadsheets and in people’s heads: seeing what depends on what, and what is on fire, takes manual work over tasks, estimates and dates. And there is nothing to hand this work to an assistant: no task list, no links, no dates — only a chat that forgets.'
how: 'Проект, задачи и связи описаны явно: у задачи есть тип, оценка, сроки, исполнитель и связи «родитель / блокирует». По ним считается критический путь, собирается Гант и видно, кто перегружен. И то же самое доступно ассистенту — он ведёт проект сам, а человек проверяет и решает.'
howEn: 'The project, its tasks and links are explicit: a task has a type, an estimate, dates, an assignee and parent/blocking links. From them the system computes the critical path, builds a Gantt chart and shows who is overloaded. The same surface is open to an assistant — it runs the project itself, while the human reviews and decides.'
roadmap:
  - { text: 'Задачи с типами: эпик, фича, задача, история, дефект и веха', textEn: 'Tasks with types: epic, feature, task, story, defect and milestone' }
  - { text: 'Связи задач и расчёт критического пути с резервами', textEn: 'Task links and critical-path calculation with reserves' }
  - { text: 'Вехи на Ганте и выгрузки: CSV, Excel и картинка', textEn: 'Milestones on the Gantt chart and exports: CSV, Excel and an image' }
  - { text: 'Занятость, подбор исполнителей и календарь проекта', textEn: 'Workload, picking assignees and the project calendar' }
  - { text: 'Веб-интерфейс: карточка задачи, лента правок, приёмка и откат', textEn: 'Web interface: task card, change feed, acceptance and rollback' }
  - { text: 'Спринты, релизы и информер «что горит»', textEn: 'Sprints, releases and the “what is burning” informer' }
links: []
---
