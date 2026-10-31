import random

CHANNELS = ("A", "B", "C", "D")
OUTCOMES = (0, 1, 2)
START = {"A": 0.4, "B": 0.9, "C": 1.2, "D": 1.6}
SIGMA = 0.1
LOW, HIGH = 0.0, 2.0


def outcome_probs(mean):
    mean = min(max(mean, LOW), HIGH)
    if mean < 1.0:
        return (1.0 - mean, mean, 0.0)
    if mean > 1.0:
        return (0.0, 2.0 - mean, mean - 1.0)
    return (0.0, 1.0, 0.0)


def mean_of(probs):
    return sum(o * p for o, p in zip(OUTCOMES, probs))


class Bandit:

    def __init__(self, seed=None, sigma=SIGMA, start=None):
        self.rng = random.Random(seed)
        self.sigma = sigma
        self.start = dict(START if start is None else start)
        self.reset()

    def reset(self):
        self.turn = 0
        self.means = dict(self.start)
        self.history = []
        return 0

    def best(self):
        return max(CHANNELS, key=lambda c: self.means[c])

    def best_at(self, turn):
        row = self.history[turn]
        return max(CHANNELS, key=lambda c: row[CHANNELS.index(c)])

    def pull(self, channel):
        self.turn += 1
        reward = self.rng.choices(OUTCOMES, weights=outcome_probs(self.means[channel]))[0]
        self.history.append(tuple(self.means[c] for c in CHANNELS))
        self.drift()
        return reward

    def drift(self):
        raise NotImplementedError("Bandit.drift")


def drift_steps(sigma, seed=7, turns=200, start=None):
    env = Bandit(seed=seed, sigma=sigma, start=start)
    steps = {c: [] for c in CHANNELS}
    for _ in range(turns):
        before = dict(env.means)
        env.pull(CHANNELS[0])
        for c in CHANNELS:
            steps[c].append(env.means[c] - before[c])
    return steps
