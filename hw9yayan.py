#################################################
# hw9.py: Tetris!
#
# Your name: Yayan Deng
# Your andrew id: yayand
#
# Your partner's name: Matthew Boughton
# Your partner's andrew id: mboughto
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

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    width = (margin * 2) + (cellSize * cols)
    height = (margin * 2) + (cellSize * rows)
    runApp(width = width, height = height)

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    # the board is a 2d-list of colors (initially built with list comprehension)
    app.board = [(['blue'] * app.cols) for row in range(app.rows)]

    # pre-load a few cells with known colors for testing purposes (DEBUG)
    app.board[0][0] = "red" # top-left is red
    app.board[0][app.cols-1] = "white" # top-right is white
    app.board[app.rows-1][0] = "lime" # bottom-left is lime
    app.board[app.rows-1][app.cols-1] = "gray" # bottom-right is gray

    # set list of tetris pieces & piece colors
    app.tetrisPieces, app.tetrisPieceColors = fallingPiece()

    # initialize a random piece
    app.fallingPiece = None
    app.fallingPieceColor = None
    newFallingPiece(app)

    # store falling piece position
    app.fallingPieceCol = (app.cols // 2) - (app.numFallingPieceCols // 2)
    app.fallingPieceRow = 0

def keyPressed(app, event):
    if event.key == '`':
        newFallingPiece(app) #debug delete these
    if event.key == 'Up':
        rotateFallingPiece(app)
        # moveFallingPiece(app, -1, 0) #debug delete
    if event.key == 'Left':
        moveFallingPiece(app, 0, -1)
    if event.key == 'Right':
        moveFallingPiece(app, 0, 1)
    if event.key == 'Down':
        moveFallingPiece(app, 1, 0)

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceCol += dcol
    app.fallingPieceRow += drow
    # check for legal move
    if not fallingPieceIsLegal(app):
        app.fallingPieceCol -= dcol
        app.fallingPieceRow -= drow

def fallingPieceIsLegal(app):
    # check for bounds/space
    for row in range(len(app.fallingPiece)):
        for colIdx in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][colIdx]:
                cellRow = app.fallingPieceRow + row
                cellCol = app.fallingPieceCol + colIdx
                if ((cellRow < 0) or (cellRow >= len(app.board)) or
                    (cellCol < 0) or (cellCol >= len(app.board[0]))):
                    return False
                elif (app.board[cellRow][cellCol] != 'blue'):
                    return False
    return True

def rotateFallingPiece(app):
    temp = copy.deepcopy(app.fallingPiece)
    newRows = len(app.fallingPiece[0])
    newCols = len(app.fallingPiece)
    newPiece = [(['None'] * newCols) for row in range(newRows)]
    # build new piece (new 2d list) using dimensions of the original
    for row in range(len(temp)):
        for col in range(len(temp[row])):
            colIdx = ((app.numFallingPieceCols - 1) - col)
            newPiece[col][row] = temp[row][colIdx]
    # set fallingPiece
    app.fallingPiece = newPiece
    app.numFallingPieceCols = newCols
    # check legality of rotation
    if not fallingPieceIsLegal(app):
        app.fallingPiece = temp
        app.numFallingPieceCols = len(app.fallingPiece[0])

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
    fill = 'gold', width = 0)

def drawBoard(app, canvas):
    # loop over rows and cols to draw the full board
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCell(app, canvas, row, col, color):
    # set xy coordinates
    x0 = app.margin + (col * app.cellSize)
    y0 = app.margin + (row * app.cellSize)
    x1 = app.margin + ((col + 1) * app.cellSize)
    y1 = app.margin + ((row + 1) * app.cellSize)

    # draw single cell
    canvas.create_rectangle(x0, y0, x1, y1,
    fill = color, width = 2.5)

def fallingPiece():
    # Seven "standard" pieces (tetrominoes), taken from the CMU Tetris tutorial
    iPiece = [
        [  True,  True,  True,  True ]]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]]
    oPiece = [
        [  True,  True ],
        [  True,  True ]]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]]
    # the following two lists were taken from the CMU Tetris tutorial
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    tetrisPieceColors = [
        "red", "yellow", "magenta", "pink", "cyan", "lime", "orange"]
    return tetrisPieces, tetrisPieceColors

def newFallingPiece(app):
    # randomizer code, taken from CMU Tetris tutorial
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    # update the number of cols of current falling piece
    app.numFallingPieceCols = len(app.fallingPiece[0])
    # update piece position
    app.fallingPieceCol = (app.cols // 2) - (app.numFallingPieceCols // 2)
    app.fallingPieceRow = 0

def drawFallingPiece(app, canvas):
    for row in range(len(app.fallingPiece)):
        for colIdx in range(len(app.fallingPiece[row])):
            if app.fallingPiece[row][colIdx]:
                drawCell(app, canvas,
                app.fallingPieceRow + row,
                app.fallingPieceCol + colIdx,
                app.fallingPieceColor)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)

#################################################
# main
#################################################

def main():
    cs112_n22_week4_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()