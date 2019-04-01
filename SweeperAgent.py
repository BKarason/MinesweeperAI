import itertools
import random
import string

class SweeperAgent:
    def __init__(self, board, bombs):
        self.board = board
        self.bombs = bombs
        self.tankSolutions = []

    def updateBoard(self,board):
        self.board = board

    def tankSolver(self):
        borderTiles = [] # listi af x,y túplum?
        emptyTiles = [] # listi af túplum?
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == ' ':
                    if self.boundryTile(i, j):
                        borderTiles.append((i,j))
                    emptyTiles.append((i,j))
        #print(borderTiles)
        # ---- hérna kæmi segregation

        totalMultCases = 1
        success = False
        highestProbability = 0.0
        prob_BestTile = -1 # ekki hundrað hvað þessi gerir
        prob_Best_s = -1 # ekki þessi heldur

        # ---- hérna væri loopað í gegnum segregations

        #tankSolutions = [] # boolean fylki
        
        # ---- hérna clone'ar hann borðið, veit ekki hvort það þurfi

        # ---- hérna gerir hann tvívítt boolean fylki sem samsvarar borðinu
        # ---- og setur true ef að reiturinn er tómur og false ef ekki

        # ----- kallar á tankRecurse með fylki af all tiles
        # núll stillum solution fylkið
        self.tankSolutions = []

        self.tankRecursive(emptyTiles,0)

    def tankRecursive(self, tileList, k):
        print(len(tileList))
        print(k)
        flagCount = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                # setja hvað eru margir reitir í kringum þennan reit
                if self.board[i][j] == 'F':
                    flagCount += 1
                    continue
                if self.board[i][j] == ' ': continue
                if self.board[i][j] == 'E': continue
                
                surround = 0
                if (i is 0 and j is 0) or (i is len(self.board) - 1 and j is len(self.board) - 1):
                    surround = 3
                elif i is 0 or j is 0 or i is len(self.board) - 1 or j is len(self.board) - 1:
                    surround = 5
                else: surround = 8
                
                # if a tile is set to -1 it means that we know that there is not a mine there

                numberOfFlags = self.numberOfTilesAround(i,j, 'F')
                numberOfEmpty = self.numberOfTilesAround(i,j, '-1')
                if(numberOfFlags > int(self.board[i][j])):
                    print("number of flags", numberOfFlags, "number on tile, ", self.board[i][j])
                    return
                
                # ekki hundrað á hvað þessi gerir
                if(surround - numberOfEmpty < int(self.board[i][j])): return
            
        if flagCount > self.bombs: return

        if k == len(tileList):
           # print("komst hingad 2")
            if flagCount < self.bombs: return
            
            solution = []
            for item in tileList:
                print(item)
                if self.board[item[0]][item[1]] == 'F': solution.append(True)
                else: solution.append(False)
            
            # þarf örugglega að núll stilla tank solutions eftir hvert sector
            print(solution)
            self.tankSolutions.append(solution)
            return
        
        currTileI = tileList[k][0]
        currTileJ = tileList[k][1]
        #print(currTileI,currTileJ)
        #print(tileList[k])

        #print("komst hingad")

        self.board[currTileI][currTileJ] = 'F'
        #print(self.board[currTileI][currTileJ])
        self.tankRecursive(tileList, k+1)
        self.board[currTileI][currTileJ] = ' '
        #print(self.board[currTileI][currTileJ])

        
        self.board[currTileI][currTileJ] = 'E'
        self.tankRecursive(tileList, k+1)
        self.board[currTileI][currTileJ] = ' '
#        print("komst hingad")

    def boundryTile(self, col, row):
        numbers = ['1','2','3','4','5','6','7','8']
        if col != 0 and self.board[col - 1][row] in numbers: return True
        if col != 0 and row != 0 and self.board[col - 1][row - 1] in numbers: return True
        if row != 0 and self.board[col][row - 1] in numbers: return True
        if col != len(self.board) - 1 and row != 0 and self.board[col + 1][row - 1] in numbers: return True
        if col != len(self.board) - 1 and self.board[col + 1][row] in numbers: return True
        if col != len(self.board) - 1 and row != len(self.board) - 1 and self.board[col + 1][row + 1] in numbers: return True
        if row != len(self.board) - 1 and self.board[col][row + 1] in numbers: return True
        if col != 0  and row != len(self.board) - 1 and self.board[col - 1][row + 1] in numbers: return True

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
        self.tankSolver()
        for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == ' ':
                        x= letters[j]
                        y= i+1
                        guess = str(x) + str(y)
                        guesses.append(guess)
        a = random.randint(0, len(guesses) - 1)
        return guesses[a]
    


