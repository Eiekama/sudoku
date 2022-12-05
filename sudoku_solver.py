import copy, time, os

def fast_solve(initialBoard):
    return getSolution(initialBoard)

def getSolution(board):
    rows,cols = 9,9
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
    for cell in rowCells[row]: cells.add(cell)
    for cell in colCells[col]: cells.add(cell)
    index = getBlockIndex(row,col)
    for cell in blockCells[index]: cells.add(cell)
    return cells

def solve(board,legals): #this could probably be improved if we apply hints to reduce legals before testing values
    if isFilled(board):
        return board
    else:
        singleton = getSingleton(legals)
        if singleton != None:
            row,col,legal = singleton
            setEntry(board,legals,row,col,legal)
            if moveIsValid(board,legals):
                solution = solve(board,legals)
                if solution != None:
                    return solution
                else:
                    setEntry(board,legals,row,col,0)
            else:
                    setEntry(board,legals,row,col,0)
        
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
    rows, cols = 9,9
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0: return False
    return True

def getCellWithLeastLegals(board,legals):
    rows,cols = 9,9
    bestRow,bestCol = None,None
    leastCount = 10
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                if len(legals[row][col]) < leastCount:
                    bestRow,bestCol = row,col
                    leastCount = len(legals[row][col])
                    if leastCount <= 2:
                        break
    return (bestRow,bestCol)

def setEntry(board,legals,row,col,n):
    board[row][col] = n
    legals[row][col] = set()
    updateLegals(board,legals,row,col)

def moveIsValid(board,legals):
    rows,cols = 9,9
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                if len(legals[row][col]) == 0: return False
    return True

def updateLegals(board,legals,entryRow,entryCol):
    for row,col in getRegionCells(entryRow,entryCol):
        if board[row][col] == 0:
            legals[row][col] = getLegalsForCell(board,row,col)

def getSingleton(legals):
    rows,cols = 9,9
    for row in range(rows):
        for col in range(cols):
            legalsInCell = legals[row][col]
            if len(legalsInCell) == 1: 
                return (row,col,list(legalsInCell)[0])
            for legal in legalsInCell:
                if isSingleton(legals,row,col,legal):
                    return (row,col,legal)
    return None

def isSingleton(legals,row,col,legal):
    index = getBlockIndex(row,col)
    for region in [rowCells[row],colCells[col],blockCells[index]]:
        if legal not in getLegalsInRegion(legals,region,row,col): return True
    return False

def getLegalsInRegion(legals,region,row,col):
    seen = set()
    for otherRow,otherCol in region:
        if (otherRow,otherCol) == (row,col): continue
        for legal in legals[otherRow][otherCol]:
            seen.add(legal)
    return seen

rowCells = (((0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),),
            ((1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),),
            ((2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),),
            ((3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),),
            ((4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),),
            ((5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),),
            ((6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),),
            ((7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),),
            ((8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),),)

colCells = (((0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),),
            ((0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),),
            ((0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),),
            ((0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),),
            ((0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),),
            ((0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),),
            ((0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),),
            ((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),),
            ((0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),),)

blockCells = (((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),),
              ((0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),),
              ((0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8),),
              ((3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2),),
              ((3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5),),
              ((3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8),),
              ((6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2),),
              ((6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5),),
              ((6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8),),)

def getBlockIndex(row,col):
    return 3*(row//3) + col//3


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
def loadBoardPaths(filters):
        boardPaths = [ ]
        for filename in os.listdir(f'tp-starter-files/boards/'):
            if filename.endswith('.txt'):
                if hasFilters(filename, filters):
                    boardPaths.append(f'tp-starter-files/boards/{filename}')
        return boardPaths
def hasFilters(filename, filters=None):
        if filters == None: return True
        for filter in filters:
            if filter not in filename:
                return False
        return True
def testBacktracker(filters):
        time0 = time.time()
        boardPaths = sorted(loadBoardPaths(filters))
        failedPaths = [ ]
        for boardPath in boardPaths:
            board = loadBoard(boardPath)
            print(boardPath)
            solution = fast_solve(board)
            if not solution:
                failedPaths.append(boardPath)
        print()
        totalCount = len(boardPaths)
        failedCount = len(failedPaths)
        okCount = totalCount - failedCount
        time1 = time.time()
        if len(failedPaths) > 0:
            print('Failed boards:')
            for path in failedPaths:
                print(f'    {path}')
        percent = round(100 * okCount/totalCount)
        print(f'Success rate: {okCount}/{totalCount} = {percent}%')
        print(f'Total time: {round(time1-time0, 2)} seconds')

def loadBoard(path):
    fileContents = readFile(path)
    board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
    return board

def main():
    testBacktracker(filters=None)

#main()