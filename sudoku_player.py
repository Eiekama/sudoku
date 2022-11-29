from cmu_graphics import *
from PIL import Image as PILImage
import re
from State import *
from UI import *

##################################
#1 Start Screen
##################################


def start_onScreenStart(app):
    app.boardLeft = 20
    app.boardTop = 20
    app.boardWidth = app.boardHeight = 360

    app.symbToNum = {'!':1,'@':2,'#':3,'$':4,'%':5,'^':6,'&':7,'*':8,'(':9,}

    app.start_buttons = [
        Button(CMUImage(PILImage.open('assets/play_button.png')),
               app.width//2-40,app.height//2+50,.6),
        Button(CMUImage(PILImage.open('assets/help_button.png')),
               app.width//2+95,app.height//2+90,.3),
        Button(CMUImage(PILImage.open('assets/settings_button.png')),
               app.width//2+95,app.height//2+15,.3),
    ]
    app.start_buttons[0].AddListener(lambda : setActiveScreen('levelSelect'))
    app.start_buttons[1].AddListener(lambda : setActiveScreen('help'))

def start_redrawAll(app):
    drawLabel('Sudoku',app.width//2,app.height//2-100,
              size=60,align='center')
    for button in app.start_buttons:
        button.drawButton()

def start_onMouseRelease(app,mouseX,mouseY):
    for button in app.start_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()


##################################
#2 Help Screen
##################################


def help_onScreenStart(app):
    app.help_buttons = [
        Button(CMUImage(PILImage.open('assets/back_button.png')),
        app.width-35,37,0.25),
    ]
    app.help_buttons[-1].AddListener(lambda : setActiveScreen('start'))

def help_redrawAll(app):
    drawLabel('wasd or shift-wasd to move',20,50,size=20,align='left')
    drawLabel('press n to autoplay singletons',20,100,size=20,align='left')
    drawLabel('in medium or higher difficulty',20,140,size=20,align='left')
    drawLabel('numbers keys to enter values',20,190,size=20,align='left')
    drawLabel('shift-number keys to enter legals',20,240,size=20,align='left')
    for button in app.help_buttons:
        button.drawButton()

def help_onMouseRelease(app,mouseX,mouseY):
    for button in app.help_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()


##################################
#3 Level Select Screen
##################################


def levelSelect_onScreenStart(app):
    app.level = 0
    app.levelSelect_buttons = [
        Button(CMUImage(PILImage.open('assets/arrow_button.png').transpose(PILImage.FLIP_LEFT_RIGHT)),
               app.width//2-135,app.height//2-50,.3),
        Button(CMUImage(PILImage.open('assets/arrow_button.png')),
               app.width//2+135,app.height//2-50,.3),
        Button(CMUImage(PILImage.open('assets/play_button.png')),
               app.width//2,app.height//2+100,.6),
        Button(CMUImage(PILImage.open('assets/back_button.png')),
            app.width-35,37,0.25),
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
        app.message = None
        app.notetakingMode = False #temp til right click is a thing
        if app.level == 5:
            app.board = Board(app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight)
            setActiveScreen('manualSelect')
        else:
            app.state = State(app.level)
            app.board = SudokuBoard(app.state,app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight)
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

def levelSelect_onMouseRelease(app,mouseX,mouseY):
    for button in app.levelSelect_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()


##################################
#4 Manual Select Screen
##################################


def manualSelect_onScreenStart(app):
    app.manualSelect_buttons = [
        Button(CMUImage(PILImage.open('assets/arrow_button.png')),
               app.width//2+135,app.height//2-50,.3),
        Button(CMUImage(PILImage.open('assets/arrow_button.png')),
               app.width//2+135,app.height//2+50,.3),
        Button(CMUImage(PILImage.open('assets/back_button.png')),
        app.width-35,37,0.25),
    ]
    app.manualSelect_buttons[0].AddListener(getBoardFromInput(app))
    app.manualSelect_buttons[1].AddListener(lambda : setActiveScreen('manual'))
    app.manualSelect_buttons[-1].AddListener(lambda : setActiveScreen('levelSelect'))

def getBoardFromInput(app):
    def f():
        entries = [[0 for _ in range(9)] for _ in range(9)]
        i = 0
        while i<9:
            input = app.getTextInput(f'Enter values for row {i+1}'
                                     +' (Use 0 for empty cells,'
                                     +' and input q to abort)')
            match = re.fullmatch("\s*(\d\s*){9}",input)
            if match != None:
                row = []
                for c in input:
                    if c in {'0','1','2','3','4','5','6','7','8','9'}:
                        row.append(int(c))
                entries[i] = row
                i += 1
            elif input == 'q': break
        if i == 9:
            app.state = State.tryCreateState(entries)
            if app.state != None:
                app.board = SudokuBoard(app.state,app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight)
                setActiveScreen('level')
    return f

def manualSelect_redrawAll(app):
    drawLabel('Enter by text',app.width//2+75,app.height//2-50,size=35,align='right')
    drawLabel('Enter graphically',app.width//2+75,app.height//2+50,size=35,align='right')
    for button in app.manualSelect_buttons:
        button.drawButton()

def manualSelect_onMouseRelease(app,mouseX,mouseY):
    for button in app.manualSelect_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()


##################################
#5 Manual Screen
##################################


def manual_onScreenStart(app):
    app.manual_buttons = [
        Button(CMUImage(PILImage.open('assets/play_button.png')),
            app.width+20,app.height-100,.6),
        Button(CMUImage(PILImage.open('assets/back_button.png')),
        app.width-35,37,0.25),
    ]
    app.manual_buttons[0].AddListener(makeLevel(app))
    app.manual_buttons[-1].AddListener(lambda : setActiveScreen('levelSelect'))

def makeLevel(app):
    def f():
        app.state = State.tryCreateState(app.board.entries)
        if app.state != None:
            app.board = SudokuBoard(app.state,app.boardLeft,app.boardTop,app.boardWidth,app.boardHeight)
            setActiveScreen('level')
        else:
            app.board.entries = [[0 for _ in range(app.board.cols)] for _ in range(app.board.rows)]
    return f

def manual_redrawAll(app):
    app.board.drawBoard()
    for button in app.manual_buttons:
        button.drawButton()

def manual_onMousePress(app, mouseX, mouseY):
    selectedCell = app.board.getCell(mouseX, mouseY)
    if selectedCell != None:
        app.board.selection = selectedCell
    
    if app.board.selection != None and app.board.numPadSelection != None:
        row,col = app.board.selection[0],app.board.selection[1]
        app.board.entries[row][col] = app.board.numPadSelection

def manual_onMouseMove(app, mouseX, mouseY):
    selectedCell = app.board.getCell(mouseX, mouseY)
    if (app.board.selection != None and 
        selectedCell == app.board.selection):
        selectedNumPadButton = app.board.getNumPadButton(mouseX, mouseY)
        if selectedNumPadButton != None:
            app.board.numPadSelection = selectedNumPadButton
    else:
        app.board.numPadSelection = None

def manual_onMouseRelease(app,mouseX,mouseY):
    for button in app.manual_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()


##################################
#6 Level Screen
##################################


def level_onScreenStart(app):
    y = 48
    app.level_buttons = [
        Button(CMUImage(PILImage.open('assets/home_button.png')),
            app.width-35,y,0.6),
            Button(CMUImage(PILImage.open('assets/help_button_small.png')),
            app.width-35,y+60,0.6),
            Button(CMUImage(PILImage.open('assets/hint_button.png')),
            app.width-35,y+120,0.6),
            Button(CMUImage(PILImage.open('assets/undo_button.png')),
            app.width-35,y+180,0.6),
            Button(CMUImage(PILImage.open('assets/undo_button.png').transpose(PILImage.FLIP_LEFT_RIGHT)),
            app.width-35,y+240,0.6),
            Button(CMUImage(PILImage.open('assets/notes_button.png')),
            app.width-35,y+300,0.6),
    ]
    app.level_buttons[0].AddListener(lambda : setActiveScreen('start'))
    app.level_buttons[-1].AddListener(toggleAutoLegals(app))

def toggleAutoLegals(app):
    def f():
        app.state.isLegalsAuto = not app.state.isLegalsAuto
        if app.state.isLegalsAuto: app.state.updateAllLegals()
    return f
    

def level_redrawAll(app):
    if app.message != None:
        drawLabel(app.message,app.width//2,400,size=20)
    app.board.drawBoard()
    for button in app.level_buttons:
        button.drawButton()

def level_onMousePress(app, mouseX, mouseY):
    if not app.state.gameOver:
        selectedCell = app.board.getCell(mouseX, mouseY)
        if selectedCell != None:
            app.board.selection = selectedCell
        
        if app.board.selection != None and app.board.numPadSelection != None:
            if not app.notetakingMode:
                app.state.setEntry(app,*app.board.selection, app.board.numPadSelection)
            else:
                row, col = app.board.selection[0], app.board.selection[1]
                if app.state.entries[row][col] == 0:
                    if app.board.numPadSelection not in app.state.legals[row][col]:
                        app.state.addLegal(row, col, app.board.numPadSelection)
                    else:
                        app.state.removeLegal(row, col, app.board.numPadSelection)
        
        if (app.width-50 < mouseX < app.width and app.height-50 < mouseY < app.height):
            app.notetakingMode = not app.notetakingMode
            #temp measure until right click is supported

def level_onMouseMove(app, mouseX, mouseY):
    if not app.state.gameOver:
        selectedCell = app.board.getCell(mouseX, mouseY)
        if (app.board.selection != None and 
            selectedCell == app.board.selection and
            not app.state.isEntryFixed(*app.board.selection)):
            selectedNumPadButton = app.board.getNumPadButton(mouseX, mouseY)
            if selectedNumPadButton != None:
                app.board.numPadSelection = selectedNumPadButton
        else:
            app.board.numPadSelection = None

def level_onMouseRelease(app,mouseX,mouseY):
    for button in app.level_buttons:
        if button.contains(mouseX,mouseY): button.onClicked()

def level_onKeyPress(app, key):
    if not app.state.gameOver:
        if key in {'0','1','2','3','4','5','6','7','8','9'}:
            if (app.board.selection != None and
                not app.state.isEntryFixed(*app.board.selection)):
                app.state.setEntry(app,*app.board.selection, int(key))
        elif key in {'!','@','#','$','%','^','&','*','('}:
            row, col = app.board.selection[0], app.board.selection[1]
            if app.state.entries[row][col] == 0:
                value = app.symbToNum[key]
                if value not in app.state.legals[row][col]:
                    app.state.addLegal(row, col, value)
                else:
                    app.state.removeLegal(row, col, value)
        
        elif key == 'n' and app.level != 0:
            singleton = app.state.getSingleton()
            if singleton == None:
                pass
                app.message = 'no singletons left'
            else:
                row,col,value = singleton
                app.state.setEntry(app,row,col,value)

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
        if app.board.selection == None:
            app.board.selection = findClosestEmptyCell(app.state.entries,-1,-1,abs(drow),abs(dcol))
        else:
            app.board.selection = findClosestEmptyCell(app.state.entries,*app.board.selection,drow,dcol)
    elif mode == 'mode2':
        if app.board.selection == None:
            app.board.selection = 0,0
        else:
            row,col = app.board.selection
            row += drow
            col += dcol
            if (row<0 or row>=app.board.rows):
                row -= drow
            if (col<0 or col>=app.board.cols):
                col -= dcol
            app.board.selection = row, col
        

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
    runAppWithScreens(initialScreen='start', width=450, height=425)

main()