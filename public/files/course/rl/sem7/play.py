# Режимы запуска: selftest, random, train, ladder, sarsa, show, vs.
#
# Вся «физика» обучения — в learn_episode и evaluate; режимы только вызывают её
# и печатают результаты. Числа на слайдах семинара сняты этими же режимами.

import random
import time

import game
import knobs
from qagent import QAgent
from sarsa import SarsaAgent


def learn_episode(agent, rng, alpha, epsilon):
    # Одна партия: агент играет до конца, таблица правится по ходам.
    # Правка отложена на шаг: SARSA нужен ход, который агент сделает из s'.
    state = game.initial_state()
    mines = None
    pending = None
    while True:
        action = agent.choose(state, rng, epsilon)
        if mines is None:
            # первый ход: мин ещё нет, клетка станет безопасной
            mines = game.new_mines(rng, safe=action)
        next_state, reward, done = game.open_cell(state, mines, action)
        if pending is not None:
            s, a, r = pending
            agent.learn(s, a, r, state, action, False, alpha)
        if done:
            agent.learn(state, action, reward, next_state, None, True, alpha)
            return reward > 0
        pending = (state, action, reward)
        state = next_state


def train(agent, episodes, alpha, epsilon, seed, quiet=False):
    rng = random.Random(seed)
    wins = 0
    for i in range(episodes):
        wins += learn_episode(agent, rng, alpha, epsilon)
        if not quiet and episodes >= 100000 and (i + 1) % 20000 == 0:
            print(f"  обучение: {i + 1:,} / {episodes:,} партий")
    return wins / episodes


def evaluate(agent, games, seed):
    # Жадная игра без случайных проб — измеряем, чему научились.
    rng = random.Random(seed)
    wins = 0
    for _ in range(games):
        state = game.initial_state()
        mines = None
        while True:
            action = agent.choose(state, rng, 0.0)
            if mines is None:
                mines = game.new_mines(rng, safe=action)
            state, reward, done = game.open_cell(state, mines, action)
            if done:
                wins += int(reward > 0)
                break
    return wins / games


def random_player(games, seed):
    # Нижняя граница: клетка наугад, таблицы нет вовсе.
    rng = random.Random(seed)
    wins = 0
    for _ in range(games):
        state = game.initial_state()
        mines = None
        while True:
            action = rng.choice(game.closed_cells(state))
            if mines is None:
                mines = game.new_mines(rng, safe=action)
            state, reward, done = game.open_cell(state, mines, action)
            if done:
                wins += int(reward > 0)
                break
    return wins / games


# ---------- режимы ----------

def cmd_selftest():
    rng = random.Random(1)
    st = game.initial_state()
    assert game.closed_cells(st) == list(range(game.SIZE))
    mines = game.new_mines(rng, safe=0)
    assert len(mines) == knobs.MINES and 0 not in mines
    st1, r, done = game.open_cell(st, mines, 0)
    assert r == 0.0 and not done and st1[0] != game.CLOSED
    agent = QAgent()
    ok = learn_episode(agent, rng, knobs.ALPHA, knobs.EPSILON)
    assert isinstance(ok, bool)
    greedy = evaluate(agent, 10, 2)
    assert 0.0 <= greedy <= 1.0
    sarsa_agent = SarsaAgent()
    learn_episode(sarsa_agent, rng, knobs.ALPHA, knobs.EPSILON)
    assert sarsa_agent.table
    assert 0.0 <= random_player(10, 3) <= 1.0
    print("selftest: ok")


def cmd_random(games, seed):
    t0 = time.time()
    share = random_player(games, seed)
    print(f"случайный игрок, {games:,} партий: побед {share:.1%} "
          f"({time.time() - t0:.1f} с)")


def cmd_train(episodes, alpha, epsilon, seed, eval_games,
              agent_cls=QAgent, title=None):
    if title:
        print(title)
    t0 = time.time()
    agent = agent_cls()
    train_win = train(agent, episodes, alpha, epsilon, seed)
    dt = time.time() - t0
    eval_win = evaluate(agent, eval_games, seed + 1000)
    print(f"партий обучения: {episodes:,}  (побед в обучении {train_win:.1%}, {dt:.1f} с)")
    print(f"таблица: {len(agent.table):,} пар (состояние, клетка)")
    print(f"жадная игра, {eval_games:,} партий: побед {eval_win:.1%}")


