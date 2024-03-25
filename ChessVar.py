# Author: Liam Bradley
# GitHub username: libradley
# Date: 10Dec23
# Description: Wrote a class named ChessVar that allows you to move chess pieces with the
# goal of capturing all of one type to win the game

class ChessVar:
    """This class contains the functions needed to set the chess board, make and verify moves, and
    switch turns. """

    def __init__(self):
        """Initial method that will contain the board, the turn. and the game state"""
        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

        self._game_state = 'UNFINISHED'
        self._current_player = 'WHITE'
        # Dictionary to track how many pieces each team has left
        self._pieces = {'WHITE': {'P': 8, 'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1},
                        'BLACK': {'p': 8, 'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1}}

    def get_board(self):
        """This method is used to return the game board"""
        return self._board

    def get_player(self):
        """This method is used to return the current player"""
        return self._current_player

    def get_game_state(self):
        """This method tells us if the game is completed or not"""
        return self._game_state

    def make_move(self, move_from, move_to):
        """This method moves a piece from one location to another on the board"""
        if self._game_state != 'UNFINISHED':
            return False

        # Use ASCII values to move the pieces
        from_row, from_col = 8 - int(move_from[1]), ord(move_from[0]) - ord('a')
        to_row, to_col = 8 - int(move_to[1]), ord(move_to[0]) - ord('a')

        # Check if the move is valid
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False

        # Moves pieces and replaces the original position with an empty space
        self._board[to_row][to_col] = self._board[from_row][from_col]
        self._board[from_row][from_col] = ' '

        # Capture opposing piece
        # Need to implement a way to update self._pieces count dictionary when a piece is captured
        if self._board[to_row][to_col].islower():
            capture_piece = self._board[to_row][to_col].upper()
            self._pieces[self._current_player][f'{capture_piece}'] -= 1
            self.remove_piece(capture_piece)

        if self._board[to_row][to_col].isupper():
            capture_piece = self._board[to_row][to_col].lower()
            self._pieces[self._current_player][f'{capture_piece}'] -= 1
            self.remove_piece(capture_piece)

        # Update the game state
        self.update_game_state()

        # Update player turn
        self._current_player = 'BLACK' if self._current_player == 'WHITE' else 'WHITE'

        return True

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """This method will see if a certain piece is able to move to a certain spot"""
        if self._board[from_row][from_col].islower() and self._current_player == 'WHITE':
            return False
        if self._board[from_row][from_col].isupper() and self._current_player == 'BLACK':
            return False

        # Checks if player is moving on or through its own pieces
        if self._board[to_row][to_col].isupper() and self._current_player == "WHITE":
            return False

        if self._board[to_row][to_col].islower() and self._current_player == "BLACK":
            return False

        # Checks to see if a move is out of bounds
        if not (0 <= from_row < 8) or not (0 <= from_col < 8) or not (0 <= to_row < 8) or not (0 <= to_col < 8):
            return False
        # Validate moves for each piece
        piece = self._board[from_row][from_col]
        if piece.lower() == 'p' and not self.is_valid_pawn_move(from_row, from_col, to_row, to_col):
            return False
        if piece.lower() == 'n' and not self.is_valid_knight_move(from_row, from_col, to_row, to_col):
            return False
        if piece.lower() == 'b' and not self.is_valid_bishop_move(from_row, from_col, to_row, to_col):
            return False
        if piece.lower() == 'r' and not self.is_valid_rook_move(from_row, from_col, to_row, to_col):
            return False
        if piece.lower() == 'q' and not self.is_valid_queen_move(from_row, from_col, to_row, to_col):
            return False
        if piece.lower() == 'k' and not self.is_valid_king_move(from_row, from_col, to_row, to_col):
            return False

        return True

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the pawn movement is valid"""
        piece = self._board[from_row][from_col]
        direction = 1 if piece.islower() else -1

        # Check if Pawn is moving regularly
        if from_col == to_col and self._board[to_row][to_col] == ' ':
            if from_row + direction == to_row:
                return True
            elif from_row + 2 * direction == to_row and from_row == 1 and piece.islower():
                return True
            elif from_row - 2 * direction == to_row and from_row == 6 and piece.isupper():
                return True

        # Check to see if the pawn is trying to capture
        if abs(from_col - to_col) == 1 and from_row + direction == to_row:
            if self._board[to_row][to_col].islower() and piece.isupper():
                return True
            elif self._board[to_row][to_col].isupper() and piece.islower():
                return True

        return False

    def is_valid_knight_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the knight move is valid"""
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the bishop move is valid"""
        return abs(from_row - to_row) == abs(from_col - to_col)

    def is_valid_rook_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the rook move is valid"""
        return from_row == to_row or from_col == to_col

    def is_valid_queen_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the queen move is valid"""
        return self.is_valid_bishop_move(from_row, from_col, to_row, to_col) or self.is_valid_rook_move(from_row, from_col, to_row, to_col)

    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        """This method is used to check if the king move is valid"""
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return row_diff <= 1 and col_diff <= 1

    def remove_piece(self, piece):
        """This method is used to remove a piece after it is captured"""
        for row in range(8):
            for col in range(8):
                if self._board[row][col] == piece:
                    self._board[row][col] = ' '

    def update_game_state(self):
        """This method is used to update the game state after a player wins"""
        for piece, count in self._pieces[self._current_player].items():
            if count == 0:
                self._game_state = f'{self._current_player.upper()}_WON'


