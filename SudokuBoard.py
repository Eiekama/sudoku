class SudokuBoard:
    def __init__(self, startBoard, solution):
        assert(isinstance(startBoard,list))
        self.rows = self.cols = self.blocks = 9
        self.entries = startBoard #[[int,...],...]
        self.fixedEntries = tuple(tuple(row) for row in startBoard)
        self.solution = solution #[[int,...],...]
        self.legals = [[set() for _ in range(self.cols)] for _ in range(self.rows)]
    
    def GetRow(self,row):
        assert(isinstance(row,int))
        return self.entries[row]

    def GetCol(self,col):
        assert(isinstance(col,int))
        return [self.entries[row][col] for row in range(self.rows)]

    def GetBlock(self,i,j=None):
        assert(isinstance(i,int))
        if j != None:
            assert(isinstance(j,int))
            blockIndex = 3 * (i // 3) + j // 3
        else:
            blockIndex = i
        topLeftRow = 3 * (blockIndex // 3)
        topLeftCol = 3 * (blockIndex % 3)
        block = []
        for row in range(topLeftRow,topLeftRow+3):
            block.extend(self.entries[row][topLeftCol:topLeftCol+3])
        return block
    
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