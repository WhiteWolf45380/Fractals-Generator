import pygame

# _________________________- Barre d'outils -_________________________
class ToolbarMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "toolbar"
        
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
        self.buttons_next_x = self.surface_width * 0.67 # démarrage de l'axe x
        self.buttons = { # trois boutons
            "start": {},
            "pause": {},
            "edit": {},
        }
        for button in self.buttons:
            image = pygame.image.load(self.main.get_path(f"assets/{button}_button.xcf")) # chargement de l'image
            image_rect = image.get_rect(midleft=(self.buttons_next_x, self.surface_height / 2)) # calcul de la position
            self.buttons_next_x = image_rect.right + 20 # calcul de la prochaine position
            self.buttons[button] = {"image": image, "image_rect": image_rect} # ajout au dictionnaire
        
        # ajout des événements (handles)
        self.ui_manager.add_handle(self.name, "down_start_button", self.handle_down_start_button)
        self.ui_manager.add_handle(self.name, "down_pause_button", self.handle_down_pause_button)
        self.ui_manager.add_handle(self.name, "down_edit_button", self.handle_down_edit_button)

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
                pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "button_hover"), self.buttons[button]["image_rect"], border_radius=2)
            self.surface.blit(self.buttons[button]["image"], self.buttons[button]["image_rect"])
        
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
    def handle_down_start_button(self):
        if not self.main.turtle.pause:
            self.main.turtle.draw("koch", 800, centered=True, color=(255, 255, 255), max_depth=8)
        else:
            self.main.turtle.do_unpause()
    
    def handle_down_pause_button(self):
        self.main.turtle.do_pause()

    def handle_down_edit_button(self):
        pass

# _________________________- Création d'éléments -_________________________
    def generate_text_button(self, name: str, x: int, y: int) -> dict:
        text, text_rect = self.ui_manager.generate_text(name, 30, color=self.ui_manager.get_color(self.name, "text"))