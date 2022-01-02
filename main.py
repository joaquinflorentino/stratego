import piece
from piece import *
import colorama
from colorama import Fore, Back
from copy import deepcopy
import random
import sys
import time
colorama.init(autoreset=True)

# CONSTANTS #

BLUE = 'BLUE'
RED = 'RED'
MARSHAL = '10'
GENERAL = ' 9'
COLONEL = ' 8'
MAJOR = ' 7'
CAPTAIN = ' 6'
LIEUTENANT = ' 5'
SERGEANT = ' 4'
MINER = ' 3'
SCOUT = ' 2'
SPY = ' 1'
BOMB = ' B'
FLAG = ' F'
WATER = ' W'
ANONYMOUS_PIECE = ' S'
EMPTY = ' 0'

pieceIdentification = {
    'Marshal [10]': MARSHAL,
    'General [9]': GENERAL,
    'Colonel [8]': COLONEL,
    '2nd Colonel [8]': COLONEL,
    'Major [7]': MAJOR,
    '2nd Major [7]': MAJOR,
    '3rd Major [7]': MAJOR,
    'Captain [6]': CAPTAIN,
    '2nd Captain [6]': CAPTAIN,
    '3rd Captain [6]': CAPTAIN,
    'Lieutenant [5]': LIEUTENANT,
    '2nd Lieutenant [5]': LIEUTENANT,
    'Sergeant [4]': SERGEANT,
    '2nd Sergeant [4]': SERGEANT,
    'Miner [3]': MINER,
    '2nd Miner [3]': MINER,
    '3rd Miner [3]': MINER,
    '4th Miner [3]': MINER,
    'Scout [2]': SCOUT,
    '2nd Scout [2]': SCOUT,
    '3rd Scout [2]': SCOUT,
    '4th Scout [2]': SCOUT,
    '5th Scout [2]': SCOUT,
    'Spy [1]': SPY,
    'Bomb [B]': BOMB,
    '2nd Bomb [B]': BOMB,
    '3rd Bomb [B]': BOMB,
    '4th Bomb [B]': BOMB,
    '5th Bomb [B]': BOMB,
    'Flag [F]': FLAG
}

pieceNames = list(pieceIdentification)

redPieces = [
    Piece(MARSHAL, RED),
    Piece(GENERAL, RED),
    Piece(COLONEL, RED),
    Piece(COLONEL, RED),
    Piece(MAJOR, RED),
    Piece(MAJOR, RED),
    Piece(MAJOR, RED),
    Piece(CAPTAIN, RED),
    Piece(CAPTAIN, RED),
    Piece(CAPTAIN, RED),
    Piece(LIEUTENANT, RED),
    Piece(LIEUTENANT, RED),
    Piece(SERGEANT, RED),
    Piece(SERGEANT, RED),
    Piece(MINER, RED),
    Piece(MINER, RED),
    Piece(MINER, RED),
    Piece(MINER, RED),
    Piece(SCOUT, RED),
    Piece(SCOUT, RED),
    Piece(SCOUT, RED),
    Piece(SCOUT, RED),
    Piece(SCOUT, RED),
    Piece(SPY, RED),
    Piece(BOMB, RED),
    Piece(BOMB, RED),
    Piece(BOMB, RED),
    Piece(BOMB, RED),
    Piece(BOMB, RED),
    Piece(FLAG, RED)
]

bluePieces = [
    Piece(MARSHAL, BLUE),
    Piece(GENERAL, BLUE),
    Piece(COLONEL, BLUE),
    Piece(COLONEL, BLUE),
    Piece(MAJOR, BLUE),
    Piece(MAJOR, BLUE),
    Piece(MAJOR, BLUE),
    Piece(CAPTAIN, BLUE),
    Piece(CAPTAIN, BLUE),
    Piece(CAPTAIN, BLUE),
    Piece(LIEUTENANT, BLUE),
    Piece(LIEUTENANT, BLUE),
    Piece(SERGEANT, BLUE),
    Piece(SERGEANT, BLUE),
    Piece(MINER, BLUE),
    Piece(MINER, BLUE),
    Piece(MINER, BLUE),
    Piece(MINER, BLUE),
    Piece(SCOUT, BLUE),
    Piece(SCOUT, BLUE),
    Piece(SCOUT, BLUE),
    Piece(SCOUT, BLUE),
    Piece(SCOUT, BLUE),
    Piece(SPY, BLUE),
    Piece(BOMB, BLUE),
    Piece(BOMB, BLUE),
    Piece(BOMB, BLUE),
    Piece(BOMB, BLUE),
    Piece(BOMB, BLUE),
    Piece(FLAG, BLUE)
]

