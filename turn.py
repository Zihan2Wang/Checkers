'''
This module contains one class, Turn, which represents the stages of the
current turn.
'''
from constants import NEW_TURN, VALID_PIECE_SELECTED, CHECK_MULTIPLE_JUMPS, \
                      MOVE_COMPLETE
import random

class Turn:
    '''
        Class -- Turn
            Represents the stages of a player's turn.
        Attributes:
            self -- the current Turn object
            player -- the player whose turn it is, black or red
            step -- the stage of the turn e.g. new turn, capture required
            valid_moves -- a dictionary of all possible valid moves for this
            player
            capture_required -- a boolean indicating if a capture is required.
            This is True if a capture is possible.
            possible_targets -- populated after a Piece is selected, a list of
            all valid Moves for that Piece. 
            final_move -- the Move that is actually made.
        Methods:
            __init__ -- constructor
            is_valid_turn -- checks if the selected Move meets the Turn
            requirements.
            is_turn_complete -- checks if the Turn is complete.
            complete_turn -- sets the step attribute to "complete".
            choose_ai_cell -- makes the AI's turn
    '''


    def __init__(self, player, valid_moves):
        '''
            Constructor -- Creates a new instance of Turn
            Parameter:
                self -- The current Turn object
                valid_moves -- A dictionary of all possible Moves for the
                current player.
        '''
        self.player = player
        self.step = NEW_TURN
        self.valid_moves = valid_moves
        self.capture_required = self.is_capture_required()
        self.possible_targets = []
        self.final_move = None


    def is_capture_required(self):
        '''
            Method -- is_capture_required
                Checks if a capture must be made.
            Parameters:
                self -- The current Turn object
            Returns:
                True if the dictionary of valid_moves contains a capturing
                Move, False otherwise.
        '''
        for piece in self.valid_moves:
            if self.valid_moves[piece][0].is_capture():
                return True
        return False


    def playable_cell_selected(self, cell_clicked):
        '''
            Method -- playable_cell_selected
                Checks if the selected cell is "playable". If the turn has
                just begun (no piece has been chosen), the cell must contain
                one of the current player's pieces. If a turn has begun (a
                piece has been chosen), the clicked cell must be a valid target
                for the chosen piece. TODO allow the user to change their mind
                and select a different piece to move
            Parameters:
                self -- The current Turn object
                cell_clicked - The cell clicked by the user
            Returns:
                True if the cell is playable, False otherwise.
        '''
        if self.step == NEW_TURN:
            return cell_clicked in self.valid_moves
        elif not self.is_turn_complete():
            return self.find_clicked_target(cell_clicked) is not None
        return False

  
    def find_clicked_target(self, cell_clicked):
        '''
            Method -- find_clicked_target
                Helper method for completing a move. Checks if the cell that
                was clicked is a valid target for the selected piece.
            Parameters:
                self -- The current Turn object
                cell_clicked -- The cell that was clicked
            Return:
                The target Cell if found or None if the clicked cell is not a
                valid target.
        '''
        for target in self.possible_targets:
            if cell_clicked == target.new_loc:
                return target
        return None


    def is_valid_turn(self, cell_clicked):
        '''
            Method -- is_valid_turn
                Checks if the selected cell is "valid". To be valid, either no
                capture is required, or, if a capture IS required, the
                selected Piece can make a capture.
            Parameters:
                self -- The current Turn object
                cell_clicked -- The cell clicked
            Returns:
                True if cell will allow the player to make a Turn meeting the
                requirements.
        '''
        if not self.playable_cell_selected(cell_clicked):
            return False
        if self.step == NEW_TURN:
            if self.allowed_start_piece(cell_clicked):
                self.finish_initial_selection(cell_clicked)
                return True
        target = self.find_clicked_target(cell_clicked)
        if target is not None and (target.is_capture() or not 
                                   self.is_capture_required()):
            self.finish_piece_move(target)
            return True
        print("A capture is possible... piece MUST be captured!")
        return False

    
    def allowed_start_piece(self, cell_clicked):
        '''
            Method -- allowed_start_piece
                Helper method called when the user selects a piece to move.
                Checks if the selected piece meets requirements.
            Parameters:
                self -- The current Turn object
                cell_clicked -- The cell clicked (or selected)
            Returns:
                True if the selected piece is allowed, False otherwise.
        '''
        return not self.is_capture_required() or \
               self.is_capture_required() and \
               self.valid_moves[cell_clicked][0].is_capture()
               

    def finish_initial_selection(self, start_loc):
        '''
            Method -- finish_initial_selection
                Helper method that updates Turn attributes when a valid
                piece is selected.
            Parameters:
                self -- the current Turn object
                start_loc -- The cell containing the selected piece
        '''
        self.step += 1
        self.possible_targets = self.valid_moves[start_loc]


    def finish_piece_move(self, move):
        '''
            Method -- finish_piece_move
                Helper method that updates Turn attributes when a piece is
                moved.
            Parameters:
                self -- the current Turn object
                move -- The Move that is being made
        '''
        self.step = CHECK_MULTIPLE_JUMPS if self.capture_required \
                    else MOVE_COMPLETE
        self.final_move = move


    def is_turn_complete(self):
        '''
            Method -- is_turn_complete
                Checks if the Turn is complete.
            Parameters:
                self -- The current Turn object
            Returns:
                True if the Turn is complete, False otherwise.
        '''
        return self.step == MOVE_COMPLETE


    def complete_turn(self):
        '''
            Method -- complete_turn
                Sets the step attribute to complete the Turn
            Parameters:
                self -- The current Turn object
        '''
        self.step = MOVE_COMPLETE


    def choose_ai_cell(self):
        '''
            Method -- choose_ai_cell
                Chooses the cells for the AI move. If there are capturing moves
                available, chooses the first option. Otherwise, picks a move at
                random.
            Parameter:
                self -- The current Turn object
        '''
        loc = None
        if self.step == NEW_TURN:
            if self.capture_required:
                for location in self.valid_moves:
                    if self.valid_moves[location][0].is_capture():
                        loc = location
                        break
            else:
                key_loc = random.randint(0, len(self.valid_moves) - 1)
                loc = list(self.valid_moves.keys())[key_loc]
            self.finish_initial_selection(loc)
        elif self.step == VALID_PIECE_SELECTED or self.step == CHECK_MULTIPLE_JUMPS:
            loc = self.possible_targets[0].new_loc
            self.finish_piece_move(self.possible_targets[0])
        return loc