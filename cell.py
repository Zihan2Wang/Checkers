'''
This module contains one class, Cell, which represents one cell on the board.
'''
class Cell:
    '''
        Class -- Cell
            Represents a single cell on the board.
        Attributes:
            self -- the current Cell object
            playable -- an int storing the color index of the cell: 0 for white
            1 for dark. This can be used as a boolean indicating whether or
            not the cell is playable (dark cells can be used, white cannot).
            location -- a tuple storing the cell's location on the board.
            occupant -- stores information about the cell's occupant. Either
            empty or a Piece object.
        Methods:
            __init__ -- constructor
            contains_piece -- checks if this cell contains a Piece
            is_empty -- checks if this cell is empty
            __str__ -- a string representation of the move
    '''
    def __init__(self, playable, location, occupant):
        '''
            Constructor -- Creates a new instance of Cell
            Parameter:
                self -- The current Cell object
                playable -- an int storing the color index of the cell: 0 for white
                1 for dark. This can be used as a boolean indicating whether or
                not the cell is playable (dark cells can be used, white cannot).
                location -- a tuple storing the cell's location on the board.
                occupant -- stores information about the cell's occupant. Either
                empty or a Piece object.
        '''
        self.playable = playable
        self.location = location
        self.occupant = occupant


    def contains_piece(self, color):
        '''
            Method -- contains_piece
                Checks if the Cell contains a Piece of the given color.
            Parameters:
                self -- The current Cell object
                color -- The piece color, black or red
            Returns:
                True if the Cell contains a Piece of the given color, False
                otherwise.
        '''
        if self.is_empty():
            return False
        return self.occupant.color == color


    def is_empty(self):
        '''
            Method -- is_empty
                Checks if the Cell is empty.
            Parameters:
                self -- The current Cell object
            Returns:
                True if the Cell is empty, False otherwise.
        '''
        return self.occupant == None

    def __str__(self):
        '''
            Method -- __str__
                Creates a string representation of the Cell
            Parameters:
                self -- The current Cell object
            Returns:
                A string representation of the Cell
        '''
        return "Cell: " + str(self.playable) + ", location: " + \
            str(self.location) + " occupant: " + str(self.occupant)