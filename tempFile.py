import pygame  # Game library
from pygame.locals import *  # Game library
import threading  # Library used to store dictionaries in a text file and read them from text files.
import os  # To allow path joining with cross-platform support
import copy  # Library used to make exact copies of lists.
import sys  # Used to simulate infinity
from collections import defaultdict  # Used for giving dictionary values default data types.
import json  # Library used to store dictionaries in a text file and read them from text files.
import math  # to help round numbers


class Board:
    # creates the board through a dictionary where each square is assigned a piece also check what pieces are currently
    # in play and works out the possible moves for a specific piece
    square = {}  # this is the dictionary that will serve as the main board and hold all the pieces
    enPassantPawn = None  # this is a property of the pawns to see if en passant can be performed
    enPassantPawnBehind = None  # this the pawn that will be taken when en passant is performed
    blackOrWhite = "White"  # the game starts off as white and this will alternate between black and white

    def __init__(self):
        pass

    def piecesInPlay(self, allegiance):
        # checks the pieces that are one the board for one side and appends them to a list and then returns that list
        playableP = []
        for tile in range(len(self.square)):
            if not self.square[tile].pieceOnSquare.toString() == "-":
                if self.square[tile].pieceOnSquare.allegiance == allegiance:
                    playableP.append(self.square[tile].pieceOnSquare)

        return playableP

    def possibleMoves(self, pieces, board):
        #checks the possible move for the piece passed in and returns the list
        allPossibleMoves = []
        for piece in pieces:
            pieceMoves = piece.possibleMoves(board)
            for move in pieceMoves:
                allPossibleMoves.append([move, piece])
        return allPossibleMoves

    def makeBoard(self):
        #creates the starting board and place the pieces in each posistion
        for x in range(64):
            #starts by makeing everpiece on the board a null piece
            self.square[x] = Square(x, NullPiece())
        self.square[0] = Square(0, Rook("Black", 0))
        self.square[1] = Square(1, Knight("Black", 1))
        self.square[2] = Square(2, Bishop("Black", 2))
        self.square[3] = Square(3, Queen("Black", 3))
        self.square[4] = Square(4, King("Black", 4))
        self.square[5] = Square(5, Bishop("Black", 5))
        self.square[6] = Square(6, Knight("Black", 6))
        self.square[7] = Square(7, Rook("Black", 7))
        self.square[8] = Square(8, Pawn("Black", 8))
        self.square[9] = Square(9, Pawn("Black", 9))
        self.square[10] = Square(10, Pawn("Black", 10))
        self.square[11] = Square(11, Pawn("Black", 11))
        self.square[12] = Square(12, Pawn("Black", 12))
        self.square[13] = Square(13, Pawn("Black", 13))
        self.square[14] = Square(14, Pawn("Black", 14))
        self.square[15] = Square(15, Pawn("Black", 15))

        self.square[48] = Square(48, Pawn("White", 48))
        self.square[49] = Square(49, Pawn("White", 49))
        self.square[50] = Square(50, Pawn("White", 50))
        self.square[51] = Square(51, Pawn("White", 51))
        self.square[52] = Square(52, Pawn("White", 52))
        self.square[53] = Square(53, Pawn("White", 53))
        self.square[54] = Square(54, Pawn("White", 54))
        self.square[55] = Square(55, Pawn("White", 55))
        self.square[56] = Square(56, Rook("White", 56))
        self.square[57] = Square(57, Knight("White", 57))
        self.square[58] = Square(58, Bishop("White", 58))
        self.square[59] = Square(59, Queen("White", 59))
        self.square[60] = Square(60, King("White", 60))
        self.square[61] = Square(61, Bishop("White", 61))
        self.square[62] = Square(62, Knight("White", 62))
        self.square[63] = Square(63, Rook("White", 63))

    def printBoard(self):
        #prints the board to the console
        count = 0
        for tiles in range(len(self.square)):
            print('|', end=self.square[tiles].pieceOnSquare.toString())
            count += 1
            if count == 8:
                print('|', end='\n')
                count = 0


