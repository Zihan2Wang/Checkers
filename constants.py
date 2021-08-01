'''
This file contains constants used by multiple classes.
'''

# Constants to reflect the state of a cell
EMPTY = None
BLACK = 0 # Black is human
RED = 1

# Pieces can only move forward until they are kings
BLACK_DIRECTIONS = ((1, 1), (1, -1))
RED_DIRECTIONS = ((-1, 1), (-1, -1))
KING_DIRECTIONS = ((1, 1), (-1, -1), (1, -1), (-1, 1))

SIZE = 8

# Move steps
NEW_TURN = 0
VALID_PIECE_SELECTED = 1
CHECK_MULTIPLE_JUMPS = 2
MOVE_COMPLETE = 3