def cmd_ladder(top, alpha, epsilon, seed, eval_games,
               agent_cls=QAgent, title=None):
    if title:
        print(title)
    n = 10
    while n <= top:
        agent = agent_cls()
        t0 = time.time()
        train(agent, n, alpha, epsilon, seed, quiet=True)
        dt = time.time() - t0
        eval_win = evaluate(agent, eval_games, seed + 1000)
        print(f"{n:>9,} партий -> побед {eval_win:6.1%}  "
              f"(таблица {len(agent.table):>7,}, {dt:5.1f} с)")
        n *= 10


def _greedy_opening(agent, seed, after):
    # Первые `after` жадных ходов на фиксированном поле — позиция для ставки.
    rng = random.Random(seed)
    state = game.initial_state()
    mines = None
    for _ in range(after):
        action = agent.choose(state, rng, 0.0)
        if mines is None:
            mines = game.new_mines(rng, safe=action)
        state, _, done = game.open_cell(state, mines, action)
        if done:
            break
    return state, mines


def cmd_show(seed, after, episodes, alpha, epsilon, agent_cls=QAgent):
    # Доска после `after` ходов агента + его оценки закрытых клеток.
    # Это позиция для голосования зала: сначала ставка, потом открытие.
    agent = agent_cls()
    t0 = time.time()
    train(agent, episodes, alpha, epsilon, knobs.SEED, quiet=True)
    state, mines = _greedy_opening(agent, seed, after)
    print(f"поле {seed}: {agent_name(agent_cls)} на {episodes:,} партиях "
          f"({time.time()-t0:.0f} с)")
    print("ходы агента: " + str(after) + ", доска (точка — закрыта):")
    print()
    print(game.render(state))
    print()
    print("оценки агента (шанс на победу после этой клетки):")
    for v, a in agent.top(state, k=5):
        r, c = divmod(a, knobs.FIELD)
        print(f"  клетка ({r + 1},{c + 1}): {v:+.3f}")
    print()
    print("расстановка мин для проверки (спойлер):", sorted(m + 1 for m in mines))


def cmd_vs(episodes, alpha, epsilon, seed, agent_cls=QAgent):
    # Человек против машины на одном поле.
    # Человек вводит клетку «строка столбец» (например, 2 3), агент отвечает
    # своим ходом. Кто наступил на мину — проиграл; кто открыл всё — выиграл.
    rng = random.Random(seed)
    agent = agent_cls()
    print(f"{agent_name(agent_cls)} учится: {episodes:,} партий...")
    train(agent, episodes, alpha, epsilon, knobs.SEED)
    state = game.initial_state()
    mines = None
    turn = "human"
    while True:
        print()
        print(game.render(state))
        if turn == "human":
            try:
                raw = input("ваша клетка (строка столбец): ").split()
            except EOFError:
                print("игра прервана")
                return
            if len(raw) < 2:
                print("так нельзя: введите две координаты, например 2 3")
                continue
            try:
                r, c = int(raw[0]) - 1, int(raw[1]) - 1
            except ValueError:
                print("так нельзя: координаты должны быть числами, например 2 3")
                continue
            if not (0 <= r < knobs.FIELD and 0 <= c < knobs.FIELD) \
                    or state[r * knobs.FIELD + c] != game.CLOSED:
                print("так нельзя: клетка вне поля или уже открыта")
                continue
            action = r * knobs.FIELD + c
            print(f"вы открываете ({r + 1},{c + 1})")
        else:
            action = agent.choose(state, rng, 0.0)
            r, c = divmod(action, knobs.FIELD)
            print(f"агент открывает ({r + 1},{c + 1})")
        if mines is None:
            mines = game.new_mines(rng, safe=action)
        state, reward, done = game.open_cell(state, mines, action)
        if done:
            print()
            print(game.render(state, mines=mines))
            if reward > 0:
                print("Последняя клетка безопасна. " + outcome_ru(turn, True).capitalize())
            else:
                print("Мина. " + outcome_ru(turn, False).capitalize())
            break
        turn = "agent" if turn == "human" else "human"


def agent_name(agent_cls):
    # Как назвать стратегию в выводе.
    return "SARSA" if agent_cls is SarsaAgent else "Q-обучение"


def outcome_ru(turn, won):
    # Итог словами: «вы выиграли» / «агент проиграл» — без падежных кульбитов.
    if turn == "human":
        return "вы выиграли" if won else "вы проиграли"
    return "агент выиграл" if won else "агент проиграл"
