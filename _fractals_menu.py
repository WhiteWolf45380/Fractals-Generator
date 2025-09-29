import pygame

# _________________________- Menu de choix de fractal -_________________________
class FractalsMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.name = "fractals_menu"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width // 5 # largeur du menu
        self.surface_height = self.main.screen_height - self.main.tools_bar.surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topleft=(0, self.main.tools_bar.surface_height))# placement en haut de l'écran
        self.surface_color = self.main.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        """surface finale post chargement servant de base au contenu dynamique"""
        self.surface_init = self.surface.copy()

    def update(self):
        """Mise à jour du menu de choix de fractal"""
        self.main.screen.blit(self.surface, self.surface_rect)

    def check_inputs_down(self):
        pass

    def check_inputs_up(self):
        pass