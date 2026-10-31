import statistics
import sys

from agent import Agent
from environment import CHANNELS, LOW, HIGH, SIGMA, Bandit, drift_steps, mean_of, outcome_probs

FLAT = {c: 1.0 for c in CHANNELS}


def guard(title, body):
    try:
        return body()
    except NotImplementedError as exc:
        return False, "%s: не заполнено — %s" % (title, exc)
    except Exception as exc:
        return False, "%s: %s" % (title, exc)


def step_sd(steps):
    flat = [value for channel in CHANNELS for value in steps[channel]]
    return statistics.pstdev(flat)


def bonus(agent, channel):
    return agent.ucb_score(channel) - agent.q[channel]


def check_probs():
    def body():
        for mean in (0.1, 0.8, 1.0, 1.9):
            probs = outcome_probs(mean)
            if abs(sum(probs) - 1.0) > 1e-12 or abs(mean_of(probs) - mean) > 1e-12:
                return False, "вероятности исходов: при μ = %.1f среднее не восстанавливается" % mean
        return True, "вероятности исходов: сумма 1 и среднее восстанавливается"
    return guard("вероятности исходов", body)


def check_drift_every_channel():
    def body():
        steps = drift_steps(SIGMA, turns=50, start=FLAT)
        worst = min(statistics.pstdev(steps[c]) for c in CHANNELS)
        return worst > 0.5 * SIGMA, "двигаются все четыре канала: слабейший шаг %.3f при σ = %.2f" % (worst, SIGMA)
    return guard("движение всех каналов", body)


def check_drift_scale():
    def body():
        steps = drift_steps(SIGMA, turns=50, start=FLAT)
        sd = step_sd(steps)
        ok = 0.85 * SIGMA < sd < 1.15 * SIGMA
        return ok, "σ задаёт размах шага: %.3f при σ = %.2f" % (sd, SIGMA)
    return guard("масштаб дрейфа", body)


def check_drift_low():
    def body():
        env = Bandit(seed=7, sigma=0.3, start=FLAT)
        for _ in range(400):
            env.pull("A")
        low = min(min(row) for row in env.history)
        return low < 0.05, "средние доходят до нижней границы: минимум %.2f при σ = 0,3" % low
    return guard("нижняя граница", body)


def check_drift_high():
    def body():
        env = Bandit(seed=7, sigma=0.3, start=FLAT)
        for _ in range(400):
            env.pull("A")
        high = max(max(row) for row in env.history)
        return high > 1.95, "средние доходят до верхней границы: максимум %.2f при σ = 0,3" % high
    return guard("верхняя граница", body)


def check_drift_inside():
    def body():
        env = Bandit(seed=7, sigma=0.5)
        for _ in range(500):
            env.pull(env.best())
        top = max(max(row) for row in env.history)
        bottom = min(min(row) for row in env.history)
        ok = bottom >= LOW - 1e-9 and top <= HIGH + 1e-9
        return ok, "средние не выходят за границы: %.2f … %.2f" % (bottom, top)
    return guard("границы средних", body)


def check_drift_seed():
    def body():
        first = Bandit(seed=7)
        second = Bandit(seed=7)
        for _ in range(100):
            first.pull("C")
            second.pull("C")
        return first.history == second.history, "один и тот же seed даёт ту же историю средних"
    return guard("повторяемость", body)


def check_update_average():
    def body():
        agent = Agent(mode="greedy")
        seen = []
        for reward in (1, 0, 2):
            agent.update("B", reward)
            seen.append(round(agent.q["B"], 12))
        return seen == [1.0, 0.5, 1.0], "честное среднее по B: 1 → 0,5 → 1,0"
    return guard("обновление 1/n", body)


def check_update_two_channels():
    def body():
        agent = Agent(mode="greedy")
        agent.update("A", 1)
        agent.update("A", 0)
        agent.update("B", 2)
        agent.update("A", 2)
        ok = abs(agent.q["A"] - 1.0) < 1e-12 and abs(agent.q["B"] - 2.0) < 1e-12
        return ok, "шаг считается по своему каналу: q[A] = %.3f, q[B] = %.3f" % (agent.q["A"], agent.q["B"])
    return guard("шаг по каналу", body)


def check_update_step():
    def body():
        agent = Agent(mode="greedy", alpha=0.5)
        for reward in (1, 0, 2):
            agent.update("B", reward)
        return abs(agent.q["B"] - 1.25) < 1e-12, "постоянный шаг α = 0,5 по B: 1 → 0,5 → 1,25"
    return guard("обновление с шагом", body)


def check_preferences_shape():
    def body():
        agent = Agent(mode="gradient")
        agent.h.update({"A": 0.0, "B": 0.0, "C": 0.0, "D": 4.0})
        weights = agent.preferences()
        ok = abs(sum(weights.values()) - 1.0) < 1e-9
        ok = ok and weights["D"] > 0.9 and weights["D"] > 10 * weights["A"]
        return ok, "вероятности концентрируются: при h[D] = 4 доля D равна %.3f" % weights["D"]
    return guard("вероятности градиентной", body)


