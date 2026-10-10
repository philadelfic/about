# run.py — прогон: соединяет среду и агента, считает эпизоды и печатает отчёт.
# Что нужно сделать — в условии задания на портале курса: файлы оставлены чистым кодом.
#
# Запуск:  python3 run.py

import random

import environment
import agent as agent_module
from environment import ACTS, EXIT, Maze, NAMES
from agent import Agent, ru


# ==== ПАРАМЕТРЫ ПРОГОНА — впишите =======================================
EPISODES = None                # ← впишите
SEED = None                    # ← впишите
EPSILON = None                 # ← впишите
MAX_STEPS = None               # ← впишите
SHOW_TABLE = False             # печатать ли таблицу оценок целиком
# =========================================================================


# агент, который считает ценность шага по модели
def model_agent(seed=SEED):
    return Agent(Maze(seed=seed), rng=random.Random(seed), mode="model")


# один эпизод от старта — один и тот же seed даёт один и тот же маршрут
def episode(seed=SEED, epsilon=0.0):
    ag = model_agent(seed)
    route, total = ag.run_episode(seed=seed, epsilon=epsilon, max_steps=MAX_STEPS)
    return route, total


# серия эпизодов: одна попытка ничего не доказывает, смотрим на среднее
def series(episodes=EPISODES, epsilon=0.0, seed=SEED):
    return model_agent(seed).average_income(episodes, epsilon=epsilon, seed=seed)


# таблица набирается прогонами и живёт между эпизодами; потом идём по ней жадно
def experience(episodes=EPISODES, epsilon=EPSILON, seed=SEED):
    ag = Agent(Maze(seed=seed), rng=random.Random(seed), mode="experience")
    got, need = ag.fill_table(episodes, epsilon=epsilon, seed=seed)
    route, total = ag.run_episode(seed=seed, epsilon=0.0, max_steps=MAX_STEPS)
    return ag, got, need, route, total


def env_block():
    return [(ok, "среда: " + text) for ok, text in environment.checks()]


def agent_block():
    return [(ok, "агент: " + text) for ok, text in agent_module.checks(model_agent(SEED))]


def episode_block():
    route, total = episode()
    return [(route[0] == 1 and route[-1] == EXIT and abs(total - 3.12) < 1e-9,
             "прогон: эпизод из S1 (seed = %d): %s — %d шагов, доход %s"
             % (SEED, " → ".join("S%d" % c for c in route), len(route) - 1, ru(total)))]


def experience_block():
    exp_agent, got, need, exp_route, exp_total = experience()
    return [(got == need and exp_route[-1] == EXIT,
             "прогон: таблица опыта %d из %d, жадно из S1 — %s (доход %s)"
             % (got, need, "дошёл до выхода" if exp_route[-1] == EXIT else "не дошёл",
                ru(exp_total)))]


def print_table(ag):
    print("\nТаблица оценок (клетка → четыре хода %s):" % " ".join(NAMES))
    for cell in range(1, EXIT):
        print("   S%-2d %s" % (cell, "  ".join("%7s" % ru(ag.q[cell][a]) for a in ACTS)))


# всё, что нужно для проверки работы: сначала считаем, потом печатаем вердикты
def report():
    missing = [n for n, v in (("EPISODES", EPISODES), ("SEED", SEED),
                              ("EPSILON", EPSILON), ("MAX_STEPS", MAX_STEPS)) if v is None]
    if missing:
        print("ещё не вписаны параметры прогона: %s" % ", ".join(missing))
        print("впишите их в блоке «ПАРАМЕТРЫ ПРОГОНА» в начале файла и запустите снова")
        return False

    results, exp_agent = [], None
    for name, fn in (("среда", env_block), ("агент", agent_block),
                     ("прогон: эпизод", episode_block),
                     ("прогон: таблица опыта", experience_block)):
        try:
            results += fn()
        except NotImplementedError as exc:
            results.append((False, "%s: ещё не дописано — %s" % (name, exc)))
        except Exception as exc:
            results.append((False, "%s: %s: %s" % (name, type(exc).__name__, exc)))

    print("Проверки работы (среда → агент → прогон):\n")
    for ok, text in results:
        print("   [%s] %s" % ("ok" if ok else "нет", text))

    if all(ok for ok, _ in results):
        try:
            exp_agent = experience()[0]
            print("\nСерия %d эпизодов: жадная %s, ε-жадная (ε = %s) %s"
                  % (EPISODES, ru(series(epsilon=0.0)), ru(EPSILON), ru(series(epsilon=EPSILON))))
        except Exception:
            pass
        if SHOW_TABLE and exp_agent is not None:
            print_table(exp_agent)

    ok = all(ok for ok, _ in results)
    print("\nитог: все проверки сошлись" if ok
          else "\nитог: есть расхождения — смотрите строки [нет] выше")
    return ok


if __name__ == "__main__":
    report()
