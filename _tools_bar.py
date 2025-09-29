import pygame

# _________________________- Barre d'outils -_________________________
class ToolsBar:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "tools_bar"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width # largeur du menu
        self.surface_height = 50 # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, self.surface_height-1), (self.surface_width, self.surface_height-1), width=1)

        """bouton d'éxécution"""
        self.start_button_image = pygame.image.load(self.main.get_path("assets/start_button.xcf"))

        """surface finale post chargement servant de base au contenu dynamique"""
        self.surface_init = self.surface.copy()

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Handles -_________________________
    def handle_inputs_down(self):
        """vérifications de la pression d'une touche"""
        pass

    def handle_inputs_up(self):
        """vérifications du relachement d'une touche"""
        pass