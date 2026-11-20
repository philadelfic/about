# Run modes: selftest, random, train, ladder, sarsa, show, vs.
#
# All the "physics" of learning lives in learn_episode and evaluate; the modes only
# call them and print results. The numbers on the seminar slides come from these modes.

import random
import time

import game
import knobs
from qagent import QAgent
from sarsa import SarsaAgent


def learn_episode(agent, rng, alpha, epsilon):
    # One game: the agent plays to the end, the table is updated move by move.
    # The update is delayed by one step: SARSA needs the move the agent will make from s'.
    state = game.initial_state()
    mines = None
    pending = None
    while True:
        action = agent.choose(state, rng, epsilon)
        if mines is None:
            # first move: no mines yet, the cell becomes safe
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
            print(f"  training: {i + 1:,} / {episodes:,} games")
    return wins / episodes


def evaluate(agent, games, seed):
    # Greedy play without random probes — we measure what has been learned.
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
    # Lower bound: a random cell, no table at all.
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


# ---------- modes ----------

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
    print(f"random player, {games:,} games: wins {share:.1%} "
          f"({time.time() - t0:.1f} s)")


def cmd_train(episodes, alpha, epsilon, seed, eval_games,
              agent_cls=QAgent, title=None):
    if title:
        print(title)
    t0 = time.time()
    agent = agent_cls()
    train_win = train(agent, episodes, alpha, epsilon, seed)
    dt = time.time() - t0
    eval_win = evaluate(agent, eval_games, seed + 1000)
    print(f"training games: {episodes:,}  (training wins {train_win:.1%}, {dt:.1f} s)")
    print(f"table: {len(agent.table):,} (state, cell) pairs")
    print(f"greedy play, {eval_games:,} games: wins {eval_win:.1%}")


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
        print(f"{n:>9,} games -> wins {eval_win:6.1%}  "
              f"(table {len(agent.table):>7,}, {dt:5.1f} s)")
        n *= 10


def _greedy_opening(agent, seed, after):
    # The first `after` greedy moves on a fixed board — a position for a bet.
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
    # The board after `after` agent moves + its estimates for closed cells.
    # This is the position for the audience bet: first the bet, then the reveal.
    agent = agent_cls()
    t0 = time.time()
    train(agent, episodes, alpha, epsilon, knobs.SEED, quiet=True)
    state, mines = _greedy_opening(agent, seed, after)
    print(f"board {seed}: {agent_name(agent_cls)} trained on {episodes:,} games "
          f"({time.time()-t0:.0f} s)")
    print("agent moves: " + str(after) + ", board (dot = closed):")
    print()
    print(game.render(state))
    print()
    print("agent estimates (chance to win after opening this cell):")
    for v, a in agent.top(state, k=5):
        r, c = divmod(a, knobs.FIELD)
        print(f"  cell ({r + 1},{c + 1}): {v:+.3f}")
    print()
    print("mine placement for checking (spoiler):", sorted(m + 1 for m in mines))


def cmd_vs(episodes, alpha, epsilon, seed, agent_cls=QAgent):
    # A human against the machine on one board.
    # The human enters a cell as "row column" (for example 2 3), the agent answers
    # with its own move. Whoever hits a mine loses; whoever opens everything wins.
    rng = random.Random(seed)
    agent = agent_cls()
    print(f"{agent_name(agent_cls)} is training: {episodes:,} games...")
    train(agent, episodes, alpha, epsilon, knobs.SEED)
    state = game.initial_state()
    mines = None
    turn = "human"
    while True:
        print()
        print(game.render(state))
        if turn == "human":
            try:
                raw = input("your cell (row column): ").split()
            except EOFError:
                print("game interrupted")
                return
            if len(raw) < 2:
                print("not allowed: enter two coordinates, for example 2 3")
                continue
            try:
                r, c = int(raw[0]) - 1, int(raw[1]) - 1
            except ValueError:
                print("not allowed: coordinates must be numbers, for example 2 3")
                continue
            if not (0 <= r < knobs.FIELD and 0 <= c < knobs.FIELD) \
                    or state[r * knobs.FIELD + c] != game.CLOSED:
                print("not allowed: cell is off the board or already open")
                continue
            action = r * knobs.FIELD + c
            print(f"you open ({r + 1},{c + 1})")
        else:
            action = agent.choose(state, rng, 0.0)
            r, c = divmod(action, knobs.FIELD)
            print(f"agent opens ({r + 1},{c + 1})")
        if mines is None:
            mines = game.new_mines(rng, safe=action)
        state, reward, done = game.open_cell(state, mines, action)
        if done:
            print()
            print(game.render(state, mines=mines))
            if reward > 0:
                print("Last cell is safe. " + outcome(turn, True).capitalize())
            else:
                print("Mine. " + outcome(turn, False).capitalize())
            break
        turn = "agent" if turn == "human" else "human"


def agent_name(agent_cls):
    # How to name the strategy in the output.
    return "SARSA" if agent_cls is SarsaAgent else "Q-learning"


def outcome(turn, won):
    # The result in words: "you won" / "agent lost" — no case gymnastics.
    if turn == "human":
        return "you won" if won else "you lost"
    return "agent won" if won else "agent lost"
