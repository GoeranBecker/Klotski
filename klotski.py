

import pygame
import random


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
NUM_BLOCKS = 6
CORNER_RADIUS = 2
GAME_SIZE = int(min(WINDOW_HEIGHT, WINDOW_WIDTH) * 0.85)
BLOCK_MARGIN = int(GAME_SIZE * 0.02)
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
        self.frame = pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2,
                                 (WINDOW_HEIGHT - GAME_SIZE) // 2,
                                 GAME_SIZE,
                                 GAME_SIZE)
        
        self.frame_inner = pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                       (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                       GAME_SIZE - 2 * BLOCK_MARGIN,
                                       GAME_SIZE - 2 * BLOCK_MARGIN)
        
        self.frame_cutout = pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + GAME_SIZE - BLOCK_MARGIN,
                                        (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN + 2 * (GAME_SIZE // NUM_BLOCKS),
                                        BLOCK_MARGIN,
                                        GAME_SIZE // NUM_BLOCKS)


    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.frame, 0, CORNER_RADIUS)
        pygame.draw.rect(surface, BLACK, self.frame_inner, 0, CORNER_RADIUS)
        pygame.draw.rect(surface, BLACK, self.frame_cutout)
        

class Tile:
    def __init__(self, frame, color, row, col, rowspan=1, colspan=1):
        self.frame = frame
        self.color = color
        self.row = row
        self.col = col
        self.rowspan = rowspan
        self.colspan = colspan
        self.dragged = False
        self.dragged_start_x = 0
        self.dragged_start_y = 0
        self.dragged_offset_x = 0
        self.dragged_offset_y = 0
        self.dragged_x = None
        self.rect = pygame.Rect(calcTileX(self.col),
                                calcTileY(self.row),
                                ((GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN) * self.rowspan + (self.rowspan - 1) * BLOCK_MARGIN,
                                ((GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN) * self.colspan + (self.colspan - 1) * BLOCK_MARGIN)
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 1, CORNER_RADIUS)


    def update(self, events, other_rects: pygame.Rect):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.posInside(event.pos[0], event.pos[1]):
                    self.dragged = True
                    self.dragged_start_x = event.pos[0]
                    self.dragged_start_y = event.pos[1]
                    self.dragged_offset_x = event.pos[0] - self.rect.x
                    self.dragged_offset_y = event.pos[1] - self.rect.y

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                indices = calcIndices(self.frame, self.rect.centerx, self.rect.centery)
                if self.dragged_x:
                    if indices is None:
                        indices = self.row, 0 if event.pos[0] < self.dragged_start_x else 5
                    self.col = indices[1]
                else:
                    if indices is None:
                        indices = 0 if event.pos[1] < self.dragged_start_y else 5, self.col
                    self.row = indices[0]
                self.dragged = False
                self.dragged_x = None

        if self.dragged:
            mouse_pos = pygame.mouse.get_pos()
            dist_x = abs(self.dragged_start_x - mouse_pos[0])
            dist_y = abs(self.dragged_start_y - mouse_pos[1])
            if self.dragged_x is None and (dist_x > 10 or dist_y > 10):
                self.dragged_x = dist_x > dist_y
            elif self.dragged_x is not None:
                if self.dragged_x: 
                    self.rect.x = mouse_pos[0] - abs(self.dragged_offset_x)
                    for rect in other_rects:
                        rect: pygame.Rect
                        if self.rect.top == rect.top:
                            if rect.x > self.dragged_start_x:
                                if self.rect.right > rect.left:
                                    self.rect.x = rect.left - self.rect.width
                            elif rect.x < self.dragged_start_x:
                                if self.rect.left < rect.right:
                                    self.rect.x = rect.right

                    # dragged_offset_x = 0
                else:
                    self.rect.y = mouse_pos[1] - abs(self.dragged_offset_y)
                    for rect in other_rects:
                        rect: pygame.Rect
                        if self.rect.left == rect.left:
                            if rect.y > self.dragged_start_y:
                                if self.rect.bottom > rect.top:
                                    self.rect.y = rect.top - self.rect.width
                            elif rect.y < self.dragged_start_y:
                                if self.rect.top < rect.bottom:
                                    self.rect.y = rect.bottom
        
        else:
            self.rect.x = calcTileX(self.col)
            self.rect.y = calcTileY(self.row)

        # print(self.dragged_x)


    def posInside(self, x, y):
        return (self.rect.left < x < self.rect.right 
                and self.rect.top < y < self.rect.bottom)
         

def calcIndices(frame: Frame, x, y):
    if (not frame.frame_inner.left < x < frame.frame_inner.right
        or not frame.frame_inner.top < y < frame.frame_inner.bottom):
            return None
    
    x -= (WINDOW_WIDTH - frame.frame_inner.width) // 2
    y -= (WINDOW_HEIGHT - frame.frame_inner.height) // 2
    row = 0
    col = 0
    tile_width = (frame.frame_inner.width - BLOCK_MARGIN) // NUM_BLOCKS
    tile_height = (frame.frame_inner.height - BLOCK_MARGIN) // NUM_BLOCKS

    if x > BLOCK_MARGIN // 2:
        x -= BLOCK_MARGIN // 2
    while x > tile_width + BLOCK_MARGIN // 2:
        if x - tile_width > 0:
            x -= tile_width
            col += 1
            
    if y > BLOCK_MARGIN // 2:
        y -= BLOCK_MARGIN // 2
    while y > tile_height + BLOCK_MARGIN // 2:
        if y - tile_height > 0:
            y -= tile_height
            row += 1

    return (row, col)



frame = Frame()
debugTiles = [Tile(frame, RED, i, j) for i in range(NUM_BLOCKS) for j in range(NUM_BLOCKS)]
tiles = [Tile(frame, GREEN, 0, 2),
         Tile(frame, BLUE, 5, 2),
         Tile(frame, BLUE, 3, 4),
         Tile(frame, BLUE, 3, 2),
         Tile(frame, BLUE, 2, 4),
         Tile(frame, BLUE, 3, 5),
         Tile(frame, BLUE, 5, 4),
         Tile(frame, BLUE, 0, 4),
         Tile(frame, BLUE, 3, 0),]


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

    rects = [tile.rect for tile in tiles]
    for tile in tiles: 
        rects.remove(tile.rect)
        tile.update(events, rects)
        rects.append(tile.rect)

    screen.fill(BLACK)

    frame.draw(screen)

    if DEBUG: 
        for tile in debugTiles: tile.draw(screen)
        # for i in range(1, NUM_BLOCKS):
        #     pygame.draw.line(screen, RED, 
        #                      (frame.frame_inner.left + BLOCK_MARGIN + i * (frame.frame_inner.width - BLOCK_MARGIN // 2) // NUM_BLOCKS, frame.frame_inner.top),
        #                      (frame.frame_inner.left + BLOCK_MARGIN + i * (frame.frame_inner.width - BLOCK_MARGIN // 2) // NUM_BLOCKS, frame.frame_inner.bottom))

    for tile in tiles: tile.draw(screen)


    pygame.display.flip()       

pygame.quit()