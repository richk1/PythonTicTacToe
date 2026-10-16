# !/usr/bin/env python3

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

__version__ = "1.1"

from tkinter import Button, Label, StringVar, Tk
from typing import Literal

import random

type Board = list[str]
type Player = Literal["X", "O"]
type Winner = Player | Literal["no one"]

# #############################################################
class T3Brd:
    """Class to represent GUI TTT board"""

    '''List of winning board location sets'''
    winlist = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def __init__(self, parent: Tk, debug: bool = False) -> None:
        """Initialize the TTT board"""

        self.debug = debug
        self.parent = parent
        self.sq = []  # list of buttons (for gui squares)
        self.b = list(' ' * 9)  # who owns each square
        self.gameover = False
        self.next_to_move = "X"  # X always goes first

        # Setup the GUI board
        for i in range(3):
            for j in range(3):
                n = i * 3 + j
                # create button for each square
                self.sq.append(Button(parent, text=self.b[n], width=4, height=2,
                                      font=("Times", 24),
                                      command=lambda n=n: self.clikme(n)))
                # arrange buttons in a 3x3 grid
                self.sq[n].grid(row=i, column=j)

        # Create button to reset board
        self.resetB = Button(parent, text='Reset', command=self.reset_board)
        self.resetB.grid(row=3, column=0)

        # Create buttons to let computer move first (pass)
        self.passB = Button(parent, text='Pass', command=self.pass_turn)
        self.passB.grid(row=3, column=1)

        self.statusText = StringVar()
        self.set_status("Select a square, or pass")
        self.status = Label(parent, textvariable=self.statusText, font=('Helvetica', 8)).grid(row=4, columnspan=3)

    def set_status(self, message: str) -> None:
        """Set the text in the status label"""

        self.statusText.set('')
        self.parent.update_idletasks()
        self.statusText.set(message)
        self.parent.update_idletasks()

    def reset_board(self) -> None:
        """Reset the state of the board, and clear the display"""

        self.set_status("Select a square, or pass")
        self.next_to_move = "X"  # X always goes first
        self.gameover = False
        for i in range(9):
            self.b[i] = ' '
            self.sq[i].configure(text=' ', bg='white')

    def pass_turn(self):
        """Let the computer go first"""

        self.next_to_move = "O"  # Computer goes first
        # if no moves have been made, tell computer to go
        if self.emptySpaces == 9:
            ComputerMove(self)

    def clikme(self, n):
        """Called when human clicks a square"""

        if self.gameover: return
        if self.b[n] != ' ': return
        if self.next_to_move != "X": return

        # process human's move
        if HumanMove(self, n) == 0:
            # return if game over
            return

        # Tell computer to move
        ComputerMove(self)

    def color_winning_squares(self):
        """Color a TTT row red to show a win"""
        w = None

        for i in T3Brd.winlist:
            if self.b[i[0]] == self.b[i[1]] == self.b[i[2]] and self.b[i[0]] != ' ':
                w = i
                
        if w is not None: 
            for j in range(3):  
                self.sq[w[j]].configure(bg="red")

    def mark_square(self, n, mark):
        """Mark square X or O"""

        self.b[n] = mark
        self.sq[n].configure(text=mark)
        self.next_to_move = "O" if mark == "X" else "X"

    @property
    def emptySpaces(self) -> int:
        """Get how many empty spaces are on the board."""
        return sum(1 for x in self.b if x == ' ')

# End of Class T3Brd
# #############################################################

