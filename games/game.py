import pygame
from ultilities.zombies_class import Zombie
from ultilities.bullet_class import Bullet
from random import randint

class Game:
    """Main game class for Zombies Shooting."""

    def __init__(self):
        """Initialize the game, screen, assets, and variables."""
        pygame.init()
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.vel = 5
        pygame.display.set_caption('Zombies Shooting')

        # Colors
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Background
        self.BG = pygame.image.load('images/background/combined_background.png').convert()
        self.BG = pygame.transform.scale(self.BG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
       
        # Font
        self.FONT = {
            'daydream': pygame.font.Font('fonts/Daydream.ttf', 20),
            'pixelcraft': pygame.font.Font('fonts/Pixelcraft.ttf', 30),
        }

        # Images / Rectangles
        self.player_rect = pygame.Rect(155, 260, 50, 50)
        self.soldier = pygame.image.load('images/soldier.png').convert_alpha()
        self.soldier = pygame.transform.scale(self.soldier, (50, 50))

        self.refresh_rect = pygame.Rect(400, 345, 50, 50)
        self.refresh = pygame.image.load('images/refresh_black.png').convert_alpha()
        self.refresh = pygame.transform.scale(self.refresh, (50, 50))

        self.r_rect = pygame.Rect(400, 345, 30, 30)
        self.r_rect.center = self.refresh_rect.center
        self.r_key = pygame.image.load('images/keys/r_black.png').convert_alpha()
        self.r_key = pygame.transform.scale(self.r_key, (30, 30))

        # Zombie settings
        self.ZOMBIE_WIDTH = 60
        self.ZOMBIE_HEIGHT = 75

        self.zombie_score = 0
        self.last_zombie_added_time = 0  
        self.zombie_spawn_delay = 5000
        self.zombies_to_add = 0

        self.zombie_frames = []
        for i in range(1, 17):
            frame = pygame.image.load(f'images/zombie1_gif/zombie1_{i}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.ZOMBIE_WIDTH, self.ZOMBIE_HEIGHT))
            self.zombie_frames.append(frame)

        self.zombie_vel = 0.7
        self.zombies = pygame.sprite.Group()
        for _ in range(3):
            self.add_zombie()

        # Bullet settings
        self.BULLET_HEIGHT = 20
        self.BULLET_WIDTH = 20

        self.last_shot_time = 0
        self.last_reload_time = 0
        self.reload_time = 3500
        self.hit_duration = 1000
        self.max_bullets = 3
        self.current_bullets = self.max_bullets

        self.frames = []
        for i in range(1, 7):
            frame = pygame.image.load(f'images/bullet_gif/bullet_{i}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.BULLET_WIDTH, self.BULLET_HEIGHT))
            self.frames.append(frame)

        self.bullets = pygame.sprite.Group()
        self.ready_reload = False

    # Zombie functions
    def add_zombie(self):
        """Add a new zombie at a random position on the right side."""
        x = randint(450, 550)
        y = randint(230, self.SCREEN_HEIGHT - self.ZOMBIE_HEIGHT)
        new_zombie = Zombie(x, y, self.ZOMBIE_WIDTH, self.ZOMBIE_HEIGHT, self.zombie_frames, self.zombie_vel, self.screen)
        self.zombies.add(new_zombie)

    def add_zombie_with_delay(self):
        """Add zombies with a delay after one is killed."""
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.last_zombie_added_time > self.zombie_spawn_delay 
            and self.zombies_to_add > 0
        ):
            self.last_zombie_added_time = current_time
            self.zombies_to_add -= 1
            self.add_zombie()

    # Shooting functions
    def shooting(self):
        """Handle shooting bullets if allowed."""
        current_time = pygame.time.get_ticks()
        if (
            self.current_bullets > 0
            and (current_time - self.last_shot_time > 350 or self.last_shot_time == 0)
        ):
            bullet_x = self.player_rect.x + self.player_rect.width
            bullet_y = self.player_rect.y + self.player_rect.height / 2 - 11.5

            if len(self.bullets) < self.max_bullets:
                bullet = Bullet(
                    bullet_x,
                    bullet_y,
                    self.BULLET_WIDTH,
                    self.BULLET_HEIGHT,
                    self.frames,
                    self.screen,
                )
                self.bullets.add(bullet)
                self.current_bullets -= 1

            self.last_shot_time = current_time

    def reloading(self):
        """Reload bullets if allowed."""
        current_time = pygame.time.get_ticks()
        if self.ready_reload or self.last_reload_time == 0:
            self.current_bullets = self.max_bullets
            self.last_reload_time = current_time
            self.ready_reload = False 

    def change_max_bullets(self):
        """Change the max bullets based on zombie score."""
        increasing_max_bullet_settings = {
            0: self.max_bullets,
            5: 4, 
            10: 5,
            20: 7,
            50: 10
        }
        self.max_bullets = increasing_max_bullet_settings[
            self.zombie_score 
            if self.zombie_score in increasing_max_bullet_settings 
            else 0]

    def remove_collided_zombies_bullets(self):
        """Remove zombies and bullets that have collided."""
        zombie_to_remove = []

        hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        for bullet, zombies_hit in hits.items():
            for zombie in zombies_hit:
                zombie.take_damage(50)
        
        for zombie in self.zombies:
            if zombie.hp <= 0:
                zombie_to_remove.append(zombie)
                self.zombie_score += 1
                self.zombies_to_add += 1

        for zombie in zombie_to_remove:
            self.zombies.remove(zombie)
        for bullet in self.bullets:
            if bullet.rect.x > self.SCREEN_WIDTH:
                self.bullets.remove(bullet)

    # Player functions
    def moving_keys(self, key):
        """Handle player movement keys."""
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.player_rect.bottom > 310:
            self.player_rect.move_ip(self.vel, -self.vel)
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.player_rect.bottom < self.SCREEN_HEIGHT:
            self.player_rect.move_ip(-self.vel, self.vel)

    def key_inputs(self):
        """Handle all key inputs."""
        key = pygame.key.get_pressed()
        self.moving_keys(key)

        if key[pygame.K_SPACE]:
            self.shooting()

        if key[pygame.K_r]:
            self.reloading()
        
    def draw_text(self):
        """Draw bullet count, score, and reload image."""
        current_time = pygame.time.get_ticks()
        bullet_count_render = self.FONT['daydream'].render(
            f"{self.current_bullets} / {self.max_bullets}", True, "black"
        )
        self.screen.blit(bullet_count_render, (470, 360))

        score_render = self.FONT['pixelcraft'].render(
            f"Score {self.zombie_score}", True, 'goldenrod'
        )
        self.screen.blit(score_render, (10, 10))

        self.ready_reload = (
            (current_time - self.last_shot_time) > self.reload_time
            and self.current_bullets < self.max_bullets
        )
        if self.ready_reload:
            self.screen.blit(self.refresh, self.refresh_rect)
            self.screen.blit(self.r_key, self.r_rect)

    def run_game(self):
        """Main game loop."""
        run = True
        while run:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.screen.blit(self.BG, (0, 0))
            self.key_inputs()
            self.remove_collided_zombies_bullets()
            self.add_zombie_with_delay()

            self.bullets.update()
            for bullet in self.bullets:
                bullet.draw()
            self.change_max_bullets()

            self.zombies.update()
            for zombie in self.zombies:
                zombie.draw()

            self.screen.blit(self.soldier, self.player_rect)
            self.draw_text()            
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()