letterValues = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

getTextColour = {
    BLUE: Fore.BLUE,
    RED: Fore.RED,
    None: Fore.WHITE
}

# BOARD UTILITIES #

def initBoard(cell, ROW_COUNT, COL_COUNT):
    return [[cell for col in range(COL_COUNT)] for row in range(ROW_COUNT)]

def addWater(board):
    tempBoard = deepcopy(board)
    tempBoard[3][2] = Piece(WATER)
    tempBoard[4][2] = Piece(WATER)
    tempBoard[3][3] = Piece(WATER)
    tempBoard[4][3] = Piece(WATER)
    tempBoard[3][6] = Piece(WATER)
    tempBoard[4][6] = Piece(WATER)
    tempBoard[3][7] = Piece(WATER)
    tempBoard[4][7] = Piece(WATER)
    return tempBoard

def flipBoard(board, colour, boardOrientation):
    tempBoard = deepcopy(board)
    if boardOrientation != colour:
        tempBoard = [i[::-1] for i in tempBoard[::-1]]
    return tempBoard

def printBoard(board, colour, boardOrientation, lastMoveCoordinate1=None, lastMoveCoordinate2=None):
    tempBoard = deepcopy(board)
    tempBoard = flipBoard(tempBoard, colour, boardOrientation)
    lastMoveCoordinate1 = flipCoordinate(lastMoveCoordinate1)
    lastMoveCoordinate2 = flipCoordinate(lastMoveCoordinate2)

    print('  |  0  1  2  3  4  5  6  7  8  9')
    print('- - - - - - - - - - - - - - - - -')
    for row in range(ROW_COUNT):
        print(letterValues[row] + ' | ', end='')
        for col in range(COL_COUNT):
            piece = tempBoard[row][col]
            pieceColour = piece.getColour()
            pieceValue = piece.getValue()
            pieceIsOpponent = pieceColour == RED and colour == BLUE or pieceColour == BLUE and colour == RED
            isPieceLastMove = (row, col) == lastMoveCoordinate1 or (row, col) == lastMoveCoordinate2
            textColour = getTextColour[pieceColour] if not isPieceLastMove else Fore.YELLOW

            if pieceValue == WATER:
                textColour = Back.CYAN
            elif pieceIsOpponent:
                pieceValue = ANONYMOUS_PIECE
            print(textColour + pieceValue, end=' ')
        print()

def updateBoard(board, row, col, piece):
    tempBoard = deepcopy(board)
    tempBoard[row][col] = piece
    return tempBoard

def setUp(board, colour, boardOrientation):
    tempBoard = deepcopy(board)

    i = 0
    while i < len(pieceNames):
        print(f'{getTextColour[colour]}[{colour}] {Fore.WHITE}Type the coordinate of your {getTextColour[colour]}{pieceNames[i]} {Fore.WHITE}(letter first, number last)')
        print(end='> ')
        rawCoordinate = input()

        if not parsableCoordinate(rawCoordinate):
            print('Invalid input')
            continue

        proccessedCoordinate = getProcessedCoordinate(rawCoordinate)
        row = proccessedCoordinate[0]
        col = proccessedCoordinate[1]

        if not validCoordinatePosition(tempBoard, colour, row, col):
            print('Invalid input')
            continue

        if colour == BLUE:
            tempBoard = updateBoard(tempBoard, row, col, bluePieces[i])
        else:
            tempBoard = updateBoard(tempBoard, row, col, redPieces[i])
        printBoard(tempBoard, colour, boardOrientation)
        i += 1
    return tempBoard

