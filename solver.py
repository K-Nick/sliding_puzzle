import numpy as np
from engine import GameEngine
from const import *
import queue

class Solver:
    @staticmethod
    def initSolver(initBoard, targetBoard):
        Solver.boardSize = initBoard.shape[0]
        Solver.initBoard = initBoard
        Solver.targetBoard = targetBoard
        Solver.getFactorial(Solver.boardSize * Solver.boardSize)

        Solver.forwardMap = dict()
        Solver.backwardMap = dict()
        Solver.forwardQueue = queue.Queue()
        Solver.backwardQueue = queue.Queue()

    @staticmethod
    def getFactorial(n):
        """计算阶乘"""
        Solver.fact = np.zeros(n+1, dtype=np.int64)
        Solver.fact[0] = 1
        for i in range(1, n+1):
            Solver.fact[i] = Solver.fact[i-1] * i

    @staticmethod
    def getHash(board):
        """康托展开，详见 https://zh.wikipedia.org/wiki/%E5%BA%B7%E6%89%98%E5%B1%95%E5%BC%80"""
        seq = board.reshape(-1)
        length = seq.shape[0]
        cnt = np.ones(length+1, dtype=np.int64)
        hash = 0
        for i in range(length):
            curRank = 0
            for j in range(seq[i]):
                curRank += cnt[j]
            cnt[seq[i]] = 0
            hash += curRank * Solver.fact[length-i]
        return hash

    @staticmethod
    def expand(status, hashMap, statusQueue):
        """BFS的单步扩展，返回扩展出的hash结果"""
        ops = [UP, DOWN, LEFT, RIGHT]
        board, blankPos, hash = status
        nextHashList = []

        for op in ops:
            if GameEngine.isValidMovement(blankPos, op):
                nextBoard, nextBlankPos = GameEngine.nextStatus(board, blankPos, op)
                nextHash = Solver.getHash(nextBoard)
                if nextHash not in hashMap.keys():
                    statusQueue.put((nextBoard, nextBlankPos, nextHash))
                    hashMap[nextHash] = (hash, op)
                    nextHashList.append(nextHash)

        return nextHashList

    @staticmethod
    def collectResult(midHash):
        hash = midHash
        moveList = []
        while Solver.forwardMap[hash] is not None:
            moveList = [Solver.forwardMap[hash][1]] + moveList
            hash = Solver.forwardMap[hash][0]

        hash = midHash
        while Solver.backwardMap[hash] is not None:
            moveList = moveList + [MOVEMENT_REV_DICT[Solver.backwardMap[hash][1]]]
            hash = Solver.backwardMap[hash][0]

        return moveList


    @staticmethod
    def bidirectionalBFS():
        board = Solver.initBoard
        blankPos = GameEngine.getBlankPosition(board)
        hash = Solver.getHash(board)
        Solver.forwardMap[hash] = None
        Solver.forwardQueue.put((board, blankPos, hash))

        revBoard = Solver.targetBoard
        revBlankPos = GameEngine.getBlankPosition(revBoard)
        revHash = Solver.getHash(revBoard)
        Solver.backwardMap[revHash] = None
        Solver.backwardQueue.put((revBoard, revBlankPos, revHash))

        if revHash == hash:
            return []

        moveList = []
        endFlag = False

        while True:
            qSize = Solver.forwardQueue.qsize()
            for i in range(qSize):
                board, blankPos, hash = Solver.forwardQueue.get()
                forwardHashList = Solver.expand((board, blankPos, hash), Solver.forwardMap, Solver.forwardQueue)
                for h in forwardHashList:
                    if h in Solver.backwardMap.keys():
                        moveList = Solver.collectResult(h)
                        endFlag = True
                if endFlag: break
            if endFlag: break

            qSize = Solver.backwardQueue.qsize()
            for i in range(qSize):
                revBoard, revBlankPos, revHash = Solver.backwardQueue.get()
                backwardHashList = Solver.expand((revBoard, revBlankPos, revHash), Solver.backwardMap, Solver.backwardQueue)
                for h in backwardHashList:
                    if h in Solver.forwardMap.keys():
                        moveList = Solver.collectResult(h)
                        endFlag = True
                if endFlag: break
            if endFlag: break

        return moveList
