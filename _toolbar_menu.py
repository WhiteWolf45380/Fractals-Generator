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
        self.surface_height = 40 # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        """boutons"""
        # bouttons liés au dessin
        self.buttons_next_x = self.surface_width * 0.99 # démarrage de l'axe x
        self.buttons = { # trois boutons
            "edit": {},
            "pause": {},
            "start": {},            
        }
        for button in self.buttons:
            image, image_rect = self.ui_manager.generate_image(f"{button}_button") # génération de l'image
            image_rect.midright = (self.buttons_next_x, self.surface_height / 2) # positionnement de l'image
            self.buttons_next_x = image_rect.left - 15 # calcul de la prochaine position
            self.buttons[button] = {"image": image, "image_rect": image_rect} # ajout au dictionnaire
        
            # ajout des événements (handlers)
        self.ui_manager.add_handler(self.name, "down_start_button", self.handle_down_start_button)
        self.ui_manager.add_handler(self.name, "down_pause_button", self.handle_down_pause_button)
        self.ui_manager.add_handler(self.name, "down_edit_button", self.handle_down_edit_button)

        # boutons textuels
        self.text_buttons_parameters = {
            "height": self.surface_height * 0.6,
            "fontsize": 18,
        }

        self.text_buttons = {
            "Fichier": {},
            "Affichage": {},
            "Outils": {},
            "Aide": {}
        }

        # menus textuels
        self.text_menus = { # stockage des éléments
            "Fichier": {
            },
            "Affichage": {
                "theme": {"name": "theme", "type": "choices", "description": "Thème","choices": [("light", "Clair"), ("dark", "Sombre")], "value": "dark"},
            },
            "Outils": {

            },
            "Aide": {

            }
        }

        # génération des boutons de texte
        next_x_offset = 20
        for text_button in self.text_buttons:
            # génération du bouton textuel
            self.text_buttons[text_button]["name"] = text_button
            self.text_buttons[text_button]["package"] = self.generate_text_button(text_button, next_x_offset, self.surface_height // 2, anchor="midleft")
            # génération du menu textuel
            self.text_menus[text_button]["package"] = self.ui_manager.generate_text_menu(self.text_menus[text_button], self.text_buttons[text_button]["package"]["back"].left, self.text_buttons[text_button]["package"]["back"].bottom)
            next_x_offset = self.text_buttons[text_button]["package"]["back"].right

        # ajout des handlers
        self.ui_manager.add_handler(self.name, "down_text_button", self.handle_down_text_button) # bouttons textuels
        self.ui_manager.add_handler(self.name, "down_text_menu_item", self.ui_manager.handle_down_text_menu_item) # items des menus textuels

        """surface finale post chargement servant de base au contenu dynamique"""
        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, self.surface_height-1), (self.surface_width, self.surface_height-1), width=1)
        self.surface_init = self.surface.copy()

        """variables utiles"""
        self.text_menus_opened = False
        self.text_menus_current = ""

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # blit des différents boutons de texte
        for text_button in self.text_buttons:
            self.update_text_button(self.text_buttons[text_button])

        # blit des différents boutons liés au dessin
        for button in self.buttons:
            if self.buttons[button]["image_rect"].collidepoint(self.main.get_relative_pos(self.surface_rect)):
                if self.ui_manager.ask_for_mouse_hover(self.name, f"{button}_button"):            
                    pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "button_hover"), self.buttons[button]["image_rect"], border_radius=2)
            self.surface.blit(self.buttons[button]["image"], self.buttons[button]["image_rect"])
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

        # blit du menu ouvert
        if self.text_menus_opened:
            self.ui_manager.update_text_menu(self.text_menus[self.text_menus_current], self.main.screen)

# _________________________- Handlers controllers -_________________________
    def handle_left_click_down(self, button: str):
        """événements associés au clique souris gauche"""
        self.ui_manager.do_handler(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """événements associés au relâchement du clique souris gauche"""

    def handle_mousewheel(self, y_offset: int):
        """événements associés à l'utilisation de la molette"""

# _________________________- Handlers -_________________________
    def handle_down_start_button(self):
        """événement(clique gauche): bouton d'éxécution"""
        if not self.main.turtle.pause:
            self.main.turtle.draw()
        else:
            self.main.turtle.do_unpause()
    
    def handle_down_pause_button(self):
        """événement(clique gauche): bouton pause"""
        self.main.turtle.do_pause()

    def handle_down_edit_button(self):
        """événement(clique gauche): bouton d'édition de l'éxécution"""
        pass

    def handle_down_text_button(self):
        """événement(clique gauche): bouton textuel"""
        self.text_menus_opened = not self.text_menus_opened
        self.text_menus_current = self.ui_manager.mouse_hover[2]
    
    def handle_down_text_menu(self):
        """événement indépendant(clique gauche): bouton textuel"""
        if self.text_menus_opened and not self.text_menus[self.text_menus_current]["package"]["surface_rect"].collidepoint((self.main.mouse_x, self.main.mouse_y)) and not self.text_buttons[self.text_menus_current]["package"]["back"].collidepoint(self.main.get_relative_pos(self.surface_rect)):
            
            self.text_menus_opened = False

# _________________________- Création d'éléments -_________________________
    def generate_text_button(self, name: str, x: int, y: int, anchor: str="topleft") -> dict:
        """génère un boutton de type texte"""
        parameters = self.text_buttons_parameters # raccourci

        # texte du bouton
        text, text_rect = self.ui_manager.generate_text(name, self.text_buttons_parameters["fontsize"], color=self.ui_manager.get_color(self.name, "text"))
        text_hover, _ = self.ui_manager.generate_text(name, self.text_buttons_parameters["fontsize"], color=self.ui_manager.get_color(self.name, "text_hover"))
        text_width = text_rect.width + 30

        # fond du bouton
        if anchor != "topleft": # calcul du coin haut gauche si ancre différente
            x, y = self.ui_manager.get_anchor_pos(x, y, text_width, parameters["height"], anchor)
        back = pygame.Rect(x, y, text_width, parameters["height"])
        text_rect.center = back.center

        return {"back": back, "text": text, "text_hover": text_hover, "text_rect": text_rect}
    
# _________________________- Mise à jour d'éléments -_________________________
    def update_text_button(self, content: dict):
        """mise à jour d'un bouton textuel"""
        package = content["package"] # raccourci

        # mouse hover
        if self.ui_manager.is_mouse_hover(package["back"], self.surface_rect):
            is_hovered = self.ui_manager.ask_for_mouse_hover(self.name, "text_button", _id=content["name"])
            self.text_menus_current = self.ui_manager.mouse_hover[2]
        else:
            is_hovered = False
        
        is_current = content["name"] == self.text_menus_current
        if is_hovered or is_current and self.text_menus_opened: # fond
            pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "button_hover"), package["back"], border_radius=7)

        # texte
        self.surface.blit(package["text_hover" if is_hovered or is_current and self.text_menus_opened else "text"], package["text_rect"])