class Move:
    # checks if the king is in check/checkmate and or stalemate also checks if castling, enpassant or promotion is being performed

    board = None
    pieceMoved = None
    placeMoved = None

    def __init__(self, board, movePiece, placeMoved):
        self.board = board
        self.pieceMoved = movePiece
        self.placeMoved = placeMoved

    def newBoard(self):

        newBoard = Board()
        square = {}

        enPassantP = None
        if self.pieceMoved.toString() == 'P':
            if not self.board.enPassantPawn == None:
                if self.placeMoved == self.board.enPassantPawnBehind:
                    enPassantP = self.board.enPassantPawn.place
        elif self.pieceMoved.toString() == 'p':
            if not self.board.enPassantPawn == None:
                if self.placeMoved == self.board.enPassantPawnBehind:
                    enPassantP = self.board.enPassantPawn.place

        for tile in range(64):
            if not tile == self.pieceMoved.place and not tile == self.placeMoved and not tile == enPassantP:
                square[tile] = self.board.square[tile]
            else:
                square[tile] = Square(tile, NullPiece())

        if self.pieceMoved.toString() == 'K' and self.pieceMoved.startMove:
            if self.placeMoved == 2:
                if self.board.square[0].pieceOnSquare.toString() == "R" \
                        and self.board.square[0].pieceOnSquare.startMove:
                    square[0] = Square(0, NullPiece())
                    square[3] = Square(3, Rook("Black", 3))
            elif self.placeMoved == 6:
                if self.board.square[7].pieceOnSquare.toString() == "R" \
                        and self.board.square[7].pieceOnSquare.startMove:
                    square[7] = Square(7, NullPiece())
                    square[5] = Square(5, Rook("Black", 5))

        elif self.pieceMoved.toString() == 'k':
            if self.placeMoved == 58:
                if self.board.square[56].pieceOnSquare.toString() == "r" \
                        and self.board.square[56].pieceOnSquare.startMove:
                    square[56] = Square(56, NullPiece())
                    square[59] = Square(59, Rook("White", 59))
            elif self.placeMoved == 62:
                if self.board.square[63].pieceOnSquare.toString() == "r" \
                        and self.board.square[56].pieceOnSquare.startMove:
                    square[63] = Square(63, NullPiece())
                    square[61] = Square(61, Rook("White", 61))

        newPiecePlace = copy.copy(self.pieceMoved)
        newPiecePlace.startMove = False
        newPiecePlace.place = self.placeMoved
        square[self.placeMoved] = Square(self.placeMoved, newPiecePlace)
        newBoard.square = square

        if self.pieceMoved.toString() == 'P':
            if self.pieceMoved.place + 16 == self.placeMoved:
                newBoard.enPassantPawn = newPiecePlace
                newBoard.enPassantPawnBehind = self.pieceMoved.place + 8
        elif self.pieceMoved.toString() == 'p':
            if self.pieceMoved.place - 16 == self.placeMoved:
                newBoard.enPassantPawn = newPiecePlace
                newBoard.enPassantPawnBehind = self.pieceMoved.place - 8

        if self.pieceMoved.toString() == 'P':
            if self.placeMoved in self.pieceMoved.eighthRow:
                newBoard.square[self.placeMoved] = Square(self.placeMoved, Queen("Black", self.placeMoved))
        elif self.pieceMoved.toString() == 'p':
            if self.placeMoved in self.pieceMoved.firstRow:
                newBoard.square[self.placeMoved] = Square(self.placeMoved, Queen("White", self.placeMoved))

        newBoard.blackOrWhite = self.board.blackOrWhite
        if newBoard.blackOrWhite == "White":
            newBoard.blackOrWhite = "Black"
        elif newBoard.blackOrWhite == "Black":
            newBoard.blackOrWhite = "White"

        correct = self.checksIfCheck(newBoard)

        if not correct:
            return False

        mate = self.checkIfMateOrStale(newBoard, newBoard.blackOrWhite)
        if mate:
            return "lose"

        return newBoard

    def checkIfBoardIsMate(self):

        newBoard = Board()
        square = {}

        enPassantP = None
        if self.pieceMoved.toString() == 'P':
            if not self.board.enPassantPawn == None:
                if self.placeMoved == self.board.enPassantPawnBehind:
                    enPassantP = self.board.enPassantPawn.place
        elif self.pieceMoved.toString() == 'p':
            if not self.board.enPassantPawn == None:
                if self.placeMoved == self.board.enPassantPawnBehind:
                    enPassantP = self.board.enPassantPawn.place

        for tile in range(64):
            if not tile == self.pieceMoved.place and not tile == self.placeMoved and not tile == enPassantP:
                square[tile] = self.board.square[tile]
            else:
                square[tile] = Square(tile, NullPiece())

        if self.pieceMoved.toString() == 'K' and self.pieceMoved.startMove:
            if self.placeMoved == 2:
                if self.board.square[0].pieceOnSquare.toString() == "R" \
                        and self.board.square[0].pieceOnSquare.startMove:
                    square[0] = Square(0, NullPiece())
                    square[3] = Square(3, Rook("Black", 3))
            elif self.placeMoved == 6:
                if self.board.square[7].pieceOnSquare.toString() == "R" \
                        and self.board.square[7].pieceOnSquare.startMove:
                    square[7] = Square(7, NullPiece())
                    square[5] = Square(5, Rook("Black", 5))

        elif self.pieceMoved.toString() == 'k':
            if self.placeMoved == 58:
                if self.board.square[56].pieceOnSquare.toString() == "r" \
                        and self.board.square[56].pieceOnSquare.startMove:
                    square[56] = Square(56, NullPiece())
                    square[59] = Square(59, Rook("White", 59))
            elif self.placeMoved == 62:
                if self.board.square[63].pieceOnSquare.toString() == "r" \
                        and self.board.square[56].pieceOnSquare.startMove:
                    square[63] = Square(63, NullPiece())
                    square[61] = Square(61, Rook("White", 61))

        newPiecePlace = copy.copy(self.pieceMoved)
        newPiecePlace.startMove = False
        newPiecePlace.place = self.placeMoved
        square[self.placeMoved] = Square(self.placeMoved, newPiecePlace)
        newBoard.square = square

        if self.pieceMoved.toString() == 'P':
            if self.pieceMoved.place + 16 == self.placeMoved:
                newBoard.enPassantPawn = newPiecePlace
                newBoard.enPassantPawnBehind = self.pieceMoved.place + 8
        elif self.pieceMoved.toString() == 'p':
            if self.pieceMoved.place - 16 == self.placeMoved:
                newBoard.enPassantPawn = newPiecePlace
                newBoard.enPassantPawnBehind = self.pieceMoved.place - 8

        if self.pieceMoved.toString() == 'P':
            if self.placeMoved in self.pieceMoved.eighthRow:
                newBoard.square[self.placeMoved] = Square(self.placeMoved, Queen("Black", self.placeMoved))
        elif self.pieceMoved.toString() == 'p':
            if self.placeMoved in self.pieceMoved.firstRow:
                newBoard.square[self.placeMoved] = Square(self.placeMoved, Queen("White", self.placeMoved))

        newBoard.blackOrWhite = self.board.blackOrWhite
        if newBoard.blackOrWhite == "White":
            newBoard.blackOrWhite = "Black"
        elif newBoard.blackOrWhite == "Black":
            newBoard.blackOrWhite = "White"

        correct = self.checksIfCheck(newBoard)

        if not correct:
            return False

        return newBoard

    def checksIfCheck(self, newBoard):

        if newBoard.blackOrWhite == "White":
            oppositionK = None
            for sq in range(len(newBoard.square)):
                if newBoard.square[sq].pieceOnSquare.toString() == "K":
                    oppositionK = newBoard.square[sq].pieceOnSquare.place
                    break

            presentPieces = newBoard.piecesInPlay("White")

            for piece in presentPieces:
                pieceLegals = piece.possibleMoves(newBoard)
                for legals in pieceLegals:
                    if legals == oppositionK:
                        return False

        else:

            oppositionK = None
            for sq in range(len(newBoard.square)):
                if newBoard.square[sq].pieceOnSquare.toString() == "k":
                    oppositionK = newBoard.square[sq].pieceOnSquare.place

            presentPieces = newBoard.piecesInPlay("Black")

            for piece in presentPieces:
                pieceLegals = piece.possibleMoves(newBoard)
                for legals in pieceLegals:
                    if legals == oppositionK:
                        return False

        return True

    @staticmethod
    def checkIfMateOrStale(board, allegiance):
        pieces = board.piecesInPlay(allegiance)
        moves = board.possibleMoves(pieces, board)

        for myMoves in moves:
            makeMove = Move(board, myMoves[1], myMoves[0])
            newboard = makeMove.checkIfBoardIsMate()
            if newboard is not False:
                return False

        return True


class Square:
    # defines what pieces is on each square and where each piece is

    pieceOnSquare = None
    squareLocation = None

    def __init__(self, coordinate, piece):
        self.squareLocation = coordinate
        self.pieceOnSquare = piece


class Piece:
    # super class for each piec passing each class if its the first move and also where the piece is in an edge column/row

    startMove = True

    def __init__(self):
        pass

    firstColumn = [0, 8, 16, 24, 32, 40, 48, 56]
    secondColumn = [1, 9, 17, 25, 33, 41, 49, 57]
    seventhColumn = [6, 14, 22, 30, 38, 46, 54, 62]
    eighthColumn = [7, 15, 23, 31, 39, 47, 55, 63]

    firstRow = [0, 1, 2, 3, 4, 5, 6, 7]
    eighthRow = [63, 62, 61, 60, 59, 58, 57, 56]


class Bishop(Piece):
    # defines how the bishop moves and what should happen if it is an edge case also the minMaxValue to the AI and what player it belonges to
    # its place on the board too
    allegiance = None
    place = None
    moveVector = [-9, -7, 7, 9]
    minMaxValue = 300

    def __init__(self, allegiance, place):
        super().__init__()
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "B" if self.allegiance == "Black" else "b"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):

        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place
            while 0 <= destCoord < 64:
                badMove = self.edgeCases(destCoord, vector)
                if badMove:
                    # print('bad')
                    break
                else:
                    destCoord += vector
                    if 0 <= destCoord < 64:
                        destTile = board.square[destCoord]
                        if destTile.pieceOnSquare.toString() == "-":
                            possibleMove.append(destCoord)
                        else:
                            if not destTile.pieceOnSquare.allegiance == self.allegiance:
                                possibleMove.append(destCoord)
                            # break regardless of allegiance because blocked
                            break

        return possibleMove

    def edgeCases(self, place, vector):
        if place in Piece.firstColumn:
            if vector == -9 or vector == 7:
                return True

        if place in Piece.eighthColumn:
            if vector == -7 or vector == 9:
                return True

        return False


