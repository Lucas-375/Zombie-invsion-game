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
        if self.rect.x > 0:
            self.rect.x -= self.vel 
        else:
            self.rect.x = randint(500, 550)
            self.rect.y = randint(230, self.screen.get_height() - ZOMBIE_HEIGHT) # Draw the HP bar above the zombie
        
    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_frame_update = now

    def draw(self):
        self.update_animation()
        self.screen.blit(self.frames[self.current_frame], self.rect.topleft)    
        super().draw_hp_bar()  # Draw the HP bar above the zombie

    def collides_with(self, other_rect):
        return self.rect.colliderect(other_rect)

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

        # Zombie gif frames
        self.frames = []
        for i in range(1, 17):
            frame = pygame.image.load(f'images/zombie1_gif/zombie1_{i}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
            self.frames.append(frame)

        # Zombies list
        self.zombies = []
        for _ in range(randint(5, 8)):
            self.add_zombie()

        # Player
        self.player_rect = pygame.Rect(300, 150, 50, 50)

    def add_zombie(self):
        x = randint(450, 550)
        y = randint(230, self.SCREEN_HEIGHT - ZOMBIE_HEIGHT)
        zombie = Zombie(x, y, self.frames, self.vel)
        self.zombies.append(zombie)

    def remove_collided_zombie(self, rect):
        for zombie in self.zombies:
            if zombie.collides_with(rect):
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

            # Move and draw zombies
            for zombie in self.zombies:
                zombie.move()
                zombie.draw(self.screen)

            # Draw the player rectangle
            pygame.draw.rect(self.screen, (255, 0, 0), self.player_rect)

            # Remove collided zombies and add new ones
            if self.remove_collided_zombie(self.player_rect):
                self.add_zombie()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()