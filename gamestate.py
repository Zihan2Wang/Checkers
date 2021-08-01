'''
This module contains one class, Game, which represents the game state. It is
responsible for tracking the locations of each piece, finding valid moves, and
tracking both players' scores.
'''
from cell import Cell
from board import Board
from move import Move
from turn import Turn
from piece import Piece
from constants import BLACK, RED, EMPTY, KING_DIRECTIONS, BLACK_DIRECTIONS, RED_DIRECTIONS, SIZE

BLACK_KING_ROW = 7
RED_KING_ROW = 0

class Game:
    '''
        Class -- Game
            Represents the game state.
        Attributes:
            self -- the current Game object
            black_score -- black's current score
            red_score -- red's current score
            board -- the game Board
            status -- the current status of the game, a list of Cells
            current_turn -- a Turn object representing the player whose turn it
            is and their possible moves
            black_possible_moves -- the possible Moves for the black player
            red_possible_moves -- the possible Moves for the red player
            winner -- The game winner. Empty to start.
        Methods:
            update_state -- Update the game state after a move
            get_additional_jumps -- If a capture has taken place, check if
            another could be made.
            extend_turn -- If a capture has taken place and additional jumps
            are available, the current turn is extended
            advance_turn -- Advances to the next player's turn.
    '''

    def __init__(self):
        '''
            Constructor -- Creates a new instance of Game
            Parameter:
                self -- The current Game object
        '''
        self.new_game()
        self.black_score = 0
        self.red_score = 0
        self.winner = EMPTY
        self.board = Board(self)

    def new_game(self):
        '''
            Method -- new_game
                Creates and populates the Game's status and current_turn
                attributes.
            Parameters:
                self -- The current Game object
        '''
        self.status = []
        # row, col starts in bottom left
        for row in range(SIZE):
            for col in range(SIZE):
                if col == 0:
                    self.status.append([])
                self.status[row].append(Cell(self.is_dark(row, col),
                                             (row, col),
                                             self.get_start_state(row, col)))
        self.populate_valid_moves()
        self.current_turn = Turn(BLACK, self.black_possible_moves)
    

    def is_dark(self, row, col):
        '''
            Method -- is_dark
                Determines if a cell's background color should be dark based on
                its location on the board.
            Parameters:
                self -- The current Game object
                row -- The cell's row number
                col -- The cell's column number
            Returns:
                True if the cell is dark, False otherwise
        '''
        return row % 2 == 0 and col % 2 == 0 or row % 2 == 1 and col % 2 == 1

    def get_start_state(self, row, col):
        '''
            Method -- get_start_state
                Get's the start state for a location on the board: empty,
                contains a black piece, or contains a red piece.
            Parameters:
                self -- The current Game object
                row -- The cell's row number
                col -- The cell's column number
            Returns:
                Empty, a black Piece, or a red Piece
        '''
        BLACK_START_ROW = 0
        BLACK_END_ROW = 2
        RED_START_ROW = 5
        if self.is_dark(row, col) or row > BLACK_END_ROW and \
           row < RED_START_ROW:
            return EMPTY
        if row >= BLACK_START_ROW and row <= BLACK_END_ROW:
            return Piece(BLACK, BLACK_DIRECTIONS)
        return Piece(RED, RED_DIRECTIONS)

    def populate_valid_moves(self):
        '''
            Method -- populate_valid_moves
                Populates the possible moves lists for both players.
            Parameters:
                self -- The current Game object
        '''
        self.black_possible_moves = self.valid_moves_for_color(BLACK)
        self.red_possible_moves = self.valid_moves_for_color(RED)
        self.check_game_over()
        

    def check_game_over(self):
        '''
            Method -- check_game_over
                Checks if the game is over. If it is, sets the winner attribute
            Parameters:
                self -- The current Game object
        '''
        if len(self.black_possible_moves) == 0:
            self.winner = RED
        elif len(self.red_possible_moves) == 0:
            self.winner = BLACK

    def valid_moves_for_color(self, piece_color):
        '''
            Method -- valid_moves_for_color
                Populates the possible moves dictionaries for a specific 
                player. Each key is the tuple location of a piece of the
                given color.
            Parameters:
                self -- The current Game object
                piece_color -- The color of the playing piece
            Returns:
                A dictionary of pieces (of the given color) that have possible
                moves. Each key is a piece location. Each value is a list of
                Moves from the piece's location.
        '''
        possible_moves = {}
        pieces = self.all_cells_containing_color(piece_color)
        for location in pieces:
            moves = self.get_moves_for_piece(location, piece_color)
            if len(moves) > 0:
                possible_moves[location] = moves
        return possible_moves

    def all_cells_containing_color(self, piece_color):
        '''
            Method -- all_cells_containing_color
                Finds all cells that contain pieces of the given color.
            Parameters:
                self -- The current Game object
                piece_color -- The color of the playing piece
            Returns:
                A list of locations (tuples) containing pieces of the color.
        '''
        pieces = []
        for row in range(len(self.status)):
            for col in range(len(self.status[row])):
                if self.status[row][col].contains_piece(piece_color):
                    pieces.append((row, col))
        return pieces

    def get_next_cell_in_direction(self, start, direction):
        '''
            Method -- get_next_cell_in_direction
                Gets the next location in a particular direction (up, left etc)
            Parameters:
                self -- The current Game object
                start -- The start location
                direction -- The direction to move in
            Returns:
                A tuple containing the next location
        '''
        return (start[0] + direction[0], start[1] + direction[1])

    def get_moves_for_piece(self, cell_loc, piece_color):
        '''
            Method -- get_moves_for_piece
                Gets all the valid Moves a piece can make. Capturing Moves are
                at the beginning of the list (if any exist).
            Parameters:
                self -- The current Game object
                cell_loc -- The start location
                piece_color -- The color of the start piece.
            Returns:
                A list of valid moves.
        '''
        moves = []
        cell = self.status[cell_loc[0]][cell_loc[1]]
        for direction in cell.occupant.piece_directions:
            next_loc = self.get_next_cell_in_direction(cell.location,
                                                        direction)
            move = self.create_move(cell.location, next_loc, direction,
                                    piece_color)
            if move is not None:
                if move.is_capture():
                    moves.insert(0, move)
                else:
                    moves.append(move)
        return moves

    
    def create_move(self, start, next_cell, direction, piece_color):
        '''
            Method -- create_move
                Creates a Move object if a move is possible from the start
                cell and in the given direction.
            Parameters:
                self -- The current Game object
                start -- The start location
                next_cell -- The adjacent cell in the given direction
                direction -- The direction to move in (for capturing moves)
            Returns:
                A Move, if one is available, or None if there isn't a valid
                move in this direction.
        '''
        move = None
        if not self.is_valid_cell(next_cell[0], next_cell[1]):
            return move
        # A non-capturing move
        check_cell = self.status[next_cell[0]][next_cell[1]]
        if check_cell.is_empty():
            move = Move(start, next_cell, None)
        # A possible capturing move
        elif check_cell.occupant.is_enemy(piece_color):
            end_loc = self.get_next_cell_in_direction(next_cell, direction)
            if self.is_valid_cell(end_loc[0], end_loc[1]) and \
               self.status[end_loc[0]][end_loc[1]].is_empty():
                move = Move(start, end_loc, check_cell)
        return move


    def get_additional_jump(self, start_cell, piece_color):
        '''
            Method -- get_additional_jump
                Gets all the additional capturing moves the current piece can
                make.
            Parameters:
                self -- The current Game object
                start_cell -- The start location
                piece_color -- The color of the start piece.
            Returns:
                A list of valid capturing moves.
        '''
        possible_capture = []
        moves = self.valid_moves_for_color(piece_color)
        if start_cell.location in moves:
            for move in moves[start_cell.location]:
                if move.is_capture():
                    possible_capture.append(move)
                else:
                    break
        if len(possible_capture) == 0:
            self.current_turn.complete_turn()
        return possible_capture

    def extend_turn(self, options):
        '''
            Method -- extend_turn
                Allows the current turn to continue. Happens if a capture has
                been made and more are available for the active piece.
            Parameters:
                self -- The current Game object
                options -- A list of capturing Moves for the current piece
        '''
        self.current_turn.final_move = None
        self.current_turn.possible_targets = options

    def is_valid_cell(self, row, col):
        '''
            Method -- is_valid_cell
                Checks if a row/col location is on the board.
            Parameters:
                self -- The current Game object
                row -- The cell's row number
                col -- The cell's column number
            Returns:
                True if the row/col is a cell
        '''
        return row >= 0 and row < SIZE and col >= 0 and col < SIZE

    def update_state(self, move):
        '''
            Method -- update_state
                Updates the game's status after a move. This updates the piece
                locations, the scores, and upgrades the piece if necessary.
            Parameters:
                self -- The current Game object
                move -- The completed Move
        '''
        new_cell = self.status[move.new_loc[0]][move.new_loc[1]]
        old_cell = self.status[move.current_loc[0]][move.current_loc[1]]
        new_cell.occupant = old_cell.occupant
        if move.new_loc[0] == BLACK_KING_ROW and new_cell.contains_piece(BLACK) \
            or move.new_loc[0] == RED_KING_ROW and new_cell.contains_piece(RED):
            new_cell.occupant.make_king()
        old_cell.occupant = EMPTY
        if move.is_capture():
            if self.current_turn.player == BLACK:
                self.black_score += 1
            else:
                self.red_score += 1
            move.capturing.occupant = EMPTY


    def advance_turn(self):
        '''
            Method -- advance_turn
                Advances the current turn, as long as the next player can move.
            Parameters:
                self -- The current Game object
        '''
        self.populate_valid_moves()
        if self.current_turn.player == BLACK and \
           len(self.red_possible_moves) > 0: 
            self.current_turn = Turn(RED, self.red_possible_moves)
        elif len(self.black_possible_moves) > 0:
            self.current_turn  = Turn(BLACK, self.black_possible_moves)

