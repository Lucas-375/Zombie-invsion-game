import pygame
from random import randint
from ultilities.life_system import HPSystem

ZOMBIE_WIDTH = 60
ZOMBIE_HEIGHT = 75

class Zombie(HPSystem):
    """A class representing a single zombie."""

    def __init__(self, x, y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT, frames, vel, screen):
        self.rect = pygame.Rect(x, y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT)
        self.frames = frames
        self.current_frame = 0
        self.last_frame_update = pygame.time.get_ticks()
        self.frame_rate = 100  # ms per frame
        self.vel = vel
        self.screen = screen
        super().__init__(max_hp=100, screen=screen, entity_rect=self.rect)

    def move(self):
        """Move a zombie to the left"""
        if self.rect.x > 0:
            self.rect.x -= self.vel 
        else:
            self.rect.x = randint(500, 550)
            self.rect.y = randint(230, self.screen.get_height() - ZOMBIE_HEIGHT) # Draw the HP bar above the zombie
        
    def update_animation(self):
        """Update the zombie's frame gif animation."""
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_update = now

    def draw(self):
        """Draw the zombie"""
        self.update_animation()
        self.screen.blit(self.frames[self.current_frame], self.rect.topleft)    
        super().draw_hp_bar()  # Draw the HP bar above the zombie

    def collides_with(self, other_rect):
        """Check if the zombie collided with another rect."""
        return self.rect.colliderect(other_rect)
