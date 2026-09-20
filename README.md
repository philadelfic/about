# Портал Олега Орловского

Личный портал: коротко о себе, живая информация о проектах, статьи и материалы для студентов.
Живёт на GitHub Pages: https://philadelfic.github.io/about/

## Стек

- [Astro](https://astro.build) — статический сайт, контент в markdown
- GitHub Actions — сборка и деплой на GitHub Pages

## Локальная разработка

```bash
npm install
npm run dev       # http://localhost:4321/about/
npm run build     # сборка в dist/
npm run preview   # предпросмотр собранного сайта
```

## Ветки и деплой

| Ветка | Что происходит |
|---|---|
| `dev` | разработка; CI собирает проект, деплоя нет |
| `test` | мерж из `dev`, полная проверка (сборка, ссылки, Lighthouse) |
| `main` | прод: сборка и деплой на GitHub Pages по push |

Push в `main` = выложено.

## Структура

```
src/
  pages/        # страницы сайта (главная, обо мне, разделы)
  layouts/      # общий каркас страницы
  styles/       # общие стили
  data/site.ts  # контакты и внешние ссылки
```

Ветка `dev` — рабочая. Всё, что не описано здесь, — в спеке: Outline «My projects» → «Портал — концепция и дизайн».
