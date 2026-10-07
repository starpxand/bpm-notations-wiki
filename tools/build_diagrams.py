"""Генератор SVG-диаграмм wiki: DFD (Гейн – Сарсон), IDEF0 (A-0 и A0), IDEF3, RAD, UML-деятельность.

Запуск: python tools/build_diagrams.py  →  docs/assets/img/*.svg
"""
from __future__ import annotations

from pathlib import Path

from svgkit import AMBER, BLUE, INK, MUTED, NAVY, ORANGE, PAPER, SOFT, Svg

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "img"


# =====================================================================
# DFD – нотация Гейна – Сарсона
# =====================================================================
def dfd_entity(s, x, y, w, h, name, dup=False):
    s.rect(x + 6, y + 6, w, h, fill="#c9d3ea", stroke="none", sw=0, cls="n")
    s.rect(x, y, w, h, fill=SOFT, stroke=NAVY, sw=2)
    if dup:  # дубликат внешней сущности – косая черта в левом нижнем углу
        s.line(x, y + h - 14, x + 14, y + h, sw=2, cls="n")
    s.text(x + w / 2, y + h / 2, name, size=15, weight=700, anchor="middle", fill=NAVY)


def dfd_process(s, x, y, w, h, num, name):
    s.rect(x, y, w, h, rx=12, fill=PAPER, stroke=NAVY, sw=2.2)
    s.line(x, y + 28, x + w, y + 28, sw=1.6, cls="n")
    s.text(x + w / 2, y + 15, num, size=13, weight=700, anchor="middle", fill=BLUE)
    s.text(x + w / 2, y + 28 + (h - 28) / 2, name, size=14, weight=600, anchor="middle")


def dfd_store(s, x, y, w, h, sid, name):
    s.add(f'<path class="n" d="M{x + w},{y} L{x},{y} L{x},{y + h} L{x + w},{y + h}" fill="{SOFT}" '
          f'stroke="{NAVY}" stroke-width="2"/>')
    s.line(x + 46, y, x + 46, y + h, sw=1.6, cls="n")
    s.text(x + 23, y + h / 2, sid, size=13, weight=700, anchor="middle", fill=BLUE)
    s.text(x + 58, y + h / 2, name, size=14, weight=600)


def flow(s, pts, text=None, at=None, anchor="middle"):
    s.path(pts, stroke=NAVY, sw=1.8, cls="e flow", packet=True)
    if text:
        s.label(*at, text, anchor=anchor)


def dfd_context():
    s = Svg("dfd0", 1120, 340, "DFD – контекстная диаграмма процесса обработки заказа")
    dfd_entity(s, 40, 60, 190, 210, "Клиент")
    dfd_process(s, 455, 50, 230, 230, "0", "Обработка заказа\nна перевозку\n«ЛогиХаб»")
    dfd_entity(s, 900, 105, 180, 120, "Перевозчик")
    rows = [(85, "Заявка", True), (125, "Платёж", True), (165, "Акт приёмки", True),
            (205, "Договор-счёт", False), (245, "Уведомления о статусе", False)]
    for y, t, to_proc in rows:
        pts = [(230, y), (455, y)] if to_proc else [(455, y), (230, y)]
        flow(s, pts, t, (342, y - 13))
    flow(s, [(685, 135), (900, 135)], "Маршрутный лист", (792, 122))
    flow(s, [(900, 195), (685, 195)], "Статус доставки", (792, 182))
    s.text(560, 318, "Входы и выходы процесса 0 = внешние потоки диаграммы уровня 1 (балансировка)",
           size=12.5, anchor="middle", fill=MUTED, italic=True)
    return s


