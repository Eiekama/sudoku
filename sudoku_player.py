from cmu_cs3_graphics import *
from PIL import Image
from SudokuBoard import SudokuBoard
from UI import *
import DrawBoard

##################################################################
# runAppWithScreens() and setActiveScreen(screen)
##################################################################

def runAppWithScreens(initialScreen, *args, **kwargs):
    appFnNames = ['onAppStart',
                  'onKeyPress', 'onKeyHold', 'onKeyRelease',
                  'onMousePress', 'onMouseDrag', 'onMouseRelease',
                  'onMouseMove', 'onStep', 'redrawAll']
             
    def checkForAppFns():
        globalVars = globals()
        for appFnName in appFnNames:
            if appFnName in globalVars:
                raise Exception(f'Do not define {appFnName} when using screens')
   
    def getScreenFnNames(appFnName):
        globalVars = globals()
        screenFnNames = [ ]
        for globalVarName in globalVars:
            screenAppSuffix = f'_{appFnName}'
            if globalVarName.endswith(screenAppSuffix):
                screenFnNames.append(globalVarName)
        return screenFnNames
   
    def wrapScreenFns():
        globalVars = globals()
        for appFnName in appFnNames:
            screenFnNames = getScreenFnNames(appFnName)
            if (screenFnNames != [ ]) or (appFnName == 'onAppStart'):
                globalVars[appFnName] = makeAppFnWrapper(appFnName)
   
    def makeAppFnWrapper(appFnName):
        if appFnName == 'onAppStart':
            def onAppStartWrapper(app):
                globalVars = globals()
                for screenFnName in getScreenFnNames('onScreenStart'):
                    screenFn = globalVars[screenFnName]
                    screenFn(app)
            return onAppStartWrapper
        else:
            def appFnWrapper(*args):
                globalVars = globals()
                screen = globalVars['_activeScreen']
                wrappedFnName = ('onScreenStart'
                                 if appFnName == 'onAppStart' else appFnName)
                screenFnName = f'{screen}_{wrappedFnName}'
                if screenFnName in globalVars:
                    screenFn = globalVars[screenFnName]
                    return screenFn(*args)
            return appFnWrapper

    def go():
        checkForAppFns()
        wrapScreenFns()
        setActiveScreen(initialScreen)
        runApp(*args, **kwargs)
   
    go()

def setActiveScreen(screen):
    globalVars = globals()
    if (screen in [None, '']) or (not isinstance(screen, str)):
        raise Exception(f'{repr(screen)} is not a valid screen')
    redrawAllFnName = f'{screen}_redrawAll'
    if redrawAllFnName not in globalVars:
        raise Exception(f'Screen {screen} requires {redrawAllFnName}()')
    globalVars['_activeScreen'] = screen

##################################################################
# end of runAppWithScreens() and setActiveScreen(screen)
##################################################################
##################################
# Start Screen
##################################

