import statistics

from environment import CHANNELS


def income(rewards):
    return sum(rewards) / len(rewards)


def best_share(actions, history):
    hits = 0
    for turn, channel in enumerate(actions):
        row = history[turn]
        best = max(CHANNELS, key=lambda c: row[CHANNELS.index(c)])
        if channel == best:
            hits += 1
    return hits / len(actions)


def regret(history, actions):
    total = 0.0
    for turn, channel in enumerate(actions):
        row = history[turn]
        total += max(row) - row[CHANNELS.index(channel)]
    return total / len(actions)


def spread(values):
    q1, _, q3 = statistics.quantiles(values, n=4)
    return statistics.median(values), q1, q3


def cell(median, q1, q3, scale=100, template="%.0f%% [%.0f–%.0f]"):
    return template % (median * scale, q1 * scale, q3 * scale)
