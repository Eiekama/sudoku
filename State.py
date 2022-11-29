import os, random, copy
import sudoku_solver

class State:
    builtinBoards = None

    def __init__(self, type, manualBoard=None):
        if State.builtinBoards == None:
            State.builtinBoards = State.getFilePathsOfBoards()
        
        assert(type in range(6))
        self.type = type

        self.rows = self.cols = self.blocks = 9
        if self.type == 5:
            self.entries = manualBoard
        else:
            self.entries = self.getBoard() #[[int,...],...]
        
        self.fixedEntries = copy.deepcopy(self.entries)
        self.solution = sudoku_solver.getSolution(self.fixedEntries) #[[int,...],...]

        self.isLegalsAuto = False if (self.type == 0 or self.type == 5) else True
        self.legals = [[set() for _ in range(self.cols)] for _ in range(self.rows)]
        if self.isLegalsAuto: self.updateAllLegals()

        self.gameOver = False
    
    @staticmethod
    def tryCreateState(board):
        rows,cols = len(board),len(board[0])
        if board == [[0 for _ in range(cols)] for _ in range(rows)]: return None
        if State.obviouslyInvalid(board): return None
        solution = sudoku_solver.getSolution(board)
        if solution == None: return None
        return State(5,board)
    
    @staticmethod
    def obviouslyInvalid(board):
        for i in range(9):
            if (State.sameValueAppearTwice(board,State.getRowCells(i)) or
                State.sameValueAppearTwice(board,State.getColCells(i)) or
                State.sameValueAppearTwice(board,State.getBlockCells(i))): return True
        return False
    
    @staticmethod
    def sameValueAppearTwice(board,cells):
        seen = set()
        for row,col in cells:
            value = board[row][col]
            if (value != 0) and (value not in seen): seen.add(board[row][col])
            elif value in seen: return True
        return False
    
    ##################################
    # Get boards from file
    ##################################

    @staticmethod
    def getFilePathsOfBoards():
        paths = [[] for _ in range(5)]
        for filename in os.listdir('tp-starter-files/boards'):
            pathToFile = f'tp-starter-files/boards/{filename}'
            if filename.startswith('easy'):     paths[0].append(pathToFile)
            elif filename.startswith('medium'): paths[1].append(pathToFile)
            elif filename.startswith('hard'):   paths[2].append(pathToFile)
            elif filename.startswith('expert'): paths[3].append(pathToFile)
            elif filename.startswith('evil'):   paths[4].append(pathToFile)
        return paths

    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()
    
    def getBoard(self):
        if self.type == 5:
            assert(self.manualBoard != None)
            return self.manualBoard
        else:
            filePath = random.choice(State.builtinBoards[self.type])
            fileContents = State.readFile(filePath)
            board = [[int(v) for v in line.split(' ')] for line in fileContents.splitlines()]
            return board

    
    ##################################
    # Legals-related functions
    ##################################
    
    def updateAllLegals(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.entries[row][col]==0:
                    self.legals[row][col] = self.getLegalsForCell(row,col)

    def updateLegals(self,entryRow,entryCol):
        # since updateLegals is called every time we change an entry,
        # we only need to update the cells in the region of that entry instead of the entire board
        for row,col in self.getRegionCells(entryRow,entryCol):
            if self.entries[row][col] == 0:
                self.legals[row][col] = self.getLegalsForCell(row,col)

    def getLegalsForCell(self,row,col):
        seen = set()
        for i,j in self.getRegionCells(row,col):
            seen.add(self.entries[i][j])
        return set(range(1,10))-seen

    def addLegal(self,row,col,n):
        self.legals[row][col].add(n)
    
    def removeLegal(self,row,col,n):
        if n in self.legals[row][col]:
            self.legals[row][col].remove(n)

    def clearLegals(self,row,col):
        self.legals[row][col] = set()
    
    def getSingleton(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if len(self.legals[row][col]) == 1:
                    return row,col,list(self.legals[row][col])[0]
        return None

    # def getSingleton(self):
    #     for row in range(self.rows):
    #         for col in range(self.cols):
    #             for legal in self.legals[row][col]:
    #                 if self.isSingleton(row,col,legal): return (row,col,legal)
    #     return None

    # def isSingleton(self,row,col,legal):
    #     for region in [self.getRowCells(row),self.getColCells(col),self.getBlockCells(row,col)]:
    #         if legal not in self.getLegalsInRegion(region,row,col): return True
    #     return False

    # def getLegalsInRegion(self,region,row,col):
    #     seen = set()
    #     for otherRow,otherCol in region:
    #         if (otherRow,otherCol) == (row,col): continue
    #         for legal in self.legals[otherRow][otherCol]:
    #             seen.add(legal)
    #     return seen
    ##################################
    # Get Regions
    ##################################

    def getRegionCells(self,row,col):
        #im not using the static methods defined below since this is technically slightly faster
        cells = set()
        blockIndex = 3 * (row // 3) + col // 3
        blockTop = 3 * (blockIndex // 3)
        blockLeft = 3 * (blockIndex % 3)
        for i in range(self.rows):
            cells.add((i,col))
        for j in range(self.cols):
            cells.add((row,j))
        for i in range(blockTop,blockTop+3):
            for j in range(blockLeft,blockLeft+3):
                cells.add((i,j))
        return cells
    
    @staticmethod
    def getRowCells(row):
        return [(row,i) for i in range(9)]

    @staticmethod
    def getColCells(col):
        return [(i,col) for i in range(9)]
    
    @staticmethod
    def getBlockCells(i,j=None):
        index = 3*(i//3) + j//3 if j != None else i
        topRow = 3 * (index // 3)
        leftCol = 3 * (index % 3)
        result = []
        for i in range(topRow,topRow+3):
            for j in range(leftCol,leftCol+3):
                result.append((i,j))
        return result

    ##################################
    # Entries related
    ##################################

    def setEntry(self,app,row,col,n):
        if not self.gameOver:
            self.entries[row][col] = n
            self.clearLegals(row,col)
            if self.isLegalsAuto: self.updateLegals(row,col)
            if self.entries == self.solution:
                app.message = 'you win!'
                self.gameOver = True

    def isEntryCorrect(self,row,col):
        return self.entries[row][col] == self.solution[row][col]
    
    def isEntryWrong(self,row,col):
        if self.entries[row][col] == 0: return False
        else: return not self.entries[row][col] == self.solution[row][col]
    
    def isEntryFixed(self,row,col):
        return self.fixedEntries[row][col] != 0