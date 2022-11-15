from cmu_cs3_graphics import *
import math

def drawBoard(app):
    for row in range(app.board.rows):
        for col in range(app.board.cols):
            drawCell(app, row, col)
    drawBlockBorder(app)
    drawBoardBorder(app)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)

    #draws cell background
    color = None
    labelColor = 'black'
    if (row,col) == app.selection:
        color = 'gold'
        labelColor = 'white'
    elif app.board.isEntryWrong(row,col):
        color = 'pink'
    elif app.board.isEntryFixed(row,col):
        color = 'whitesmoke'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='grey',
             borderWidth=app.cellBorderWidth)
    #draws number in cell, if applicable
    if app.board.entries[row][col] != 0:
        cx, cy = cellLeft+0.5*cellWidth, cellTop+0.5*cellHeight
        drawLabel(app.board.entries[row][col], cx, cy,
                  size=25, fill=labelColor)

    #draws legals (and numpad for selected cell)
    cellWidth = (cellWidth-2*app.cellBorderWidth)/3
    cellHeight = (cellHeight-2*app.cellBorderWidth)/3
    for i in range(9):
        x = cellLeft + app.cellBorderWidth + (i%3)*cellWidth
        y = cellTop + app.cellBorderWidth + (i//3)*cellHeight
        cx, cy = x + 0.5*cellWidth, y+0.5*cellHeight
        if i+1 in app.board.legals[row][col]:
            drawLabel(i+1, cx, cy,
                      fill='grey', align='center')
        elif (row,col) == app.selection and i+1 == app.numPadSelection:
            drawLabel(i+1, cx, cy,
                      fill='darkgrey', align='center')


def getNumPadButton(app, x, y):
    cellLeft, cellTop = getCellLeftTop(app, *app.selection)
    cellWidth, cellHeight = getCellSize(app)

    dx, dy = x-cellLeft, y-cellTop
    row = math.floor(dy / (cellHeight/3))
    col = math.floor(dx / (cellWidth/3))
    if ((0 <= row < app.board.rows) and
        (0 <= col < app.board.cols)):
        return row*3 + col%3 + 1
    else:
        return None
    
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.board.cols
    cellHeight = app.boardHeight / app.board.rows
    return (cellWidth, cellHeight)

def getBlockLeftTop(app, index):
    cellWidth, cellHeight = getCellSize(app)
    topLeftRow = 3 * (index // 3)
    topLeftCol = 3 * (index % 3)
    blockLeft = app.boardLeft + topLeftCol * cellWidth
    blockTop = app.boardTop + topLeftRow * cellHeight
    return (blockLeft, blockTop)

def drawBlockBorder(app):
    for i in range(9):
        blockLeft, blockTop = getBlockLeftTop(app, i)
        cellWidth, cellHeight = getCellSize(app)
        drawRect(blockLeft, blockTop, 3*cellWidth, 3*cellHeight,
                fill=None, border='black',
                borderWidth=app.cellBorderWidth)

def drawBoardBorder(app):
    borderWidth = 2*app.cellBorderWidth
    drawRect(app.boardLeft-borderWidth, app.boardTop-borderWidth,
                app.boardWidth+2*borderWidth, app.boardHeight+2*borderWidth,
                fill=None, border='black',
                borderWidth=borderWidth)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if ((0 <= row < app.board.rows) and
        (0 <= col < app.board.cols)):
        return (row, col)
    else:
        return None