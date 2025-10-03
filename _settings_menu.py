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
        self.ui_manager.add_handler(self.name, "down_collapse_button", self.handle_down_collapse_button)

        """surface finale post chargement servant de base au contenu dynamique"""
        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, 0), (0, self.surface_height), width=2)
        self.surface_init = self.surface.copy()

        """variables utiles"""
        # ouverture/fermeture
        self.opened = True
        self.offset_x_init = self.surface_rect.left
        self.offset_x_final = self.surface_rect.left + (self.surface_rect.width - self.collapse_button_dict["back"].width)
        self.offset_duration = 1.2
        self.offset_progression = 1

        # paramètres des éléments
        self.parameters = {
            "general": {
                "text_fontsize": 20, # taille de la police des textes descriptif
                "text_wlimit": self.surface_width * 0.35, # limite de longueur du texte
                "value_fontsize": 15, # taille de la police des valeurs
                "value_wlimit": self.surface_width * 0.2, # limite de longueur des valeurs
                "x_offset": 25, # décalage entre le texte et le contenu interactif
            },
            "bar": {
                "generate": self.generate_setting_bar, # fonction générative
                "update": self.update_setting_bar, # fonction de mise à jour
                "handler": self.handle_down_setting_bar, # fonction d'événement
                "bar_width": 150, # largeur de la barre
                "bar_height": 8, # hauteur de la barre
                "thumb_width": 8, # épaisseur du slider
                "thumb_height": 30, # hauteur du slider
            },
            "color": {
                "generate": self.generate_setting_color, # fonction générative
                "update": self.update_setting_color, # fonction de mise à jour
                "width": 40, # hauteur du rect
                "border": 1, # bordure du rect
                "x_offset": 350,# décalage pour etre sur la droite du menu
            }
        }
        
        # ajout des handlers des éléments
        for category in self.parameters:
            if self.parameters[category].get("handler") is not None:
                self.ui_manager.add_handler(self.name, f"down_setting_{category}", self.parameters["bar"]["handler"])

        # propriétés
        self.settings_y_init = self.title_back.bottom + 30 # placement vertical initial
        self.settings_y_next = self.settings_y_init # placement vertical dynamique

        """propriétés"""
        self.settings = { # caractéristiques des paramètres
            "depth": {"category": "bar", "description": "Profondeur", "value": 1, "value_min": 0, "value_max": 20},
            "size": {"category": "bar", "description": "Taille", "value": 400, "value_min": 100, "value_max": 1500},
            "width": {"category": "bar", "description": "Epaisseur", "value": 1, "value_min": 1, "value_max": 20},
            "color_r": {"category": "bar", "description": "Canal rouge", "value": self.ui_manager.get_color(self.name, "line")[0], "value_min": 0, "value_max": 255},
            "color_g": {"category": "bar", "description": "Canal vert", "value": self.ui_manager.get_color(self.name, "line")[1], "value_min": 0, "value_max": 255},
            "color_b": {"category": "bar", "description": "Canal bleu", "value": self.ui_manager.get_color(self.name, "line")[2], "value_min": 0, "value_max": 255},
            "color_result": {"category": "color", "masters": ["color_r", "color_g", "color_b"]},
            "x_offset": {"category": "bar", "description": "x (horizontal)", "value": 0, "value_min": -1000, "value_max": 1000},
            "y_offset": {"category": "bar", "description": "y (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "a": {"category": "bar", "description": "a (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "b": {"category": "bar", "description": "n (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "c": {"category": "bar", "description": "c (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "d": {"category": "bar", "description": "d (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "e": {"category": "bar", "description": "e (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "f": {"category": "bar", "description": "f (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "g": {"category": "bar", "description": "g (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "h": {"category": "bar", "description": "h (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "i": {"category": "bar", "description": "i (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "j": {"category": "bar", "description": "j (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "k": {"category": "bar", "description": "k (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "l": {"category": "bar", "description": "l (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "m": {"category": "bar", "description": "m (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "n": {"category": "bar", "description": "n (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "o": {"category": "bar", "description": "o (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
            "p": {"category": "bar", "description": "p (vertical)", "value": 0, "value_min": -1000, "value_max": 1000},
        }

        # génération des paramètres
        for setting in self.settings:
            self.settings[setting]["name"] = setting # attribution d'un nom pour faciliter l'identification
            self.settings[setting]["package"] = self.generate_setting(self.settings[setting]) # génération du paramètre

        """barre de défilement"""
        self.scroll_bar = self.ui_manager.generate_scroll_bar(self.surface_rect, 1, y_offset_start=self.title_back.height, back=True, hidden=False)
        self.ui_manager.add_handler(self.name, "down_scroll_bar", self.ui_manager.handle_down_scroll_bar)

    def update(self):
        """Mise à jour du menu des propriétés"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # ouverture/fermeture du menu
        if self.offset_progression < 1:
            self.offset_progression = min(1.0, self.offset_progression + self.main.dt / self.offset_duration)

            # easing
            eased = self.ui_manager.get_ease_out(self.offset_progression, intensity=1.5)

            # interpolation
            x = self.offset_x_init + (self.offset_x_final - self.offset_x_init) * eased
            self.surface_rect.left = int(x)

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict, opened=self.opened)

        # clipping pour le scroll des paramètres
        clip_rect = pygame.Rect(0, self.title_back.bottom, self.surface_width, self.surface_height - self.title_back.bottom)
        self.surface.set_clip(clip_rect)

            # update des paramètres
        self.settings_y_next = self.settings_y_init - self.scroll_bar["y_dif"]
        for setting_content in self.settings.values():
            self.settings_y_next = self.update_setting(setting_content, self.settings_y_next)
        
        # fin de clipping
        self.surface.set_clip(None)

        # update de la barre de défilement
        self.ui_manager.update_scroll_bar(self.scroll_bar, self.surface, self.surface_rect, menu=self.name, ratio=(self.surface_height - self.title_back.height)/(self.settings_y_next+self.scroll_bar["y_dif"]))
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Handles controllers -_________________________
    def handle_left_click_down(self, button: str):
        """événements associés au clique souris gauche"""
        self.ui_manager.do_handler(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """événements associés au relâchement du clique souris gauche"""

    def handle_mousewheel(self, y_offset: int):
        """événements associés à l'utilisation de la molette"""
        if self.surface_rect.collidepoint((self.main.mouse_x, self.main.mouse_y)):
            self.ui_manager.handle_mousewheel_scroll_bar(self.scroll_bar, y_offset)

# _________________________- Handlers -_________________________
    def handle_down_collapse_button(self):
        """événement : appui sur le boutton d'ouverture/fermeture du menu"""
        self.opened = not self.opened
        self.offset_progression = 0
        # position actuelle comme nouveau départ
        self.offset_x_init = self.surface_rect.left
        if self.opened:
            self.offset_x_final = self.main.screen_width - self.surface_width
        else:
            self.offset_x_final = self.main.screen_width - self.collapse_button_dict["back"].width

    def handle_down_setting_bar(self):
        """événement : attrape une barre"""
        _id = self.ui_manager.mouse_hover[2] # récupération de l'id
        is_grabbed = self.ui_manager.ask_for_mouse_grabbing(self.name, "setting_bar", _id=_id)
        if is_grabbed:
            self.settings[_id]["delta"] = self.main.get_relative_pos(self.surface_rect)[0] - self.settings[_id]["package"]["thumb"].centerx

# _________________________- Création d'éléments -_________________________
    def generate_setting(self, content: dict) -> dict:
        """génère un paramètre"""
        parameters = self.parameters["general"] # raccourci

        # dictionnaire final du paramètre
        package = {}

        # texte
        if content.get("description") is not None:
            package["text"], package["text_rect"] = self.ui_manager.generate_text(f"{content['description']}", parameters["text_fontsize"], color=self.ui_manager.get_color(self.name, "text"), wlimit=parameters["text_wlimit"], end=" :")
            package["text_rect"].left = parameters["x_offset"]

        # éléments interactifs
        setting_handler = self.parameters.get(content['category'], {}).get("generate", lambda _: {})(content, (package["text_rect"].right if content.get("description") is not None else 0) + parameters["x_offset"])
        for key, value in setting_handler.items():
            package[key] = value
    
        return package
    
    def generate_value(self, value: int, x: int) -> dict:
        """génère un compteur (qui affiche la valeur)"""
        parameters = self.parameters["general"] # raccourci
        value_text, value_text_rect = self.ui_manager.generate_text(str(value), parameters["value_fontsize"], color=self.ui_manager.get_color(self.name, "text"), wlimit=parameters["value_wlimit"]) # génération du texte
        value_text_rect.left = x # fixation de la coordonnée x
        return {"value_text": value_text, "value_text_rect": value_text_rect}

    def generate_setting_bar(self, content: dict, x: int) -> dict:
        """génère une barre"""
        parameters = self.parameters["bar"] # raccourci

        # barre
        bar = pygame.Rect(0, 0, parameters["bar_width"], parameters["bar_height"])
        bar.left = x

        # slider
        thumb = pygame.Rect(0, 0, parameters["thumb_width"], parameters["thumb_height"])
        left_limit = bar.left + thumb.width / 2
        right_limit = bar.right - thumb.width / 2
        thumb.centerx = left_limit + (content["value"] - content["value_min"]) / (content["value_max"] - content["value_min"]) * (bar.width - thumb.width) # positionnement x
        content["value"] = self.main.snap_value(content["value_min"] + (content["value_max"] - content["value_min"]) * (thumb.centerx - left_limit) / (right_limit - left_limit), content["value_min"], content["value_max"]) # simple snap
        thumb.centerx = left_limit + (content["value"] - content["value_min"]) / (content["value_max"] - content["value_min"]) * (bar.width - thumb.width) # double snap
        
        # compteur
        value_dict = self.generate_value(content["value"], bar.right + 15)

        return {"bar": bar, "thumb": thumb, "value_text": value_dict["value_text"], "value_text_rect": value_dict["value_text_rect"]}
    
    def generate_setting_color(self, content: dict, x: int) -> dict:
        """génère un rectangle de couleur (utile pour le résultat rgb)"""
        parameters = self.parameters["color"] # raccourci

        # rectangle
        height = self.settings[content["masters"][-1]]["package"]["text_rect"].bottom - self.settings[content["masters"][0]]["package"]["text_rect"].top # hauteur variable
        rect = pygame.Rect(x, 0, parameters["width"], height)
        rect.left = x + parameters["x_offset"]

        return {"rect": rect}

# _________________________- Mise à jour d'éléments -_________________________
    def update_setting(self, content: dict, y: int):
        """met à jour un paramètre"""
        package = content["package"] # raccourci
        if content.get("description") is not None: # si il y a bien un text a blit
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
            is_hovered = self.ui_manager.ask_for_mouse_hover(self.name, "setting_bar", _id=content["name"])
        else:
            is_hovered = False

        # si l'utilisateur attrape la barre
        is_grabbed = self.ui_manager.is_mouse_grabbing(self.name, "setting_bar", _id=content["name"])
        if is_grabbed:
            # limites
            right_limit = package["bar"].right - package["thumb"].width / 2 # limite minimum
            left_limit = package["bar"].left + package["thumb"].width / 2 # limite maximum

            # repositionnement
            package["thumb"].centerx = min(max(self.main.get_relative_pos(self.surface_rect)[0] - content.get("delta", 0), left_limit), right_limit) # suivi du curseur - delta (ancre de saisi)

            # calcul de la nouvelle valeur
            ratio = (package["thumb"].centerx - left_limit) / (right_limit - left_limit) # ratio entre le min et le max

            # snaps
            content["value"] = self.main.snap_value(content["value_min"] + ratio * (content["value_max"] - content["value_min"]), content["value_min"], content["value_max"]) # affectation de la valeur selon la position horizontale
            package["thumb"].centerx = min(max(left_limit + (right_limit - left_limit) * (content["value"] - content["value_min"]) / (content["value_max"] - content["value_min"]), left_limit), right_limit) # on fait un "snap" afin de faire correspondre l'arrondi

            # génération de la valeur textuelle
            value_dict = self.generate_value(content["value"], package["value_text_rect"].left)
            package["value_text"], _ = value_dict["value_text"], value_dict["value_text_rect"]
    
        # affichage
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "bar"), package["bar"])
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, f"thumb_{'hover' if is_hovered or is_grabbed else 'idle'}"), package["thumb"])
        self.surface.blit(package["value_text"], package["value_text_rect"])

    def update_setting_color(self, content: dict):
        """met à jour un rectangle de couleur"""
        package = content["package"]# raccourci

        # repositionnement
        package["rect"].top = self.settings[content["masters"][0]]["package"]["text_rect"].top
        package["rect"].height = self.settings[content["masters"][-1]]["package"]["text_rect"].bottom - self.settings[content["masters"][0]]["package"]["text_rect"].top

        # affichage
        pygame.draw.rect(self.surface, tuple(self.settings[content["masters"][i]]["value"] for i in range(3)), package["rect"])
        pygame.draw.rect(self.surface, (0, 0, 0), package["rect"], self.parameters["color"]["border"])

        return self.settings_y_next