def dfd_level1():
    s = Svg("dfd1", 1300, 820, "DFD уровня 1 – обработка заказа на перевозку (нотация Гейна – Сарсона)")
    W, H = 195, 100
    dfd_entity(s, 30, 300, 150, 74, "Клиент")
    dfd_process(s, 250, 60, W, H, "1", "Принять и\nпроверить заявку")
    dfd_process(s, 250, 530, W, H, "2", "Рассчитать стоимость\nи выставить счёт")
    dfd_store(s, 520, 315, 210, 44, "D1", "Заказы")
    dfd_store(s, 520, 588, 210, 44, "D2", "Тарифы")
    dfd_process(s, 820, 60, W, H, "3", "Скомплектовать\nгруз")
    dfd_store(s, 1080, 88, 200, 44, "D3", "Остатки склада")
    dfd_process(s, 820, 530, W, H, "4", "Организовать\nдоставку")
    dfd_entity(s, 1115, 532, 150, 74, "Перевозчик")
    dfd_process(s, 820, 690, W, H, "5", "Закрыть заказ\nи рассчитать OTIF")
    dfd_entity(s, 1115, 703, 150, 74, "Клиент", dup=True)

    flow(s, [(105, 300), (105, 110), (250, 110)], "Заявка", (160, 97))
    flow(s, [(90, 374), (90, 560), (250, 560)], "Платёж", (165, 547))
    flow(s, [(250, 605), (135, 605), (135, 374)], "Договор-счёт", (192, 620))
    flow(s, [(445, 110), (625, 110), (625, 315)], "Проверенная заявка", (535, 97))
    flow(s, [(565, 359), (565, 555), (445, 555)], "Параметры груза", (505, 455), anchor="middle")
    flow(s, [(520, 610), (445, 610)], "Ставки", (482, 625))
    flow(s, [(730, 330), (775, 330), (775, 110), (820, 110)], "Заказ к сборке", (775, 220))
    flow(s, [(1080, 110), (1015, 110)], "Наличие", (1047, 97))
    flow(s, [(917, 160), (917, 530)], "ТТН", (917, 345))
    flow(s, [(1015, 555), (1115, 555)], "Маршрутный\nлист", (1065, 528))
    flow(s, [(1115, 590), (1015, 590)], "Статус\nдоставки", (1065, 612))
    flow(s, [(917, 630), (917, 690)], "Факт доставки", (905, 668), anchor="end")
    flow(s, [(1115, 750), (1015, 750)], "Акт приёмки", (1065, 735))
    flow(s, [(990, 630), (990, 652), (1190, 652), (1190, 703)], "Уведомления", (1190, 668))
    flow(s, [(820, 740), (750, 740), (750, 350), (730, 350)], "On Time / In Full", (750, 520))
    return s


# =====================================================================
# IDEF0
# =====================================================================
def idef_frame(s, node, title, number):
    """Рамка IDEF0 с полями УЗЕЛ / НАЗВАНИЕ / НОМЕР."""
    y = s.h - 58
    s.rect(10, 10, s.w - 20, s.h - 20, fill="none", stroke=NAVY, sw=1.4, cls="n")
    s.line(10, y, s.w - 10, y, sw=1.4, cls="n")
    s.line(150, y, 150, s.h - 10, sw=1.4, cls="n")
    s.line(s.w - 150, y, s.w - 150, s.h - 10, sw=1.4, cls="n")
    for x, cap, val in ((22, "УЗЕЛ:", node), (162, "НАЗВАНИЕ:", title), (s.w - 138, "НОМЕР:", number)):
        s.text(x, y + 16, cap, size=10.5, weight=700, fill=MUTED)
        s.text(x, y + 36, val, size=14, weight=700, fill=NAVY)


def idef_block(s, x, y, w, h, name, num):
    s.rect(x, y, w, h, fill=PAPER, stroke=NAVY, sw=2.4)
    s.text(x + w / 2, y + h / 2, name, size=15, weight=700, anchor="middle", fill=NAVY)
    s.text(x + w - 8, y + h - 11, num, size=12, weight=700, anchor="end", fill=MUTED)


