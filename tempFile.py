import pygame
import copy
import sys

class Board:
    # creates the board through a dictionary where each square is assigned a piece also check what pieces are current in play and works out
    #the possible moves for a specific piece
    square = {}
    enPassantPawn = None
    enPassantPawnBehind = None
    blackOrWhite = "White"

    def __init__(self):
        pass

    def piecesInPlay(self, allegiance):

        playableP = []
        for tile in range(len(self.square)):
            if not self.square[tile].pieceOnSquare.toString() == "-":
                if self.square[tile].pieceOnSquare.allegiance == allegiance:
                    playableP.append(self.square[tile].pieceOnSquare)

        return playableP

    def possibleMoves(self, pieces, board):
        allPossibleMoves = []
        for piece in pieces:
            pieceMoves = piece.possibleMoves(board)
            for move in pieceMoves:
                allPossibleMoves.append([move, piece])
        return allPossibleMoves


    def makeBoard(self):

        for x in range(64):
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
    #defines what pieces is on each square and where each piece is

    pieceOnSquare = None
    squareLocation = None

    def __init__(self, coordinate, piece):
        self.squareLocation = coordinate
        self.pieceOnSquare = piece

class Piece:
    #super class for each piec passing each class if its the first move and also where the piece is in an edge column/row

    startMove = True

    def __init__(self):
        pass

    firstColumn = [0,8,16,24,32,40,48,56]
    secondColumn = [1,9,17,25,33,41,49,57]
    seventhColumn = [6,14,22,30,38,46,54,62]
    eighthColumn = [7,15,23,31,39,47,55,63]

    firstRow = [0,1,2,3,4,5,6,7]
    eighthRow = [63,62,61,60,59,58,57,56]

class Bishop(Piece):
    #defines how the bishop moves and what should happen if it is an edge case also the minMaxValue to the AI and what player it belonges to
    #its place on the board too
    allegiance = None
    place = None
    moveVector = [-9, -7, 7, 9]
    minMaxValue = 300

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "B" if self.allegiance == "Black" else "b"


    def possibleMoves(self, board):

        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place
            while 0 <= destCoord < 64:
                badMove = self.edgeCases(destCoord, vector)
                if badMove:
                    #print('bad')
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
    moveVector = [-17,-15,-10,-6,6,10,15,17]
    minMaxValue = 300

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place


    def toString(self):
        return "N" if self.allegiance == "Black" else "n"

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

    def possibleMoves(self, board):
        possibleMove = []
        for vector in self.moveVector:
            destCoord = self.place
            while 0 <= destCoord < 64:
                badMove = self.edgeCases(destCoord, vector)
                if badMove:
                    #print('bad')
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
    moveVector = [-8,-1,1,8]
    minMaxValue = 500

    def __init__(self, allegiance, place):
        self.allegiance = allegiance
        self.place = place

    def toString(self):
        return "R" if self.allegiance == "Black" else "r"

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
                            # break regardless of allegiance because blocked
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

class BoardEvaluator:

    def __init__(self):
        pass

    def evaluate(self, board, depth):
        return self.scorePlayer("White", board) - self.scorePlayer("Black", board)

    def scorePlayer(self, player, board):
        return self.pieceValue(player, board) + self.mobility(player, board)

    def mobility(self, player, board):
        presentPieces = board.piecesInPlay(player)
        return len(board.possibleMoves(presentPieces, board))

    def pieceValue(self, player, board):
        pieceValues = 0
        presentPieces = board.piecesInPlay(player)

        for piece in presentPieces:
            pieceValues += piece.minMaxValue

        return pieceValues

class Minimax:

    board = None
    depth = None
    boardEvaluator = None
    currentValue = None
    highestSeenValue = None
    lowestSeenValue = None
    bestMove = None

    def __init__(self, board, depth):
        self.board = board
        self.depth = depth
        self.boardEvaluator = BoardEvaluator()

    def getMove(self):

        blackOrWhite = self.board.blackOrWhite
        presentPieces = self.board.piecesInPlay(blackOrWhite)
        allPossibleMoves = self.board.possibleMoves(presentPieces, self.board)

        self.highestSeenValue = -sys.maxsize
        self.lowestSeenValue = sys.maxsize

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if newboard is not False:

                if blackOrWhite == "White":
                    self.currentValue = self.min(newboard, self.depth)
                else:
                    self.currentValue = self.max(newboard, self.depth)

                if blackOrWhite == "White" and self.currentValue > self.highestSeenValue:
                    self.highestSeenValue = self.currentValue
                    self.bestMove = newboard
                if blackOrWhite == "Black" and self.currentValue < self.lowestSeenValue:
                    self.lowestSeenValue = self.currentValue
                    self.bestMove = newboard

        return self.bestMove

    def max(self, board, depth):

        # TODO checkmate/stalemate
        if depth == 0 and not Move.checkIfMateOrStale(board, board.blackOrWhite):
            return self.boardEvaluator.evaluate(board, depth)

        highestSeenValue = -sys.maxsize
        presentPieces = board.piecesInPlay(board.blackOrWhite)
        allPossibleMoves = board.possibleMoves(presentPieces, board)

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if not newboard == False:
                minMaxValue = self.min(newboard, depth - 1)
                if minMaxValue >= highestSeenValue:
                    highestSeenValue = minMaxValue

        return highestSeenValue

    def min(self, board, depth):

        # TODO checkmate/stalemate
        if depth == 0 and not Move.checkIfMateOrStale(board, board.blackOrWhite):
            return self.boardEvaluator.evaluate(board, depth)

        lowestSeenValue = sys.maxsize
        presentPieces = board.piecesInPlay(board.blackOrWhite)
        allPossibleMoves = board.possibleMoves(presentPieces, board)

        for myMoves in allPossibleMoves:
            makeMove = Move(self.board, myMoves[1], myMoves[0])
            newboard = makeMove.newBoard()
            if not newboard == False:
                minMaxValue = self.min(newboard, depth - 1)
                if minMaxValue <= lowestSeenValue:
                    lowestSeenValue = minMaxValue

        return lowestSeenValue

