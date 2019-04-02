import itertools
import random
import string

class SweeperAgent:
    def __init__(self, board, bombs):
        self.board = board
        self.bombs = bombs
        self.tankSolutions = []
        self.letters = string.ascii_lowercase
        self.segregations = []
        self.segregate = False
        self.bruteForceLimit = 8
        self.tankSolverUsed = False

    def getTankSolver(self):
        return self.tankSolverUsed

    def updateBoard(self,board):
        self.board = board

    def tankSolver(self):
        self.tankSolverUsed = True
        # núll stillum segregate, og tile lista
        self.segregate = False
        borderTiles = []
        emptyTiles = [] 
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == ' ':
                    if self.boundryTile(i, j):
                        borderTiles.append((i,j))
                    emptyTiles.append((i,j))
        #print(borderTiles)
        

        nonBorderTiles = len(emptyTiles) - len(borderTiles)
        # 8 er limit'ið sem að við setjum okkur fyrir brute force
        if(nonBorderTiles > self.bruteForceLimit): self.segregate = True
        
        # núll stillum segregated areas lista
        self.segregations = []
        if not self.segregate:
            #fyrst það eru svo fáar auðar eftir, segregate'um við ekki og setjum bara empty tiles í segregated listann
            self.segregations.append(emptyTiles)
        else:
            self.segregations = self.tankSegregate(borderTiles)
        #print("nr of segregations:")
        #print(len(self.segregations))

        highestProbability = 0.0
        prob_BestTile = -1 
        prob_Best_s = -1 



        for s in range(len(self.segregations)):

            # núll stillum tank solutions fyrir hvert segregation
            self.tankSolutions = []

            # skoða hvort að tank recursive sé ekki alveg pottþétt að skila rétt
            self.tankRecursive(self.segregations[s],0)

            # fundum engar lausnir fyrir þetta segregation
            if len(self.tankSolutions) == 0: 
                continue

            for i in range(len(self.segregations[s])):
                mineInAllSolutions = True
                emptyInAllSolutions = True
                for solution in self.tankSolutions:
                    # skoða hvort að þetta séu ekki pottþétt réttar if setningar
                    if not solution[i]: mineInAllSolutions = False
                    if solution[i]: emptyInAllSolutions = False
                
                currTileI = self.segregations[s][i][0]
                currTileJ = self.segregations[s][i][1]

                if mineInAllSolutions:
                    # returna streng til þess að flagga þennan reit
                    x = self.letters[currTileJ]
                    y = currTileI + 1
                    answer = str(x) + str(y) + "f"
                    return answer
                
                if emptyInAllSolutions :
                    # returna streng til þess að velja þennan reit
                    x = self.letters[currTileJ]
                    y = currTileI + 1
                    answer = str(x) + str(y)
                    return answer 

            # since there are no guaranteed solutions we calculate the highest propabilitiy
            highestEmptyRate = -10000
            tileWithHighestEmptyRate = -1
            for i in range(len(self.segregations[s])):
                tileEmptyRate = 0
                for solution in self.tankSolutions:
                    if not solution[i]: tileEmptyRate += 1
                if tileEmptyRate > highestEmptyRate:
                    highestEmptyRate = tileEmptyRate
                    tileWithHighestEmptyRate = i

            probability = float(highestEmptyRate)/float(len(self.tankSolutions))
            
            if probability > highestProbability:
                highestProbability = probability
                prob_BestTile = tileWithHighestEmptyRate
                prob_Best_s = s
        
        if self.bruteForceLimit == 8 and nonBorderTiles > 8 and nonBorderTiles <= 13:
            self.bruteForceLimit = 13
            self.tankSolver()
            self.bruteForceLimit = 8
        
        # skilum svarinu með hæstu líkurnar af öllum segregationum
        i = self.segregations[prob_Best_s][prob_BestTile][0]
        j = self.segregations[prob_Best_s][prob_BestTile][1]
        x = self.letters[j]
        y = i + 1
        answer = str(x) + str(y)

        return answer


    def tankSegregate(self, borderTileList):
        allRegions = [] # listi af listum af tiles
        covered = [] # listi af tiles

        while True :
            queue = [] # listi af tiles
            finishedRegion = [] # listi af tiles
            
            # find a tile to start a region, and make sure it's not in some other region
            for tile in borderTileList:
                if tile not in covered:
                    queue.append(tile)
                    break
            
            if len(queue) == 0:
                break
            
            while len(queue) > 0:
                tile = queue.pop()

                finishedRegion.append(tile)
                covered.append(tile)
                
                # find all connecting tiles
                for cTile in borderTileList:
                    isConnected = False

                    # skif if it's already been assigned to a region
                    if cTile in finishedRegion: continue
                    
                    # ef að þetta tile er hefur meira en 1 tile á milli sín og upprunalega , þá bara continue
                    if abs(tile[0] - cTile[0]) > 2 or abs(tile[1] - cTile[1]) > 2: isConnected = False
                    
                    isConnected = self.tileSearch(tile,cTile)

                    if not isConnected: continue
                    
                    if cTile not in queue: queue.append(cTile)
            
            allRegions.append(finishedRegion)
        
        return allRegions


    def tileSearch(self, tile, cTile):

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] != ' ' and self.board[i][j]:
                    if abs(i - cTile[0]) <= 1 and abs(i - tile[0]) <= 1 and abs(j - cTile[1]) <= 1 and abs(j - tile[1]) <= 1:
                        return True
        return False

    def tankRecursive(self, tileList, k):
        flagCount = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                # setja hvað eru margir reitir í kringum þennan reit
                if self.board[i][j] == 'F':
                    flagCount += 1
                    continue
                if self.board[i][j] == ' ' or self.board[i][j] == 'E': continue
                
                surround = 0
                if (i is 0 and j is 0) or (i is len(self.board) - 1 and j is len(self.board) - 1) or (i is 0 and j is len(self.board) - 1) or (i is len(self.board) - 1 and j is 0):
                    surround = 3
                elif i is 0 or j is 0 or i is len(self.board) - 1 or j is len(self.board) - 1:
                    surround = 5
                else:
                    surround = 8
                
                # if a tile is set to -1 it means that we know that there is not a mine there

                numberOfFlags = self.numberOfTilesAround(i,j, 'F')
                # kannski ekki numberoftiles(i,j,' ')
                numberOfEmpty = self.numberOfTilesAround(i,j, 'E') + self.numberOfTilesAround(i,j, ' ')
                
                if(numberOfFlags > int(self.board[i][j])):
                    #print("number of flags", numberOfFlags, "number on tile, ", self.board[i][j])
                    return
                
                # ekki hundrað á hvað þessi gerir
                if(surround - numberOfEmpty < int(self.board[i][j])):
                    return
            
        if flagCount > self.bombs: return

        if k == len(tileList):
           # print("komst hingad 2")
            if flagCount < self.bombs and not self.segregate: return
            
            solution = []
            for item in tileList:
                #print(item)
                if self.board[item[0]][item[1]] == 'F': solution.append(True)
                else: solution.append(False)
            self.tankSolutions.append(solution)
            return
        
        currTileI = tileList[k][0]
        currTileJ = tileList[k][1]


        self.board[currTileI][currTileJ] = 'F'
        self.tankRecursive(tileList, k+1)
        self.board[currTileI][currTileJ] = ' '

        
        self.board[currTileI][currTileJ] = 'E'
        self.tankRecursive(tileList, k+1)
        self.board[currTileI][currTileJ] = ' '


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
        firstMove = True
        for item in itertools.chain.from_iterable(self.board):
            if item is not ' ': firstMove = False
        if(firstMove):
            a = random.randint(0, len(self.board) - 1)
            b = random.randint(1, len(self.board))
            bla = self.letters[a] + str(b)
            return bla
        if(not firstMove):
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] != ' ' and self.board[i][j] != '0' and self.board[i][j] != 'F':
                        numberOfEmpty = self.numberOfTilesAround(i,j, ' ')
                        numberOfFlags = self.numberOfTilesAround(i,j, 'F')
                        if int(self.board[i][j]) == numberOfFlags:
                            ans = self.findEmpty(i,j)
                            if(ans != "none"):
                                x = self.letters[ans[1]]
                                y = ans[0]+1
                                answer = str(x) + str(y)
                                return answer
                        if int(self.board[i][j]) == numberOfEmpty and numberOfEmpty == 1:
                            ans = self.findEmpty(i,j)
                            x = self.letters[ans[1]]
                            y = ans[0]+1
                            answer = str(x) + str(y) + "f"
                            return answer
                        if int(self.board[i][j]) == numberOfEmpty + numberOfFlags :
                            ans = self.findEmpty(i,j)
                            if(ans != "none"):
                                x = self.letters[ans[1]]
                                y = ans[0]+1
                                answer = str(x) + str(y) + "f"
                                return answer
        return self.tankSolver()
        print("fann ekki lausn ")


