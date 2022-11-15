from cmu_cs3_graphics import *
from SudokuBoard import SudokuBoard
import DrawBoard

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def onAppStart(app):
    startValues = readFile('images-boards-and-solutions-for-1-thru-3/easy-01.png.txt')
    startBoard = [[int(v) for v in line.split(' ')] for line in startValues.splitlines()]
    solValues = readFile('images-boards-and-solutions-for-1-thru-3/easy-01-solution.png-solution.txt')
    solBoard = [[int(v) for v in line.split(' ')] for line in solValues.splitlines()]
    app.board = SudokuBoard(startBoard, solBoard)

    app.boardLeft = 20
    app.boardTop = 20
    app.boardWidth = app.boardHeight = 360
    app.cellBorderWidth = 1

    app.selection = None
    app.numPadSelection = None

def redrawAll(app):
    DrawBoard.drawBoard(app)

def onMousePress(app, mouseX, mouseY):
    if app.numPadSelection != None:
        # app.board.setEntry(*app.selection, app.numPadSelection)
        # app.selection = None
        row, col = app.selection[0], app.selection[1]
        if app.numPadSelection not in app.board.legals[row][col]:
            app.board.addLegal(row, col, app.numPadSelection)
        else:
            app.board.removeLegal(row, col, app.numPadSelection)

def onMouseMove(app, mouseX, mouseY):
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

def onKeyPress(app, key):
    if key in {'0','1','2','3','4','5','6','7','8','9'}:
        if (app.selection != None and
            not app.board.isEntryFixed(*app.selection)):
            app.board.setEntry(*app.selection, int(key))
            app.selection = None
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
    runApp()

main()