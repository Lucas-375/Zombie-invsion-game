import pygame

class Bullet:
        def __init__(self, x, y, width, height, frames, screen):
            self.rect = pygame.Rect(x, y, width, height)
            self.speed = 6
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_delay = 40  # milliseconds
            self.frames = frames
            self.screen = screen

        def move(self):
            """Move the bullet."""
            self.rect.x += self.speed

        def update_animation(self):
            """Update the bullet's frame gif animation."""
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_delay:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)

        def draw(self):
            """Draw the bullet."""
            self.screen.blit(self.frames[self.current_frame], self.rect.topleft)
            self.update_animation()