def start_onScreenStart(app):
    app.start_buttons = [
        Button(CMUImage(Image.open('assets/play_button.png')),
               app.width//2-40,app.height//2+50,.6),
        Button(CMUImage(Image.open('assets/help_button.png')),
               app.width//2+95,app.height//2+90,.3),
        Button(CMUImage(Image.open('assets/settings_button.png')),
               app.width//2+95,app.height//2+15,.3),
    ]
    app.start_buttons[0].AddListener(lambda : setActiveScreen('levelSelect'))
    app.start_buttons[1].AddListener(lambda : setActiveScreen('help'))

def start_redrawAll(app):
    drawLabel('Sudoku',app.width//2,app.height//2-100,
              size=60,align='center')
    for button in app.start_buttons:
        button.drawButton()

def start_onMousePress(app,mouseX,mouseY):
    for button in app.start_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()

##################################
# Level Select Screen
##################################

def levelSelect_onScreenStart(app):
    app.level = 0
    app.levelSelect_buttons = [
        Button(CMUImage(Image.open('assets/arrow_button.png').transpose(Image.FLIP_LEFT_RIGHT)),
               app.width//2-135,app.height//2-50,.3),
        Button(CMUImage(Image.open('assets/arrow_button.png')),
               app.width//2+135,app.height//2-50,.3),
        Button(CMUImage(Image.open('assets/play_button.png')),
               app.width//2,app.height//2+100,.6),
        Button(CMUImage(Image.open('assets/back_button.png')),
            app.width-35,37,0.25),
        # Button('Easy',200,50,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Medium',200,100,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Hard',200,150,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Expert',200,200,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Evil',200,250,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Manual',200,300,90,35,fill='lavender',align='center',labelSize=24),
        # Button('Back',200,350,90,35,fill='lavender',align='center',labelSize=24),
    ]
    app.levelSelect_buttons[0].AddListener(changeLevel(app,-1))
    app.levelSelect_buttons[1].AddListener(changeLevel(app,1))
    app.levelSelect_buttons[-2].AddListener(startLevel(app))
    app.levelSelect_buttons[-1].AddListener(lambda : setActiveScreen('start'))

def changeLevel(app,sign):
    def f():
        app.level += sign
        app.level %= 6
    return f

def startLevel(app):
    def f():
        app.board = SudokuBoard(app.level)
        setActiveScreen('level')
    return f

def levelSelect_redrawAll(app):
    def getString(i):
        if i == 0: return 'Easy'
        elif i == 1: return 'Medium'
        elif i == 2: return 'Hard'
        elif i == 3: return 'Expert'
        elif i == 4: return 'Evil'
        elif i == 5: return 'Manual'
    
    drawLabel('Select Difficulty',20,20,size=50,align='top-left')
    drawLabel(getString(app.level),app.width//2,app.height//2-50,size=50)
    for button in app.levelSelect_buttons:
        button.drawButton()

def levelSelect_onMousePress(app,mouseX,mouseY):
    for button in app.levelSelect_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()

##################################
# Help Screen
##################################

def help_onScreenStart(app):
    app.help_buttons = [
            Button(CMUImage(Image.open('assets/back_button.png')),
            app.width-35,37,0.25),
        ]
    app.help_buttons[-1].AddListener(lambda : setActiveScreen('start'))

def help_redrawAll(app):
    drawLabel('insert helpful text here',200,150,size=20,align='center')
    for button in app.help_buttons:
        button.drawButton()

def help_onMousePress(app,mouseX,mouseY):
    for button in app.help_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()

##################################
# Level Screen
##################################
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def level_onScreenStart(app):
    app.boardLeft = 20
    app.boardTop = 20
    app.boardWidth = app.boardHeight = 360
    app.cellBorderWidth = 1

    app.selection = None
    app.numPadSelection = None

def level_redrawAll(app):
    DrawBoard.drawBoard(app)

def level_onMousePress(app, mouseX, mouseY):
    if app.selection != None and app.numPadSelection != None:
        app.board.setEntry(*app.selection, app.numPadSelection)
        app.selection = None
        # row, col = app.selection[0], app.selection[1]
        # if app.numPadSelection not in app.board.legals[row][col]:
        #     app.board.addLegal(row, col, app.numPadSelection)
        # else:
        #     app.board.removeLegal(row, col, app.numPadSelection)

def level_onMouseMove(app, mouseX, mouseY):
    selectedCell = DrawBoard.getCell(app, mouseX, mouseY)
    if selectedCell != None:
        if app.board.isEntryFixed(*selectedCell):
            app.selection = None
        else:
            app.selection = selectedCell
    else:
        app.selection = None
    
    if app.selection != None:
        selectedNumPadButton = DrawBoard.getNumPadButton(app, mouseX, mouseY)
        if selectedNumPadButton != None:
            app.numPadSelection = selectedNumPadButton
    else:
        app.numPadSelection = None

def level_onKeyPress(app, key):
    if key in {'0','1','2','3','4','5','6','7','8','9'}:
        if (app.selection != None and
            not app.board.isEntryFixed(*app.selection)):
            app.board.setEntry(*app.selection, int(key))
            app.selection = None
    elif key == 'escape':
        app.selection = None
        setActiveScreen('start')
    #move to next non-empty cell
    elif key == 'w': #up
        moveSelection(app,-1,0,'mode1')
    elif key == 's': #down
        moveSelection(app,1,0,'mode1')
    elif key == 'a': #left
        moveSelection(app,0,-1,'mode1')
    elif key == 'd': #right
        moveSelection(app,0,1,'mode1')
    #move to next cell
    elif key == 'W': #shift-up
        moveSelection(app,-1,0,'mode2')
    elif key == 'S': #shift-down
        moveSelection(app,1,0,'mode2')
    elif key == 'A': #shift-left
        moveSelection(app,0,-1,'mode2')
    elif key == 'D': #shift-right
        moveSelection(app,0,1,'mode2')

def moveSelection(app,drow,dcol,mode):
    if mode == 'mode1':
        if app.selection == None:
            app.selection = findClosestEmptyCell(app.board.entries,-1,-1,abs(drow),abs(dcol))
        else:
            app.selection = findClosestEmptyCell(app.board.entries,*app.selection,drow,dcol)
    elif mode == 'mode2':
        if app.selection == None:
            app.selection = 0,0
        else:
            row,col = app.selection
            row += drow
            col += dcol
            if (row<0 or row>=app.board.rows):
                row -= drow
            if (col<0 or col>=app.board.cols):
                col -= dcol
            app.selection = row, col
        

def findClosestEmptyCell(entries,row,col,drow,dcol):
    # i know the below is technically bad style but its a little difficult to write
    # a helper function for this so im leaving it as is for now
    rows,cols = len(entries),len(entries[0])
    if dcol == 0:
        leftBound,rightBound = col,col
        if drow > 0:
            rowsToCheck = rows-(row+1)
        elif drow < 0:
            rowsToCheck = row
        while leftBound>=0 or rightBound<cols:
            currRow = row
            for _ in range(rowsToCheck):
                currRow += drow
                for column in [leftBound,rightBound]:
                    if 0<=column<cols:
                        currCol = column
                        if entries[currRow][currCol] == 0: return (currRow,currCol)
            leftBound -= 1
            rightBound += 1
    elif drow == 0:
        topBound,bottomBound = row,row
        if dcol > 0:
            colsToCheck = cols-(col+1)
        elif dcol < 0:
            colsToCheck = col
        while topBound>=0 or bottomBound<rows:
            currCol = col
            for _ in range(colsToCheck):
                currCol += dcol
                for r in [topBound,bottomBound]:
                    if 0<=r<rows:
                        currRow = r
                        if entries[currRow][currCol] == 0: return (currRow,currCol)
            topBound -= 1
            bottomBound += 1
    
    #if theres no empty cell, selection doesnt change
    return (row,col)

def main():
    runAppWithScreens(initialScreen='start', width=450)

main()