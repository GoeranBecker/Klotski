

import pygame
import random


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
GAME_SIZE = int(WINDOW_HEIGHT * 0.85)
BLOCK_MARGIN = int(GAME_SIZE * 0.02)
NUM_BLOCKS = 6
CORNER_RADIUS = 2
FPS = 30
DEBUG = True

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Klotski")
clock = pygame.time.Clock()     ## For syncing the FPS


def calcTileX(colIndex):
    return (WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN + colIndex * (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS + BLOCK_MARGIN


def calcTileY(rowIndex):
    return (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN + rowIndex * (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS + BLOCK_MARGIN
    


class Frame:
    def __init__(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2,
                                                    (WINDOW_HEIGHT - GAME_SIZE) // 2,
                                                    GAME_SIZE,
                                                    GAME_SIZE), 0, CORNER_RADIUS)
        pygame.draw.rect(surface, BLACK, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                                    (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                                    GAME_SIZE - 2 * BLOCK_MARGIN,
                                                    GAME_SIZE - 2 * BLOCK_MARGIN), 0, CORNER_RADIUS)
        pygame.draw.rect(surface, BLACK, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + GAME_SIZE - BLOCK_MARGIN,
                                                (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN + 2 * (GAME_SIZE // NUM_BLOCKS),
                                                BLOCK_MARGIN,
                                                GAME_SIZE // NUM_BLOCKS))
        

class Tile:
    def __init__(self, color, row, col, rowspan=1, colspan=1):
        self.color = color
        self.row = row
        self.col = col
        self.rowspan = rowspan
        self.colspan = colspan
        self.dragged = False
        self.rect = pygame.Rect(calcTileX(self.col),
                                calcTileY(self.row),
                                ((GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN) * self.rowspan + (self.rowspan - 1) * BLOCK_MARGIN,
                                ((GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN) * self.colspan + (self.colspan - 1) * BLOCK_MARGIN)
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 1, CORNER_RADIUS)


    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.dragged == True
                print(self.posInside(event.pos[0], event.pos[1]))


    def posInside(self, x, y):
        return (self.rect.left < x < self.rect.right 
                and self.rect.top < y < self.rect.bottom)
         

frame = Frame()
debugTiles = [Tile(RED, i, j) for i in range(NUM_BLOCKS) for j in range(NUM_BLOCKS)]
tiles = []
tiles.append(Tile(GREEN, 2, 0))


## Game loop
running = True
while running:

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    
    events = pygame.event.get()
    for event in events:        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

    for tile in tiles: tile.update(events)

    screen.fill(BLACK)

    frame.draw(screen)

    if DEBUG: 
        for tile in debugTiles: tile.draw(screen)

    for tile in tiles: tile.draw(screen)


    pygame.display.flip()       

pygame.quit()