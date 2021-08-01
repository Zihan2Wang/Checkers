'''
This module contains one class, Move, which represents a single valid Move for
one piece. A single move means one location change. Capturing moves that take
multiple pieces are represented as multiple Moves—-one per jump.
'''
class Move:
    '''
        Class -- Move
            Represents a single valid Move for one Piece.
        Attributes:
            self -- the current Move object
            current_loc -- the start cell
            new_loc -- the end cell
            capturing -- stores a tuple of the captured location, if applicable
        Methods:
            __init__ -- constructor
            is_capture -- checks if this is a capturing move
            __str__ -- a string representation of the move
    '''
    def __init__(self, current_loc, new_loc, capturing):
        self.current_loc = current_loc
        self.new_loc = new_loc
        self.capturing = capturing

    def is_capture(self):
        return self.capturing is not None

    def __str__(self):
        if self.is_capture():
            return str(self.current_loc) + " to " + str(self.new_loc) + " CAPTURE"
        return str(self.current_loc) + " to " + str(self.new_loc)
