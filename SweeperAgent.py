import itertools
import random
import string

class SweeperAgent:
    def __init__(self, board, bombs):
        self.board = board
        self.bombs = bombs

    def updateBoard(self,board):
        self.board = board

    def tankSolver(self):
        

    def numberOfTilesAround(self,col, row, val):
        numberOfEmpty = 0
        if col != 0 and self.board[col - 1][row] == val: numberOfEmpty += 1
        if col != 0 and row != 0 and self.board[col - 1][row - 1] == val: numberOfEmpty += 1
        if row != 0 and self.board[col][row - 1] == val: numberOfEmpty += 1
        if col != len(self.board) - 1 and row != 0 and self.board[col + 1][row - 1] == val: numberOfEmpty += 1
        if col != len(self.board) - 1 and self.board[col + 1][row] == val: numberOfEmpty += 1
        if col != len(self.board) - 1 and row != len(self.board) - 1 and self.board[col + 1][row + 1] == val: numberOfEmpty += 1
        if row != len(self.board) - 1 and self.board[col][row + 1] == val: numberOfEmpty += 1
        if col != 0  and row != len(self.board) - 1 and self.board[col - 1][row + 1] == val: numberOfEmpty += 1
        return numberOfEmpty

    def findEmpty(self,col, row):
        if col != 0 and self.board[col - 1][row] == ' ': return (col - 1, row)
        if col != 0 and row != 0 and self.board[col - 1][row - 1] == ' ': return (col - 1, row - 1)
        if row != 0 and self.board[col][row - 1] == ' ': return (col, row - 1)
        if col != len(self.board) - 1 and row != 0 and self.board[col + 1][row - 1] == ' ': return (col + 1, row - 1)
        if col != len(self.board) - 1 and self.board[col + 1][row] == ' ': return (col + 1, row)
        if col != len(self.board) - 1 and row != len(self.board) - 1 and self.board[col + 1][row + 1] == ' ': return (col + 1, row + 1)
        if row != len(self.board) - 1 and self.board[col][row + 1] == ' ': return (col, row + 1)
        if col != 0  and row != len(self.board) - 1 and self.board[col - 1][row + 1] == ' ': return (col - 1, row + 1)
        return "none"

    def getMove(self):
        guesses = []
        firstMove = True
        letters = string.ascii_lowercase
        for item in itertools.chain.from_iterable(self.board):
            if item is not ' ': firstMove = False
        if(firstMove):
            a = random.randint(0, len(self.board) - 1)
            b = random.randint(1, len(self.board))
            bla = letters[a] + str(b)
            return bla
        if(not firstMove):
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] != ' ' and self.board[i][j] != '0' and self.board[i][j] != 'F':
                        numberOfEmpty = self.numberOfTilesAround(i,j, ' ')
                        numberOfFlags = self.numberOfTilesAround(i,j, 'F')
                        if int(self.board[i][j]) == numberOfFlags:
                            svar = self.findEmpty(i,j)
                            if(svar != "none"):
                                x = letters[svar[1]]
                                y = svar[0]+1
                                svarid = str(x) + str(y)
                                return svarid
                        if int(self.board[i][j]) == numberOfEmpty and numberOfEmpty == 1:
                            svar = self.findEmpty(i,j)
                            x = letters[svar[1]]
                            y = svar[0]+1
                            svarid = str(x) + str(y) + "f"
                            return svarid
                        if int(self.board[i][j]) == numberOfEmpty + numberOfFlags :
                            svar = self.findEmpty(i,j)
                            if(svar != "none"):
                                x = letters[svar[1]]
                                y = svar[0]+1
                                svarid = str(x) + str(y) + "f"
                                return svarid
        for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == ' ':
                        x= letters[j]
                        y= i+1
                        guess = str(x) + str(y)
                        guesses.append(guess)
        a = random.randint(0, len(guesses) - 1)
        return guesses[a]
    