class King(Piece):
    # defines how the king moves and what should happen if it is an edge case also the value to the AI and what player it belonges to
    # its place on the board too and check if its in check and if its being attacked
    allegiance = None
    place = None
    moveVector = [-9, -7, 7, 9, -8, -1, 1, 8]
    minMaxValue = 1100

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "K" if self.allegiance == "Black" else "k"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):

        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place + vector

            badMove = self.edgeCases(self.place, vector)
            if not badMove:

                if 0 <= destCoord < 64:
                    destTile = board.square[destCoord]
                    if destTile.pieceOnSquare.toString() == "-":
                        possibleMove.append(destCoord)
                    else:
                        if not destTile.pieceOnSquare.allegiance == self.allegiance:
                            possibleMove.append(destCoord)

        allEnemyAttacks = []
        enemyPieces = None

        if self.allegiance == "Black":

            enemyPieces = board.piecesInPlay("White")

            for enemy in range(len(enemyPieces)):
                if not enemyPieces[enemy].toString() == "k":
                    moves = enemyPieces[enemy].possibleMoves(board)
                else:
                    moves = enemyPieces[enemy].helperCalLegalMoves(board)
                for move in range(len(moves)):
                    allEnemyAttacks.append(moves[move])

        elif self.allegiance == "White":

            enemyPieces = board.piecesInPlay("Black")

            for enemy in range(len(enemyPieces)):
                if not enemyPieces[enemy].toString() == "K":
                    moves = enemyPieces[enemy].possibleMoves(board)
                else:
                    moves = enemyPieces[enemy].helperCalLegalMoves(board)
                for move in range(len(moves)):
                    allEnemyAttacks.append(moves[move])

        if self.startMove and self.allegiance == "Black":

            if board.square[0].pieceOnSquare.toString() == "R" and board.square[2].pieceOnSquare.startMove:
                if board.square[1].pieceOnSquare.toString() == "-":
                    if board.square[2].pieceOnSquare.toString() == "-":
                        if board.square[3].pieceOnSquare.toString() == "-":
                            if not 3 in allEnemyAttacks and not 2 in allEnemyAttacks and not 4 in allEnemyAttacks:
                                possibleMove.append(2)

            if board.square[7].pieceOnSquare.toString() == "R" and board.square[2].pieceOnSquare.startMove:
                if board.square[6].pieceOnSquare.toString() == "-":
                    if board.square[5].pieceOnSquare.toString() == "-":
                        if not 5 in allEnemyAttacks and not 6 in allEnemyAttacks and not 4 in allEnemyAttacks:
                            possibleMove.append(6)

        elif self.startMove and self.allegiance == "White":

            if board.square[56].pieceOnSquare.toString() == "r" and board.square[2].pieceOnSquare.startMove:
                if board.square[57].pieceOnSquare.toString() == "-":
                    if board.square[58].pieceOnSquare.toString() == "-":
                        if board.square[59].pieceOnSquare.toString() == "-":
                            if not 58 in allEnemyAttacks and not 59 in allEnemyAttacks and not 60 in allEnemyAttacks:
                                possibleMove.append(58)

            if board.square[63].pieceOnSquare.toString() == "r" and board.square[2].pieceOnSquare.startMove:
                if board.square[62].pieceOnSquare.toString() == "-":
                    if board.square[61].pieceOnSquare.toString() == "-":
                        if not 62 in allEnemyAttacks and not 61 in allEnemyAttacks and not 60 in allEnemyAttacks:
                            possibleMove.append(62)

        finalLegal = []
        for move in possibleMove:
            if not move in allEnemyAttacks:
                finalLegal.append(move)

        return finalLegal

    def edgeCases(self, place, vector):
        if place in Piece.firstColumn:
            if vector == -9 or vector == 7 or vector == -1:
                return True
        if place in Piece.eighthColumn:
            if vector == -7 or vector == 9 or vector == 1:
                return True
        return False

    def helperCalLegalMoves(self, board):

        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place + vector
            badMove = self.edgeCases(self.place, vector)
            if not badMove:
                if 0 <= destCoord < 64:
                    destTile = board.square[destCoord]
                    if destTile.pieceOnSquare.toString() == "-":
                        possibleMove.append(destCoord)
                    else:
                        if not destTile.pieceOnSquare.allegiance == self.allegiance:
                            possibleMove.append(destCoord)

        return possibleMove


class Knight(Piece):
    allegiance = None
    place = None
    moveVector = [-17, -15, -10, -6, 6, 10, 15, 17]
    minMaxValue = 300

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "N" if self.allegiance == "Black" else "n"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):

        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place + vector
            if 0 <= destCoord < 64:
                badMove = self.edgeCases(self.place, vector)
                if not badMove:
                    destTile = board.square[destCoord]
                    if destTile.pieceOnSquare.toString() == "-":
                        possibleMove.append(destCoord)
                    else:
                        if not destTile.pieceOnSquare.allegiance == self.allegiance:
                            possibleMove.append(destCoord)

        return possibleMove

    def edgeCases(self, place, vector):
        if place in Piece.firstColumn:
            if vector == -17 or vector == -10 or vector == 6 or vector == 15:
                return True

        if place in Piece.secondColumn:
            if vector == -10 or vector == 6:
                return True

        if place in Piece.seventhColumn:
            if vector == -6 or vector == 10:
                return True

        if place in Piece.eighthColumn:
            if vector == -15 or vector == -6 or vector == 10 or vector == 17:
                return True

        return False


class NullPiece(Piece):

    def __init__(self):
        pass

    def toString(self):
        return "-"


class Pawn(Piece):
    allegiance = None
    place = None
    moveVector = [7, 9, 8, 16]
    allianceMultiple = None
    startMove = True
    minMaxValue = 100

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place
        if self.allegiance == "Black":
            self.allianceMultiple = 1
        else:
            self.allianceMultiple = -1

    def toString(self):
        return "P" if self.allegiance == "Black" else "p"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):

        possibleMove = []

        for vector in self.moveVector:

            destCoord = self.place + (vector * self.allianceMultiple)

            if 0 <= destCoord < 64:

                if vector == 8 and board.square[destCoord].pieceOnSquare.toString() == "-":

                    if self.allegiance == "Black" and destCoord in Piece.eighthRow:
                        possibleMove.append(destCoord)
                    elif self.allegiance == "White" and destCoord in Piece.firstRow:
                        possibleMove.append(destCoord)
                    else:
                        possibleMove.append(destCoord)

                elif vector == 16 and self.startMove and board.square[destCoord].pieceOnSquare.toString() == "-":

                    behindJump = self.place + (8 * self.allianceMultiple)
                    if board.square[behindJump].pieceOnSquare.toString() == "-":
                        possibleMove.append(destCoord)

                elif vector == 7:

                    if self.place in Piece.firstColumn and self.allegiance == "Black":
                        pass
                    elif self.place in Piece.eighthColumn and self.allegiance == "White":
                        pass
                    else:

                        if not board.square[destCoord].pieceOnSquare.toString() == "-":

                            piece = board.square[destCoord].pieceOnSquare
                            if not self.allegiance == piece.allegiance:

                                if self.allegiance == "Black" and destCoord in Piece.eighthRow:
                                    possibleMove.append(destCoord)
                                elif self.allegiance == "White" and destCoord in Piece.firstRow:
                                    possibleMove.append(destCoord)
                                else:
                                    possibleMove.append(destCoord)

                        elif not board.enPassantPawn == None:

                            if board.enPassantPawnBehind == destCoord:
                                enPP = board.enPassantPawn
                                if not self.allegiance == enPP.allegiance:
                                    possibleMove.append(destCoord)


                elif vector == 9:

                    if self.place in Piece.eighthColumn and self.allegiance == "Black":
                        pass
                    elif self.place in Piece.firstColumn and self.allegiance == "White":
                        pass
                    else:

                        if not board.square[destCoord].pieceOnSquare.toString() == "-":
                            piece = board.square[destCoord].pieceOnSquare
                            if not self.allegiance == piece.allegiance:

                                if self.allegiance == "Black" and destCoord in Piece.eighthRow:
                                    possibleMove.append(destCoord)
                                elif self.allegiance == "White" and destCoord in Piece.firstRow:
                                    possibleMove.append(destCoord)
                                else:
                                    possibleMove.append(destCoord)

                        elif not board.enPassantPawn == None:

                            if board.enPassantPawnBehind == destCoord:
                                enPP = board.enPassantPawn
                                if not self.allegiance == enPP.allegiance:
                                    possibleMove.append(destCoord)

        return possibleMove


