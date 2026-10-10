# agent.py — агент: оценка ценности действий и выбор хода.
# Что нужно сделать — в условии задания на портале курса: файлы оставлены чистым кодом.

import random

from environment import (ACTS, EXIT, GAMMA, NAMES, STEP_R, Maze, values,
                         missing_params)

# числа, по которым агент себя проверяет (из лекции; от старта не зависят)
CHECK_ROW_S6 = {0: 1.97, 1: 4.13, 2: 1.97, 3: 4.13}
CHECK_ROW_S7 = {0: 3.77, 1: 5.93, 2: 3.77, 3: 5.93}


# число с запятой, как на слайдах
def ru(x, nd=2):
    return ("%%.%df" % nd % x).replace(".", ",")


class Agent:
    # агент: оценки ценности действий и выбор хода

    def __init__(self, env, rng=None, mode="model"):
        self.env = env
        self.rng = rng if rng is not None else random.Random()
        self.mode = mode                         # "model" или "experience"
        self.v = values()                        # карта ценностей клеток из лекции
        self.q = {s: {a: 0.0 for a in ACTS} for s in range(1, EXIT)}   # таблица оценок
        self.seen = set()                        # какие пары (клетка, ход) уже пробовали

    # ценность шага по модели
    def q_value(self, state, action):
        # Пропуск «на подумать» №1: что здесь посчитать — в условии задания на портале.
        raise NotImplementedError(
            "q_value ещё не дописан — что вписать, написано в условии задания на портале")

    # правило обновления из опыта
    def learn(self, state, action, reward, next_state, done):
        # Пропуск «на подумать» №2: что здесь посчитать — в условии задания на портале.
        raise NotImplementedError(
            "learn ещё не дописан — что вписать, написано в условии задания на портале")

    # четыре оценки для клетки: по модели или по набранной таблице
    def row(self, state):
        if self.mode == "model":
            return {a: self.q_value(state, a) for a in ACTS}
        return dict(self.q[state])

    # выбор хода: жадно (максимум по строке) или ε-жадно (иногда пробуем наугад)
    def act(self, state, epsilon=0.0, allow_random=True):
        if allow_random and epsilon > 0 and self.rng.random() < epsilon:
            return self.rng.choice(ACTS)
        row = self.row(state)
        best = max(row.values())
        ties = [a for a in ACTS if row[a] == best]
        return ties[-1]                          # при равенстве договорились идти вправо

    # один эпизод: выбрали ход, среда ответила, копим доход — идём до выхода
    def run_episode(self, seed=None, epsilon=0.0, learn=False, max_steps=200):
        if seed is not None:
            self.rng = random.Random(seed)
            self.env.rng = random.Random(seed)   # один seed — один и тот же эпизод
        state = self.env.reset()
        route, total, step = [state], 0.0, 0
        while True:
            action = self.act(state, epsilon)
            state, reward, done = self.env.step(action)
            route.append(state)
            if learn:
                self.learn(route[-2], int(action), reward, state, done)
            total += reward * GAMMA ** step
            step += 1
            if done or step >= max_steps:
                break
        return route, round(total, 2)

    # сколько пар (клетка, ход) уже пробовали — таблица полна, когда набраны все
    def table_report(self):
        return len(self.seen), (EXIT - 1) * len(ACTS)

    # наполнить таблицу прогонами: таблица живёт между эпизодами
    def fill_table(self, episodes=200, epsilon=0.1, seed=7):
        for k in range(episodes):
            self.run_episode(seed=seed + k, epsilon=epsilon, learn=True)
        return self.table_report()

    # средний доход по многим эпизодам: одна попытка ничего не доказывает
    def average_income(self, episodes=200, epsilon=0.0, seed=7):
        incomes = []
        for k in range(episodes):
            rng = random.Random(seed + k)         # своя случайность на эпизод
            agent = Agent(Maze(rng=rng), rng=rng)
            _, total = agent.run_episode(epsilon=epsilon)
            incomes.append(total)
        return round(sum(incomes) / len(incomes), 2)


class _ProbeEnv:
    # крошечная заглушка среды: нужна только чтобы спросить недописанную функцию
    def transitions(self, state, action):
        return {state: 1.0}


# какие тела ещё не дописаны (два пропуска «на подумать»)
def open_steps():
    if missing_params():
        return []                            # сначала параметры среды — иначе спрашивать не о чем
    probe = object.__new__(Agent)            # пустой агент: без __init__, только для вопроса
    probe.env = _ProbeEnv()
    probe.v = {1: 0.0, 2: 0.0, 6: 0.0, 7: 0.0}   # карта нужна только чтобы спросить функцию
    probe.q = {s: {a: 0.0 for a in ACTS} for s in (1, 2, 6, 7, 12)}
    probe.seen = set()
    todo = []
    for name, call in (("q_value", lambda: probe.q_value(1, 0)),
                       ("learn", lambda: probe.learn(1, 0, 0.0, 2, False))):
        try:
            call()
        except NotImplementedError:
            todo.append(name)
        except Exception as exc:
            todo.append("%s (падает: %s: %s)" % (name, type(exc).__name__, exc))
    return todo


# что агент проверяет у себя: строки q для двух клеток из лекции
def checks(agent):
    out = []
    for state, want in ((6, CHECK_ROW_S6), (7, CHECK_ROW_S7)):
        row = {a: round(agent.q_value(state, a), 2) for a in ACTS}
        bad = [a for a in ACTS if abs(row[a] - want[a]) > 1e-9]
        out.append((not bad, "строка q для S%d: %s"
                    % (state, " · ".join("%s%s" % (NAMES[a], ru(row[a])) for a in ACTS))))
    return out


# агент сам себя проверяет — блок в конце файла, а не отдельный файл проверок
def self_check(agent=None, verbose=True):
    if agent is None:
        agent = Agent(Maze(seed=7), rng=random.Random(7))
    result = checks(agent)
    if verbose:
        for ok, text in result:
            print("   [%s] агент: %s" % ("ok" if ok else "нет", text))
    return all(ok for ok, _ in result)


if __name__ == "__main__":
    env_todo = missing_params()
    step_todo = open_steps()
    if env_todo or step_todo:
        print("Агент: каркас ещё не заполнен — проверять пока нечего.")
        if env_todo:
            print("   в среде (environment.py) не вписаны параметры: %s" % ", ".join(env_todo))
        if step_todo:
            print("   у агента (agent.py) не дописаны функции: %s" % ", ".join(step_todo))
        print("\nВпишите параметры среды и допишите функции агента,")
        print("затем запустите снова: python3 agent.py")
    else:
        env = Maze(seed=7)
        agent = Agent(env, rng=random.Random(7))

        print("Строка q для S6:", " · ".join("%s%s" % (NAMES[a], ru(agent.q_value(6, a))) for a in ACTS))
        print("Строка q для S7:", " · ".join("%s%s" % (NAMES[a], ru(agent.q_value(7, a))) for a in ACTS))

        route, total = agent.run_episode(seed=7)
        print("\nЭпизод (seed = 7, старт S%d):" % route[0],
              " → ".join("S%d" % c for c in route), "— %d шагов, доход %s"
              % (len(route) - 1, ru(total)))

        print("\nПроверки агента:")
        ok = self_check(agent)
        print("\nитог: все проверки агента сошлись" if ok
              else "\nитог: есть расхождения — смотрите строки [нет] выше")
