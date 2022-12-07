from cmu_graphics import *
from PIL import Image as PILImage
import math
from State import *

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

class UI:
    colors = {  'darkest':(105, 109, 125),
             'mediumdark':(104, 176, 171),
                 'medium':(143, 192, 169),
            'mediumlight':(200, 213, 185),
               'lightest':(250, 243, 221),
                  'wrong':(254, 181,  92),
                   'hint':(219, 178, 230),}
    onColorChanged = Event()
    onColorChanged += lambda:Button.updateImages()

class Button:

    sourceImages = {'play' : PILImage.open('assets/play_button.png'),
                    'help' : PILImage.open('assets/help_button.png'),
                'settings' : PILImage.open('assets/settings_button.png'),
               'leftarrow' : PILImage.open('assets/arrow_button.png').transpose(PILImage.FLIP_LEFT_RIGHT),
              'rightarrow' : PILImage.open('assets/arrow_button.png'),
                    'back' : PILImage.open('assets/back_button.png'),
                    'home' : PILImage.open('assets/home_button.png'),
               'helpsmall' : PILImage.open('assets/help_button_small.png'),
                    'hint' : PILImage.open('assets/hint_button.png'),
                    'undo' : PILImage.open('assets/undo_button.png'),
                    'redo' : PILImage.open('assets/undo_button.png').transpose(PILImage.FLIP_LEFT_RIGHT),
                   'notes' : PILImage.open('assets/notes_button.png'),}

    images = dict()

    @staticmethod
    def makeColorCMUImage(sourceImage,offset=(0,0,0)):
        def addOffset(tuple1,tuple2):
            result = []
            for i in range(len(tuple1)):
                sum = tuple1[i]+tuple2[i]
                if sum<0: sum = 1
                elif sum>255: sum = 255
                result.append(sum)
            return tuple(result)
        
        rgbImage = sourceImage.convert('RGBA')

        newImage = PILImage.new(mode='RGBA', size=rgbImage.size)
        for x in range(newImage.width):
            for y in range(newImage.height):
                r,g,b,a = rgbImage.getpixel((x,y))
                if a == 0:
                    color = (0,0,0,0)
                else:
                    if r == 0:
                        color = addOffset(UI.colors['darkest'],offset) + (255,)
                    elif r == 51:
                        color = addOffset(UI.colors['mediumdark'],offset) + (255,)
                    elif r == 102:
                        color = addOffset(UI.colors['medium'],offset) + (255,)
                    elif r == 153:
                        color = addOffset(UI.colors['mediumlight'],offset) + (255,)
                    elif r == 204:
                        color = addOffset(UI.colors['lightest'],offset) + (255,)
                newImage.putpixel((x,y),color)
        return CMUImage(newImage)

    @staticmethod
    def updateImages():
        for key in Button.sourceImages:
            Button.images[key] = [Button.makeColorCMUImage(Button.sourceImages[key]),
                                  Button.makeColorCMUImage(Button.sourceImages[key],offset=(20,20,20)),
                                  Button.makeColorCMUImage(Button.sourceImages[key],offset=(40,40,40)),]

    def __init__(self,imageName,cx,cy,scale=1):
        if Button.images == dict(): Button.updateImages()
        self.ownImages = Button.images[imageName]
        self.image = self.ownImages[0]
        UI.onColorChanged += lambda:self.getImages(imageName)
        self.cx, self.cy = cx, cy
        self.width = self.ownImages[0].image.width * scale
        self.height = self.ownImages[0].image.height * scale
        self.onClicked = Event()
        self.onHover = Event()
        self.onStartClick = Event()

        self.onClicked += self.changeImage(0)
        self.onHover += self.changeImage(1)
        self.onStartClick += self.changeImage(2)

    def getImages(self,imageName):
        self.ownImages = Button.images[imageName]
        self.image = self.ownImages[0]

    def changeImage(self,index):
        def f():
            self.image = self.ownImages[index]
        return f

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
    def __init__(self,state,left,top,width,height,
                 rows=9,cols=9,cellBorderWidth=1):
        self.left,self.top,self.width,self.height = left,top,width,height
        self.rows,self.cols,self.cellBorderWidth = rows,cols,cellBorderWidth
        self.entries = [[0 for _ in range(rows)] for _ in range(cols)]
        self.numPadSelection = None
        self.state = state

    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row,col)
        self.drawBorders()

    def drawCell(self,row,col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()

        #draws cell background
        bgColor = 'lightest'
        labelColor = 'darkest'
        if (row,col) == self.state.selection:
            bgColor = 'medium'
            labelColor = 'lightest'
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                 fill=rgb(*UI.colors[bgColor]), border=rgb(*UI.colors['mediumdark']),
                 borderWidth=self.cellBorderWidth)

        #draws number in cell, if applicable
        if self.entries[row][col] != 0:
            cx, cy = cellLeft+0.5*cellWidth, cellTop+0.5*cellHeight
            drawLabel(self.entries[row][col], cx, cy,
                      size=25, fill=rgb(*UI.colors[labelColor]))
        
        #draws numpad
        cellWidth = (cellWidth-2*self.cellBorderWidth)/3
        cellHeight = (cellHeight-2*self.cellBorderWidth)/3
        for i in range(9):
            x = cellLeft + self.cellBorderWidth + (i%3)*cellWidth
            y = cellTop + self.cellBorderWidth + (i//3)*cellHeight
            cx, cy = x + 0.5*cellWidth, y+0.5*cellHeight
            if (row,col) == self.state.selection and i+1 == self.numPadSelection:
                drawLabel(i+1, cx, cy,
                            fill=rgb(*UI.colors['mediumlight']), align='center')

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
                    fill=None, border=rgb(*UI.colors['darkest']),
                    borderWidth=self.cellBorderWidth)
        
        borderWidth = 2*self.cellBorderWidth
        drawRect(self.left-borderWidth, self.top-borderWidth,
                    self.width+2*borderWidth, self.height+2*borderWidth,
                    fill=None, border=rgb(*UI.colors['darkest']),
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
        super().__init__(state,left,top,width,height)
    
    def drawCell(self,row,col):
        cellLeft, cellTop = self.getCellLeftTop(row, col)
        cellWidth, cellHeight = self.getCellSize()

        #draws cell background
        bgColor = 'lightest'
        labelColor = 'darkest'
        if self.state.isEntryWrong(row,col) or (row,col) in self.state.cellsWithWrongLegals:
            bgColor = 'wrong'
        elif (row,col) == self.state.selection:
            bgColor = 'medium'
            labelColor = 'lightest'
        elif self.state.isEntryFixed(row,col):
            bgColor = 'mediumlight'
        elif (row,col) in self.state.hints[0]:
                bgColor = 'hint'
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                 fill=rgb(*UI.colors[bgColor]), border=rgb(*UI.colors['mediumdark']),
                 borderWidth=self.cellBorderWidth)

        #draws number in cell, if applicable
        if self.state.entries[row][col] != 0:
            cx, cy = cellLeft+0.5*cellWidth, cellTop+0.5*cellHeight
            drawLabel(self.state.entries[row][col], cx, cy,
                      size=25, fill=rgb(*UI.colors[labelColor]))
        
        #draws legals (and numpad for medium cell)
        cellWidth = (cellWidth-2*self.cellBorderWidth)/3
        cellHeight = (cellHeight-2*self.cellBorderWidth)/3
        for i in range(9):
            x = cellLeft + self.cellBorderWidth + (i%3)*cellWidth
            y = cellTop + self.cellBorderWidth + (i//3)*cellHeight
            cx, cy = x + 0.5*cellWidth, y+0.5*cellHeight
            if i+1 in self.state.legals[row][col]:
                drawLabel(i+1, cx, cy,
                            fill=rgb(*UI.colors['mediumdark']), align='center')
            elif (row,col) == self.state.selection and i+1 == self.numPadSelection:
                drawLabel(i+1, cx, cy,
                          fill=rgb(*UI.colors['mediumlight']), align='center')
