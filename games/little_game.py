import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.vel = 5

        # Colors
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Background
        self.BG = pygame.image.load('images/background/combined_background.png').convert()
        self.BG = pygame.transform.scale(self.BG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
       
        # Font
        self.font = pygame.font.Font('fonts/Daydream.ttf', 24)

        # Rectangles
        self.obstacle = pygame.Rect(300, 100, 50, 50)

        # Images
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

        # Bullet settings
        self.bullet_height = 25
        self.bullet_width = 25

        self.last_shot_time = 0
        self.last_reload_time = 0
        self.reload_time = 3500
                
        self.hit_duration = 1000
        
        self.max_bullets = 3
        self.current_bullets = self.max_bullets

        self.frames = []
        for i in range(1, 7):
            frame = pygame.image.load(f'images/bullet_gif/bullet_{i}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (self.bullet_width, self.bullet_height))
            self.frames.append(frame)

        self.bullets = []
        self.ready_reload = False

    class Bullet:
        def __init__(self, x, y, width, height, frames, screen):
            self.rect = pygame.Rect(x, y, width, height)
            self.speed = 7
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_delay = 60  # milliseconds
            self.frames = frames
            self.screen = screen

        def move(self):
            self.rect.x += self.speed

        def update_animation(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_delay:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)

        def draw(self):
            self.screen.blit(self.frames[self.current_frame], self.rect.topleft)
            self.update_animation()

    def moving_keys(self, key):
        # if key[pygame.K_d] and self.player_rect.right < self.SCREEN_WIDTH:
        #     self.player_rect.move_ip(self.vel, 0)
        # if key[pygame.K_a] and self.player_rect.left > 0:
        #     self.player_rect.move_ip(-self.vel, 0)
        # if key[pygame.K_w] and self.player_rect.bottom > 310:
        #     self.player_rect.move_ip(0, -self.vel)
        # if key[pygame.K_s] and self.player_rect.bottom < self.SCREEN_HEIGHT:
        #     self.player_rect.move_ip(0, self.vel)

        if key[pygame.K_w] and self.player_rect.bottom > 310:
            self.player_rect.move_ip(self.vel, -self.vel)
        if key[pygame.K_s] and self.player_rect.bottom < self.SCREEN_HEIGHT:
            self.player_rect.move_ip(-self.vel, self.vel)
    def shooting(self):
        current_time = pygame.time.get_ticks()
        if (
            self.current_bullets > 0
            and (current_time - self.last_shot_time > 350 or self.last_shot_time == 0)
        ):
            bullet_x = self.player_rect.x + self.player_rect.width
            bullet_y = self.player_rect.y + self.player_rect.height / 2 - 11.5

            if len(self.bullets) < self.max_bullets:
                bullet = self.Bullet(
                    bullet_x,
                    bullet_y,
                    self.bullet_width,
                    self.bullet_height,
                    self.frames,
                    self.screen,
                )
                self.bullets.append(bullet)
                self.current_bullets -= 1

            self.last_shot_time = current_time

    def reloading(self):
        current_time = pygame.time.get_ticks()
        if self.ready_reload or self.last_reload_time == 0:
            self.current_bullets = self.max_bullets
            self.last_reload_time = current_time
            self.ready_reload = False

    def run_game(self):
        run = True
        while run:
            self.clock.tick(60)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.screen.blit(self.BG, (0, 0))

            key = pygame.key.get_pressed()
            self.moving_keys(key)

            if key[pygame.K_SPACE]:
                self.shooting()

            self.ready_reload = (
                (current_time - self.last_shot_time) > self.reload_time
                and self.current_bullets < self.max_bullets
            )

            if key[pygame.K_r]:
                self.reloading()

            # Drawing bullets
            for bullet in self.bullets:
                bullet.move()
                bullet.draw()

            # Draw obstacle
            obstacle_color = (
                self.GREEN
                if any(b.rect.colliderect(self.obstacle) for b in self.bullets)
                else self.RED
            )
            pygame.draw.rect(self.screen, obstacle_color, self.obstacle)

            # Remove collided bullets and those off screen
            self.bullets[:] = [
                b
                for b in self.bullets
                if not b.rect.colliderect(self.obstacle)
                and b.rect.x < self.SCREEN_WIDTH
            ]

            # Draw player rect
            self.screen.blit(self.soldier, self.player_rect)

            # Draw text
            font_render = self.font.render(
                f"{self.current_bullets} / {self.max_bullets}", True, "black"
            )
            self.screen.blit(font_render, (470, 350))

            # Draw reload image
            if self.ready_reload:
                self.screen.blit(self.refresh, self.refresh_rect)
                self.screen.blit(self.r_key, self.r_rect)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()


