# Base agent: the Q table and the choice of a move.
#
# Q is a dict (state, cell) -> estimate of the chance to win.
# It starts at zeros: "I know nothing about anything".

from game import closed_cells


class Agent:
    def __init__(self):
        self.table = {}

    def q(self, state, action):
        return self.table.get((state, action), 0.0)

    def choose(self, state, rng, epsilon):
        # ε-greedy choice: with probability epsilon — at random, otherwise — the best.
        # On equal Q the lower-numbered cell wins (strict `>` in the loop);
        # the same order is used in top — otherwise the slide would show one cell
        # while the agent opened another one in class.
        closed = closed_cells(state)
        if rng.random() < epsilon:
            return rng.choice(closed)
        best, best_q = None, None
        for a in closed:
            v = self.q(state, a)
            if best_q is None or v > best_q:
                best, best_q = a, v
        return best

    def top(self, state, k=3):
        # The best k closed cells with their estimates — for the demo in class.
        scored = sorted(
            closed_cells(state), key=lambda a: (-self.q(state, a), a)
        )
        return [(self.q(state, a), a) for a in scored[:k]]
