import pygame
from pygame.locals import *
import argparse
import numpy as np
from const import *
from engine import GameEngine



def parseArgs():
    """处理输入的参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_size", type=int, default=3, help="拼图的尺寸n，最终生成n x n的拼图")
    parser.add_argument("--input_puzzle", type=str, default=None, help="输入初始地图（可选）")
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

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
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
            if board[i,j]:
                drawTile(j, i, board[i, j])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARD_SIZE * TILESIZE
    height = BOARD_SIZE * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    args = parseArgs()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    # 设置游戏按钮，120为到窗口右边缘的距离，90，60，30分别为到窗口下边缘距离
    RESET_SURF, RESET_RECT = makeText("Reset", TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText("New Game", TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText("Solve", TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    GameEngine.initEngine(BOARD_SIZE)
    board, blankPos = GameEngine.getNewPuzzle(args.input_puzzle)

    while True:
        drawBoard(board, '')
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=="__main__":
    main()