# environment.py — среда «лабиринт»: правила игры, модель мира, награды.
# Что нужно сделать — в условии задания на портале курса: файлы оставлены чистым кодом.


# ==== ПАРАМЕТРЫ ЛАБИРИНТА — впишите ======================================
ROWS = None            # ← впишите
COLS = None            # ← впишите
EXIT = None            # ← впишите
CELLS = None if ROWS is None or COLS is None else ROWS * COLS   # считается само
START = None           # ← впишите
GAMMA = None           # ← впишите
STEP_R = None          # ← впишите
EXIT_R = None          # ← впишите
P_OK = None            # ← впишите
P_SLIP = None          # ← впишите
# =========================================================================

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTS = (UP, DOWN, LEFT, RIGHT)
NAMES = ("↑", "↓", "←", "→")                         # для печати и картинки
DELTA = {UP: (0, 1), DOWN: (0, -1), LEFT: (-1, 0), RIGHT: (1, 0)}

DEMO_ROUTE = [6, 7, 8, 8, 12]                        # маршрут из лекции
BEST_ROUTE = [1, 2, 3, 4, 8, 12]                     # оптимальный маршрут от старта


# какие параметры блока «ПАРАМЕТРЫ ЛАБИРИНТА» ещё не вписаны
def missing_params():
    todo = (("ROWS", ROWS), ("COLS", COLS), ("EXIT", EXIT), ("START", START),
            ("GAMMA", GAMMA), ("P_OK", P_OK), ("P_SLIP", P_SLIP),
            ("STEP_R", STEP_R), ("EXIT_R", EXIT_R))
    return [name for name, value in todo if value is None]


# номер клетки -> (столбец, строка), строка считается снизу
def rc(cell):
    top = (cell - 1) // COLS
    return (cell - 1) % COLS, ROWS - 1 - top


# обратно: (столбец, строка) -> номер клетки
def num(col, row):
    return (ROWS - 1 - row) * COLS + col + 1


# куда ведёт шаг; за границей сетки агент остаётся на месте
def target(cell, delta):
    col, row = rc(cell)
    c2, r2 = col + delta[0], row + delta[1]
    if 0 <= c2 < COLS and 0 <= r2 < ROWS:
        return num(c2, r2)
    return cell


# два перпендикулярных направления — снос идёт вбок от команды
def perp(delta):
    dcol, drow = delta
    return [(-drow, dcol), (drow, -dcol)]


# ценности «по расстоянию» — карта из лекции 3, для счёта вручную
def values():
    by_d = {0: EXIT_R}
    for k in range(1, CELLS + 1):
        by_d[k] = STEP_R + GAMMA * by_d[k - 1]
    return {i: round(by_d[abs(rc(i)[0] - rc(EXIT)[0]) + abs(rc(i)[1] - rc(EXIT)[1])])
            for i in range(1, CELLS + 1)}


class Maze:
    # среда лабиринта: состояния, действия, переходы, награда, дисконт

    def __init__(self, seed=None, rng=None):
        import random
        self.rng = rng if rng is not None else random.Random(seed)
        self.state = START
        self.steps = 0

    def reset(self):
        self.state = START
        self.steps = 0
        return self.state

    # строка модели мира: {куда: вероятность}
    def transitions(self, cell, act):
        out = {}
        outs = [(target(cell, DELTA[act]), P_OK)]
        outs += [(target(cell, d), P_SLIP) for d in perp(DELTA[act])]
        for s2, p in outs:
            out[s2] = out.get(s2, 0.0) + p        # граница: вероятности складываются
        return out

    # один шаг: разыгрываем исход и отдаём агенту новое состояние, награду и конец
    def step(self, act):
        outs = self.transitions(self.state, act)
        cands = list(outs)
        s2 = self.rng.choices(cands, weights=[outs[c] for c in cands])[0]
        done = s2 == EXIT
        reward = EXIT_R if done else STEP_R
        self.state, self.steps = s2, self.steps + 1
        return s2, reward, done

    # доход по готовому маршруту
    @staticmethod
    def route_income(route):
        total = sum((EXIT_R if c == EXIT else STEP_R) * GAMMA ** k
                    for k, c in enumerate(route[1:]))
        return round(total, 2)


# что среда проверяет у себя: вероятности, границы, доход маршрутов
def checks():
    todo = missing_params()
    if todo:
        return [(False, "ещё не вписаны параметры лабиринта: %s — впишите их в начале файла" % ", ".join(todo))]

    env = Maze(seed=0)
    out = []

    rows, bad = 0, 0
    for cell in range(1, CELLS + 1):
        if cell == EXIT:
            continue
        for act in ACTS:
            rows += 1
            if abs(sum(env.transitions(cell, act).values()) - 1) > 1e-12:
                bad += 1
    out.append((bad == 0, "суммы вероятностей в каждой строке дают 1 (%d строки)" % rows))

    env.reset()
    stay = env.step(UP)[0]        # из S1 вверх — за границей остаёмся на месте
    out.append((stay == START, "за границей агент остаётся на месте (S%d → вверх → S%d)"
                % (START, stay)))

    def ru(x):
        return ("%.2f" % x).replace(".", ",")

    demo = Maze.route_income(DEMO_ROUTE)
    out.append((abs(demo - 4.58) < 1e-9, "доход маршрута из лекции = %s" % ru(demo)))

    best = Maze.route_income(BEST_ROUTE)
    out.append((abs(best - 3.12) < 1e-9, "доход оптимального маршрута из S1 = %s" % ru(best)))

    return out


# среда сама себя проверяет — блок в конце файла, а не отдельный файл проверок
def self_check(verbose=True):
    result = checks()
    if verbose:
        for ok, text in result:
            print("   [%s] среда: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


if __name__ == "__main__":
    todo = missing_params()
    if todo:
        print("Среда: лабиринт ещё не настроен — параметры не вписаны:")
        for name in todo:
            print("   %s" % name)
        print("\nВпишите их в блоке «ПАРАМЕТРЫ ЛАБИРИНТА» в начале файла")
        print("(пометки «← впишите») и запустите снова: python3 environment.py")
    else:
        print("Среда: лабиринт %d x %d, старт S%d, выход S%d" % (ROWS, COLS, START, EXIT))
        print("\nСтрока модели мира: из S6 вправо (действие %d)" % RIGHT)
        for s2, p in Maze(seed=0).transitions(6, RIGHT).items():
            print("   %.1f -> S%d" % (p, s2))
        print("\nЦенности клеток (округления карты):", values())
        print("\nМаршрут из лекции:", " -> ".join("S%d" % c for c in DEMO_ROUTE),
              "— доход", Maze.route_income(DEMO_ROUTE))
        print("Оптимальный маршрут из S1:", " -> ".join("S%d" % c for c in BEST_ROUTE),
              "— доход", Maze.route_income(BEST_ROUTE))

        print("\nПроверки среды:")
        ok = self_check()
        print("\nитог: все проверки среды сошлись" if ok
              else "\nитог: есть расхождения — смотрите строки [нет] выше")
