# Simulator knobs: every letter from the seminar lives here.
# Change them from the console only — see the flags in README.md.

FIELD = 4          # board is FIELD x FIELD
MINES = 2          # mines on the board
GAMMA = 1.0        # episodic task: the return is not discounted

ALPHA = 0.1        # forgetting rate (the same letter as in the cafe)
EPSILON = 0.1      # share of random probes

SEED = 42          # default seed
