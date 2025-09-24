import pygame


class Settings:
    
    def __init__(self, main):
        """passerelles"""
        self.main = main

        """pygame"""
        self.surface_width = self.main.screen_width // 3
        self.surface_height = self.main.screen_height
        self.surface = pygame.Surface((self.surface_width, self.surface_height))
        self.surface.fill((70, 70, 70))

    def update(self):
        self.main.screen.blit(self.surface, (self.main.screen_width - self.surface_width, 0))