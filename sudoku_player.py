from cmu_cs3_graphics import *
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
            Button('Start',200,200,80,50,fill='lavender',align='center',labelSize=25),
            Button('Help',200,270,80,50,fill='lavender',align='center',labelSize=25),
        ]
    app.start_buttons[0].AddListener(lambda : setActiveScreen('levelSelect'))
    app.start_buttons[1].AddListener(lambda : setActiveScreen('help'))

def start_redrawAll(app):
    drawLabel('Sudoku',200,100,size=30,align='center')
    for button in app.start_buttons:
        button.drawButton()

def start_onMousePress(app,mouseX,mouseY):
    for button in app.start_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()

##################################
# Level Select Screen
##################################

def levelSelect_onScreenStart(app):
    app.levelSelect_buttons = [
            Button('Easy',200,50,90,35,fill='lavender',align='center',labelSize=24),
            Button('Medium',200,100,90,35,fill='lavender',align='center',labelSize=24),
            Button('Hard',200,150,90,35,fill='lavender',align='center',labelSize=24),
            Button('Expert',200,200,90,35,fill='lavender',align='center',labelSize=24),
            Button('Evil',200,250,90,35,fill='lavender',align='center',labelSize=24),
            Button('Manual',200,300,90,35,fill='lavender',align='center',labelSize=24),
            Button('Back',200,350,90,35,fill='lavender',align='center',labelSize=24),
        ]
    for i in range(6):
        app.levelSelect_buttons[i].AddListener(setLevel(app,i))
    app.levelSelect_buttons[-1].AddListener(lambda : setActiveScreen('start'))

def setLevel(app,i):
    def f():
        app.board = SudokuBoard(i)
        setActiveScreen('level')
    return f

def levelSelect_redrawAll(app):
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
            Button('Back',200,350,90,35,fill='lavender',align='center',labelSize=24),
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
    if app.numPadSelection != None:
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
    #move to next non-fixed entry
    elif key == 'j': #up
        pass
    elif key == 'k': #down
        pass
    elif key == 'h': #left
        pass
    elif key == 'l': #right
        pass
    #move to next empty entry
    elif key == 'J': #shift-up
        pass
    elif key == 'K': #shift-down
        pass
    elif key == 'H': #shift-left
        pass
    elif key == 'L': #shift-right
        pass
    #move to next block
    elif key == '∆': #option-up
        pass
    elif key == '˚': #option-down
        pass
    elif key == '˙': #option-left
        pass
    elif key == '¬': #option-right
        pass

def main():
    runAppWithScreens(initialScreen='start')

main()