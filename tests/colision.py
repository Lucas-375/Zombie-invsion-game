import pygame
from random import randint

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Collision Detection Example')

obstacles = []
for _ in range(16):
    obstacle_rect = pygame.Rect(randint(0, 500), randint(0, 300), 25, 25)
    obstacles.append(obstacle_rect)

line_start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# define colors
BG = (50, 50, 50)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

run = True
while run:
    
    # set background colour
    screen.fill(BG)

    pos = pygame.mouse.get_pos()
   
    # draw the line from the center to the mouse position
    pygame.draw.line(screen, WHITE, line_start, pos, 5)

    # draw the rectangles
    for obstacle in obstacles:
        if obstacle.clipline((line_start, pos)):
            pygame.draw.rect(screen, RED, obstacle)
        else:
            pygame.draw.rect(screen, GREEN, obstacle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.flip()

pygame.quit()