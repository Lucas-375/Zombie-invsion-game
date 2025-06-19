import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, frames, screen):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 40  # milliseconds
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 6
        self.screen = screen

    def update(self):
        """Move and animate the bullet."""
        self.rect.x += self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self):
        """Draw the bullet (optional, for custom effects)."""
        self.screen.blit(self.image, self.rect.topleft)