def idef0_context():
    s = Svg("idefc", 1100, 560, "IDEF0 – контекстная диаграмма A-0 «Обработать заказ на перевозку»")
    x, y, w, h = 350, 200, 400, 130
    idef_block(s, x, y, w, h, "Обработать заказ\nна перевозку", "A0")
    s.path([(60, 265), (x, 265)], sw=2)
    s.label(170, 250, "Заявка клиента", anchor="middle")
    for cx, t in ((400, "Регламент\nприёма заявок"), (500, "Тарифы,\nдоговор"), (600, "Правила\nкомплектации"),
                  (700, "Окна\nдоставки")):
        s.path([(cx, 130), (cx, y)], stroke=BLUE, sw=2)
        s.text(cx, 108, t, size=12.5, anchor="middle", fill=BLUE)
    s.path([(x + w, 240), (1040, 240)], sw=2)
    s.label(870, 226, "Договор-счёт клиенту")
    s.path([(x + w, 290), (1040, 290)], sw=2)
    s.label(870, 276, "Выполненный заказ, акт, OTIF")
    s.path([(550, 450), (550, y + h)], stroke=ORANGE, sw=2)
    s.text(550, 468, "Менеджер, кладовщик, водитель; сервисы платформы «ЛогиХаб»", size=12.5,
           anchor="middle", fill=AMBER)
    s.text(30, 32, "Цель: показать функции обработки заказа, их входы, результаты, правила и ресурсы", size=12.5,
           fill=INK)
    s.text(30, 52, "Точка зрения: руководитель логистической службы", size=12.5, fill=INK)
    idef_frame(s, "A-0", "Обработать заказ на перевозку", "1")
    return s


def idef0_a0():
    s = Svg("idef0", 1240, 720, "IDEF0 – декомпозиция A0 «Обработать заказ на перевозку»")
    W, H = 200, 84
    B = [(170, 110), (420, 225), (680, 340), (930, 455)]
    names = ["Принять и\nпроверить заявку", "Рассчитать\nи выставить счёт", "Скомплектовать\nи отгрузить груз",
             "Доставить\nи закрыть заказ"]
    for i, ((x, y), n) in enumerate(zip(B, names), 1):
        idef_block(s, x, y, W, H, n, f"A{i}")
    top, bottom = 60, 610
    # управление (сверху)
    ctrl = ["Регламент приёма заявок", "Тарифы, договор", "Правила комплектации", "Окна доставки"]
    for (x, y), t in zip(B, ctrl):
        s.path([(x + 100, top), (x + 100, y)], stroke=BLUE, sw=2)
        s.text(x + 108, top + 4, t, size=12.5, fill=BLUE)
    # механизмы (снизу)
    mech = ["Менеджер, сервис «Заказы»", "Сервис расчёта", "Кладовщик, сканер", "Водитель, «Трекинг»"]
    for (x, y), t in zip(B, mech):
        s.path([(x + 100, bottom), (x + 100, y + H)], stroke=ORANGE, sw=2)
        s.text(x + 108, bottom - 6, t, size=12.5, fill=AMBER)
    # вход
    s.path([(25, 152), (170, 152)], sw=2)
    s.label(95, 138, "Заявка клиента")
    # выходы → входы следующих блоков
    s.path([(370, 135), (395, 135), (395, 250), (420, 250)], sw=2)
    s.label(376, 120, "Проверенная заявка", anchor="start")
    s.path([(620, 250), (650, 250), (650, 365), (680, 365)], sw=2)
    s.label(654, 300, "Оплаченный\nзаказ", anchor="start")
    s.path([(880, 365), (905, 365), (905, 480), (930, 480)], sw=2)
    s.label(909, 415, "Груз, ТТН", anchor="start")
    # выходы на границу (с мостиками над стрелками управления)
    s.path([(620, 285), (1215, 285)], sw=2, bridges=[(780, 285), (1030, 285)])
    s.label(1120, 271, "Договор-счёт клиенту")
    s.path([(1130, 497), (1215, 497)], sw=2)
    s.label(1173, 532, "Выполненный\nзаказ, акт,\nOTIF")
    idef_frame(s, "A0", "Обработать заказ на перевозку", "2")
    return s


