import copy

def getSolution(board):
    rows,cols = len(board),len(board[0])
    board = copy.deepcopy(board)
    legals = [[set() for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if board[row][col]==0:
                legals[row][col] = getLegalsForCell(board,row,col)
    return solve(board,legals)

def getLegalsForCell(board,row,col):
    seen = set()
    for i,j in getRegionCells(row,col):
        seen.add(board[i][j])
    return set(range(1,10))-seen

def getRegionCells(row,col):
    cells = set()
    blockIndex = 3 * (row // 3) + col // 3
    blockTop = 3 * (blockIndex // 3)
    blockLeft = 3 * (blockIndex % 3)
    for i in range(9):
        cells.add((i,col))
    for j in range(9):
        cells.add((row,j))
    for i in range(blockTop,blockTop+3):
        for j in range(blockLeft,blockLeft+3):
            cells.add((i,j))
    return cells

def solve(board,legals): #this could probably be improved if we apply hints to reduce legals before testing values
    if isFilled(board):
        return board
    else:
        row,col = getCellWithLeastLegals(board,legals)
        for legal in legals[row][col]:
            setEntry(board,legals,row,col,legal)
            
            if moveIsValid(board,legals):
                solution = solve(board,legals)
                if solution != None:
                    return solution
                else:
                    setEntry(board,legals,row,col,0)
            else:
                setEntry(board,legals,row,col,0)
    return None

def isFilled(board):
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0: return False
    return True

def getCellWithLeastLegals(board,legals):
    rows,cols = len(board),len(board[0])
    bestRow,bestCol = None,None
    leastCount = 10
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                if len(legals[row][col]) < leastCount:
                    bestRow,bestCol = row,col
                    leastCount = len(legals[row][col])
                    if leastCount == 1:
                        break
    return (bestRow,bestCol)

def setEntry(board,legals,row,col,n):
    board[row][col] = n
    legals[row][col] = set()
    updateLegals(board,legals,row,col)

def moveIsValid(board,legals):
    rows,cols = len(board),len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                if len(legals[row][col]) == 0: return False
    return True

def updateLegals(board,legals,entryRow,entryCol):
    for row,col in getRegionCells(entryRow,entryCol):
        if board[row][col] == 0:
            legals[row][col] = getLegalsForCell(board,row,col)

##################################
# below code just for testing
##################################

def prettyPrint(L):
    output = '[\n'
    for list in L:
        output += f'{repr(list)},\n'
    print(output+']')

def readFile(path):
        with open(path, "rt") as f:
            return f.read()

def main():
    print('Testing solver...')
    filePath = 'tp-starter-files/boards/expert-01.png.txt'
    fileContents = readFile(filePath)
    board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    filePath = 'tp-starter-files/solutions/expert-01-solution.png-solution.txt'
    fileContents = readFile(filePath)
    solution = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    result = getSolution(board)
    assert(result==solution)

    filePath = 'tp-starter-files/boards/evil-01.png.txt'
    fileContents = readFile(filePath)
    board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    filePath = 'tp-starter-files/solutions/evil-01-solution.png-solution.txt'
    fileContents = readFile(filePath)
    solution = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    result = getSolution(board)
    assert(result==solution)

    filePath = 'tp-starter-files/boards/evil-02.png.txt'
    fileContents = readFile(filePath)
    board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    filePath = 'tp-starter-files/solutions/evil-02-solution.png-solution.txt'
    fileContents = readFile(filePath)
    solution = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    result = getSolution(board)
    assert(result==solution)

    filePath = 'tp-starter-files/boards/evil-03.png.txt'
    fileContents = readFile(filePath)
    board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    filePath = 'tp-starter-files/solutions/evil-03-solution.png-solution.txt'
    fileContents = readFile(filePath)
    solution = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    result = getSolution(board)
    assert(result==solution)

    print('Passed!')

#main()