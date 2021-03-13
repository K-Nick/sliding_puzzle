import pygame
import sys
from pygame.locals import *
import argparse
import numpy as np
from const import *
from engine import GameEngine
from solver import Solver



def parseArgs():
    """处理输入的参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_size", type=int, default=3, help="拼图的尺寸n，最终生成n x n的拼图")
    parser.add_argument("--input_puzzle", type=str, default=None, help="输入初始拼图（可选）")
    parser.add_argument("--random_step", type=int, default=20, help="打乱生成新拼图时的随机步数")
    args = parser.parse_args()

    global BOARD_SIZE, XMARGIN, YMARGIN, TARGET_STATE
    BOARD_SIZE =  args.board_size
    XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARD_SIZE + (BOARD_SIZE - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARD_SIZE + (BOARD_SIZE - 1))) / 2)

    return args

def makeText(text, color, bgcolor, top, left):
    """在游戏界面上设置带背景的字"""
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return textSurf, textRect

def getLeftTopOfTile(tileX, tileY):
    """计算拼图区域的左上角位置"""
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return left, top

def drawTile(tiley, tilex, number, adjx=0, adjy=0):
    """画数字块"""
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def drawBoard(board, message):
    """画拼图"""
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i, j]:
                drawTile(i, j, board[i, j])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARD_SIZE * TILESIZE
    height = BOARD_SIZE * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = GameEngine.getBlankPosition(board)
    if direction == UP:
        movex = blankx - 1
        movey = blanky
    elif direction == DOWN:
        movex = blankx + 1
        movey = blanky
    elif direction == LEFT:
        movex = blankx
        movey = blanky - 1
    elif direction == RIGHT:
        movex = blankx
        movey = blanky + 1

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movey, movex)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], -i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    args = parseArgs()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    # 设置游戏按钮，120为到窗口右边缘的距离，60，30分别为到窗口下边缘距离
    NEW_SURF, NEW_RECT = makeText("New Game", TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText("Solve", TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    GameEngine.initEngine(BOARD_SIZE)
    board, blankPos = GameEngine.getNewPuzzle(input_puzzle=args.input_puzzle, numSlides=args.random_step)


    while True:

        msg = INSTRUCTION

        # 以下for event阶段将根据用户操作判断滑动方向slideTo
        slideTo = None

        # 判断是否胜利
        if (board == GameEngine.TARGET_BOARD).all():
            msg = WIN

        # 绘制当前轮的图像
        drawBoard(board, msg)

        # 每一轮检测是否触发ESC键退出游戏
        checkForQuit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if NEW_RECT.collidepoint(event.pos):
                    board, blankPos = GameEngine.getNewPuzzle(args.input_puzzle, args.random_step)
                    # print("------NEW PUZZLE------")
                    # print(board)
                elif SOLVE_RECT.collidepoint(event.pos):
                    Solver.initSolver(board, GameEngine.TARGET_BOARD)
                    moveList = Solver.bidirectionalBFS()
                    print(moveList)
                    for move in moveList:
                        slideAnimation(board, move, SOLVE_INSTRUCTION, 8)
                        board, blankPos = GameEngine.nextStatus(board, blankPos, move)

            if event.type == KEYUP:
                # 仅从键盘检测输入
                if event.key in (K_LEFT, K_a) and GameEngine.isValidMovement(blankPos, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and GameEngine.isValidMovement(blankPos, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and GameEngine.isValidMovement(blankPos, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and GameEngine.isValidMovement(blankPos, DOWN):
                    slideTo = DOWN

        if slideTo: # 该轮读到用户操作
            slideAnimation(board, slideTo, INSTRUCTION, 8)
            board, blankPos = GameEngine.nextStatus(board, blankPos, slideTo)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def testHash():
    GameEngine.initEngine(3)
    boardA = np.array([
        [2, 0, 5],
        [4, 1, 3],
        [7, 8, 6]
    ])
    boardB = np.array([
        [4, 2, 0],
        [5, 1, 3],
        [7, 8, 6]
    ])
    Solver.initSolver(GameEngine.TARGET_BOARD, GameEngine.TARGET_BOARD)
    print(Solver.getHash(boardA))
    print(Solver.getHash(boardB))

def testSolver():
    args = parseArgs()
    GameEngine.initEngine(3)
    board = np.array([
        [7, 1, 0],
        [5, 4, 3],
        [8, 2, 6]
    ])
    blankPos = GameEngine.getBlankPosition(board)
    Solver.initSolver(board, GameEngine.TARGET_BOARD)
    moveList = Solver.bidirectionalBFS()
    print(moveList)

def testRepeat():
    """
    [[4 2 5]
     [1 0 3]
     [7 8 6]]
    """
    args = parseArgs()
    GameEngine.initEngine(3)
    board, blankPos = GameEngine.getNewPuzzle(args.input_puzzle, args.random_step)
    Solver.initSolver(board, GameEngine.TARGET_BOARD)
    moveList = Solver.bidirectionalBFS()
    print(moveList)
    lastMove = None
    for idx, move in enumerate(moveList):
        if MOVEMENT_REV_DICT[move] == lastMove:
            print(idx, move)
            input()
        lastMove = move

if __name__=="__main__":
    main()
    # testSolver()
    # for i in range(100): testRepeat()