# =====================================================================
# IDEF3
# =====================================================================
def uob(s, x, y, w, h, name, num):
    s.rect(x, y, w, h, fill=PAPER, stroke=NAVY, sw=2.2)
    s.line(x, y + h - 22, x + w, y + h - 22, sw=1.4, cls="n")
    s.line(x + 34, y + h - 22, x + 34, y + h, sw=1.4, cls="n")
    s.text(x + w / 2, y + (h - 22) / 2, name, size=14, weight=700, anchor="middle", fill=NAVY)
    s.text(x + 17, y + h - 11, str(num), size=12, weight=700, anchor="middle", fill=BLUE)


def junction(s, x, y, kind, num, h=200):
    s.rect(x, y - h / 2, 30, h, fill=SOFT, stroke=NAVY, sw=2.2)
    s.text(x + 15, y, kind, size=19, weight=800, anchor="middle", fill=ORANGE)
    s.text(x + 15, y + h / 2 + 14, f"J{num}", size=12, weight=700, anchor="middle", fill=MUTED)


def idef3():
    s = Svg("idef3", 1300, 380, "IDEF3 – сценарий «от оплаты до закрытия заказа»")
    W, H = 150, 72
    cy, up, dn = 190, 115, 265
    uob(s, 20, cy - H / 2, W, H, "Получить\nоплату", 1)
    junction(s, 200, cy, "&", 1)
    uob(s, 255, up - H / 2, W, H, "Скомплектовать\nгруз", 2)
    uob(s, 255, dn - H / 2, W, H, "Оформить\nТТН", 3)
    junction(s, 435, cy, "&", 2)
    uob(s, 490, cy - H / 2, W, H, "Доставить\nгруз", 4)
    junction(s, 670, cy, "X", 3)
    uob(s, 725, up - H / 2, W, H, "Подписать\nакт приёмки", 5)
    uob(s, 725, dn - H / 2, W, H, "Рассмотреть\nпретензию", 6)
    junction(s, 905, cy, "X", 4)
    uob(s, 960, cy - H / 2, W, H, "Закрыть заказ,\nпересчитать OTIF", 7)
    a = dict(sw=2)
    s.path([(170, cy), (200, cy)], **a)
    for (x1, x2), ys in (((230, 255), (up, dn)), ((705, 725), (up, dn))):
        for yy in ys:
            s.path([(x1, yy), (x2, yy)], **a)
    for (x1, x2), ys in (((405, 435), (up, dn)), ((875, 905), (up, dn))):
        for yy in ys:
            s.path([(x1, yy), (x2, yy)], **a)
    s.path([(465, cy), (490, cy)], **a)
    s.path([(640, cy), (670, cy)], **a)
    s.path([(935, cy), (960, cy)], **a)
    s.label(800, up - 50, "нет замечаний", italic=True, fill=AMBER)
    s.label(800, dn + 52, "есть замечания", italic=True, fill=AMBER)
    # объект и пояснение к перекрёсткам
    s.rect(1140, 60, 145, 260, rx=10, fill=SOFT, stroke="#d5dceb", sw=1, cls="n")
    s.text(1152, 82, "Обозначения", size=13, weight=800, fill=NAVY)
    for i, (k, t) in enumerate((("&", "И – все ветви"), ("X", "исключающее\nИЛИ – одна"), ("O", "ИЛИ – одна\nили несколько"))):
        yy = 115 + i * 62
        s.rect(1152, yy - 18, 22, 36, fill=PAPER, stroke=NAVY, sw=1.6, cls="n")
        s.text(1163, yy, k, size=14, weight=800, anchor="middle", fill=ORANGE)
        s.text(1182, yy, t, size=11.5, fill=INK)
    s.text(1152, 300, "1 … 7 – номера UOB", size=11.5, fill=MUTED)
    return s


