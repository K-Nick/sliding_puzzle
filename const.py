TILESIZE = 50
WINDOWWIDTH = 1280
WINDOWHEIGHT = 640
FPS = 30
BLANK = 0

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

MOVEMENT_DICT = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1)
}

MOVEMENT_REV_DICT = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

INSTRUCTION = 'Click tile or press arrow keys to slide.'
SOLVE_INSTRUCTION = "Automatically Solving..."
WIN = 'You WIN!'

# global but should be set by player
BOARD_SIZE = 0
XMARGIN = 0
YMARGIN = 0
