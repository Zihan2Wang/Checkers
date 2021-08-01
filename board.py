'''
This module contains one class, Board, which creates and updates the UI.
'''
import turtle
import time
from constants import SIZE, EMPTY, VALID_PIECE_SELECTED, \
    BLACK, RED, NEW_TURN
from cell import Cell

class Board:
    '''
        Class -- Board
            The game UI.
        Attributes:
            self -- the current Board object
            high_bound -- the top/right edge of the board in pixels
            low_bound -- the bottom/left edge of the board in pixels
            game_state -- a reference to the Game object controlling this game
            graphics -- the Turtle object that
        Methods:
            No methods used by other classes.
    '''
    SQUARE = 50
    CELL_COLORS = ("light gray", "white")
    PIECE_COLORS = ("black", "firebrick")
    RADIUS = 24
    KING_RADIUS = 16

    def __init__(self, game_ref):
        '''
            Constructor -- Creates a new instance of Board
            Parameter:
                self -- The current Turn object
                game_ref -- The Game object that stores the game state
        '''
        turtle.setup(SIZE * self.SQUARE + self.SQUARE,
                     SIZE * self.SQUARE + self.SQUARE)
        turtle.screensize(SIZE * self.SQUARE, SIZE * self.SQUARE)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)

        self.high_bound = self.SQUARE * SIZE/2
        self.low_bound = 0 - self.high_bound
        self.game_state = game_ref

        # Create the Turtle to draw the board
        self.graphics = turtle.Turtle()
        self.graphics.penup()
        self.graphics.hideturtle()

        # Line color is black, fill color is gray
        self.graphics.color("black", self.CELL_COLORS[0])

        # Move the Turtle to the upper left corner
        self.corner = -SIZE * self.SQUARE / 2
        self.graphics.setposition(self.corner, self.corner)

        # Draw the board
        self.draw_square(self.SQUARE * SIZE)
        self.draw_cells(self.game_state.status)

        self.screen = turtle.Screen()
        self.screen.onclick(self.board_click)
        turtle.done()


    def draw_square(self, width):
        '''
            Method -- draw_square
                Draws a square of a given size.
            Parameters:
                self -- the current Board object
                width -- the width of each side
        '''
        self.graphics.pendown()
        for i in range(4):
            self.graphics.forward(width)
            self.graphics.left(90)
        self.graphics.penup()

    def draw_cells(self, cells):
        '''
            Method -- draw_cells
                Draw all the cells.
            Parameters:
                self -- the current Board object
                cells -- a list of Cells
        '''
        # Draw the gray squares
        for row in range(len(cells)):
            for col in range(len(cells[row])):
                self.draw_cell(cells[row][col])

    def draw_cell(self, cell):
        '''
            Method -- draw_cell
                Draw an individual cell.
            Parameters:
                self -- the current Board object
                cells -- the Cell to draw
        '''
        self.graphics.setposition(self.corner + self.SQUARE * cell.location[1],
                                  self.corner + self.SQUARE * cell.location[0])
        # Draw the background
        color = self.CELL_COLORS[int(cell.playable)]
        self.graphics.color("dark gray", color)  
        self.graphics.begin_fill()
        self.draw_square(self.SQUARE)
        self.graphics.end_fill()

        # Draw the piece if necessary
        if not cell.is_empty():
            self.draw_piece(cell)

    def draw_piece(self, cell):
        '''
            Method -- draw_piece
                Draw a piece.
            Parameters:
                self -- the current Board object
                cell -- the Cell that contains the Piece
        '''
        center = self.get_center(cell.location[0], cell.location[1], self.RADIUS)
        self.graphics.setposition(center[0], center[1])
        self.graphics.pendown()
        self.graphics.begin_fill()
        self.graphics.color(self.PIECE_COLORS[cell.occupant.color], self.PIECE_COLORS[cell.occupant.color])
        self.graphics.circle(self.RADIUS)
        self.graphics.end_fill()
        self.graphics.penup()
        if cell.occupant.is_king:
            self.graphics.pencolor("white")
            center = self.get_center(cell.location[0], cell.location[1],
                                     self.KING_RADIUS)
            self.graphics.setposition(center[0], center[1])
            self.graphics.pendown()
            self.graphics.circle(self.KING_RADIUS)
            self.graphics.penup()


    def highlight_choice(self, selected_loc, targets):
        '''
            Method -- highlight_choice
                Highlight the piece selected by the player and the possible
                moves for that piece
            Parameters:
                self -- the current Board object
                selected_loc -- the selected cell
                targets -- a list of cells that the piece could move to
        '''
        self.graphics.pencolor("deep sky blue")
        self.graphics.setposition(self.corner + self.SQUARE * selected_loc[1],
                                  self.corner + self.SQUARE * selected_loc[0])
        self.draw_square(self.SQUARE)
        self.graphics.pencolor("red")
        for target in targets:
            self.graphics.setposition(self.corner + self.SQUARE * \
                                      target.new_loc[1], self.corner + \
                                      self.SQUARE * target.new_loc[0])
            self.draw_square(self.SQUARE)


    def clear_highlights(self, selected_loc, targets):
        '''
            Method -- clear_highlights
                Remove the highlights on a cell
            Parameters:
                self -- the current Board object
                selected_loc -- the originally selected cell
                targets -- a list of cells that the piece could move to
        '''
        self.graphics.pencolor("dark gray")
        self.graphics.setposition(self.corner + self.SQUARE * selected_loc[1], self.corner + self.SQUARE * selected_loc[0])
        self.draw_square(self.SQUARE)
        for target in targets:
            self.graphics.setposition(self.corner + self.SQUARE * target.new_loc[1], self.corner + self.SQUARE * target.new_loc[0])
            self.draw_square(self.SQUARE)

    def get_center(self, row, col, radius):
        '''
            Method -- get_center
                Gets the center point of a cell for drawing pieces
            Parameters:
                self -- the current Board object
                row -- the cell row
                col -- the cell column
                radius -- the radius of the piece
        '''
        x = col * self.SQUARE +self.SQUARE / 2 + self.low_bound
        y = row * self.SQUARE + (self.SQUARE / 2) - radius + self.low_bound
        return (x, y)

    def board_click(self, x, y):
        '''
            Method -- board_click
                The click event listener. Handles the human's turn.
            Parameters:
                self -- the current Board object
                x -- The X coordinate of the click
                y -- The Y coordinate of the click
        '''
        if self.is_in_bounds(x, y) and self.game_state.current_turn.player == BLACK:
            location = (self.get_cell(y), self.get_cell(x))
            if self.game_state.current_turn.is_valid_turn(location):
                self.make_move(location)
                if self.game_state.current_turn.is_turn_complete():
                    self.next_player() # OR CALL FROM TURN (WHEN COMPLETES)

    # TRY SPLITTIng THIS TO MAkE DELAY - IF HAPPENS BUT ELSE IS DELAYED
    def make_move(self, location):
        '''
            Method -- make_move
                Updates the board after a click
            Parameters:
                self -- the current Board object
                location -- the clicked cell
        '''
        if self.game_state.current_turn.step == VALID_PIECE_SELECTED:
            self.highlight_choice(location, 
                                 self.game_state.current_turn.possible_targets)
        else:
            move = self.game_state.current_turn.final_move
            self.clear_highlights(move.current_loc, 
                                 self.game_state.current_turn.possible_targets)
            self.game_state.update_state(move)
            self.draw_cell(self.game_state.status[move.current_loc[0]]\
                                                 [move.current_loc[1]])
            self.draw_cell(self.game_state.status[move.new_loc[0]]\
                                                 [move.new_loc[1]])
            if move.is_capture():
                self.draw_cell(move.capturing)
                # Check if there is another capture available from the new cell
                additional_jumps = self.game_state.get_additional_jump(
                                        self.game_state.status[move.new_loc[0]]
                                                              [move.new_loc[1]],
                                        self.game_state.current_turn.player)
                if len(additional_jumps) > 0:
                    self.game_state.extend_turn(additional_jumps)
                    self.highlight_choice(move.new_loc, additional_jumps)    

    def is_in_bounds(self, x, y):
        '''
            Method -- is_in_bounds
                Checks if the click was in bounds of the board
            Parameters:
                self -- the current Board object
                x -- the X coordinate of the click
                y -- the Y coordinate of the click
            Returns:
                True if the click is in bounds, False otherwise.
        '''
        if x >= self.low_bound and x <= self.high_bound and \
           y >= self.low_bound and y <= self.high_bound:
            return True
        return False
    
    def get_cell(self, val):
        '''
            Method -- get_cell
                Converts a click coordinate to a cell location.
            Parameters:
                self -- the current Board object
                val -- the click location (x or y)
            Returns:
                The index of the cell that was clicked. Works for row and col.
        '''
        scaled = val - self.low_bound
        return int(scaled // self.SQUARE)

    def next_player(self):
        '''
            Method -- next_player
                Advances to the next player's turn or ends the game if no-one
                can move.
            Parameters:
                self -- the current Board object
        '''
        self.game_state.advance_turn()
        if self.game_state.winner is not EMPTY:
            self.end_game()
            print("GAME OVER")
        elif self.game_state.current_turn.player == RED:
            self.screen.ontimer(self.ai_move, 1000)
            #self.ai_move()

    def end_game(self):
        '''
            Method -- end_game
                Draws the game over message
            Parameters:
                self -- the current Board object
        '''
        self.graphics.setposition(0, 50)
        self.graphics.color("green")
        style = ("Courier", 48, "bold")
        self.graphics.write("Game Over!", font=style, align="center")
        self.graphics.setposition(0, -50)
        if self.game_state.winner == RED:
            self.graphics.write("Computer wins", font=style, align="center")
        else:
            self.graphics.write("You win", font=style, align="center")
    
    def ai_move(self):
        '''
            Method -- ai_move
                Handles the AI move
            Parameters:
                self -- the current Board object
        '''
        location = self.game_state.current_turn.choose_ai_cell()
        self.make_move(location)
        print("AI moved to", location)
        if self.game_state.current_turn.player == RED and \
           not self.game_state.current_turn.is_turn_complete():
            print("b")
            self.screen.ontimer(self.ai_move, 2000)
            #self.ai_move()
        else:
            print("Black's turn")
            self.game_state.advance_turn()