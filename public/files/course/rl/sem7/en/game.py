# Environment: board, mines, opening cells.
#
# State is a tuple of FIELD*FIELD numbers:
#   -1  cell is closed
#   0…8 how many mines are among the neighbours (cell is open)
#
# Fair-play rule: mines are placed AFTER the first click,
# so the first opened cell is always safe.

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
    # Place MINES mines; the cell `safe` gets none.
    cells = [i for i in range(SIZE) if i != safe]
    return frozenset(rng.sample(cells, knobs.MINES))


def initial_state():
    return (CLOSED,) * SIZE


def closed_cells(state):
    return [i for i, v in enumerate(state) if v == CLOSED]


def open_cell(state, mines, idx):
    # Open cell idx. Returns (new_state, reward, done):
    #   a mine      -> (state, -1, True)
    #   the last    -> (state, +1, True)
    #   an ordinary -> (state', 0, False)
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
    # Printable board: four rows, cells in a row. A dot is a closed cell.
    # Mines are shown only once the game is over.
    rows = []
    for r in range(knobs.FIELD):
        row = ""
        for c in range(knobs.FIELD):
            v = state[r * knobs.FIELD + c]
            if v == CLOSED:
                # a closed cell with a mine is shown as a star — only after the game
                row += "*" if mines is not None and (r * knobs.FIELD + c) in mines else "."
            else:
                row += str(v)
        rows.append(row)
    return "\n".join(rows)
