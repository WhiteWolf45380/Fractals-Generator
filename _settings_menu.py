import pygame

# _________________________- Menu des paramètres -_________________________
class SettingsMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "settings"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width // 4 # largeur du menu
        self.surface_height = self.main.screen_height - self.main.menus["toolbar"].surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topright=(self.main.screen_width, self.main.menus["toolbar"].surface_height))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        # titre
        self.title_back = pygame.Rect(0, 0, self.surface_width, 40)
        self.title_text, self.title_text_rect = self.ui_manager.generate_text("Propriétés", 25, color=self.ui_manager.get_color(self.name, "title"))
        self.title_text_rect.midleft = (self.surface_width * 0.05, 20)
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "highlight"), self.title_back)
        self.surface.blit(self.title_text, self.title_text_rect)

        """boutton de repli"""
        self.collapse_button_dict = self.ui_manager.generate_collapse_button("right", 0, self.surface_height / 2, anchor="midleft")
        self.ui_manager.add_handle(self.name, "down_collapse_button", self.handle_down_collapse_button)

        """surface finale post chargement servant de base au contenu dynamique"""
        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, 0), (0, self.surface_height), width=2)
        self.surface_init = self.surface.copy()

        """variables utiles"""
        # ouverture/fermeture
        self.x_init = self.surface_rect.left
        self.opened = True
        self.offset_velocity = 13
        self.offset_closed = self.surface_width - self.collapse_button_dict["back"].width
        self.offset_current = 0

        # paramètres des éléments
        self.parameters = {
            "bar": {
                "generate": self.generate_setting_bar,
                "update": self.update_setting_bar,
                "bar_width": 100,
                "bar_height": 10,
                "thumb_width": 10,
                "thumb_height": 20,
            }
        }

        # propriétés
        self.settings_x = 50 # décalage horizontal
        self.settings_y_init = self.title_back.bottom + 50 # placement vertical initial
        self.settings_y_next = self.settings_y_init # placement vertical dynamique

        """propriétés"""
        self.settings = { # caractéristiques des paramètres
            "size": {"category": "bar", "text_content": "Taille", "value": 400, "value_min": 100, "value_max": 2000}
        }

        # génération des paramètres
        for setting in self.settings:
            self.settings[setting]["name"] = setting # attribution d'un nom pour faciliter l'identification
            self.settings[setting]["package"] = self.generate_setting(self.settings[setting]["text_content"], self.settings[setting]["category"]) # génération du paramètre

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # ouverture/fermeture du menu
        if self.opened and self.offset_current > 0:
            progression = self.offset_current / self.offset_closed
            self.offset_current = max(0, self.offset_current - self.offset_velocity * self.get_incrementation(progression))
        elif not self.opened and self.offset_current < self.offset_closed:
            progression = 1 - self.offset_current / self.offset_closed
            self.offset_current = min(self.offset_closed, self.offset_current + self.offset_velocity * self.get_incrementation(progression))
        self.surface_rect.left = self.x_init + self.offset_current

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict, opened=self.opened)

        # update des paramètres
        self.settings_y_next = self.settings_y_init
        for setting_content in self.settings.values():
            self.settings_y_next = self.update_setting(setting_content, self.settings_y_next)
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)
    
    def get_incrementation(self, progression: float) -> float:
        """renvoie un ratio pour une croissance non linéaire"""
        return progression ** 0.5

# _________________________- Handles controllers -_________________________
    def handle_left_click_down(self, button: str):
        """évènements associés au clique souris gauche"""
        self.ui_manager.do_handle(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """évènements associés au relâchement du clique souris gauche"""
        pass

# _________________________- Handlers -_________________________
    def handle_down_collapse_button(self):
        """événement : appui sur le boutton d'ouverture/fermeture du menu"""
        self.opened = not self.opened

# _________________________- Création d'éléments -_________________________
    def generate_setting(self, text_content: str, category: str) -> dict:
        """génère un paramètre"""
        # dictionnaire final du paramètre
        package = {}
        # texte
        package["text"], package["text_rect"] = self.ui_manager.generate_text(f"{text_content} :", 20, color=self.ui_manager.get_color(self.name, "text"), wlimit=20)
        package["text_rect"].left = self.settings_x
        # éléments interactifs
        setting_handler = self.parameters.get(category, {}).get("generate", lambda _: {})(package["text_rect"].right)
        for key, value in setting_handler.items():
            package[key] = value
        
        return package

    def generate_setting_bar(self, text_right) -> dict:
        """génère une barre"""
        parameters = self.parameters["bar"] # raccourci
        # barre
        bar = pygame.Rect(0, 0, parameters["bar_width"], parameters["bar_height"])
        bar.left = text_right + 20
        # le slider
        thumb = pygame.Rect(0, 0, parameters["thumb_width"], parameters["thumb_height"])

        return {"bar": bar, "thumb": thumb}

# _________________________- Mise à jour d'éléments -_________________________
    def update_setting(self, content: dict, y: int):
        """met à jour un paramètre"""
        package = content["package"] # raccourci
        package["text_rect"].top = y # repositionnement du texte
        self.surface.blit(package["text"], package["text_rect"]) # blit du texte
        forced_next_y = self.parameters.get(content["category"], {}).get("update", lambda _: {})(content) # mise à jour du contenu interactif
        
        return forced_next_y if forced_next_y is not None else package["text_rect"].bottom + 20
    
    def update_setting_bar(self, content: dict):
        """met à jour une barre"""
        package = content["package"] # raccourci
        # mise à jour des positions verticales
        package["bar"].centery = package["text_rect"].centery
        package["thumb"].centery = package["bar"].centery
        # si l'utilisateur attrape la barre
        if self.ui_manager.is_mouse_grabbing(self.name, content["name"]):
            right_limit = package["bar"].right - package["thumb"].width / 2 # limite minimum
            left_limit = package["bar"].left + package["thumb"].width / 2 # limite maximum
            package["thumb"].centerx = min(max(self.main.get_relative_pos(self.surface_rect)[0] - content.get("delta", 0), left_limit), right_limit) # suivi du curseur - delta (ancre de saisi)
            ratio = (content["thumb"].centerx - left_limit) / (right_limit - left_limit) # ratio entre le min et le max
            content["value"] = ratio * (content["value_max"] - content["value_min"]) # affectation de la valeur selon la position horizontale
        # blit
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "bar"), package["bar"])
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, f"thumb_{'hover' if self.ui_manager.mouse_hover == (self.name, content['name']) else 'idle'}"), package["thumb"])