def check_preferences_monotone():
    def body():
        agent = Agent(mode="gradient")
        agent.h.update({"A": 3.0, "B": 0.0, "C": 0.0, "D": 0.0})
        weights = agent.preferences()
        ok = weights["A"] == max(weights.values()) and weights["A"] > 0.8
        return ok, "больший h даёт большую вероятность: при h[A] = 3 доля A равна %.3f" % weights["A"]
    return guard("монотонность вероятностей", body)


def check_ucb_quality():
    def body():
        agent = Agent(mode="ucb", c=2.0)
        agent.q.update({"A": 1.0, "B": 1.0, "C": 1.0, "D": 2.0})
        agent.n.update({"A": 20, "B": 20, "C": 20, "D": 20})
        agent.turn = 200
        chosen = agent.choose()
        return chosen == "D", "ucb не забывает оценку: при q[D] = 2 и равных n берёт D (%s)" % chosen
    return guard("ucb и оценка", body)


def check_ucb_rare():
    def body():
        agent = Agent(mode="ucb", c=2.0)
        agent.q.update({"A": 1.0, "B": 1.0, "C": 1.0, "D": 1.0})
        agent.n.update({"A": 50, "B": 50, "C": 1, "D": 50})
        agent.turn = 151
        chosen = agent.choose()
        return chosen == "C", "ucb тянет редкий канал: C при равных оценках (%s)" % chosen
    return guard("ucb и редкость", body)


def check_ucb_decay():
    def body():
        agent = Agent(mode="ucb", c=2.0)
        agent.turn = 1000
        agent.n.update({"A": 1, "B": 100, "C": 100, "D": 100})
        ratio = bonus(agent, "A") / bonus(agent, "B")
        return 8.0 < ratio < 12.5, "бонус падает как 1/√n: отношение редкого к частому %.1f" % ratio
    return guard("затухание бонуса", body)


def check_ucb_turn():
    def body():
        agent = Agent(mode="ucb", c=2.0)
        agent.n.update({"A": 50, "B": 50, "C": 50, "D": 50})
        agent.turn = 100
        early = bonus(agent, "A")
        agent.turn = 400
        late = bonus(agent, "A")
        return late > early, "бонус растёт с числом ходов: %.2f на 100-м, %.2f на 400-м" % (early, late)
    return guard("рост бонуса", body)


def check_ucb_scale():
    def body():
        small = Agent(mode="ucb", c=2.0)
        big = Agent(mode="ucb", c=4.0)
        for agent in (small, big):
            agent.turn = 500
            agent.n.update({"A": 25, "B": 25, "C": 25, "D": 25})
        ratio = bonus(big, "A") / bonus(small, "A")
        return 1.8 < ratio < 2.2, "c масштабирует бонус: при c = 4 он в %.2f раза больше" % ratio
    return guard("масштаб бонуса", body)


def check_run():
    def body():
        shares = {}
        for mode, params in (("жадная", dict(mode="greedy")),
                             ("ucb", dict(mode="ucb", c=2.0))):
            values = []
            for seed in (1, 2, 3, 4, 5):
                env = Bandit(seed=seed, sigma=SIGMA)
                agent = Agent(seed=seed + 100000, **params)
                actions = []
                for _ in range(300):
                    channel = agent.choose()
                    reward = env.pull(channel)
                    agent.update(channel, reward)
                    actions.append(channel)
                hits = sum(1 for i, c in enumerate(actions) if c == env.best_at(i))
                values.append(hits / len(actions))
            shares[mode] = statistics.median(values)
        gap = shares["ucb"] - shares["жадная"]
        return gap > 0.2, "стратегии различимы: ucb %.0f%%, жадная %.0f%%" % (
            100 * shares["ucb"], 100 * shares["жадная"])
    return guard("прогон целиком", body)


def main():
    checks = (
        check_probs,
        check_drift_every_channel,
        check_drift_scale,
        check_drift_low,
        check_drift_high,
        check_drift_inside,
        check_drift_seed,
        check_update_average,
        check_update_two_channels,
        check_update_step,
        check_preferences_shape,
        check_preferences_monotone,
        check_ucb_quality,
        check_ucb_rare,
        check_ucb_decay,
        check_ucb_turn,
        check_ucb_scale,
        check_run,
    )
    results = [check() for check in checks]
    print("Проверки кода лабораторной 2:")
    for ok, text in results:
        print("   [%s] %s" % ("ok" if ok else "нет", text))
    passed = all(ok for ok, _ in results)
    if passed:
        print("\nитог: все %d проверок сошлись" % len(results))
    else:
        print("\nитог: есть незакрытые места — смотрите [нет]")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