# =====================================================================
# RAD
# =====================================================================
def rad():
    s = Svg("rad", 1290, 960, "RAD – согласование заказа клиентом, менеджером и складом")
    lanes = [(20, 340, "Клиент"), (360, 860, "Менеджер по логистике"), (880, 1270, "Склад")]
    for x1, x2, t in lanes:
        s.rect(x1, 20, x2 - x1, 920, rx=22, fill=SOFT, stroke=NAVY, sw=2, cls="n")
        s.text((x1 + x2) / 2, 52, t, size=18, weight=800, anchor="middle", fill=NAVY)
    C, M, L, R, S = 110, 560, 490, 680, 1080

    def thread(x, y1, y2):
        s.line(x, y1, x, y2, sw=2.4, cls="e")

    def act(x, y, t, side=1):
        s.rect(x - 10, y - 10, 20, 20, fill=NAVY, stroke=NAVY, sw=1)
        s.text(x + 18 * side, y, t, size=13.5, anchor="start" if side > 0 else "end")

    def inter(xs, y, t, at):
        s.line(min(xs), y, max(xs), y, stroke=BLUE, sw=2, cls="e")
        for x in xs:
            s.rect(x - 10, y - 10, 20, 20, fill=PAPER, stroke=NAVY, sw=2)
        s.label(*at, t, size=13)

    def tri(x, y, down=True):
        pts = [(x - 12, y - 10), (x + 12, y - 10), (x, y + 10)] if down else [(x - 12, y + 10), (x + 12, y + 10), (x, y - 10)]
        s.poly(pts, fill=PAPER, stroke=NAVY, sw=2)

    # клиент
    thread(C, 85, 900)
    act(C, 130, "Оформить заявку")
    inter([C, M], 200, "Передать заявку", (330, 187))
    inter([C, L], 420, "Запросить и получить уточнение", (260, 407))
    inter([C, R], 560, "Выставить счёт", (400, 547))
    act(C, 620, "Оплатить счёт")
    act(C, 870, "Принять груз")
    # менеджер
    thread(M, 85, 300)
    act(M, 260, "Проверить заявку")
    tri(M, 312)
    s.line(L, 330, R, 330, sw=2.4, cls="e")
    for x in (L, R):
        thread(x, 330, 342)
        tri(x, 352)
    s.label(L - 18, 352, "заявка неполная", italic=True, fill=AMBER, size=13, anchor="end")
    s.label(R + 18, 352, "заявка корректна", italic=True, fill=AMBER, size=13, anchor="start")
    thread(L, 362, 460)
    # итерация: возврат к проверке
    s.path([(L, 460), (L, 480), (385, 480), (385, 236), (M - 4, 236)], stroke=ORANGE, sw=2, dash="6 5",
           bridges=[(385, 420)])
    s.label(395, 500, "повторная проверка", italic=True, fill=AMBER, size=12.5, anchor="start")
    thread(R, 362, 900)
    act(R, 440, "Рассчитать стоимость")
    act(R, 495, "Сформировать\nдоговор-счёт")
    act(R, 615, "Подтвердить оплату")
    inter([R, S], 690, "Передать заказ на склад", (870, 677))
    # склад: параллельность (part refinement)
    thread(S, 85, 690)
    s.text(S + 12, 150, "ожидание заказа", size=12.5, fill=MUTED, italic=True)
    thread(S, 690, 728)
    tri(S, 738, down=False)
    thread(S, 748, 758)
    s.line(1010, 758, 1150, 758, sw=2.4, cls="e")
    for x in (1010, 1150):
        thread(x, 758, 845)
        tri(x, 772, down=False)
    act(1010, 810, "Скомплектовать\nгруз", side=-1)
    act(1150, 810, "Оформить\nТТН", side=1)
    s.line(1010, 845, 1150, 845, sw=2.4, cls="e")
    thread(S, 845, 900)
    act(S, 880, "Передать груз\nк отгрузке")
    return s


