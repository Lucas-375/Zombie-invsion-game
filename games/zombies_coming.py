import pygame
from random import randint

ZOMBIE_WIDTH = 75
ZOMBIE_HEIGHT = 80

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.vel = 2.3
        pygame.display.set_caption('Zombies Coming')

        # Colors
        self.BG = (50, 50, 50)
        self.GREEN = (0, 255, 0)

        # Zombies list
        self.zombies = []
        for _ in range(randint(5, 8)):
            self.add_zombie()

        # Rectangles
        self.player_rect = pygame.Rect(300, 150, 50, 50)

        # Zombie gif
        self.frames = []
        for i in range(1, 17):
            frame = pygame.image.load(f'images/zombie1_gif/zombie1_{i}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
            self.frames.append(frame)
        self.current_frame = 0
        self.frame_rate = 100
        self.last_frame_update = pygame.time.get_ticks()

    def update_zombie_frame(self):
        """Update the current frame for the zombie animation."""
        self.now = pygame.time.get_ticks()
        if self.now - self.last_frame_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_update = self.now

    def draw_zombies(self):
        """Draw all zombies on the screen."""
        for zombie in self.zombies:
            self.update_zombie_frame()
            self.screen.blit(self.frames[self.current_frame], (zombie.x, zombie.y))
    
    def add_zombie(self):
        """Add a new zombie at a random position on the right side."""
        x = randint(450, 550)
        y = randint(0, self.SCREEN_HEIGHT - ZOMBIE_HEIGHT)
        new_zombie = pygame.Rect(x, y, ZOMBIE_WIDTH, ZOMBIE_HEIGHT)
        self.zombies.append(new_zombie)

    def remove_collided_zombie(self, rect):
        for zombie in self.zombies:
            if zombie.colliderect(rect):
                self.zombies.remove(zombie)
                return True
        return False

    def run_game(self):
        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill(self.BG)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  

            # Draw the zombies
            for zombie in self.zombies:
                if zombie.x > 0:
                    zombie.x -= self.vel
                else:
                    zombie.x = randint(500, 550)
                    zombie.y = randint(0, 340)

            self.draw_zombies()
            
            # Draw the player rectangle
            pygame.draw.rect(self.screen, (255, 0, 0), self.player_rect)

            # Remove collided zombies
            if self.remove_collided_zombie(self.player_rect):
                self.add_zombie()

            # Check for new zombies

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()