class Queen(Piece):
    allegiance = None
    place = None
    moveVector = [-9, -7, 7, 9, -8, -1, 1, 8]
    minMaxValue = 900

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "Q" if self.allegiance == "Black" else "q"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):
        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place
            while 0 <= destCoord < 64:
                badMove = self.edgeCases(destCoord, vector)
                if badMove:
                    # print('bad')
                    break
                else:
                    destCoord += vector
                    if 0 <= destCoord < 64:
                        destTile = board.square[destCoord]
                        if destTile.pieceOnSquare.toString() == "-":
                            possibleMove.append(destCoord)
                        else:
                            if not destTile.pieceOnSquare.allegiance == self.allegiance:
                                possibleMove.append(destCoord)
                            # break regardless of allegiance because blocked
                            break

        return possibleMove

    def edgeCases(self, place, vector):
        if place in Piece.firstColumn:
            if vector == -9 or vector == 7 or vector == -1:
                return True

        if place in Piece.eighthColumn:
            if vector == -7 or vector == 9 or vector == 1:
                return True

        return False


class Rook(Piece):
    allegiance = None
    place = None
    moveVector = [-8, -1, 1, 8]
    minMaxValue = 500

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "R" if self.allegiance == "Black" else "r"

    def getPlace(self):
        return self.place

    def possibleMoves(self, board):
        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place
            while 0 <= destCoord < 64:
                badMove = self.edgeCases(destCoord, vector)
                if badMove:
                    break
                else:
                    destCoord += vector
                    if 0 <= destCoord < 64:
                        destTile = board.square[destCoord]
                        if destTile.pieceOnSquare.toString() == "-":
                            possibleMove.append(destCoord)
                        else:
                            if not destTile.pieceOnSquare.allegiance == self.allegiance:
                                possibleMove.append(destCoord)
                            break

        return possibleMove

    def edgeCases(self, place, vector):
        if place in Piece.firstColumn:
            if vector == -1:
                return True

        if place in Piece.eighthColumn:
            if vector == 1:
                return True

        return False


class BoardCheck:

    def __init__(self):
        pass

    def analysis(self, board, depth):
        return self.boardScore("White", board) - self.boardScore("Black", board)

    def boardScore(self, player, board):
        return self.pieceWorth(player, board) + self.canMove(player, board)

    def canMove(self, player, board):
        presentPieces = board.piecesInPlay(player)
        return len(board.possibleMoves(presentPieces, board))

    def pieceWorth(self, player, board):
        pieceValues = 0
        presentPieces = board.piecesInPlay(player)

        for piece in presentPieces:
            pieceValues += piece.minMaxValue

        return pieceValues


class Minimax:
    board = None
    depth = None
    BoardCheck = None
    currentWorth = None
    highestWorth = None
    lowestWorth = None
    bestMove = None

    def __init__(self, board, depth):
        self.board = board
        self.depth = depth
        self.BoardCheck = BoardCheck()

    def getBestMove(self):

        blackOrWhite = self.board.blackOrWhite
        presentPieces = self.board.piecesInPlay(blackOrWhite)
        allPossibleMoves = self.board.possibleMoves(presentPieces, self.board)

        self.highestWorth = -sys.maxsize
        self.lowestWorth = sys.maxsize

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if newboard is not False:
                if blackOrWhite == "White":
                    self.currentWorth = self.min(newboard, self.depth, -sys.maxsize, sys.maxsize)
                else:
                    self.currentWorth = self.max(newboard, self.depth, -sys.maxsize, sys.maxsize)
                if blackOrWhite == "White" and self.currentWorth > self.highestWorth:
                    self.highestWorth = self.currentWorth
                    self.bestMove = newboard
                if blackOrWhite == "Black" and self.currentWorth < self.lowestWorth:
                    self.lowestWorth = self.currentWorth
                    self.bestMove = newboard
        return self.bestMove

    def max(self, board, depth, alpha, beta):

        if depth == 0 and not Move.checkIfMateOrStale(board, board.blackOrWhite):
            return self.BoardCheck.analysis(board, depth)

        highestWorth = -sys.maxsize
        presentPieces = board.piecesInPlay(board.blackOrWhite)
        allPossibleMoves = board.possibleMoves(presentPieces, board)

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if not newboard == False:
                minMaxValue = self.min(newboard, depth - 1, alpha, beta)
                if minMaxValue > highestWorth:
                    highestWorth = minMaxValue
                alpha = max(alpha, minMaxValue)
                if beta <= alpha:
                    break
        return highestWorth

    def min(self, board, depth, alpha, beta):

        if depth == 0 and not Move.checkIfMateOrStale(board, board.blackOrWhite):
            return self.BoardCheck.analysis(board, depth)

        lowestWorth = sys.maxsize
        presentPieces = board.piecesInPlay(board.blackOrWhite)
        allPossibleMoves = board.possibleMoves(presentPieces, board)

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if not newboard == False:
                minMaxValue = self.max(newboard, depth - 1, alpha, beta)
                if minMaxValue < lowestWorth:
                    lowestWorth = minMaxValue
                beta = min(beta, minMaxValue)
                if beta <= alpha:
                    break
        return lowestWorth


pygame.init()
screen = pygame.display.set_mode((800, 800))  # ,FULLSCREEN)

background = pygame.image.load(os.path.join('media', 'board.png')).convert()
background = pygame.transform.scale(background, (800, 800))
playwhite_pic = pygame.image.load(os.path.join('Media', 'playWhite.png')).convert_alpha()
playblack_pic = pygame.image.load(os.path.join('Media', 'playBlack.png')).convert_alpha()
withfriend_pic = pygame.image.load(os.path.join('Media', 'withfriend.png')).convert_alpha()
withAI_pic = pygame.image.load(os.path.join('Media', 'withAI.png')).convert_alpha()
size_of_bg = background.get_rect().size
square_width = size_of_bg[0] / 8
square_height = size_of_bg[1] / 8
withfriend_pic = pygame.transform.scale(withfriend_pic, (int(square_width * 4), int(square_height * 4)))
withAI_pic = pygame.transform.scale(withAI_pic, (int(square_width * 4), int(square_height * 4)))
playwhite_pic = pygame.transform.scale(playwhite_pic, (int(square_width * 4), int(square_height * 4)))
playblack_pic = pygame.transform.scale(playblack_pic, (int(square_width * 4), int(square_height * 4)))

screen = pygame.display.set_mode((size_of_bg))  # ,FULLSCREEN)
pygame.display.set_caption("PyChess")
screen.blit(background, (0, 0))
clock = pygame.time.Clock()

chessBoard = Board()
chessBoard.makeBoard()
# chessBoard.printBoard()

everyTile = []
everyPiece = []
blackOrWhite = chessBoard.blackOrWhite


def display_text(message, style, size, colour, x, y):
    text = pygame.font.Font(style, size).render(message, True, colour, (0))
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def createSqParams():
    allPossibleSquares = []
    minimumX = 0
    maximumX = 100
    minimumY = 0
    maximumY = 100
    for _ in range(8):
        for _ in range(8):
            allPossibleSquares.append([minimumX, maximumX, minimumY, maximumY])
            minimumX += 100
            maximumX += 100
        minimumX = 0
        maximumX = 100
        minimumY += 100
        maximumY += 100
    return allPossibleSquares


def squares(x, y, w, h, color):
    pygame.draw.rect(screen, color, [x, y, w, h])
    everyTile.append([color, [x, y, w, h]])


