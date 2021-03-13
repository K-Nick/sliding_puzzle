from const import *
import numpy as np
import random
import pandas as pd

class GameEngine:

    BOARD_SIZE = 3
    TARGET_BOARD = None
    TARGET_BLANK_POS = None

    @staticmethod
    def initEngine(board_size):
        GameEngine.BOARD_SIZE = board_size
        GameEngine.TARGET_BOARD, GameEngine.TARGET_BLANK_POS = GameEngine.getTargetStatus()

    @staticmethod
    def getBlankPosition(board):
        BOARD_SIZE = GameEngine.BOARD_SIZE
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i, j] == BLANK:
                    return i, j

    @staticmethod
    def isValidMovement(blankPos, movement):
        BOARD_SIZE = GameEngine.BOARD_SIZE
        dx, dy = MOVEMENT_DICT[movement]
        curx, cury = blankPos
        nextx, nexty = curx+dx, cury+dy
        return 0 <= nextx < BOARD_SIZE and 0 <= nexty < BOARD_SIZE

    @staticmethod
    def getRandomMove(blankPos, lastMove=None):
        moveList = [UP, DOWN, LEFT, RIGHT]

        if lastMove == UP or not GameEngine.isValidMovement(blankPos, DOWN):
            moveList.remove(DOWN)
        if lastMove == DOWN or not GameEngine.isValidMovement(blankPos, UP):
            moveList.remove(UP)
        if lastMove == RIGHT or not GameEngine.isValidMovement(blankPos, LEFT):
            moveList.remove(LEFT)
        if lastMove == LEFT or not GameEngine.isValidMovement(blankPos, RIGHT):
            moveList.remove(RIGHT)
        # print(GameEngine.BOARD_SIZE,blankPos, lastMove, moveList)

        return random.choice(moveList)

    @staticmethod
    def getTargetStatus():
        BOARD_SIZE = GameEngine.BOARD_SIZE
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        counter = 1
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board[i, j] = counter
                counter += 1

        board[BOARD_SIZE-1][BOARD_SIZE-1] = BLANK

        return board, (BOARD_SIZE-1, BOARD_SIZE-1)


    @staticmethod
    def getNewPuzzle(input_puzzle=None, numSlides=20):
        """获取初始局面，如用户已经输入则直接返回"""

        if input_puzzle is not None:
            print(f"reading from {input_puzzle}...")
            # board = np.genfromtxt(input_puzzle, dtype=int)
            board = pd.read_csv(input_puzzle, header=None).to_numpy()
            print(board)
            blankPos = GameEngine.getBlankPosition(board)

        else:
            board = GameEngine.TARGET_BOARD.copy()
            blankPos = GameEngine.TARGET_BLANK_POS

            move = None

            for i in range(numSlides):
                move = GameEngine.getRandomMove(blankPos, move)
                board, blankPos = GameEngine.nextStatus(board, blankPos, move)

        print(board)

        return board, blankPos

    @staticmethod
    def nextStatus(board, blankPos, movement):
        """模拟生成执行动作movement后的状态board, blankPos"""
        board = board.copy()
        if GameEngine.isValidMovement(blankPos, movement):
            dx, dy = MOVEMENT_DICT[movement]
            curx, cury = blankPos
            nextx, nexty = curx+dx, cury+dy
            tmp = board[nextx, nexty]
            board[nextx, nexty] = board[curx, cury]
            board[curx, cury] = tmp

            blankPos = (nextx, nexty)

        return board, blankPos

