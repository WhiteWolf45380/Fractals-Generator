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

        """boutons"""
        # bouttons liés au dessin
        self.buttons_next_x = self.surface_width * 0.98 # démarrage de l'axe x
        self.buttons = { # trois boutons
            "edit": {},
            "pause": {},
            "start": {},            
        }
        for button in self.buttons:
            image = pygame.image.load(self.main.get_path(f"assets/{button}_button.xcf")) # chargement de l'image
            image_rect = image.get_rect(midright=(self.buttons_next_x, self.surface_height / 2)) # calcul de la position
            self.buttons_next_x = image_rect.left - 20 # calcul de la prochaine position
            self.buttons[button] = {"image": image, "image_rect": image_rect} # ajout au dictionnaire
        
            # ajout des événements (handlers)
        self.ui_manager.add_handle(self.name, "down_start_button", self.handle_down_start_button)
        self.ui_manager.add_handle(self.name, "down_pause_button", self.handle_down_pause_button)
        self.ui_manager.add_handle(self.name, "down_edit_button", self.handle_down_edit_button)

        # bouttons de texte
        self.text_buttons_parameters = {
            "height": self.surface_height * 0.6,
            "fontsize": 22,
        }

        self.text_buttons = {
            "Fichier": {},
            "Affichage": {},
            "Outils": {},
            "Aide": {}
        }

            # génération des boutons de texte
        next_x_offset = 20
        for text_button in self.text_buttons:
            self.text_buttons[text_button] = self.generate_text_button(text_button, next_x_offset, self.surface_height // 2, anchor="midleft")
            next_x_offset = self.text_buttons[text_button]["back"].right

        """surface finale post chargement servant de base au contenu dynamique"""
        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, self.surface_height-1), (self.surface_width, self.surface_height-1), width=1)
        self.surface_init = self.surface.copy()

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # blit des différents boutons de texte
        for text_button in self.text_buttons:
            if self.ui_manager.is_mouse_hover(self.text_buttons[text_button]["back"], self.surface_rect):
                if self.ui_manager.ask_for_mouse_hover(self.name, f"{text_button}_button"):
                    pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "button_hover"), self.text_buttons[text_button]["back"], border_radius=7)
            self.surface.blit(self.text_buttons[text_button]["text"], self.text_buttons[text_button]["text_rect"])

        # blit des différents boutons liés au dessin
        for button in self.buttons:
            if self.buttons[button]["image_rect"].collidepoint(self.main.get_relative_pos(self.surface_rect)):
                if self.ui_manager.ask_for_mouse_hover(self.name, f"{button}_button"):            
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
        """handler du boutton d'éxécution"""
        if not self.main.turtle.pause:
            self.main.turtle.draw("koch", 800)
        else:
            self.main.turtle.do_unpause()
    
    def handle_down_pause_button(self):
        """handler du boutton pause"""
        self.main.turtle.do_pause()

    def handle_down_edit_button(self):
        """handler du boutton d'édition de l'éxécution"""
        pass

# _________________________- Création d'éléments -_________________________
    def generate_text_button(self, name: str, x: int, y: int, anchor: str="topleft") -> dict:
        """génère un boutton de type texte"""
        parameters = self.text_buttons_parameters # raccourci

        # texte du bouton
        text, text_rect = self.ui_manager.generate_text(name, self.text_buttons_parameters["fontsize"], color=self.ui_manager.get_color(self.name, "text"))
        text_width = text_rect.width + 30

        # fond du bouton
        if anchor != "topleft": # calcul du coin haut gauche si ancre différente
            x, y = self.ui_manager.get_anchor_pos(x, y, text_width, parameters["height"], anchor)
        back = pygame.Rect(x, y, text_width, parameters["height"])
        text_rect.center = back.center

        return {"back": back, "text": text, "text_rect": text_rect}