#################################################
# hw9.py: Tetris!
#
# Your name:Matthew Boughton 
# Your andrew id:mboughto
#
# Your partner's name:Yayan Deng
# Your partner's andrew id:yayand
#################################################

import cs112_n22_week4_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def playTetris():
    #sets up tetris hyperparameters
    rows, cols, cellSize, margin = gameDimensions()
    width = margin*2 + cellSize*cols
    height = margin*2 + cellSize*rows
    runApp(width=width, height=height)
    
def gameDimensions():
    #represents dimentions of tetris board
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return rows, cols, cellSize, margin

def appStarted(app):
    #starts tetris app
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.timerDelay = 200
    app.gameOver = False
    resetGame(app)
    app.score = 0
    
def resetGame(app):
    #inputing information into model on piece data 
    initializeBoard(app)
    allocatePieces(app)
    newFallingPiece(app)

def allocatePieces(app):
    #allocates piece data into model

    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, 
                        oPiece, sPiece, tPiece, zPiece ]

    app.tetrisPieceColors = [ "red", "yellow", "magenta", 
                            "pink", "cyan", "green", "orange" ]

def initializeBoard(app):
    #gets dimentions of actual tetris board
    app.boardx0 = app.margin
    app.boardx1 = app.margin + app.cols*app.cellSize
    app.boardy0 = app.margin 
    app.boardy1 = app.margin + app.rows*app.cellSize

    #setsup board grid 2D array of "blue" strings
    color = "blue"
    app.board = []
    for row in range(app.rows):
        app.board += [[color]*app.cols] 

def newFallingPiece(app):
    #creates a new fallingtetris piece and makes its data 
    randomIndex = random.randint(0,len(app.tetrisPieces)-1)
    app.fallingPiece = copy.copy(app.tetrisPieces[randomIndex])
    mid = app.cols//2 
    
    app.pieceCol = mid - len(app.fallingPiece[0])//2 
    app.pieceRow = 0

    app.pieceColor = app.tetrisPieceColors[random.randint(0,6)]
    app.pCols = len(app.fallingPiece[0])
    app.pRows = len(app.fallingPiece) 
   
def fallingPieceValid(app):
    #determines if tetris piece placement is valid
    for row in range(app.pRows):
        for col in range(app.pCols):
            if app.fallingPiece[row][col]:
                boardRow = app.pieceRow + row
                boardCol = app.pieceCol + col
                if boardRow <0 or boardRow >= app.rows:
                    #block row outside edges
                    return False
                elif boardCol < 0 or boardCol >= app.cols:
                    #block column outside edges
                    return False
                elif app.board[boardRow][boardCol] != 'blue':
                    #there is a block on top of already created board
                    return False

    return True 

def rotateFallingPiece(app):
    #rotates piece model
    originalPieceCopy = copy.deepcopy(app.fallingPiece)
    #reversion is like a temperary value i think 
    originalRows = len(originalPieceCopy)
    originalCols = len(originalPieceCopy[0])
    newCols,newRows = (originalRows,originalCols)
    newPiece = [[0]*newCols for row in range(newRows)]

    
    oldRows = app.pRows
    oldRow = app.pieceRow

    oldCols = app.pCols
    oldCol = app.pieceCol
    

    for oRow in range(originalRows):
        for oCol in range(originalCols):
            originalBlock = originalPieceCopy[oRow][originalCols - oCol-1]
            newPiece[oCol][oRow] = originalBlock
    

    app.fallingPiece = copy.deepcopy(newPiece)
    app.pRows = len(app.fallingPiece)
    app.pCols = len(app.fallingPiece[0])
    #need to get new row and new col
    #newRow = oldRow + oldNumRows//2 - newNumRows//2
    newRow = oldRow + oldRows//2 - oldRows//2
    newCol = oldCol + oldCols//2 - oldCols//2

    app.pieceRow = newRow
    app.pieceCol = newCol
    
    #change falling piece dimention and speed values
    #if not legal, revert back
    if not fallingPieceValid(app):
        #piece not in valid location
        app.fallingPiece = originalPieceCopy
        app.pRows = len(app.fallingPiece)
        app.pCols = len(app.fallingPiece[0])
        app.pieceCol = oldCol
        app.pieceRow = oldRow
    
def moveFallingPiece(app,drow,dcol):
    #moves falling piece according to drow, dcol
    app.pieceRow += drow  
    app.pieceCol += dcol

    if not fallingPieceValid(app):
        app.pieceRow -= drow
        app.pieceCol -= dcol
        return False
    return True 
    
