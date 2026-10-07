<div align="center">

# 🗺️ Нотации моделирования бизнес-процессов

**Мини-wiki: Flow Chart · DFD · RAD · IDEF · ERD · UML · BPMN – описание, элементы, правила и пример на одном процессе**

[![Deploy](https://github.com/starpxand/bpm-notations-wiki/actions/workflows/deploy.yml/badge.svg)](https://github.com/starpxand/bpm-notations-wiki/actions/workflows/deploy.yml)
[![Docs](https://img.shields.io/badge/docs-MkDocs%20Material-0b1b3f)](https://starpxand.github.io/bpm-notations-wiki/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Открыть wiki](https://starpxand.github.io/bpm-notations-wiki/)

</div>

## О проекте

Проектное задание по дисциплине «Современные программные средства». Для каждой нотации:
краткое описание, таблица элементов, правила составления, пример и ссылки на источники.
Все примеры построены на одном процессе – обработке заказа на перевозку в учебной
платформе [«ЛогиХаб»](https://starpxand.github.io/logihub-wiki/), – поэтому нотации легко
сравнить между собой.

| Нотация | Что показывает | Пример |
|---|---|---|
| Flow Chart | порядок шагов и решения | блок-схема обработки заявки (Mermaid) |
| DFD | потоки и хранилища данных | контекстная диаграмма и диаграмма уровня 1, нотация Гейна – Сарсона (SVG) |
| RAD | роли и их взаимодействия | клиент – менеджер – склад: выбор, итерация, параллельность (SVG) |
| IDEF | функции, управление, механизмы; сценарии | IDEF0 A-0 и A0, IDEF3 (SVG) |
| ERD | структура данных | модель «воронья лапка» (Mermaid) |
| UML | программная система | деятельность (SVG), последовательность, состояния, классы (Mermaid) |
| BPMN | сквозной бизнес-процесс | интерактивная модель bpmn-js с проходом по шагам |

Сайт динамический: диаграммы появляются с анимацией, открываются во весь экран с масштабом,
BPMN-модель можно пройти по шагам, на странице сравнения – интерактивный подбор нотации.
Источники оформлены по ГОСТ Р 7.0.100-2018.

## Запуск

```bash
pip install -r requirements.txt
python tools/build_diagrams.py   # пересобрать SVG-диаграммы
mkdocs serve                     # http://127.0.0.1:8000
```

## Структура

```text
docs/                  страницы wiki (Markdown)
docs/assets/fx.js      динамика: Mermaid, полноэкранный просмотр, bpmn-js, анимации
docs/assets/img/       SVG-диаграммы
tools/                 генератор SVG-диаграмм (DFD, RAD, IDEF0, IDEF3, UML)
overrides/home.html    главная страница
```

## Автор

Попов А.С., группа 5ИТб-2, ФГБОУ ВО «КнАГУ» · [@starpxand](https://github.com/starpxand) · лицензия MIT