def automateSetUp(board, colour):
    tempBoard = deepcopy(board)
    pieceCount = len(bluePieces)
    tempPieces = deepcopy(bluePieces) if colour == BLUE else deepcopy(redPieces)

    for row in range(5, ROW_COUNT):
        for col in range(COL_COUNT):
            randomPiece = tempPieces[random.randint(0, len(tempPieces) - 1)]
            tempBoard[row][col] = randomPiece
            tempPieces.remove(randomPiece)
    return tempBoard

def chooseSetUpMethod(board, colour, boardOrientation):
    tempBoard = deepcopy(board)
    tempBoard = flipBoard(board, colour, boardOrientation)
    boardOrientation = colour
    isChoosingSetUpMethod = True

    while isChoosingSetUpMethod:
        printBoard(tempBoard, colour, boardOrientation)
        print(f'{getTextColour[colour]}[{colour}] {Fore.WHITE}Randomize your piece set-up? (y/n)')
        print(end='> ')
        answer = input().lower()

        if answer == 'y':
            isChoosingSetUpMethod = False
            return automateSetUp(tempBoard, colour)
        elif answer == 'n':
            isChoosingSetUpMethod = False
            return setUp(tempBoard, colour, boardOrientation)
        else:
            print('Invalid input')
            continue

def movePieceOrigin(board, colour, boardOrientation, lastMoveCoordinate1=None, lastMoveCoordinate2=None):
    tempBoard = deepcopy(board)
    tempBoard = flipBoard(tempBoard, colour, boardOrientation)
    boardOrientation = colour
    printBoard(tempBoard, colour, boardOrientation, lastMoveCoordinate1, lastMoveCoordinate2)
    requestingPieceOrigin = True

    if cantMoveOnTurn(tempBoard, BLUE):
        print('BLUE CAN NOT MOVE ANY OF THEIR PIECES. RED WINS')
        sys.exit()
    elif cantMoveOnTurn(tempBoard, RED):
        print('RED CAN NOT MOVE ANY OF THEIR PIECES. BLUE WINS')
        sys.exit()

    while requestingPieceOrigin:
        print(f'{getTextColour[colour]}[{colour}] {Fore.WHITE}Type the coordinate of the piece you want to move |e.g H4| (1/2)')
        print(end='> ')
        rawCoordinate = input()

        if not parsableCoordinate(rawCoordinate):
            print('Invalid input')
            continue

        proccessedCoordinate = getProcessedCoordinate(rawCoordinate)
        row = proccessedCoordinate[0]
        col = proccessedCoordinate[1]
        pieceOrigin = tempBoard[row][col]

        if not validPieceOrigin(pieceOrigin, colour):
            print('Invalid piece selected')
            continue
        requestingPieceOrigin = False
        movePieceDestination(tempBoard, colour, boardOrientation, row, col)

