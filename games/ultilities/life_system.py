import pygame

class HPSystem:
    """A class to manage the health points (HP) system for a game entity."""
    def __init__(self, max_hp: int, screen, entity_rect, pos: tuple=None, size: tuple=None):
        self.hp = max_hp
        self.max_hp = max_hp
        self.screen = screen
        self.entity_rect = entity_rect
        self.pos = pos
        self.size = size

    def draw_hp_bar(self):
        """Draws the health points bar above the entity."""
        bar_width = self.entity_rect.width if self.size is None else self.size[0]
        bar_height = 6 if self.size is None else self.size[1]
        hp_ratio = max(self.hp, 0) / self.max_hp 
        hp_bar_width = int(bar_width * hp_ratio)
        hp_bar_x = self.entity_rect.x + (self.entity_rect.width - bar_width) // 2 if self.pos is None else self.pos[0]  
        hp_bar_y = self.entity_rect.y - bar_height - 4 if self.pos is None else self.pos[1]
        
        # Draw the background of the HP bar
        pygame.draw.rect(self.screen, (50, 50, 50), (hp_bar_x, hp_bar_y, bar_width, bar_height))

        # Draw the HP bar
        if hp_bar_width > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), (hp_bar_x, hp_bar_y, hp_bar_width, bar_height))

    def take_damage(self, damage):
        """Reduces the HP by the specified damage amount."""
        self.hp -= damage
        if not self.is_alive():
            self.hp = 0

    def kill(self):
        self.hp = 0

    def is_alive(self):
        """Checks if the entity is still alive."""
        return self.hp > 0