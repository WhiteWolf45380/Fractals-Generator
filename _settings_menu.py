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
                "handler": self.handle_down_setting_bar,
                "bar_width": 200,
                "bar_height": 10,
                "thumb_width": 10,
                "thumb_height": 40,
            }
        }
        
        # ajout des handlers des éléments
        for category in self.parameters:
            if self.parameters[category].get("handler") is not None:
                self.ui_manager.add_handle(self.name, f"down_setting_{category}", self.parameters["bar"]["handler"])

        # propriétés
        self.settings_x = 20 # décalage horizontal
        self.settings_y_init = self.title_back.bottom + 30 # placement vertical initial
        self.settings_y_next = self.settings_y_init # placement vertical dynamique

        """propriétés"""
        self.settings = { # caractéristiques des paramètres
            "size": {"category": "bar", "text_content": "Taille", "value": 400, "value_min": 100, "value_max": 1500}
        }

        # génération des paramètres
        for setting in self.settings:
            self.settings[setting]["name"] = setting # attribution d'un nom pour faciliter l'identification
            self.settings[setting]["package"] = self.generate_setting(self.settings[setting]) # génération du paramètre

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
        self.ui_manager.mouse_grabbing = None

# _________________________- Handlers -_________________________
    def handle_down_collapse_button(self):
        """événement : appui sur le boutton d'ouverture/fermeture du menu"""
        self.opened = not self.opened

    def handle_down_setting_bar(self):
        """événement : attrape une barre"""
        _id = self.ui_manager.mouse_hover[2] # récupération de l'id
        grabbed = self.ui_manager.ask_for_mouse_grabbing(self.name, "setting_bar", _id=_id)
        if grabbed:
            self.settings[_id]["delta"] = self.main.get_relative_pos(self.surface_rect)[0] - self.settings[_id]["package"]["thumb"].centerx

# _________________________- Création d'éléments -_________________________
    def generate_setting(self, content: dict) -> dict:
        """génère un paramètre"""
        # dictionnaire final du paramètre
        package = {}
        # texte
        package["text"], package["text_rect"] = self.ui_manager.generate_text(f"{content['text_content']} :", 25, color=self.ui_manager.get_color(self.name, "text"), wlimit=self.surface_width * 0.3)
        package["text_rect"].left = self.settings_x
        # éléments interactifs
        setting_handler = self.parameters.get(content['category'], {}).get("generate", lambda _: {})(content, package["text_rect"].right)
        for key, value in setting_handler.items():
            package[key] = value
    
        return package
    
    def generate_value(self, value: int, x: int) -> dict:
        """génère un compteur (qui affiche la valeur)"""
        value_text, value_text_rect = self.ui_manager.generate_text(str(value), 20, color=self.ui_manager.get_color(self.name, "text"), wlimit=self.surface_width * 0.2)
        value_text_rect.left = x
        return {"value_text": value_text, "value_text_rect": value_text_rect}

    def generate_setting_bar(self, content: dict, x: int) -> dict:
        """génère une barre"""
        parameters = self.parameters["bar"] # raccourci
        # barre
        bar = pygame.Rect(0, 0, parameters["bar_width"], parameters["bar_height"])
        bar.left = x + 50
        # slider
        thumb = pygame.Rect(0, 0, parameters["thumb_width"], parameters["thumb_height"])
        ratio = (content["value"] - content["value_min"]) / (content["value_max"] - content["value_min"])
        thumb.centerx = bar.left + thumb.width / 2 + ratio * (bar.width - thumb.width)
        
        # compteur
        value_dict = self.generate_value(content["value"], bar.right + 30)

        return {"bar": bar, "thumb": thumb, "value_text": value_dict["value_text"], "value_text_rect": value_dict["value_text_rect"]}

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
        package["value_text_rect"].centery = package["bar"].centery
        # si l'utilisateur survole la barre
        if self.ui_manager.is_mouse_hover(package["thumb"], self.surface_rect):
            hovered = self.ui_manager.ask_for_mouse_hover(self.name, "setting_bar", _id=content["name"])
        else:
            hovered = False
        # si l'utilisateur attrape la barre
        grabbed = self.ui_manager.is_mouse_grabbing(self.name, "setting_bar", _id=content["name"])
        if grabbed:
            right_limit = package["bar"].right - package["thumb"].width / 2 # limite minimum
            left_limit = package["bar"].left + package["thumb"].width / 2 # limite maximum
            package["thumb"].centerx = min(max(self.main.get_relative_pos(self.surface_rect)[0] - content.get("delta", 0), left_limit), right_limit) # suivi du curseur - delta (ancre de saisi)
            ratio = (package["thumb"].centerx - left_limit) / (right_limit - left_limit) # ratio entre le min et le max
            content["value"] = round(content["value_min"] + ratio * (content["value_max"] - content["value_min"])) # affectation de la valeur selon la position horizontale
            package["thumb"].centerx = min(max(left_limit + (right_limit - left_limit) * (content["value"] - content["value_min"]) / (content["value_max"] - content["value_min"]), left_limit), right_limit) # on fait un "snap" afin de faire correspondre l'arrondi
            value_dict = self.generate_value(content["value"], package["value_text_rect"].left)
            package["value_text"], _ = value_dict["value_text"], value_dict["value_text_rect"]
        # blit
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "bar"), package["bar"])
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, f"thumb_{'hover' if hovered or grabbed else 'idle'}"), package["thumb"])
        self.surface.blit(package["value_text"], package["value_text_rect"])