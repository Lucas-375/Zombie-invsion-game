import pygame
pygame.init()

    
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting colours

BG = (50, 50, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# font

font = pygame.font.Font('fonts/Daydream.ttf', 24)

# Rectangles

rect_1 = pygame.Rect(200, 100, 50, 50)
obstacle = pygame.Rect(300, 100, 50, 50)

# images

# # white rectangle for reloading bullets

refresh_rect = pygame.Rect(400, 345, 50, 50)
refresh = pygame.image.load('images/refresh_black.png').convert_alpha()
refresh = pygame.transform.scale(refresh, (50, 50))

# # 'r' key

r_rect = pygame.Rect(400, 345, 30, 30)
r_rect.center = refresh_rect.center
r_key = pygame.image.load('images/keys/r_black.png').convert_alpha()
r_key = pygame.transform.scale(r_key, (30, 30))
 
# bullet settings

bullet_height = 25
bullet_width = 25

last_shot_time = 0

reload_time = 3500
last_reload_time = 0

hit_duration = 1000

max_bullets = 3
current_bullets = max_bullets

bullet_gif = pygame.image.load('images/bullet.gif').convert_alpha()
bullet_gif = pygame.transform.scale(bullet_gif, (bullet_width, bullet_height))

frames = []
for i in range(1, 7):
    frame = pygame.image.load(f'images/bullet_gif/bullet_{i}.png').convert_alpha()
    frame = pygame.transform.scale(frame, (bullet_width, bullet_height))
    frames.append(frame)

# Bullet class  

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, bullet_width, bullet_height)
        self.speed = 7
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 60  # millisecods

    def move(self):
        self.rect.x += self.speed

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(frames)

    def draw(self):
        screen.blit(frames[self.current_frame], self.rect.topleft)
        self.update_animation()

bullets = []

# Keys

# # Moving

def moving_keys(key):
    if key[pygame.K_d] and rect_1.right < SCREEN_WIDTH:
        rect_1.move_ip(vel, 0)
    if key[pygame.K_a] and rect_1.left > 0:
        rect_1.move_ip(-vel, 0)
    if key[pygame.K_w] and rect_1.top > 0:
        rect_1.move_ip(0, -vel)
    if key[pygame.K_s] and rect_1.bottom < SCREEN_HEIGHT:
        rect_1.move_ip(0, vel)

# # Space / shooting

def shooting():
    global last_shot_time, current_bullets

    current_time = pygame.time.get_ticks()

    if current_bullets > 0 and (current_time - last_shot_time > 350 or last_shot_time == 0):
        bullet_x = rect_1.x + rect_1.width
        bullet_y = rect_1.y + rect_1.height / 2 - 5
        
        if len(bullets) <= max_bullets:
            bullets.append(Bullet(bullet_x, bullet_y))
            current_bullets -= 1

        last_shot_time = current_time

# # r / reloading

def reloading():
    global ready_reload, current_bullets, last_reload_time

    current_time = pygame.time.get_ticks()

    if ready_reload or last_reload_time == 0:
        current_bullets = max_bullets
        last_reload_time = current_time
        ready_reload = False


# Running

clock = pygame.time.Clock()
vel = 5

run = True
while run:

    clock.tick(60) 

    current_time = pygame.time.get_ticks() # Get the current time in milliseconds

    screen.fill(BG)

    # Event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Keys

    key = pygame.key.get_pressed()

    # # Moving

    moving_keys(key)
    
    # # Shooting 
      
    if key[pygame.K_SPACE]:
        shooting()

    # # Reloading bullets

    ready_reload = (current_time - last_shot_time) > reload_time and current_bullets < max_bullets

    if key[pygame.K_r]:
        reloading()

    # Drawing bullets
    for bullet in bullets:
        bullet.move()
        bullet.draw()

    # # draw obstacle
    pygame.draw.rect(screen, GREEN if any(b.rect.colliderect(obstacle) for b in bullets) else RED, obstacle)

    # # Remove collided bullets from the list
    bullets[:] = [b for b in bullets if not b.rect.colliderect(obstacle) and b.rect.x < SCREEN_WIDTH]
    
    # Draw rect

    pygame.draw.rect(screen, BLUE, rect_1)
    
    # Draw text
    
    font_render = font.render(f'{current_bullets} / {max_bullets}', True, 'black')
    screen.blit(font_render, (470, 350))

    # draw image
    if ready_reload:
        screen.blit(refresh, refresh_rect)
        screen.blit(r_key, r_rect)

    # Update display

    pygame.display.flip()

quit()
