import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Working With Rectangles')

soldier = pygame.image.load('soldier.png').convert_alpha()
# Ensure the image is scaled to the desired size    
soldier = pygame.transform.scale(soldier, (112, 144))

rect_1 = pygame.Rect(200, 100, 150, 100)
rect_2 = soldier.get_rect()
rect_2.center = (200, 200)

clock = pygame.time.Clock()

run = True
while run:

    clock.tick(60)

    screen.fill((255, 255, 255))

    screen.blit(soldier, rect_2)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        if rect_2.x >= 0:
            rect_2.move_ip(-5, 0)
    if key[pygame.K_d]:
        if rect_2.x <= SCREEN_WIDTH - rect_2.width:
            rect_2.move_ip(5, 0)
    if key[pygame.K_w]:
        if rect_2.y >= 0:
            rect_2.move_ip(0, -5)
    if key[pygame.K_s]:
        if rect_2.y <= SCREEN_HEIGHT - rect_2.height:
            rect_2.move_ip(0, 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()

pygame.quit()
