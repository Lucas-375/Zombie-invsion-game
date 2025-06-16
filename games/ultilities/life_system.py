import pygame

class HPSystem:
    """A class to manage the health points (HP) system for a game entity."""
    def __init__(self, max_hp, screen, entity_rect):
        self.hp = max_hp
        self.max_hp = max_hp
        self.screen = screen
        self.entity_rect = entity_rect

    def draw_hp_bar(self):
        """Draws the health points bar above the entity."""
        bar_width = self.entity_rect.width
        bar_height = 6
        hp_ratio = max(self.hp, 0) / self.max_hp
        hp_bar_width = int(bar_width * hp_ratio)
        hp_bar_x = self.entity_rect.x + (self.entity_rect.width - bar_width) // 2
        hp_bar_y = self.entity_rect.y - bar_height - 4
        
        # Draw the background of the HP bar
        pygame.draw.rect(self.screen, (50, 50, 50), (hp_bar_x, hp_bar_y, bar_width, bar_height))

        # Draw the HP bar
        if hp_bar_width > 0:
            pygame.draw.rect(self.screen, (0, 255, 0), (hp_bar_x, hp_bar_y, hp_bar_width, bar_height))

    def take_damage(self, damage):
        """Reduces the HP by the specified damage amount."""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0