def HumanMove(brd: T3Brd, n: int) -> int:
    """Returns 0 to return control to GUI, 1 to let computer take a turn."""

    rv = 1
    if brd.b[n] != ' ': return 0  # abort if square not empty
    if brd.debug: print("user chooses " + str(n))

    # mark square with an X
    brd.mark_square(n, 'X')

    # Check for a human win
    if checkForWin(brd.b) == 'X':
        print("X wins")
        brd.set_status("X wins")
        brd.gameover = True
        brd.color_winning_squares()

    # Check for a tie
    elif brd.emptySpaces == 0:
        print("Its a tie")
        brd.set_status("Its a tie")
        brd.gameover = True
    if brd.gameover: rv = 0
    return rv

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def validMoves(b: Board) -> list[int]:
    """Create a list of valid moves for the given board.
    Args:
        b (Board): The current state of the Tic-Tac-Toe board.
    Returns:
        list[int]: A list of indices representing valid moves.
    """

    return [i for i, v in enumerate(b) if v == ' ']

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def getNewComputerMove(brd: T3Brd) -> int:
    """Get the best move for the computer
    Args:
        brd (T3Brd): The current state of the Tic-Tac-Toe board.
    Returns:
        int: The best move for the computer.
    """

    nvm = len(validMoves(brd.b))  # nvm also equals number of plays left
    mdict = scoreMoves(brd.b, 'O', nvm)
    (mm, ms) = minScore(mdict)
    if brd.debug: print(mdict)
    return mm

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def ComputerMove(brd: T3Brd) -> None:
    """Called by the GUI to make the computer's move.
    Args:
        brd (T3Brd): The current state of the Tic-Tac-Toe board.
    """

    brd.set_status('Thinking')
    m = getNewComputerMove(brd)
    if brd.debug: print("Computer chooses " + str(m))

    brd.mark_square(m, 'O')

    if checkForWin(brd.b) == 'O':
        print("O wins")
        brd.set_status("O wins")
        brd.color_winning_squares()
        brd.gameover = True
        return

    if brd.emptySpaces == 0:
        print("Its a tie")
        brd.set_status("Its a tie")
        brd.gameover = True
        return

    brd.set_status('Your move');

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def checkForWin(b: Board) -> Winner:
    '''Check to see if anyone has TTT  
    Returns 'X', 'O', or 'no one' '''

    for i in T3Brd.winlist:
        player = b[i[0]]
        if player == ' ':
            continue
        if player == b[i[1]] == b[i[2]]:
            if player == 'X': return 'X'
            if player == 'O': return 'O'
    return 'no one'

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def minScore(mlist: dict[int, int]) -> tuple[int, int]:
    """Find a move with the minimum score.
    Args:
        mlist (dict[int, int]): A dictionary mapping moves to their scores.
    Returns:
        tuple[int, int]: A tuple containing the move with the minimum score and its score.
    """
    if not mlist:
        raise ValueError("minScore requires at least one move")

    minimum_score = min(mlist.values())
    tied_moves = [m for m, s in mlist.items() if s == minimum_score]
    return random.choice(tied_moves), minimum_score

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def scoreBoard(b: Board, remaining: int) -> tuple[Winner, int]:
    '''Determine score of a board  

    Args:
        b (Board): The current state of the Tic-Tac-Toe board.
        remaining (int): The number of remaining moves.
    Returns:
        tuple[Winner, int]: A tuple containing the winner ('X', 'O', or 'no one') and the score.
    '''

    # note that when X wins score will be near 100, and when O wins score will be near 0

    # can't win unless 5 moves have been made, so 4 or less remaining
    if (remaining > 4): return ('no one', 50)
    w = checkForWin(b)
    s = 50
    # Adjust the score based on the remaining moves to prioritize faster wins and slower losses
    if w == 'X': s = 100 - 4 + remaining
    if w == 'O': s = 0 + 4 - remaining
    return (w, s)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def scoreMoves(b: Board, player: Player, depth: int) -> dict[int, int]:
    """Return the minimax score for each legal move."""
    if depth <= 0:
        return {}

    scores = {}
    other_player = 'O' if player == 'X' else 'X'

    for move in validMoves(b):
        next_board = list(b)
        next_board[move] = player
        # Use a fresh window per root move so every dictionary score is exact.
        scores[move] = minimax(
            next_board, other_player, depth - 1,
            float('-inf'), float('inf')
        )
    return scores

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def minimax(board: Board, turn: Player, remaining: int, alpha: int | float, beta: int | float) -> int | float:
    """Minimax algorithm with alpha-beta pruning.
    Args:
        board (Board): The current state of the Tic-Tac-Toe board.
        turn (Player): The player whose turn it is ('X' or 'O').
        remaining (int): The remaining depth to search.
        alpha (int | float): The alpha value for pruning. (best guaranteed value for the maximizing player X)
        beta (int | float): The beta value for pruning. (best guaranteed value for the minimizing player O)
    Returns:
        int: The minimax score for the current board state.
    """
    winner, score = scoreBoard(board, remaining)
    if winner != 'no one':
        return score

    moves = validMoves(board)

    # if out of moves and no winner
    if remaining <= 0 or not moves:
        return score

    if turn == 'X':
        best = float('-inf')
        for move in moves:
            next_board = list(board)
            next_board[move] = turn
            best = max(
                best,
                minimax(next_board, 'O', remaining - 1, alpha, beta)
            )
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best

    # Minimizing player O's turn
    best = float('inf')
    for move in moves:
        next_board = list(board)
        next_board[move] = turn
        best = min(
            best,
            minimax(next_board, 'X', remaining - 1, alpha, beta)
        )
        beta = min(beta, best)
        if alpha >= beta:
            break
    return best

# ###############################################################

if __name__ == "__main__":
    try:
        root = Tk()
        root.title("Tic-Tac-Toe")
        brd = T3Brd(root)
        root.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")
