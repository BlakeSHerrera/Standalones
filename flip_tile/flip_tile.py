#flip_tile.py

import pygame, time, random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = GRAY = (127, 127, 127)

class tile:
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def flip(self):
        global game_display
        self.color = not self.color
        game_display.fill(GRAY, rect = [
            self.x * tile.SIZE,
            self.y * tile.SIZE,
            tile.SIZE,
            tile.SIZE])
        game_display.fill(WHITE if self.color else BLACK, rect = [
            self.x * tile.SIZE + 1,
            self.y * tile.SIZE + 1,
            tile.SIZE - 1,
            tile.SIZE - 1])

def num(s = ''):
    while True:
        try:
            return int(input(s + ': '))
        except ValueError:
            print('not a num')

def __main__(nr, nc, ts):

    def ib(r, c):
        return 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS
    
    NUM_ROWS = nr
    NUM_COLS = nc
    tile.SIZE = ts

    DISPLAY_WIDTH = NUM_COLS * tile.SIZE + 1
    DISPLAY_HEIGHT = NUM_ROWS * tile.SIZE + 1
    DISPLAY_CAPTION = 'Flip tile'
    FPS = 10
    CLOCK = pygame.time.Clock()

    global game_display
    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption(DISPLAY_CAPTION)

    game_display.fill(GRAY)

    tiles = []
    for r in range(NUM_ROWS):
        tiles.append([])
        for c in range(NUM_COLS):
            tiles[-1].append(tile(c, r, True))
            tiles[-1][-1].flip()

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                r = event.pos[1] // tile.SIZE
                c = event.pos[0] // tile.SIZE
                if event.button == 3: #rclick
                    if ib(r, c):
                        tiles[r][c].flip()
                elif event.button == 1: #lclick
                    for dr, dc in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
                        if ib(r + dr, c + dc):
                            tiles[r + dr][c + dc].flip()
                pygame.display.update()
        CLOCK.tick(FPS)

__main__(num('cols'), num('rows'), num('size of tile (pixels)'))

pygame.quit()