pygame.init()
gameDisplay = pygame.display.set_mode((800, 800))
pygame.display.set_caption("PyChess")
clock = pygame.time.Clock()

chessBoard = Board()
chessBoard.makeBoard()
# chessBoard.printBoard()

everyTile = []
everyPiece = []
blackOrWhite = chessBoard.blackOrWhite

def display_text(message, style, size, colour, x, y):
    text = pygame.font.Font(style,size).render(message, True, colour, (0))
    textRect = text.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(text, textRect)

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
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])
    everyTile.append([color, [x, y, w, h]])

def drawChessPieces():
    xpos = 0
    ypos = 0
    color = 0
    width = 100
    height = 100
    black = (150,75,0)
    white = (255,255,255)
    number = 0
    for _ in range(8):
        for _ in range(8):
            if color % 2 == 0:
                squares(xpos, ypos, width, height, white)
                if not chessBoard.square[number].pieceOnSquare.toString() == "-":
                    img = pygame.image.load("./ChessArt/" + chessBoard.square[number].pieceOnSquare.allegiance[0].upper() + chessBoard.square[
                        number].pieceOnSquare.toString().upper() + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    everyPiece.append([img, [xpos, ypos], chessBoard.square[number].pieceOnSquare])
                xpos += 100
            else:
                squares(xpos, ypos, width, height, black)
                if not chessBoard.square[number].pieceOnSquare.toString() == "-":
                    img = pygame.image.load("./ChessArt/" + chessBoard.square[number].pieceOnSquare.allegiance[0].upper() + chessBoard.square[
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


allSqParams = createSqParams()
drawChessPieces()


selectedImage = None
selectedLegals = None
resetC = []
quitGame = False
mx, my = pygame.mouse.get_pos()
prevx, prevy = [0,0]
loseGame = False
winImage = False
winColour = None
word = None
count = 0

while not quitGame:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if selectedImage == None:
                mx, my = pygame.mouse.get_pos()
                for piece in range(len(everyPiece)):

                    if everyPiece[piece][2].allegiance == blackOrWhite:

                        if everyPiece[piece][1][0] < mx < everyPiece[piece][1][0]+100:
                            if everyPiece[piece][1][1] < my < everyPiece[piece][1][1] + 100:
                                selectedImage = piece
                                prevx = everyPiece[piece][1][0]
                                prevy = everyPiece[piece][1][1]

                                selectedLegals = everyPiece[selectedImage][2].possibleMoves(chessBoard)
                                for legals in selectedLegals:
                                    resetC.append([legals, everyTile[legals][0]])


                                    if everyTile[legals][0] == (150,75,0):
                                        everyTile[legals][0] = (127, 255, 0)
                                    else:
                                        everyTile[legals][0] = (118, 238, 0)


        if event.type == pygame.MOUSEMOTION and not selectedImage == None:

            mx, my = pygame.mouse.get_pos()
            everyPiece[selectedImage][1][0] = mx-50
            everyPiece[selectedImage][1][1] = my-50

        if event.type == pygame.MOUSEBUTTONUP:

            for resets in resetC:
                everyTile[resets[0]][0] = resets[1]

            try:



                pieceMoves = everyPiece[selectedImage][2].possibleMoves(chessBoard)
                legal = False
                theMove = 0
                for moveDes in pieceMoves:
                    if allSqParams[moveDes][0] < everyPiece[selectedImage][1][0]+50 < allSqParams[moveDes][1]:
                        if allSqParams[moveDes][2] < everyPiece[selectedImage][1][1]+50 < allSqParams[moveDes][3]:
                            legal = True
                            theMove = moveDes
                if legal == False:
                    everyPiece[selectedImage][1][0] = prevx
                    everyPiece[selectedImage][1][1] = prevy
                else:
                    everyPiece[selectedImage][1][0] = allSqParams[theMove][0]
                    everyPiece[selectedImage][1][1] = allSqParams[theMove][2]

                    thisMove = Move(chessBoard, everyPiece[selectedImage][2], theMove)
                    newBoard = thisMove.newBoard()
                    if newBoard != False and newBoard != "lose":
                        chessBoard = newBoard
                    elif newBoard == "lose" and blackOrWhite == "Black":
                        chessBoard = newBoard
                        quitGame = True
                        word = "Black Wins"
                        winColour = (255, 255, 255)
                    elif newBoard == "lose" and blackOrWhite == "White":
                        chessBoard = newBoard
                        quitGame = True
                        word = "White Wins"
                        winColour = (0, 0, 0)

                    newP = updateChessPieces()
                    everyPiece = newP
                    blackOrWhite = newBoard.blackOrWhite

                    if blackOrWhite == "Black":
                        aiBoard = True
                        minimax = Minimax(chessBoard, 1)
                        aiBoard = minimax.getMove()
                        chessBoard = aiBoard
                        newP = updateChessPieces()
                        everyPiece = newP
                        blackOrWhite = aiBoard.blackOrWhite

            except:
                pass

            prevy = 0
            prevx = 0
            selectedImage = None


    gameDisplay.fill((255, 255, 255))

    for info in everyTile:
        pygame.draw.rect(gameDisplay, info[0], info[1])

    for img in everyPiece:
        gameDisplay.blit(img[0], img[1])



    pygame.display.update()
    clock.tick(60)

while not loseGame:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

    display_text(word, "freesansbold.ttf", 32, winColour, 400, 400)
    pygame.display.update()
    clock.tick(60)