def movePieceDestination(board, colour, boardOrientation, row1, col1):
    tempBoard = deepcopy(board)
    requestingPieceDestination = True
    pieceOrigin = tempBoard[row1][col1]
    pieceOriginName = getPieceName(pieceOrigin)

    while requestingPieceDestination:
        print(f'{getTextColour[colour]}[{colour}] {Fore.WHITE}Type the coordinate of where you want {getTextColour[colour]}{pieceOriginName} {Fore.WHITE}to move (2/2)')
        print(end='> ')
        rawCoordinate = input()
        didAttackHappen = False
        didPieceOriginWinAttack = False
        didBothPiecesLose = False

        if not parsableCoordinate(rawCoordinate):
            print('Invalid input')
            continue

        proccessedCoordinate = getProcessedCoordinate(rawCoordinate)
        row2 = proccessedCoordinate[0]
        col2 = proccessedCoordinate[1]
        pieceDestination = tempBoard[row2][col2]

        if not validMove(tempBoard, row1, col1, row2, col2):
            print('Invalid move')
            movePieceOrigin(tempBoard, colour, boardOrientation)
        else:
            if pieceOrigin.getColour() != pieceDestination.getColour() and pieceDestination.getValue() != EMPTY:
                tempBoard = attack(tempBoard, row1, col1, row2, col2)
                didAttackHappen = True
            else:                
                tempBoard = updateBoard(tempBoard, row2, col2, pieceOrigin)

            tempBoard = updateBoard(tempBoard, row1, col1, Piece(EMPTY))
            colour = BLUE if colour == RED else RED
            lastMoveCoordinate1 = (row1, col1)
            lastMoveCoordinate2 = (row2, col2)

            if didAttackHappen:
                pieceOriginAfterAttack = tempBoard[row1][col1]
                pieceDestinationAfterAttack = tempBoard[row2][col2]

                if pieceOriginAfterAttack.getValue() == EMPTY and pieceDestinationAfterAttack.getValue() == EMPTY:
                    didBothPiecesLose = True
                elif pieceDestinationAfterAttack.getValue() == pieceOrigin.getValue():
                    didPieceOriginWinAttack = True

                if didPieceOriginWinAttack:
                    movePieceOrigin(tempBoard, colour, boardOrientation, lastMoveCoordinate1, lastMoveCoordinate2)
                elif didBothPiecesLose:
                    movePieceOrigin(tempBoard, colour, boardOrientation, None, None)
                else:
                    movePieceOrigin(tempBoard, colour, boardOrientation, None, lastMoveCoordinate2)
            else:
                movePieceOrigin(tempBoard, colour, boardOrientation, lastMoveCoordinate1, lastMoveCoordinate2)
        requestingPieceDestination = False

def attack(board, row1, col1, row2, col2):
    tempBoard = deepcopy(board)
    pieceOrigin = tempBoard[row1][col1]
    pieceDestination = tempBoard[row2][col2]
    pieceOriginValue = pieceOrigin.getValue()
    pieceDestinationValue = pieceDestination.getValue()
    pieceOriginColour = pieceOrigin.getColour()
    pieceDestinationColour = pieceDestination.getColour()

    valList = list(pieceIdentification.values())
    pos = valList.index(pieceOriginValue)
    pos2 = valList.index(pieceDestinationValue)
    pieceOriginName = getPieceName(pieceOrigin)
    pieceDestinationName = getPieceName(pieceDestination)

    if pieceDestinationValue == BOMB:
        if pieceOriginValue == MINER:
            tempBoard = updateBoard(tempBoard, row2, col2, pieceOrigin)
            print(f'{getTextColour[pieceOriginColour]}{pieceOriginName} {Fore.WHITE}disarms {getTextColour[pieceDestinationColour]}{pieceDestinationName}')
        else:
            tempBoard = updateBoard(tempBoard, row1, col1, Piece(EMPTY))
            print(f'{getTextColour[pieceDestinationColour]}{pieceDestinationName} {Fore.WHITE}eliminates {getTextColour[pieceOriginColour]}{pieceOriginName}')
    elif pieceDestinationValue == FLAG:
        print(f'{pieceOriginColour} WINS')
        sys.exit()
    else:
        if pieceDestinationValue > pieceOriginValue:
            if pieceDestinationValue == MARSHAL and pieceOriginValue == SPY:
                tempBoard = updateBoard(tempBoard, row2, col2, pieceOrigin)
                print(f'{getTextColour[pieceOriginColour]}{pieceOriginName} {Fore.WHITE}eliminates {getTextColour[pieceDestinationColour]}{pieceDestinationName}')
            else:
                print(f'{getTextColour[pieceDestinationColour]}{pieceDestinationName} {Fore.WHITE}eliminates {getTextColour[pieceOriginColour]}{pieceOriginName}')
        elif pieceOriginValue > pieceDestinationValue:
            if pieceDestinationValue == SPY and pieceOriginValue == MARSHAL:
                tempBoard = updateBoard(tempBoard, row1, col1, Piece(EMPTY))
                print(f'{getTextColour[pieceDestinationColour]}{pieceDestinationName} {Fore.WHITE}eliminates {getTextColour[pieceOriginColour]}{pieceOriginName}')
            else:
                tempBoard = updateBoard(tempBoard, row2, col2, pieceOrigin)
                print(f'{getTextColour[pieceOriginColour]}{pieceOriginName} {Fore.WHITE}eliminates {getTextColour[pieceDestinationColour]}{pieceDestinationName}')
        elif pieceOriginValue == pieceDestinationValue:
            tempBoard = updateBoard(tempBoard, row2, col2, Piece(EMPTY))
            print(f'Both teams lose {pieceOriginName}')
    time.sleep(0.8)
    return tempBoard