# =====================================================================
# UML – диаграмма деятельности
# =====================================================================
def uml_activity():
    s = Svg("umla", 1000, 960, "UML – диаграмма деятельности «Обработка заказа» с разделами")
    lanes = [(10, 330, "Клиент"), (330, 660, "Менеджер"), (660, 990, "Склад")]
    for x1, x2, t in lanes:
        s.rect(x1, 10, x2 - x1, 940, fill=PAPER, stroke=NAVY, sw=1.6, cls="n")
        s.rect(x1, 10, x2 - x1, 40, fill=SOFT, stroke=NAVY, sw=1.6, cls="n")
        s.text((x1 + x2) / 2, 30, t, size=15, weight=800, anchor="middle", fill=NAVY)

    def action(cx, cy, t, w=180, h=46):
        s.rect(cx - w / 2, cy - h / 2, w, h, rx=16, fill="#eef2fb", stroke=NAVY, sw=2)
        s.text(cx, cy, t, size=13.5, weight=600, anchor="middle")

    def diamond(cx, cy, r=18):
        s.poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=PAPER, stroke=NAVY, sw=2)

    def bar(x1, x2, y):
        s.rect(x1, y - 4, x2 - x1, 8, fill=NAVY, stroke=NAVY, sw=1)

    def final(cx, cy):
        s.circle(cx, cy, 14, fill=PAPER, stroke=NAVY, sw=2)
        s.circle(cx, cy, 8, fill=NAVY, stroke=NAVY, sw=1)

    a = dict(sw=1.9)
    s.circle(170, 82, 11, fill=NAVY, stroke=NAVY, sw=1)
    action(170, 145, "Оформить заявку")
    s.path([(170, 93), (170, 122)], **a)
    s.rect(110, 195, 120, 36, fill=PAPER, stroke=NAVY, sw=2)
    s.text(170, 213, "Заявка", size=13.5, weight=700, anchor="middle", fill=BLUE)
    s.path([(170, 168), (170, 195)], **a)
    diamond(495, 245)                                   # узел слияния
    s.path([(230, 213), (495, 213), (495, 227)], **a)
    action(495, 315, "Проверить заявку")
    s.path([(495, 263), (495, 292)], **a)
    diamond(495, 385)                                   # узел решения
    s.path([(495, 338), (495, 367)], **a)
    action(170, 385, "Уточнить заявку")
    s.path([(477, 385), (260, 385)], **a)
    s.label(370, 371, "[данные неполные]", size=12.5, fill=AMBER, italic=True)
    s.path([(170, 362), (170, 245), (477, 245)], **a)
    action(495, 470, "Выставить счёт")
    s.path([(495, 403), (495, 447)], **a)
    s.label(560, 425, "[заявка корректна]", size=12.5, fill=AMBER, italic=True)
    action(170, 470, "Оплатить счёт")
    s.path([(405, 470), (260, 470)], **a)
    diamond(495, 560)
    s.path([(170, 493), (170, 560), (477, 560)], **a)
    final(615, 560)
    s.path([(513, 560), (601, 560)], **a)
    s.label(557, 532, "[нет оплаты\nза 3 дня]", size=12, fill=AMBER, italic=True)
    s.text(615, 600, "заказ\nотменён", size=12, anchor="middle", fill=MUTED)
    bar(720, 930, 640)                                  # разветвитель
    s.path([(495, 578), (495, 615), (825, 615), (825, 636)], **a)
    s.label(487, 598, "[оплата поступила]", size=12.5, fill=AMBER, italic=True, anchor="end")
    action(745, 720, "Скомплектовать\nгруз", w=140, h=56)
    action(905, 720, "Оформить\nТТН", w=140, h=56)
    s.path([(745, 644), (745, 692)], **a)
    s.path([(905, 644), (905, 692)], **a)
    bar(720, 930, 800)                                  # соединитель
    s.path([(745, 748), (745, 796)], **a)
    s.path([(905, 748), (905, 796)], **a)
    action(825, 865, "Передать груз к отгрузке", w=220)
    s.path([(825, 804), (825, 842)], **a)
    final(825, 925)
    s.path([(825, 888), (825, 911)], **a)
    return s


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("dfd_context", dfd_context), ("dfd_level1", dfd_level1), ("idef0_context", idef0_context),
                     ("idef0_logihub", idef0_a0), ("idef3_logihub", idef3), ("rad_logihub", rad),
                     ("uml_activity", uml_activity)):
        (OUT / f"{name}.svg").write_text(fn().render(), encoding="utf-8")
        print("ok", name)


if __name__ == "__main__":
    main()
