import pygame, sys
from pygame.locals import *
import os
pygame.init() 

class GameObject():
	def __init__(self, screen, x:int | None, y:int | None, width:int, height:int, colour=None, middle_x=False, middle_y=False):
		self.screen = screen
		self.x = x if not middle_x else (main_x // 2) - (width // 2)
		self.y = y if not middle_y else (main_y // 2) - (height // 2)
		self.width = width
		self.height = height
		self.colour = colour if colour else (0, 0, 0)
	
	def draw(self):
		pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))

		
def check_collision(new_x, new_y):
	collision = (
		new_x + red.width > black.x and
		new_x < black.x + width_yellow and
		new_y < black.y + height_yellow and
		new_y + red.width > black.y
	)
	
	if collision:
		print(f'collsion at [x={new_x}] and [y={new_y}]') 
	
	return collision

main_x, main_y = 600, 400
screen = pygame.display.set_mode((main_x, main_y)) 
pygame.display.set_caption("Moving rectangle") 

red = GameObject(screen,  180, None, 70, 70, (255, 0, 0), middle_y=True)
black = GameObject(screen, 400, None, 40, 40, (0, 0, 0), middle_y=True)
vel = 12
vel_original = vel
run = True

while run:
	pygame.time.delay(15)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	keys = pygame.key.get_pressed()
	
	if (keys[pygame.K_LEFT] or keys[pygame.K_a]): 
		if red.x > 0:

			if not check_collision(red.x - vel, red.y):
				red.x -= vel

	if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
		if red.x < (main_x - red.width):
			
			if not check_collision(red.x + vel, red.y):
				red.x += vel

	if (keys[pygame.K_UP] or keys[pygame.K_w]): 
		if red.y > 0:
			
			if not check_collision(red.x, red.y - vel):
				red.y -= vel

	if (keys[pygame.K_DOWN] or keys[pygame.K_s]): 
		if red.y < (main_y - red.height):
			
			if not check_collision(red.x, red.y + vel):
				red.y += vel 


	width_yellow, height_yellow = 40, 40

	screen.fill((255, 255, 255))
	black.draw()
	red.draw()
	 
	pygame.display.update()

pygame.quit()