def drawChessPieces():
    xpos = 0
    ypos = 0
    color = 0
    width = 100
    height = 100
    black = (150, 75, 0)
    white = (255, 255, 255)
    number = 0
    for _ in range(8):
        for _ in range(8):
            if color % 2 == 0:
                squares(xpos, ypos, width, height, white)
                if not chessBoard.square[number].pieceOnSquare.toString() == "-":
                    img = pygame.image.load(
                        "./ChessArt/" + chessBoard.square[number].pieceOnSquare.allegiance[0].upper() +
                        chessBoard.square[
                            number].pieceOnSquare.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    everyPiece.append([img, [xpos, ypos], chessBoard.square[number].pieceOnSquare])
                xpos += 100
            else:
                squares(xpos, ypos, width, height, black)
                if not chessBoard.square[number].pieceOnSquare.toString() == "-":
                    img = pygame.image.load(
                        "./ChessArt/" + chessBoard.square[number].pieceOnSquare.allegiance[0].upper() +
                        chessBoard.square[
                            number].pieceOnSquare.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    everyPiece.append([img, [xpos, ypos], chessBoard.square[number].pieceOnSquare])
                xpos += 100

            color += 1
            number += 1
        color += 1
        xpos = 0
        ypos += 100


def updateChessPieces():
    xpos = 0
    ypos = 0
    number = 0
    newPieces = []

    for _ in range(8):
        for _ in range(8):
            if not chessBoard.square[number].pieceOnSquare.toString() == "-":
                img = pygame.image.load(
                    "./ChessArt/" + chessBoard.square[number].pieceOnSquare.allegiance[0].upper() + chessBoard.square[
                        number].pieceOnSquare.toString().upper() + ".png")
                img = pygame.transform.scale(img, (100, 100))

                newPieces.append([img, [xpos, ypos], chessBoard.square[number].pieceOnSquare])
            xpos += 100
            number += 1
        xpos = 0
        ypos += 100

    return newPieces


def getPiece(nextMove):
    piece = nextMove[0]
    if (piece == 'P'):
        return Pawn("Black", nextMove[2])
    if (piece == 'N'):
        return Knight("Black", nextMove[2])
    if (piece == 'B'):
        return Bishop("Black", nextMove[2])
    if (piece == 'R'):
        return Rook("Black", nextMove[2])
    if (piece == 'Q'):
        return Queen("Black", nextMove[2])
    if (piece == 'K'):
        return King("Black", nextMove[2])
    if (piece == 'p'):
        return Pawn("White", nextMove[2])
    if (piece == 'n'):
        return Knight("White", nextMove[2])
    if (piece == 'b'):
        return Bishop("White", nextMove[2])
    if (piece == 'r'):
        return Rook("White", nextMove[2])
    if (piece == 'q'):
        return Queen("White", nextMove[2])
    if (piece == 'k'):
        return King("White", nextMove[2])
    else:
        return -1


def AIfunc(board, depth, bestmove):
    key = getKey(board)
    key = str(key)
    keyList = list(openings.keys())
    if key in openings:
        index = keyList.index(key)
        if index < len(keyList) - 1:
            global keyIndex
            keyIndex = keyList[index + 1]
            nextMove = openings[keyList[index + 1]]
            nextMoveP = getPiece(nextMove)
            move = Move(board, nextMoveP, nextMove[1])
            aiBoard = move.newBoard()
            bestmove[0] = aiBoard
        else:
            minimax = Minimax(board, depth)
            aiBoard = minimax.getBestMove()
            bestmove[0] = aiBoard
    else:
        minimax = Minimax(board, depth)
        aiBoard = minimax.getBestMove()
        bestmove[0] = aiBoard


zobTable = [[[17179197446815650701, 1154844145221621806, 11085137450493743338, 3887530209885000385,
              12529131482715354759, 6247290991168312813, 15133363498377682977, 1241404763509902715,
              12715397164611021514, 7493738668958658267, 12196670224541324867, 8906562352436999799],
             [4292791217008259540, 17236550921565253447, 6756036817444727438, 10878743308410949057, 5447114016650911531,
              12795488236068956870, 11712724217570232554, 4904272680575930947, 2899418716999618197,
              17340615460366208615, 14782947413287016489, 10963276077094590402],
             [13862405785630475490, 15446867018565696893, 1807617036236300950, 14979062947917088847,
              14671758390389166954, 13817058817644412275, 15261791545994651457, 18394785521997910959,
              16777815033363946603, 12305913086126685074, 11534983954797159558, 156157558993542102],
             [14299924855616413571, 3399724350796733321, 5534384655333648606, 14884826038023455060,
              16921382950131356971, 7505564794136392304, 16572304495493707526, 16666795585392177560,
              10256857946271305813, 14765013356969982392, 16541955494617678045, 10787878810479628863],
             [8170159480547274288, 7095819353049965823, 14045412811416158393, 4038427435353146348, 4873399232181781032,
              16987609536075417597, 581278871702215846, 6348996598990855478, 10529634393434862452, 5265545011967972081,
              12161140469158785346, 8956764859122089211],
             [2269370330361048395, 9785834306588232392, 12052701407169646245, 12235919867459832241, 8312843802235738627,
              18192383751391738112, 16315297097745715550, 11153916729143331175, 16553264043843169879,
              2688922178447116637, 4225928587224735559, 5227007926353550988],
             [13286844079412621950, 10815825078707863494, 2575937406162696820, 15335821335721517634,
              15940758216915031480, 18336831339796636851, 11609760918507333939, 7546469239847541103,
              6112077511858298408, 12844621204247597430, 4416074792331299561, 2526274715812826300],
             [2868951330749776138, 1634431261184725670, 10587141490503028399, 15375729959039586077,
              14314072046509303682, 622390259324962416, 15921330102540107193, 2188833529409872488, 11071091188729844516,
              7611535635466326834, 13167217550036064899, 4893332082477455001]], [
                [1494834659979043600, 14421660602289264426, 18072961746173838411, 2459730110135072084,
                 16113513345174457314, 5527845781472391213, 8566880512923473743, 15888584315340582263,
                 7215563780187651197, 5738149389418983263, 16745167454829362822, 13898429297375388752],
                [14537594889735770597, 4863478788697226715, 12120849598204517824, 2913386921004193529,
                 3686533833470919334, 17261299594254363031, 7275440452696635002, 2633753684432249143,
                 9988324174098079088, 3567016806588914998, 17226355548743059613, 3795085118855392023],
                [6852551679301439810, 15511334640590891605, 4837628554990365224, 3667523217860653772,
                 13435327837219756424, 7976750152768913557, 2836442345107214649, 5562210851906831403,
                 2797757228225874056, 386528612313687052, 86773323175462976, 2479749341528623841],
                [7455332624756276043, 2287821452107790862, 1695406574336795520, 17295704217527421653,
                 13310980102645682494, 7386678962955299631, 10282025955303555888, 9460148140624197108,
                 9320117211736788461, 6069601958200782505, 7244203915725550084, 6937259291253194437],
                [5327437948625325250, 4618346387826059687, 6722083313783897017, 11826036675074332650,
                 5302028186360306604, 16439955740279465452, 17381831223479046794, 6888560233549979701,
                 18263807177911834098, 13221925361001682778, 1484311119629218524, 8398520213891426774],
                [12892090285121458630, 14255156366632128347, 17990422390944962789, 10580678185289519323,
                 9715198308371644735, 12573493060611818764, 16398302841625714402, 14795486190536546682,
                 10278698442573549314, 4448869755554493861, 12833424165783207267, 11581121572229012071],
                [4571564398042140710, 7941100208686840787, 2071028007265345508, 15254330060646678378,
                 16543147383463440457, 9970517155514761717, 4613217884852427775, 13607743706145823837,
                 9643745486724264255, 9909545379881873711, 15739739805389507445, 14543070383154962264],
                [9337693512291980494, 4637423607740758165, 7976792071003657239, 8569161164907338607,
                 13010650874538179340, 9579055313866840734, 14903577041301204039, 12020542864149369203,
                 2568606311686396436, 15930295424172472468, 5395170414957250348, 12889268359740003418]], [
                [6214365294772683330, 15144301846699448569, 7380254423465316661, 3265607101067837275,
                 6925058697800276922, 8002291576426154834, 364512873738800593, 8936334720646424278, 5879730210161966280,
                 7886757687506641155, 12447359541009005642, 902121087686690742],
                [2494925701285025776, 12080376915499966625, 10048324385988803264, 18026176912001429985,
                 10547153446129720720, 14803898189240712321, 8212792877320956622, 1813984015431365158,
                 4164318454127338554, 7257271810282281545, 5058259733949390793, 5430591373227853130],
                [5650206961626598218, 8403243012567623812, 7971809870463753455, 8324418955728609960,
                 5847389489820718276, 12861344294088254785, 3985627926792223194, 14074576738596379253,
                 14677166034508512139, 13621946245343074601, 13874700052369206398, 12423702041521748374],
                [16013535669150441128, 7091905072847175840, 13943620389096099538, 12940558574404671786,
                 316144609941403776, 7008188781076427849, 13148803750370605367, 14947037516198990673,
                 17934185488913587367, 10687011564366282725, 12706082396497878590, 3035876250453060416],
                [16759367682222613731, 7481516247192760574, 4704115504388297021, 6542091791646790136,
                 1580625029137816715, 4019937839424546465, 5003001401166683744, 757306544573155546, 1497210414499683892,
                 16655275106876854939, 17528459834311873144, 5810515643603331317],
                [3100371139621831553, 34842226261830814, 3317540249493556498, 12553174747352813870,
                 12330333184744010550, 9903795369380363763, 9282235490939305989, 3764672702068916173,
                 5489687301381393292, 3743853516331175155, 10700786144920453341, 1422855245756071034],
                [9021732339738937936, 6877828916081025237, 3315595814449989472, 5102245831711735738,
                 4871514502094011651, 14780846039104111316, 6422016438319560468, 12421749884990867707,
                 2645285026156701854, 8094437560671599037, 14394069007187574684, 4980677506738404015],
                [3570108796848505982, 2262342564668585965, 15603378909120003962, 13792614784546624533,
                 4628812069025814954, 11650230909512687099, 6639954813820879519, 235138984295974775,
                 5065402318780347029, 5669415031938778553, 136022731187366557, 12534193030783728958]], [
                [9057150258758321531, 4706380025942219411, 6884268404378183479, 9519141923547941280,
                 1737662302142684460, 14832412851403929910, 17148136807581064711, 16187371660529908184,
                 10097957530407338257, 13963296446884438377, 15516297513279393445, 4255116113140342425],
                [4143997852207425897, 17199117635402387900, 17507713064090560022, 7464921127706627996,
                 11293534774622164598, 544894323790630034, 16130883687318079989, 4932810093143297032,
                 15244910330919665612, 6998364527351719657, 6196033879278607507, 13578155971392022245],
                [14104483415741139248, 17767200272222823625, 1641111235999016162, 9898729614007092558,
                 2265010478066071205, 3213018870679997313, 9996120152602427866, 2166987039331751876,
                 4269256707115893588, 12505149818295394742, 17642157693215138499, 14560903522844049670],
                [12336349563374544904, 13072386464279897443, 12256848464050894563, 10283571094822742803,
                 3480047493419944332, 4937910143372815291, 2703513239551252680, 112021330175099790,
                 15176333759716495338, 7907220604891510503, 1279601363542711304, 1771355025144135513],
                [16055170427380330174, 10412295799212880941, 1956690157979490183, 18156456157422122801,
                 5045050702590075802, 17147535757222991566, 11843449064277991239, 9119336116222550821,
                 11810686577073615330, 9465657769440607386, 13258594520277194467, 2721795938200935902],
                [11242291636113650436, 18087539754925142644, 7851356524259643410, 10395772949025933891,
                 16846626780208402801, 14004590674968409323, 10993307540259059695, 15231806697658448140,
                 6335674981234088049, 16635691215119439705, 13430813529873799311, 496149870859320667],
                [15017535252616913755, 13377814955895564006, 9278624148563598792, 10705858844730391868,
                 6054639366195952542, 16512665990536741857, 5240473528433390819, 1276116723136729736,
                 1626532608959698937, 2243773748318051610, 392180416385343789, 1770327995109111219],
                [15205107118464123574, 4645091044466051851, 8902042562601612089, 169990998953792424,
                 7787659640838290319, 14447850727981345915, 12212558322750895291, 6852053545451632516,
                 12174111268183934111, 15993551378379701946, 7195994424113606970, 348870426017589155]], [
                [1708465630801716979, 2646434717507468850, 18114689701313482528, 13053573902662609117,
                 12413420647452552203, 1587408464207320469, 12089020703048570287, 5002093172807646495,
                 18324254515687796447, 13785705213788601076, 16835335138566744385, 5780374958758414113],
                [10167872654003736533, 379868114724746064, 10276506513900832150, 2232778987079187366,
                 320544241784020308, 14985646153299191644, 11766755446721704408, 15684515578072210322,
                 9951663285025163417, 16938538556582837101, 7565445093958246396, 1319295817319803491],
                [2072874790914578614, 2139301763043786559, 17930431013442088650, 10965619201521439400,
                 961138447506307691, 2754088317359159334, 13931703990751932736, 1886771357370118147,
                 8627780109988105023, 11443749749303071669, 6273001227716749187, 7558529180683327443],
                [13972618324677873439, 9860756961086705806, 15636398416982848096, 11564326282351584988,
                 4991273375931247896, 12601544983114293740, 14910850928399852481, 12013286922218018142,
                 8681704437853329197, 9175843415446454191, 5863145214337365950, 1813240857757573643],
                [5971453749365250058, 8300963991836007141, 15161208582042964005, 10907514865778899268,
                 1922994855137772144, 2593575501824895132, 7377866345434716207, 1128892665014918545,
                 2151291765727964165, 6355211125733522180, 7449359791541518080, 5869105836722996427],
                [9025745579515081201, 14040020928807309380, 4781832042733405947, 15405341984559411130,
                 7686079994357982540, 8832155864809441273, 4680934631261033541, 2493459526419583919,
                 17147851466026960911, 12321752277310381154, 7688012981077484254, 13950985270391952592],
                [16864356949447156546, 15122018731483272760, 16032705622721490559, 12807570485118977858,
                 2349551870122095560, 8496557656728826607, 15554121699388512895, 2758463923494997134,
                 9310243176552629680, 2668187961693629556, 16551920873919309118, 3201468020397667968],
                [11196086044151020917, 2416662933399197770, 18275122503182960973, 11326703883896890733,
                 12362474933088466719, 1299190838134746799, 582158542434185271, 16261650963336651444, 51468537373925342,
                 11040390325576589355, 7232556151948475391, 3633184505537816575]], [
                [14513973250618136395, 13711785410842643888, 1878627983395126297, 216773293812849583,
                 2155432310882281853, 11635323018828468367, 14315665053798211527, 13711309031362072613,
                 14389067690636265087, 6664612157971258022, 13064275568141236139, 8046546155204179712],
                [16874424174096987982, 3097098870387372063, 7411112765886158857, 3914266866602858175,
                 4968554339201889274, 10225587566906047848, 15460044597684003268, 6417748947926689564,
                 14605321215217354922, 7477390811505664688, 4085846963842593893, 10815993487455893768],
                [11307857294187323617, 17381689548724801521, 9762982568930750796, 13490521178494523588,
                 17181007979684657600, 7739000956943664808, 11735533945091165968, 3614517230639604713,
                 15201038555577469280, 7833416863171183653, 13977193331456620317, 3378747264193553099],
                [5886240513789157534, 1024955253331005566, 11484557122306348477, 9059863243246535349,
                 16075249157205815314, 4447360412438072738, 5706351325453474927, 6047449379477254476,
                 12886537979475360321, 11015240546803074568, 16046529514093309354, 216338636075510340],
                [7583770619158220798, 6681448317433835164, 4524236674997580501, 7797206832683917359,
                 12720280209738729429, 9154953757690486000, 14887878999342534348, 16503263526149690083,
                 8958857229203312026, 12538715698969061087, 9666827644162010412, 16793331664577594900],
                [3993150917591623063, 4323059468746554894, 16184731850926831461, 132494861385880571,
                 10089721295799166791, 8005509791875936061, 5999474572681481267, 18426163514496074537,
                 3221661218401300903, 2102310075536902234, 12059142819331138293, 16679825405911481793],
                [11177994410793241341, 6466743308186655564, 3046908614053538336, 8757595242885905876,
                 15114825683403011879, 14178132689199963864, 10647868359661467442, 10871335119625063225,
                 14213975395259492091, 14094637462758766574, 17010736165836623179, 14794577045922115212],
                [2578965414327160206, 15233330741287611941, 8660834178295178222, 15661744522554474200,
                 17149796886184900613, 138879219994464465, 5565173620243746285, 5796415092095602671,
                 17020567709861161339, 17569585374269407128, 2867447810576714811, 6150259373872710020]], [
                [11360060902110288700, 13553803114616787073, 4125313948115713700, 13531212403081671110,
                 6731309112495350321, 792322303066632482, 5264125829950981111, 6585241606485849267,
                 14005822711306834336, 10884768677803915551, 13843613762089098521, 711989768065564732],
                [5239729562000266469, 15773956917046133974, 10222752111224406081, 11117336956003002706,
                 6213992356072169589, 9151199903954581623, 8307260444909706521, 15913912732687518170,
                 17078520070113961752, 12397386860697506237, 1107834944911351037, 9447346601892798254],
                [13151976222491048251, 13248406915750084869, 12741545936539560487, 14699831203714436699,
                 16008674291380385102, 2962857731643731987, 7134711138938381377, 1819248168484313915,
                 4234234976102872800, 2858132778650151378, 7879247699371676330, 15833076705217134046],
                [11324345502755142815, 6591251177445589662, 4127248575439742063, 7325435283506391204,
                 3149794567717908614, 3774077527463537406, 6214463952742939768, 18355614285957955185,
                 13349945048061914110, 1811868115873309891, 47302645112327191, 11688994719554230379],
                [14295651465832737460, 10452135084097195165, 7169499925818386482, 9966577526082191893,
                 13789202548669246284, 17827447366496434034, 12750559137428699799, 17478931752807876830,
                 965992379777140831, 13378642989904258697, 1847253822602051038, 15807198197132458892],
                [1012806065359159276, 13832583025126518993, 12668109231234005392, 13008591223928736343,
                 11936404547528731245, 3005253507473002867, 11469915278287964149, 3606939090940557784,
                 3791788217976334662, 13518232447610069654, 17551344569957266380, 14921805047621057062],
                [7816801014833067991, 1325086057539512458, 6328684695871489227, 782188046984930908, 8689924547460939618,
                 4024381993571795577, 5688721810562824820, 13013160027474913285, 8645707602959711025,
                 10632074743334270903, 6986845264191210988, 8695388815719712198],
                [8117596629073037163, 1069480841878748492, 8803642224878131071, 11254792400119106601,
                 717885398722442268, 12370449402956227523, 4438546772763858108, 6823950132416611281, 462904132505778871,
                 13763268431059869097, 11957738966196694212, 6510433065626191643]], [
                [1863184029973575689, 17370762402634742700, 11397008290360482272, 16108514045154730403,
                 13351550492867029713, 18072867076286633831, 11960132755821980524, 6420906549229061557,
                 7307072672847135488, 15085355145299448124, 3992466098702236020, 13870519894343830700],
                [15128981231230775536, 3745691695548657537, 12438542846094468909, 5775610973403401647,
                 177643186658695131, 1951420551133205996, 18136853196254298687, 2758910982128193708,
                 11250353315220102567, 4545374054882558662, 5870853829075876069, 14051576434752000397],
                [13250848215522762231, 3482089043870545274, 1659460992960983771, 3457109434788803520,
                 5095408037073224621, 9427825945975555806, 5704399868848869785, 4755456706681824726,
                 15583457755185832751, 6955498478489185749, 9700705879531056413, 14417525749347753763],
                [17626564733823423550, 11417916157395528372, 17790677554138263289, 11781272645845319620,
                 11924236904369849308, 2631989059472571929, 1670896097906018432, 16688145299163767615,
                 10538281742408482106, 4182234031058838977, 18296295809948709863, 9001137332307141835],
                [6508228369615541873, 15644347896929491371, 91453336012113742, 2484560851390491272,
                 14735899336878420023, 9609953362136851859, 12628004706451353746, 2138951364254087583,
                 13372373668688609161, 6156615530046408073, 2780780214149146871, 1178254920501662351],
                [14550171531053664904, 4666787841796210434, 9565004971039408045, 15660465681527599081,
                 17181535682709290424, 3632271278265460122, 11188786554374230205, 2154457976699930469,
                 5561126545175877183, 3070711696189246145, 12552226321624763053, 3924034947059558791],
                [18235135807900218860, 14685653036976753883, 16653426931840419535, 7587937925086874872,
                 678044083374041425, 13914626145507934956, 15465505123271033281, 13383183029095927258,
                 4510850512670238448, 4613391316051681865, 5279625405004261968, 10000799588009619058],
                [12590958125279107624, 17961805887528740440, 10507433266794060227, 5432184285240265319,
                 1265247534841707932, 9658277335968378860, 1315870582785863449, 17540355477125478954,
                 10420235724315105760, 15828767359619837988, 6144116186250660202, 4723056348332041363]]]


def indexPiece(piece):
    if (piece == 'P'):
        return 0
    if (piece == 'N'):
        return 1
    if (piece == 'B'):
        return 2
    if (piece == 'R'):
        return 3
    if (piece == 'Q'):
        return 4
    if (piece == 'K'):
        return 5
    if (piece == 'p'):
        return 6
    if (piece == 'n'):
        return 7
    if (piece == 'b'):
        return 8
    if (piece == 'r'):
        return 9
    if (piece == 'q'):
        return 10
    if (piece == 'k'):
        return 11
    else:
        return -1


def getKey(board):
    h = 0
    for tiles in range(len(board.square)):
        if board.square[tiles].pieceOnSquare.toString() != "-":
            piece = indexPiece(board.square[tiles].pieceOnSquare.toString())
            row = math.ceil((tiles + 1) / 8)
            column = (tiles + 1) - ((row - 1) * 8)
            h ^= zobTable[row - 1][column - 1][piece]
    return h


allSqParams = createSqParams()

isRecord = False
openings = defaultdict(list)
try:
    file_handle = open('openingTable.txt', 'r+')
    openings = json.loads(file_handle.read())
except:
    if isRecord:
        file_handle = open('openingTable.txt', 'w')

ax, ay = 0, 1
selectedImage = None
selectedLegals = None
resetC = []
loseGame = False
quitGame = False
mx, my = pygame.mouse.get_pos()
prevx, prevy = [0, 0]
winImage = False
winColour = None
winMessage = None
counter = 0
isMenu = True
aiPlayer = -1
playGame = -1
isAI = -1
isTransition = False
isAIthink = False
preTile = None
preboard = None

while not quitGame:
    if isMenu == True:
        screen.blit(background, (0, 0))
        display_text("press z to undo a move", "freesansbold.ttf", 32, (75, 139, 190), 400, 100)
        if isAI == -1:
            screen.blit(withfriend_pic, (0, square_height * 2))
            screen.blit(withAI_pic, (square_width * 4, square_height * 2))
        elif isAI == True:
            screen.blit(playwhite_pic, (0, square_height * 2))
            screen.blit(playblack_pic, (square_width * 4, square_height * 2))
        if playGame != -1:
            drawChessPieces()
            isMenu = False
            if aiPlayer == 0 and isAI:
                # minimax = Minimax(chessBoard, 1)
                # aiBoard = minimax.getBestMove()
                # chessBoard = aiBoard
                # newP = updateChessPieces()
                # everyPiece = newP
                # blackOrWhite = aiBoard.blackOrWhite
                bestMove = [0]
                move_thread = threading.Thread(target=AIfunc,
                                               args=(chessBoard, 2, bestMove))
                move_thread.start()
                isAIthink = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quitGame = True
                break
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if (pos[0] < square_width * 4 and pos[1] > square_height * 2 and pos[1] < square_height * 6):
                    if isAI == -1:
                        isAI = False
                        playGame = False
                    elif isAI == True:
                        aiPlayer = 1
                        playGame = False
                elif (pos[0] > square_width * 4 and pos[1] > square_height * 2 and pos[1] < square_height * 6):
                    if isAI == -1:
                        isAI = True
                    elif isAI == True:
                        aiPlayer = 0
                        playGame = False
        pygame.display.update()
        clock.tick(60)
        continue
    counter += 1
    if isAIthink and counter % 6 == 0:
        for eachTile in everyTile:
            everyTile[ax][0] = (75, 139, 190)
            if ax % 2 == 0 and ay % 2 != 0:
                everyTile[ax - 1][0] = (255, 255, 255)
            elif ax % 2 != 0 and ay % 2 != 0:
                everyTile[ax - 1][0] = (150, 75, 0)
            elif ax % 2 == 0 and ay % 2 == 0:
                everyTile[ax - 1][0] = (150, 75, 0)
            elif ax % 2 != 0 and ay % 2 == 0:
                everyTile[ax - 1][0] = (255, 255, 255)
        if ax % 8 == 0:
            ay += 1
        ax += 1
        if ax == 64:
            ax, ay = 0, 1
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            break
        if isAIthink:
            continue
        if event.type == pygame.MOUSEBUTTONDOWN:

            if selectedImage == None:
                mx, my = pygame.mouse.get_pos()
                for piece in range(len(everyPiece)):

                    if everyPiece[piece][2].allegiance == blackOrWhite:

                        if everyPiece[piece][1][0] < mx < everyPiece[piece][1][0] + 100:
                            if everyPiece[piece][1][1] < my < everyPiece[piece][1][1] + 100:
                                selectedImage = piece
                                prevx = everyPiece[piece][1][0]
                                prevy = everyPiece[piece][1][1]
                                preTile = everyPiece[selectedImage][2].getPlace()

                                selectedLegals = everyPiece[selectedImage][2].possibleMoves(chessBoard)
                                for legals in selectedLegals:
                                    resetC.append([legals, everyTile[legals][0]])

                                    if everyTile[legals][0] == (150, 75, 0):
                                        everyTile[legals][0] = (127, 255, 0)
                                    else:
                                        everyTile[legals][0] = (118, 238, 0)

        if event.type == pygame.MOUSEMOTION and not selectedImage == None:
            mx, my = pygame.mouse.get_pos()
            everyPiece[selectedImage][1][0] = mx - 50
            everyPiece[selectedImage][1][1] = my - 50

        if event.type == pygame.MOUSEBUTTONUP:

            for resets in resetC:
                everyTile[resets[0]][0] = resets[1]

            try:

                pieceMoves = everyPiece[selectedImage][2].possibleMoves(chessBoard)
                legal = False
                theMove = 0
                for moveDes in pieceMoves:
                    if allSqParams[moveDes][0] < everyPiece[selectedImage][1][0] + 50 < allSqParams[moveDes][1]:
                        if allSqParams[moveDes][2] < everyPiece[selectedImage][1][1] + 50 < allSqParams[moveDes][3]:
                            legal = True
                            theMove = moveDes
                if legal == False:
                    everyPiece[selectedImage][1][0] = prevx
                    everyPiece[selectedImage][1][1] = prevy
                else:
                    preboard = chessBoard
                    everyPiece[selectedImage][1][0] = allSqParams[theMove][0]
                    everyPiece[selectedImage][1][1] = allSqParams[theMove][2]
                    thisMove = Move(chessBoard, everyPiece[selectedImage][2], theMove)
                    newBoard = thisMove.newBoard()
                    if newBoard != False and newBoard != "lose":
                        chessBoard = newBoard
                    if newBoard == "lose" and blackOrWhite == "Black":
                        quitGame = True
                        loseGame = True
                        winMessage = "Black Wins"
                        winColour = (0, 0, 0)
                    elif newBoard == "lose" and blackOrWhite == "White":
                        quitGame = True
                        loseGame = True
                        winMessage = "White Wins"
                        winColour = (0, 0, 0)
                    newP = updateChessPieces()
                    everyPiece = newP
                    blackOrWhite = newBoard.blackOrWhite
                    # chessBoard.printBoard()
                    # print(preTile)
                    # print(thisMove)
                    # print(openings)
                    # evaluate(newBoard)
                    if isAI and newBoard != "lose":
                        if blackOrWhite == "White" and aiPlayer == 0:
                            # minimax = Minimax(chessBoard, 1)
                            # aiBoard = minimax.getBestMove()
                            # chessBoard = aiBoard
                            # newP = updateChessPieces()
                            # everyPiece = newP
                            # blackOrWhite = aiBoard.blackOrWhite
                            bestMove = [0]
                            move_thread = threading.Thread(target=AIfunc,
                                                           args=(chessBoard, 2, bestMove))
                            move_thread.start()
                            isAIthink = True
                        else:
                            # minimax = Minimax(chessBoard, 1)
                            # aiBoard = minimax.getBestMove()
                            # chessBoard = aiBoard
                            # newP = updateChessPieces()
                            # everyPiece = newP
                            # blackOrWhite = chessBoard.blackOrWhite
                            bestMove = [0]
                            move_thread = threading.Thread(target=AIfunc,
                                                           args=(chessBoard, 2, bestMove))
                            move_thread.start()
                            isAIthink = True
                    # print("start")
                    if isRecord:
                        # print("start")
                        key = getKey(chessBoard)
                        key = str(key)
                        openingMove = [chessBoard.square[theMove].pieceOnSquare.toString(), theMove, preTile]
                        # print(openingMove)
                        if key not in openings:
                            openings[key] = openingMove

            except:
                pass

            prevy = 0
            prevx = 0
            selectedImage = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and preboard != None:
                chessBoard = preboard
                newP = updateChessPieces()
                everyPiece = newP
                blackOrWhite = chessBoard.blackOrWhite

    if isAIthink:
        if not move_thread.is_alive():
            isAIthink = False
            num = 0
            for i in range(8):
                for _ in range(8):
                    if num % 2 == 0 and i % 2 != 0:
                        everyTile[num][0] = (150, 75, 0)
                    elif num % 2 != 0 and i % 2 != 0:
                        everyTile[num][0] = (255, 255, 255)
                    elif num % 2 == 0 and i % 2 == 0:
                        everyTile[num][0] = (255, 255, 255)
                    elif num % 2 != 0 and i % 2 == 0:
                        everyTile[num][0] = (150, 75, 0)
                    num += 1

            # for each in range(0,63):
            #     if each % 2 == 0:
            #         everyTile[each][0] = (255, 255, 255)
            #     else:
            #         everyTile[each][0] = (150, 75, 0)
            chessBoard = bestMove[0]
            if chessBoard == "lose" and blackOrWhite == "Black":
                quitGame = True
                loseGame = True
                winMessage = "Black Wins"
                winColour = (0, 0, 0)
            elif chessBoard == "lose" and blackOrWhite == "White":
                quitGame = True
                loseGame = True
                winMessage = "White Wins"
                winColour = (0, 0, 0)
            newP = updateChessPieces()
            everyPiece = newP
            blackOrWhite = chessBoard.blackOrWhite

    if not isMenu:
        screen.fill((255, 255, 255))

    for info in everyTile:
        pygame.draw.rect(screen, info[0], info[1])

    for img in everyPiece:
        screen.blit(img[0], img[1])

    pygame.display.update()
    clock.tick(60)

while loseGame:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

    display_text(winMessage, "freesansbold.ttf", 32, winColour, 400, 400)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

if isRecord:
    file_handle.seek(0)
    json = json.dumps(openings)
    file_handle.write(json)
    file_handle.truncate()
    file_handle.close()
quit()
