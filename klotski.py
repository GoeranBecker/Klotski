

import pygame
import random


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
GAME_SIZE = int(WINDOW_HEIGHT * 0.85)
BLOCK_MARGIN = int(GAME_SIZE * 0.02)
NUM_BLOCKS = 6
CORNER_RADIUS = 2
FPS = 30

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


## group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()

## Game loop
running = True
while running:

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False


    #2 Update
    all_sprites.update()


    #3 Draw/render
    screen.fill(BLACK)


    all_sprites.draw(screen)

    pygame.draw.rect(screen, WHITE, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2,
                                                (WINDOW_HEIGHT - GAME_SIZE) // 2,
                                                GAME_SIZE,
                                                GAME_SIZE), 0, CORNER_RADIUS)
    pygame.draw.rect(screen, BLACK, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                                (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN,
                                                GAME_SIZE - 2 * BLOCK_MARGIN,
                                                GAME_SIZE - 2 * BLOCK_MARGIN), 0, CORNER_RADIUS)
    pygame.draw.rect(screen, BLACK, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + GAME_SIZE - BLOCK_MARGIN,
                                              (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN + 2 * (GAME_SIZE // NUM_BLOCKS),
                                              BLOCK_MARGIN,
                                              GAME_SIZE // NUM_BLOCKS))
    
    # pygame.draw.rect(screen, GREEN, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN,
        #                                         (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN,
        #                                         GAME_SIZE - 3 * BLOCK_MARGIN,
        #                                         GAME_SIZE - 3 * BLOCK_MARGIN), 1, CORNER_RADIUS)
    
    # pygame.draw.rect(screen, GREEN, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + 2 * BLOCK_MARGIN,
        #                                         (WINDOW_HEIGHT - GAME_SIZE) // 2 + 2 * BLOCK_MARGIN,
        #                                         (GAME_SIZE - 4 * BLOCK_MARGIN) // NUM_BLOCKS,
        #                                         GAME_SIZE - 4 * BLOCK_MARGIN), 1, CORNER_RADIUS)
    
    # for i in range(NUM_BLOCKS):
    #     pygame.draw.rect(screen, GREEN, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + 2 * BLOCK_MARGIN + i * ((GAME_SIZE - 4 * BLOCK_MARGIN) // NUM_BLOCKS),
            #                                         (WINDOW_HEIGHT - GAME_SIZE) // 2 + 2 * BLOCK_MARGIN,
            #                                         (GAME_SIZE - 4 * BLOCK_MARGIN) // NUM_BLOCKS,
            #                                         GAME_SIZE - 4 * BLOCK_MARGIN), 1, CORNER_RADIUS)

    # for i in range(NUM_BLOCKS):
    #     pygame.draw.rect(screen, GREEN, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN + i * (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS + BLOCK_MARGIN,
    #                                                 (WINDOW_HEIGHT - GAME_SIZE) // 2 + 2 * BLOCK_MARGIN,
    #                                                 (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN,
    #                                                 GAME_SIZE - 4 * BLOCK_MARGIN), 1, CORNER_RADIUS)
    
    for i in range(NUM_BLOCKS):
        for j in range(NUM_BLOCKS):
            pygame.draw.rect(screen, GREEN, pygame.Rect((WINDOW_WIDTH - GAME_SIZE) // 2 + BLOCK_MARGIN + i * (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS + BLOCK_MARGIN,
                                                        (WINDOW_HEIGHT - GAME_SIZE) // 2 + BLOCK_MARGIN + j * (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS + BLOCK_MARGIN,
                                                        (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN,
                                                        (GAME_SIZE - 3 * BLOCK_MARGIN) // NUM_BLOCKS - BLOCK_MARGIN), 1, CORNER_RADIUS)
    
    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()