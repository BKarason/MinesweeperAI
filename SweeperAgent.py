import itertools
import random
import string

def SweeperAgent(grid):
    firstMove = True
    letters = string.ascii_lowercase
    for item in itertools.chain.from_iterable(grid):
        if item is not ' ': firstMove = False
    if(firstMove):
        a = random.randint(0, len(grid) - 1)
        b = random.randint(0, len(grid) - 1)
        print(a, b)
        return letters[a] + str(b)
    #print('First move:', firstMove)

