from cmu_graphics import *
import math

class Event(object): # taken from https://www.geeksforgeeks.org/mimicking-events-python/
 
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)

class Button:
    def __init__(self,image,cx,cy,scale=None):
        self.image = image
        self.cx, self.cy = cx, cy
        if scale == None:
            self.width = image.image.width
            self.height = image.image.height
        else:
            self.width = image.image.width * scale
            self.height = image.image.height * scale
        self.onClicked = Event()

    def AddListener(self,method):
        self.onClicked += method

    def RemoveListener(self,method):
        self.onClicked -= method
    
    def drawButton(self):
        drawImage(self.image, self.cx, self.cy, align='center',
                  width=self.width, height=self.height)
    
    def contains(self,x,y):
        return (self.cx-0.5*self.width < x < self.cx+0.5*self.width and
                self.cy-0.5*self.height < y < self.cy+0.5*self.height)

class Board: #adapted from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187
             #         and https://cs3-112-f22.academy.cs.cmu.edu/notes/4189
    def __init__(self,left,top,width,height,
                 rows=9,cols=9,cellBorderWidth=1):
        self.left,self.top,self.width,self.height = left,top,width,height
        self.rows,self.cols,self.cellBorderWidth = rows,cols,cellBorderWidth
        self.entries = [[0 for _ in range(rows)] for _ in range(cols)]
        self.numPadSelection = None
        self.colors = {  'darkBorder':'black',
                       'mediumBorder':'grey',
                        'lightBorder':'darkgrey',
                        'inverseDark':'white',
                            'default': None,
                           'selected':'gold',
                              'wrong':'pink',
                              'fixed':'lightgrey',
                               'hint':'lavender',
                      'selectedFixed':'goldenrod',
                      'selectedWrong':'lightsalmon',
                       'selectedHint':'mediumpurple' }

    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row,col)
        self.drawBorders()

    def drawCell(self,row,col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()

        #draws cell background
        bgColor = 'default'
        labelColor = 'darkBorder'
        if (row,col) == self.state.selection:
            bgColor = 'selected'
            labelColor = 'inverseDark'
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                 fill=self.colors[bgColor], border=self.colors['mediumBorder'],
                 borderWidth=self.cellBorderWidth)

        #draws number in cell, if applicable
        if self.entries[row][col] != 0:
            cx, cy = cellLeft+0.5*cellWidth, cellTop+0.5*cellHeight
            drawLabel(self.entries[row][col], cx, cy,
                      size=25, fill=self.colors[labelColor])
        
        #draws numpad
        cellWidth = (cellWidth-2*self.cellBorderWidth)/3
        cellHeight = (cellHeight-2*self.cellBorderWidth)/3
        for i in range(9):
            x = cellLeft + self.cellBorderWidth + (i%3)*cellWidth
            y = cellTop + self.cellBorderWidth + (i//3)*cellHeight
            cx, cy = x + 0.5*cellWidth, y+0.5*cellHeight
            if (row,col) == self.state.selection and i+1 == self.numPadSelection:
                drawLabel(i+1, cx, cy,
                            fill=self.colors['lightBorder'], align='center')

    def getNumPadButton(self,x,y):
        cellLeft, cellTop = self.getCellLeftTop(*self.state.selection)
        cellWidth, cellHeight = self.getCellSize()

        dx, dy = x-cellLeft, y-cellTop
        row = math.floor(dy / (cellHeight/3))
        col = math.floor(dx / (cellWidth/3))
        if ((0 <= row < self.rows) and
            (0 <= col < self.cols)):
            return row*3 + col%3 + 1
        else:
            return None

    def getCellLeftTop(self,row,col):
        cellWidth, cellHeight = self.getCellSize()
        cellLeft = self.left + col * cellWidth
        cellTop = self.top + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellWidth = self.width / self.cols
        cellHeight = self.height / self.rows
        return (cellWidth, cellHeight)
    
    def getBlockLeftTop(self, index):
        cellWidth, cellHeight = self.getCellSize()
        topLeftRow = 3 * (index // 3)
        topLeftCol = 3 * (index % 3)
        blockLeft = self.left + topLeftCol * cellWidth
        blockTop = self.top + topLeftRow * cellHeight
        return (blockLeft, blockTop)

    def drawBorders(self):
        for i in range(9):
            blockLeft, blockTop = self.getBlockLeftTop(i)
            cellWidth, cellHeight = self.getCellSize()
            drawRect(blockLeft, blockTop, 3*cellWidth, 3*cellHeight,
                    fill=None, border=self.colors['darkBorder'],
                    borderWidth=self.cellBorderWidth)
        
        borderWidth = 2*self.cellBorderWidth
        drawRect(self.left-borderWidth, self.top-borderWidth,
                    self.width+2*borderWidth, self.height+2*borderWidth,
                    fill=None, border=self.colors['darkBorder'],
                    borderWidth=borderWidth)
    
    def getCell(self, x, y):
        dx = x - self.left
        dy = y - self.top
        cellWidth, cellHeight = self.getCellSize()
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if ((0 <= row < self.rows) and
            (0 <= col < self.cols)):
            return (row, col)
        else:
            return None


class SudokuBoard(Board): 
    def __init__(self,state,left,top,width,height):
        super().__init__(left,top,width,height)
        self.state = state
    
    def drawCell(self,row,col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()

        #draws cell background
        bgColor = 'default'
        labelColor = 'darkBorder'
        if (row,col) == self.state.selection:
            if self.state.isEntryFixed(row,col):
                bgColor = 'selectedFixed'
            elif self.state.isEntryWrong(row,col) or (row,col) in self.state.cellsWithWrongLegals:
                bgColor = 'selectedWrong'
            elif (row,col) in self.state.hints[0]:
                bgColor = 'selectedHint'
            else:
                bgColor = 'selected'
            labelColor = 'inverseDark'
        elif self.state.isEntryWrong(row,col) or (row,col) in self.state.cellsWithWrongLegals:
            bgColor = 'wrong'
        elif self.state.isEntryFixed(row,col):
            bgColor = 'fixed'
        elif (row,col) in self.state.hints[0]:
                bgColor = 'hint'
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                 fill=self.colors[bgColor], border=self.colors['mediumBorder'],
                 borderWidth=self.cellBorderWidth)

        #draws number in cell, if applicable
        if self.state.entries[row][col] != 0:
            cx, cy = cellLeft+0.5*cellWidth, cellTop+0.5*cellHeight
            drawLabel(self.state.entries[row][col], cx, cy,
                      size=25, fill=self.colors[labelColor])
        
        #draws legals (and numpad for selected cell)
        cellWidth = (cellWidth-2*self.cellBorderWidth)/3
        cellHeight = (cellHeight-2*self.cellBorderWidth)/3
        for i in range(9):
            x = cellLeft + self.cellBorderWidth + (i%3)*cellWidth
            y = cellTop + self.cellBorderWidth + (i//3)*cellHeight
            cx, cy = x + 0.5*cellWidth, y+0.5*cellHeight
            if i+1 in self.state.legals[row][col]:
                drawLabel(i+1, cx, cy,
                            fill=self.colors['mediumBorder'], align='center')
            elif (row,col) == self.state.selection and i+1 == self.numPadSelection:
                drawLabel(i+1, cx, cy,
                            fill=self.colors['lightBorder'], align='center')