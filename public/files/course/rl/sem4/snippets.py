# snippets.py — куски к трём пропускам занятия 4: выбрать, вставить, запустить проверку.
#
#   1) environment.py, Bandit.step  — чем двигать средние каждый спринт;
#   2) agent.py, Agent.update       — правило обновления оценки;
#   3) run.py, --strategy           — стратегия выбора.
#
# В первых двух пропусках верный кусок один, в третьем верного нет.

SNIPPETS = {
    "1. environment.py, Bandit.step": {
        "а": "# сдвинуть каждое среднее и удержать в границах LO..HI\n"
             "for a in APPROACHES:\n"
             "    self.mu[a] = min(max(self.mu[a] + self.rng.gauss(0.0, self.sigma), LO), HI)",
        "б": "# вероятности наград из семинара 3\n"
             'PROBS = {"A": (0.8, 0.1, 0.1), "B": (0.3, 0.6, 0.1), "C": (0.1, 0.5, 0.4)}',
        "в": "# новые средние на каждый спринт\n"
             "self.mu = {a: self.rng.uniform(LO, HI) for a in APPROACHES}",
    },
    "2. agent.py, Agent.update": {
        "а": "step = 1.0 / self.n[act]          # шаг 1/n",
        "б": "step = self.alpha                # шаг α",
        "в": "self.q[act] = reward             # вместо шага и сдвига — одна строка",
    },
    "3. run.py, --strategy": {
        "а": 'mode="eps", epsilon=0.1        # ε-жадная',
        "б": 'mode="gradient"                # градиентная',
        "в": 'mode="ucb", c=2.0              # UCB',
    },
}
