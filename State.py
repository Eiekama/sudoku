import os, random, copy
import sudoku_solver

class State:
    builtinBoards = None

    def __init__(self, type, manualBoard=None):
        if State.builtinBoards == None:
            State.builtinBoards = State.getFilePathsOfBoards()
        
        assert(type in range(6))
        self.type = type

        self.manualBoard = manualBoard

        self.rows = self.cols = self.blocks = 9
        self.entries = self.getBoard() #[[int,...],...]
        self.fixedEntries = copy.deepcopy(self.entries)
        self.solution = sudoku_solver.getSolution(self.fixedEntries) #[[int,...],...]
        self.legals = [[set() for _ in range(self.cols)] for _ in range(self.rows)]
    
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

    ##################################
    # Others
    ##################################

    def getRegionCells(self,row,col):
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
    
    def setEntry(self,row,col,n):
        self.entries[row][col] = n
        self.clearLegals(row,col)

    def isEntryCorrect(self,row,col):
        return self.entries[row][col] == self.solution[row][col]
    
    def isEntryWrong(self,row,col):
        if self.entries[row][col] == 0: return False
        else: return not self.entries[row][col] == self.solution[row][col]
    
    def isEntryFixed(self,row,col):
        return self.fixedEntries[row][col] != 0

    def addLegal(self,row,col,n):
        self.legals[row][col].add(n)
    
    def removeLegal(self,row,col,n):
        if n in self.legals[row][col]:
            self.legals[row][col].remove(n)

    def clearLegals(self,row,col):
        self.legals[row][col] = set()