def keyPressed(app,event):
    if event.key == 'r':
        resetGame(app)
    if app.gameOver:
        return    
    
    if event.key == "Down":
        moveFallingPiece(app, 1,0)
    elif event.key == "Left":
        moveFallingPiece(app, 0, -1)
    elif event.key == "Right":
        moveFallingPiece(app, 0, +1)
    elif event.key == "Up":
        rotateFallingPiece(app)
    elif event.key == "Space":
        hardDrop(app)
        
def timerFired(app):
    #moves piece down as time goes on 
    moved = moveFallingPiece(app, 1, 0)
    
    if not moved and app.pieceRow == 0:
        app.gameOver = True
        
    elif not moved:
        #if block stayed still, place on board and get new falling piece
        placePieceOnBoard(app)
        newFallingPiece(app)
    
    checkFullRows(app)
    app.firstMove = False

def hardDrop(app):
    while True:
        if not moveFallingPiece(app, 1, 0):
            break

def checkFullRows(app):
    streak = 0
    #find what rows fully != blue

    #this section finds all the full rows and stores in fullRows list
    fullRows = [] 
    for row in range(app.rows):
        #assumes row is full row, but goes through column to check
        app.isFullRow = True

        for col in range(app.cols):
            bColor = app.board[row][col]

            if bColor == "blue":
                #empty space, cannot be a fullRow
                app.isFullRow = False
                break
        
        if app.isFullRow:
            #if the row is full, add row to fullRow list  
            fullRow = row
            fullRows.append(fullRow)
    streak = len(fullRows)
    #goes through fullRows list, removingpieces from given 
    #board and moving rest of board down. Returns score of all the
    if streak >0: 
        removeFullRows(app,fullRows)
                        
    app.score += streak**2

def removeFullRows(app,fullRows):
    sortedFullRows = sorted(fullRows)
    for rowRemove in sortedFullRows:
        #rowRemove is row that needs to be removed
        newBoard = [ (["blue"] * app.cols) for row in range(app.rows)]

        for row in range(0,rowRemove):
            for col in range(app.cols):
                bcolor = app.board[row][col] #board color
                newBoard[row+1][col] = bcolor

        app.board = copy.deepcopy(newBoard)
    
def placePieceOnBoard(app):
    #changes app.board from blue to color or piece
    for row in range(app.pRows):
        for col in range(app.pCols):
            bRow = row + app.pieceRow
            bCol = col + app.pieceCol
            if app.fallingPiece[row][col]:
                
                app.board[bRow][bCol] = app.pieceColor

################################################
# Canvas Drawing
################################################

def redrawAll(app,canvas):
    
    drawOrange(app,canvas)
    drawBoard(app,canvas)
    drawPiece(app,canvas)
    drawScore(app,canvas)
    if app.gameOver:
        drawGameover(app, canvas)
    
def drawScore(app,canvas):
    x = (app.boardx0+app.boardx1)/2
    y = app.cellSize/2
    canvas.create_text(x,y,text = f"score: {app.score}"
                        ,fill = "black", font="Helvetica 18")

def drawGameover(app,canvas):
    
    gameText = "Game Over!!!"
    rx0 = app.boardx0
    rx1 = app.boardx1
    ry0 = app.boardy0 + app.cellSize*2
    ry1 = app.boardy0 + app.cellSize*5

    x = (app.boardx0 + app.boardx1)/2 
    y = (ry0+ry1)/2 

    canvas.create_rectangle(rx0,ry0,rx1,ry1, fill = "black")
    canvas.create_text(x,y,text =gameText, fill = "White",
                        font="Helvetica 24 bold")
    

def drawPiece(app,canvas):
    
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            val = app.fallingPiece[row][col]
            
            if val:
                drawCell(app, canvas, app.pieceColor, row+app.pieceRow, 
                        app.pieceCol+col)

def drawOrange(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = "orange")

def drawBoard(app,canvas):
    for row in range(app.rows):
        
        for col in range(app.cols):

            tempColor = app.board[row][col]

            drawCell(app,canvas,tempColor,row,col)

def drawCell(app,canvas,color,row,col):

    x0 = app.boardx0 + col*app.cellSize
    x1 = x0 + app.cellSize
    y0 = app.boardy0 + row*app.cellSize
    y1 = y0 + app.cellSize
    canvas.create_rectangle(x0,y0,x1,y1, fill = color, width = 3)

#################################################
# main
#################################################

def main():
    cs112_n22_week4_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
