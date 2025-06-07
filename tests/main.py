import pygame, sys
from pygame.locals import *

pygame.init()
x = 600
y = 400
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Propane')
colours = {
    'black': (0, 0, 0, 255),
    'blue': (0, 0, 255, 255),
    'cyan': (0, 255, 255, 255),
    'gold': (255, 215, 0, 255),
    'gray': (190, 190, 190, 255),
    'green': (0, 255, 0, 255),
    'orange': (255, 165, 0, 255),
    'purple': (160, 32, 240, 255),
    'red': (255, 0, 0, 255),
    'violet': (238, 130, 238, 255),
    'yellow': (255, 255, 0, 255),
    'white': (255, 255, 255, 255),
}

while True:
    
    screen.fill(colours['cyan'])
    pygame.draw.rect(screen, colours['gold'], pygame.Rect(100, 100, 50, 100))
    
    pygame.display.flip()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            print(f'{key} was pressed')
        if event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            print(f'{key} was released')

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse
            print(f'x = {pos[0]} | y = {pos[1]}')
            if pos[1] == 0 and pos[0] == 0:
                print('You clicked exactly in the right-top corner')
            if pos[0] == (x - 1) and pos[1] == 1:
                print('You clicked exactly in the left-top corner')
            
        