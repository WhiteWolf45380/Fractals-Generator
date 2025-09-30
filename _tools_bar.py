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

        """boutons"""
        self.buttons_next_x = self.surface_width * 0.66
        self.buttons = {
            "start": {},
            "pause": {},
            "edit": {},
        }
        for button in self.buttons:
            image = pygame.image.load(self.main.get_path(f"assets/{button}_button.xcf"))
            image_rect = image.get_rect(midleft=(self.buttons_next_x, self.surface_height / 2))
            self.buttons_next_x = image_rect.right + 20
            self.buttons[button] = {"image": image, "image_rect": image_rect}

        """surface finale post chargement servant de base au contenu dynamique"""
        self.surface_init = self.surface.copy()

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # blit des différents bouttons
        for button in self.buttons:
            if self.buttons[button]["image_rect"].collidepoint(self.main.get_relative_pos(self.surface_rect)):
                hovered = self.ui_manager.ask_for_following(self.name, f"{button}_button")
            else:
                hovered = False
            
            if hovered:
                pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "button_hover"), self.buttons[button]["image_rect"], border_radius=3)
            self.surface.blit(self.buttons[button]["image"], self.buttons[button]["image_rect"])
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Handles -_________________________
    def handle_inputs_down(self):
        """vérifications de la pression d'une touche"""
        pass

    def handle_inputs_up(self):
        """vérifications du relachement d'une touche"""
        pass