# OTHER #

def getProcessedCoordinate(rawCoordinate):
    rawRow = rawCoordinate[0].upper()
    rawCol = rawCoordinate[1]
    row = letterValues.index(rawRow)
    col = int(rawCol)
    proccessedCoordinate = (row, col)
    return proccessedCoordinate

def parsableCoordinate(rawCoordinate):
    if len(rawCoordinate) == 2:
        rawRow = rawCoordinate[0].upper()
        rawCol = rawCoordinate[1]
        return rawRow in letterValues and rawCol.isnumeric() and int(rawCol) in range(0, 10)
    return False

def flipCoordinate(coordinate):
    if coordinate != None:
        row = coordinate[0]
        col = coordinate[1]
        flippedCoordinate = (0 + (ROW_COUNT - 1 - row), 0 + (COL_COUNT - 1 - col))
        return flippedCoordinate
    return coordinate

def validCoordinatePosition(board, colour, row, col):
    cellValue = board[row][col].getValue()
    if row >= 5 and 0 <= col <= 9:
        return cellValue == EMPTY
    return False

def validPieceOrigin(piece, colour):
    rejects = [EMPTY, WATER, BOMB, FLAG]
    return piece.getValue() not in rejects and piece.getColour() == colour

def getPieceName(piece):
    pieceValue = piece.getValue()
    valList = list(pieceIdentification.values())
    pos = valList.index(pieceValue)
    return pieceNames[pos]

def validMove(board, row1, col1, row2, col2):
    pieceOrigin = board[row1][col1]
    pieceDestination = board[row2][col2]
    validPieceDestination = pieceDestination.getColour() != pieceOrigin.getColour() and pieceDestination.getValue() != WATER

    if validPieceDestination:
        if pieceOrigin.getValue() == SCOUT:
            move = []
            if row1 != row2 and col1 == col2:
                slope = 1 if row2 > row1 else -1
                for row1 in range(row1 + slope, row2, slope):
                    move.append(board[row1][col1])
            elif col1 != col2 and row1 == row2:
                slope = 1 if col2 > col1 else -1
                for col1 in range(col1 + slope, col2):
                    move.append(board[row1][col1])
            else:
                return False
            return all(piece.getValue() == EMPTY for piece in move)
        else:
            if row1 != row2 and col1 == col2:
                rowDisplacement = abs(row2 - row1)
                if rowDisplacement <= 1:
                    return True
            elif col1 != col2 and row1 == row2:
                colDisplacement = abs(col2 - col1)
                if colDisplacement <= 1:
                    return True
    return False

def cantMoveOnTurn(board, colour):
    stationary = [FLAG, BOMB]
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
                piece = board[row][col]
                if piece.getColour() == colour and piece.getValue() not in stationary:
                    return False
    return True



def main():
    colour = BLUE
    boardOrientation = colour
    tempBoard = chooseSetUpMethod(board, colour, boardOrientation)
    printBoard(tempBoard, colour, boardOrientation)

    colour = BLUE if colour == RED else RED

    tempBoard = chooseSetUpMethod(tempBoard, colour, boardOrientation)
    boardOrientation = colour

    movePieceOrigin(tempBoard, colour, boardOrientation)

board = initBoard(Piece(EMPTY), 8, 10)
board = addWater(board)
ROW_COUNT = len(board)
COL_COUNT = len(board[0])

# Start up stratego
if __name__ == '__main__':
    main()
