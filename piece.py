'''
This module contains one class, Piece, which represents a game piece.
'''
from constants import KING_DIRECTIONS


class Piece:
    '''
        Class -- Piece
            Represents a game piece.
        Attributes:
            self -- the current Piece object
            color -- the piece's color
            piece_directions -- a list of directions that the piece can move in
            is_king -- True if the piece is a king, False otherwise.
        Methods:
            __init__ -- constructor
            is_enemy -- Checks if this Piece is a player's enemy
            make_king -- Converts this Piece into a king
    '''


    def __init__(self, color, piece_directions):
        '''
            Constructor -- Creates a new instance of Piece
            Parameter:
                self -- The current Piece object
                color -- The Piece's color.
                piece_directions -- A list of tuples storing the directions
                that the piece can move in.
        '''
        self.color = color
        self.piece_directions = piece_directions
        self.is_king = False


    def is_enemy(self, player):
        '''
            Method -- is_enemey
                Checks if this piece is the enemy of the given player. E.g. if
                this piece is black and player is red, then this piece is the
                enemy.
            Parameters:
                self -- The current Piece object
                player -- The color of the other piece.
            Returns:
                True if this piece is the enemy of player, False otherwise.
        '''
        return self.color is not player


    def make_king(self):
        '''
            Method -- make_king
                Makes this piece a king.
            Parameters:
                self -- The current Piece object
        '''
        self.piece_directions = KING_DIRECTIONS
        self.is_king = True
