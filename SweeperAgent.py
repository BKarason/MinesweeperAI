import itertools
import random
import string

def SweeperAgent(grid):
    def numberOfTilesAround(col, row, val):
        numberOfEmpty = 0
        if col != 0 and grid[col - 1][row] == val: numberOfEmpty += 1
        if col != 0 and row != 0 and grid[col - 1][row - 1] == val: numberOfEmpty += 1
        if row != 0 and grid[col][row - 1] == val: numberOfEmpty += 1
        if col != len(grid) - 1 and row != 0 and grid[col + 1][row - 1] == val: numberOfEmpty += 1
        if col != len(grid) - 1 and grid[col + 1][row] == val: numberOfEmpty += 1
        if col != len(grid) - 1 and row != len(grid) - 1 and grid[col + 1][row + 1] == val: numberOfEmpty += 1
        if row != len(grid) - 1 and grid[col][row + 1] == val: numberOfEmpty += 1
        if col != 0  and row != len(grid) - 1 and grid[col - 1][row + 1] == val: numberOfEmpty += 1
        return numberOfEmpty
    def findEmpty(col, row):
        if col != 0 and grid[col - 1][row] == ' ': return (col - 1, row)
        if col != 0 and row != 0 and grid[col - 1][row - 1] == ' ': return (col - 1, row - 1)
        if row != 0 and grid[col][row - 1] == ' ': return (col, row - 1)
        if col != len(grid) - 1 and row != 0 and grid[col + 1][row - 1] == ' ': return (col + 1, row - 1)
        if col != len(grid) - 1 and grid[col + 1][row] == ' ': return (col + 1, row)
        if col != len(grid) - 1 and row != len(grid) - 1 and grid[col + 1][row + 1] == ' ': return (col + 1, row + 1)
        if row != len(grid) - 1 and grid[col][row + 1] == ' ': return (col, row + 1)
        if col != 0  and row != len(grid) - 1 and grid[col - 1][row + 1] == ' ': return (col - 1, row + 1)
        return "none"
    firstMove = True
    letters = string.ascii_lowercase
    for item in itertools.chain.from_iterable(grid):
        if item is not ' ': firstMove = False
    if(firstMove):
        a = random.randint(0, len(grid) - 1)
        b = random.randint(1, len(grid))
        bla = letters[a] + str(b)
        return bla
    if(not firstMove):
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != ' ' and grid[i][j] != '0' and grid[i][j] != 'F':
                    numberOfEmpty = numberOfTilesAround(i,j, ' ')
                    numberOfFlags = numberOfTilesAround(i,j, 'F')
                    if int(grid[i][j]) == numberOfFlags:
                        svar = findEmpty(i,j)
                        if(svar != "none"):
                            x = letters[svar[1]]
                            y = svar[0]+1
                            print(x,y)
                    if int(grid[i][j]) == numberOfEmpty and numberOfEmpty == 1:
                        svar = findEmpty(i,j)
                        x = letters[svar[1]]
                        y = svar[0]+1
                        print(x,y,"f")
                    if int(grid[i][j]) == numberOfEmpty + numberOfFlags :
                        svar = findEmpty(i,j)
                        if(svar != "none"):
                            x = letters[svar[1]]
                            y = svar[0]+1
                            svarid = str(x) + str(y) + "f"
                            return svarid
    a = random.randint(0, len(grid) - 1)
    b = random.randint(1, len(grid))
    bla = letters[a] + str(b)
    return bla
    #print('First move:', firstMove)


