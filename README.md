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
| DFD | потоки и хранилища данных | диаграмма уровня 1 (Mermaid) |
| RAD | роли и их взаимодействия | клиент – менеджер – склад (SVG) |
| IDEF0 | функции, управление, механизмы | декомпозиция A0 (SVG) |
| ERD | структура данных | модель «воронья лапка» (Mermaid) |
| UML | программная система | последовательность, состояния, классы (Mermaid) |
| BPMN | сквозной бизнес-процесс | модель bpmn-js |

## Запуск

```bash
pip install -r requirements.txt
mkdocs serve   # http://127.0.0.1:8000
```

## Автор

Попов А.С., группа 5ИТб-2, ФГБОУ ВО «КнАГУ» · [@starpxand](https://github.com/starpxand) · лицензия MIT
