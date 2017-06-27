# !/usr/bin/env python3

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

__version__ = "1.0"

# tkinter for py3, Tkinter for py2
from tkinter import *
import random

dbg = False


# #############################################################
class T3Brd:
    """Class to represent GUI TTT board"""

    '''List of winning board location sets'''
    winlist = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def __init__(self, parent):
        """Initialize the TTT board"""

        self.parent = parent
        self.sq = []  # list of buttons (for gui squares)
        self.b = list(' ' * 9)  # who owns each square
        self.gameover = False

        # Setup the GUI board
        for i in range(3):
            for j in range(3):
                n = i * 3 + j
                # create button for each square
                self.sq.append(Button(parent, text=self.b[n], width=4, height=2,
                                      font=("Times", "24"),
                                      command=lambda k=n: self.clikme(k)))
                # arrange buttons in a 3x3 grid
                self.sq[n].grid(row=i, column=j)

        # Create button to reset board
        self.resetB = Button(parent, text='Reset', command=self.reset_f)
        self.resetB.grid(row=3, column=0)

        # Create buttons to let computer move first (pass)
        self.passB = Button(parent, text='Pass', command=self.passF).grid(row=3, column=1)

        self.statusText = StringVar()
        self.set_status("Select a square, or pass")
        self.status = Label(parent, textvariable=self.statusText, font=('Helvetica', 8)).grid(row=4, columnspan=3)

    def set_status(self, message):
        """Set the text in the status label"""

        self.statusText.set('')
        self.parent.update_idletasks()
        self.statusText.set(message)
        self.parent.update_idletasks()

    def reset_f(self):
        """Reset the state of the board, and clear the display"""

        self.set_status("Select a square, or pass")
        self.gameover = False
        for i in range(9):
            self.b[i] = ' '
            self.sq[i].configure(text=' ', bg='white')

    def passF(self):
        """Let the computer go first"""

        # if no moves have been made, tell computer to go
        if self.emptySpaces == 9:
            ComputerMove(self)

    def clikme(self, n):
        """Called when human clicks a square"""

        if self.gameover: return

        # process human's move
        if HumanMove(self, n) == 0:
            # return if game over
            return

        # Tell computer to move
        ComputerMove(self)

    def color_winning_squares(self):
        """Color a TTT row red to show a win"""

        for i in T3Brd.winlist:
            if self.b[i[0]] == self.b[i[1]] == self.b[i[2]] and self.b[i[0]] != ' ':
                w = i
        for j in range(3):
            self.sq[w[j]].configure(bg="red")

    def mark_square(self, n, mark):
        """Mark square X or O"""

        self.b[n] = mark
        self.sq[n].configure(text=mark)

    @property
    def emptySpaces(self):
        """Get how many empty spaces are on the board."""

        i = 0
        for x in self.b:
            if x == ' ': i += 1
        return i


# End of Class T3Brd
# #############################################################

def HumanMove(brd, n):
    """Returns 0 to return control to GUI, 1 to let computer take a turn."""

    rv = 1
    if brd.b[n] != ' ': return 0  # abort if square not empty
    if dbg: print("user chooses " + str(n))

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
def validMoves(b):
    """Create a list of valid moves."""

    return [i for i, v in enumerate(b) if v == ' ']


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def getNewComputerMove(brd):
    """Get the best move for the computer
    :rtype : object
    :param brd:
    """

    nvm = len(validMoves(brd.b))  # nvm also equals number of plays left
    mdict = scoreMoves(brd.b, 'O', nvm)
    (mm, ms) = minScore(mdict)
    if dbg: print(mdict)
    return mm


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def ComputerMove(brd):
    """Called by the GUI to make the computer's move"""

    brd.set_status('Thinking')
    m = getNewComputerMove(brd)
    if dbg: print("Computer chooses " + str(m))

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
def checkForWin(b):
    '''Check to see if anyone has TTT
    Returns 'X', 'O', or 'no one' '''

    for i in T3Brd.winlist:
        player = b[i[0]]
        if player == ' ':
            continue
        if player == b[i[1]] == b[i[2]]:
            return player
    return 'no one'


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def minScore(mlist):
    ms = 101
    for (m, s) in mlist.items():
        if s < ms:
            mm = m
            ms = s
    return (mm, ms)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def scoreBoard(b):
    '''Determine score of a board
    Win for x= 100
    Win for o= 0
    Win for none = 50'''

    used = sum([1 for x in b if x != ' '])
    if used < 3: return ('no one', 50)

    w = checkForWin(b)
    s = 50
    if w == 'X': s = 100
    if w == 'O': s = 0
    return (w, s)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def scoreMoves(b, player, depth):
    '''Examine all possible moves to 'depth' with 'player' going first
    returns dictionary list of scores'''

    # initialize move result list
    mlist = {}

    # return if 0 depth search requested
    if depth == 0: return mlist

    # generate list of valid moves; return if empty
    VM = validMoves(b)
    if len(VM) == 0: return mlist

    # Evaluate all valid moves
    for i in VM:

        # copy current board and score all of players valid moves
        b2 = list(b)
        b2[i] = player

        # Can player win in 1 move?
        # if move resulted in a win, return
        # (there could be multiple wins, but 1st found is good enough)
        (w, sb) = scoreBoard(b2)
        if w == player:
            mlist = dict()  # remove all other moves evaluated, since they werent wins
            mlist[i] = sb
            return mlist

        # continue to next move if requested depth is 1
        if depth == 1:
            mlist[i] = 50
            continue

        # now predict move otherplayer would take
        otherplayer = 'O' if player == 'X' else 'X';

        # recursively score depth-1 moves ahead for this move
        xlist = scoreMoves(b2, otherplayer, depth - 1)

        # select best move for otherplayer among moves examined

        # if list is empty, go to next valid move
        if len(xlist) == 0: continue

        # player X will choose max score, player O will choose min score
        if otherplayer == 'X':
            mlist[i] = max(xlist.values())
        else:
            mlist[i] = min(xlist.values())

    return mlist


# ###############################################################

if __name__ == "__main__":
    root = Tk()
    brd = T3Brd(root)
    root.mainloop()
