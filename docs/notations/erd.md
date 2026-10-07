# ERD – модель «сущность – связь»

<div class="lh-stats" markdown>
<div class="lh-stat"><span>Появилась</span><b>1976, П. Чен</b></div>
<div class="lh-stat"><span>Нотации</span><b>Чена, «воронья лапка», IDEF1X</b></div>
<div class="lh-stat"><span>Отвечает на вопрос</span><b>Какие данные хранить и как они связаны?</b></div>
<div class="lh-stat"><span>Сложность</span><b>средняя</b></div>
</div>

## Описание

**ERD (Entity-Relationship Diagram)** описывает **структуру данных** предметной области:
объекты (сущности), их характеристики (атрибуты) и связи между ними. Модель предложена
**П. Ченом** в 1976 году [[7]](../sources.md#src-7). Сегодня распространены нотации Чена (концептуальное
моделирование) и **«воронья лапка»** (Crow's Foot) Г. Эверета, а также IDEF1X [[12]](../sources.md#src-12) –
для логических и физических моделей баз данных.

В моделировании бизнес-процессов ERD отвечает на вопрос, **о каких объектах процесс хранит
информацию**, и служит основой для проектирования базы данных автоматизируемой системы [[20]](../sources.md#src-20).

**Когда применять:** проектирование базы данных, согласование терминов предметной области,
анализ информационных объектов процесса.

**Ограничения:** не описывает действия, последовательность и участников процесса.

## Элементы нотации

| Элемент | Нотация Чена | «Воронья лапка» | Назначение |
|---|---|---|---|
| Сущность | прямоугольник | прямоугольник со списком атрибутов | класс объектов: Клиент, Заказ |
| Атрибут | овал | строка внутри сущности | свойство сущности |
| Первичный ключ | подчёркнутый атрибут | отметка PK | уникальный идентификатор экземпляра |
| Внешний ключ | – | отметка FK | ссылка на первичный ключ другой сущности |
| Связь | ромб | линия между сущностями с глаголом | отношение между сущностями |
| Кардинальность | 1, N, M у линий | концы линии: черта – «один», «лапка» – «много», кружок – «необязательно» | сколько экземпляров участвует в связи |

## Правила составления

1. Сущности называются существительными в единственном числе.
2. У каждой сущности определяется первичный ключ.
3. Для каждой связи указываются кардинальность (1:1, 1:N, M:N) и обязательность участия.
4. Связи «многие ко многим» на логическом уровне разрешаются промежуточной сущностью.
5. Модель нормализуется (как правило, до третьей нормальной формы) – каждый факт хранится в одном месте.
6. Вычисляемые значения (например, итоговая стоимость) не дублируются без необходимости.

## Пример: данные процесса обработки заказа (нотация «воронья лапка»)

```mermaid
erDiagram
    CLIENT["Клиент"] {
        uuid id PK
        string name "наименование"
        string inn "ИНН"
    }
    ORDER["Заказ"] {
        uuid id PK
        uuid client_id FK
        string status "статус"
        date planned_delivery "плановая доставка"
        bool on_time "On Time"
        bool in_full "In Full"
    }
    CARGO["Грузовое место"] {
        uuid id PK
        uuid order_id FK
        uuid warehouse_id FK
        string cargo_type "тип груза"
        decimal weight_kg "вес, кг"
    }
    ROUTE["Рейс"] {
        uuid id PK
        uuid order_id FK
        uuid vehicle_id FK
        uuid driver_id FK
        int distance_km "расстояние, км"
    }
    DOCUMENT["Документ"] {
        uuid id PK
        uuid order_id FK
        string type "заявка, счёт, ТТН, акт"
        date created_at "дата"
    }
    VEHICLE["Транспорт"] {
        uuid id PK
        string plate "госномер"
        int capacity_kg "грузоподъёмность"
    }
    DRIVER["Водитель"] {
        uuid id PK
        string full_name "ФИО"
    }
    WAREHOUSE["Склад"] {
        uuid id PK
        string address "адрес"
    }
    CLIENT ||--o{ ORDER : "оформляет"
    ORDER ||--|{ CARGO : "включает"
    WAREHOUSE ||--o{ CARGO : "хранит"
    ORDER ||--o| ROUTE : "исполняется по"
    VEHICLE ||--o{ ROUTE : "назначается на"
    DRIVER ||--o{ ROUTE : "выполняет"
    ORDER ||--o{ DOCUMENT : "сопровождается"
```

!!! note "Что видно и чего не видно"
    ERD показывает, что один клиент оформляет много заказов, заказ включает одно или несколько
    грузовых мест и сопровождается документами, а признаки On Time и In Full хранятся в заказе.
    Как и когда эти данные появляются, по диаграмме понять нельзя.

## Ссылки

1. Chen, P. P. The Entity-Relationship Model – Toward a Unified View of Data / P. P. Chen // ACM Transactions on Database Systems. – 1976. – Vol. 1, № 1. – P. 9-36.
2. Integration Definition for Information Modeling (IDEF1X) : Federal Information Processing Standards Publication 184 / National Institute of Standards and Technology. – Gaithersburg, 1993. – URL: <https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub184.pdf> (дата обращения: 07.10.2026).
3. What Is an Entity Relationship Diagram? // Lucid : сайт. – URL: <https://www.lucidchart.com/pages/er-diagrams> (дата обращения: 07.10.2026).
4. Mermaid : diagramming and charting tool : сайт. – URL: <https://mermaid.js.org> (дата обращения: 07.10.2026).
