# Среда: поле, мины, открытие клеток.
#
# Состояние — кортеж из FIELD*FIELD чисел:
#   -1  клетка закрыта
#   0…8 сколько мин среди соседей (клетка открыта)
#
# Правило честной игры: мины ставятся ПОСЛЕ первого клика,
# первая открытая клетка всегда безопасна.

import knobs

CLOSED = -1
SIZE = knobs.FIELD * knobs.FIELD


def _neighbors(idx):
    r, c = divmod(idx, knobs.FIELD)
    out = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < knobs.FIELD and 0 <= cc < knobs.FIELD:
                out.append(rr * knobs.FIELD + cc)
    return tuple(out)


NEIGHBORS = tuple(_neighbors(i) for i in range(SIZE))


def new_mines(rng, safe):
    # Расставить MINES мин, клетка safe — без мины.
    cells = [i for i in range(SIZE) if i != safe]
    return frozenset(rng.sample(cells, knobs.MINES))


def initial_state():
    return (CLOSED,) * SIZE


def closed_cells(state):
    return [i for i, v in enumerate(state) if v == CLOSED]


def open_cell(state, mines, idx):
    # Открыть клетку idx. Возвращает (новое_состояние, награда, конец_партии):
    #   мину      -> (state, -1, True)
    #   последнюю -> (state, +1, True)
    #   обычную   -> (state', 0, False)
    if idx in mines:
        return state, -1.0, True
    cnt = sum(1 for j in NEIGHBORS[idx] if j in mines)
    lst = list(state)
    lst[idx] = cnt
    state = tuple(lst)
    if all(v != CLOSED for i, v in enumerate(state) if i not in mines):
        return state, 1.0, True
    return state, 0.0, False


def render(state, mines=None):
    # Доска для печати: четыре строки, клетки подряд. Точка — закрытая клетка.
    # mines показываем только когда партия кончилась.
    rows = []
    for r in range(knobs.FIELD):
        row = ""
        for c in range(knobs.FIELD):
            v = state[r * knobs.FIELD + c]
            if v == CLOSED:
                # закрытую клетку с миной показываем звёздочкой — только после партии
                row += "*" if mines is not None and (r * knobs.FIELD + c) in mines else "."
            else:
                row += str(v)
        rows.append(row)
    return "\n".join(rows)
