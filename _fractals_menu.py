import pygame

# _________________________- Menu de choix de fractal -_________________________
class FractalsMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "fractals"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width // 5 # largeur du menu
        self.surface_height = self.main.screen_height - self.main.menus["toolbar"].surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topleft=(0, self.main.menus["toolbar"].surface_height))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (self.surface_width - 2, 0), (self.surface_width - 2, self.surface_height), width=2)

        """boutton de repli"""
        self.collapse_button_dict = self.ui_manager.generate_collapse_button("left", self.surface_width, self.surface_height / 2, anchor="midright")

        """surface finale post chargement servant de base au contenu dynamique"""
        self.surface_init = self.surface.copy()

    def update(self):
        """Mise à jour du menu de choix de fractal"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict)

        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Handles controllers -_________________________
    def handle_left_click_down(self, button: str):
        """évènements associés au clique souris gauche"""
        self.ui_manager.do_handle(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """évènements associés au relâchement du clique souris gauche"""
        pass

# _________________________- Handles -_________________________
