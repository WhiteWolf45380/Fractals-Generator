import pygame


# _________________________- Manager de l'UI -_________________________
class UIManager:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.name = "ui_manager"
        
        """thèmes"""
        self.themes = {
            "dark": {
                "toolbar": {
                    "back": (50, 53, 56), 
                    "text": (215, 220, 230),
                    "text_hover": (255, 255, 255),
                    "line": (220, 220, 220),
                    "button_hover": (65, 69, 71),
                },
                "text_menu": {
                    "back": (69, 72, 75),
                    "text": (255, 255, 255),
                    "item_hover": (52, 55, 58),
                    "item_icons": (150, 150, 150),
                },
                "fractals": {
                    "back": (50, 53, 56), 
                    "title": (30, 35, 40),
                    "section": (255, 255, 255),
                    "text": (225, 230, 240),
                    "title_highlight": (170, 173, 176),
                    "section_highlight": (84, 87, 90),
                    "line": (180, 180, 180), 
                    "selection": (20, 180, 255),
                    "button_hover": (90, 90, 90),
                    "collapse_idle": (240, 240, 240),
                    "collapse_hover": (170, 170, 170),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                    "scroll_bar_back": (45, 48, 51),
                    "scroll_bar_thumb_idle": (63, 66, 66),
                    "scroll_bar_thumb_hover": (70, 73, 76),
                },
                "settings": {
                    "back": (40, 43, 46),
                    "title": (25, 30, 35),
                    "section": (255, 255, 255),
                    "text": (220, 225, 235),
                    "title_highlight": (160, 163, 166),
                    "section_highlight": (74, 77, 80),
                    "line": (180, 180, 180),
                    "button_hover": (85, 85, 85),
                    "bar": (70, 70, 70),
                    "thumb_idle": (150, 150, 150),
                    "thumb_hover": (240, 240, 240),
                    "collapse_idle": (221, 221, 221),
                    "collapse_hover": (160, 160, 160),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                    "scroll_bar_back": (37, 40, 43),
                    "scroll_bar_thumb_idle": (55, 58, 61),
                    "scroll_bar_thumb_hover": (62, 65, 68),
                },
                "turtle": {
                    "back": (35, 37, 40)
                },
            },

            "light": {
                "toolbar": {
                    "back": (200, 200, 200), 
                    "text": (30, 30, 30),
                    "text_hover": (0, 0, 0),
                    "line": (35, 35, 35),
                    "button_idle": (225, 225, 225),
                    "button_hover": (180, 180, 180),
                },
                "text_menu": {
                    "back": (255, 255, 255),
                    "text": (0, 0, 0),
                    "item_hover": (205, 205, 205),
                    "item_icons": (90, 90, 90),
                },
                "fractals": {
                    "back": (230, 230, 230), 
                    "title": (255, 255, 255),
                    "section": (0, 0, 0),
                    "text": (17, 17, 17), 
                    "title_highlight": (45, 45, 45),
                    "section_highlight": (165, 165, 165),
                    "line": (75, 75, 75),
                    "selection": (40, 60, 255),
                    "button_hover": (190, 190, 190),
                    "collapse_idle": (17, 17, 17),
                    "collapse_hover": (100, 100, 100),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                    "scroll_bar_back": (240, 240, 240),
                    "scroll_bar_thumb_idle": (170, 170, 170),
                    "scroll_bar_thumb_hover": (155, 155, 155),
                },
                "settings": {
                    "back": (235, 235, 235), 
                    "title": (255, 255, 255),
                    "section": (0, 0, 0),
                    "text": (26, 26, 26),
                    "title_highlight": (55, 55, 55),
                    "section_highlight": (175, 175, 175),
                    "line": (75, 75, 75),
                    "button_hover": (195, 195, 195),
                    "bar": (150, 150, 150),
                    "thumb_idle": (105, 105, 105),
                    "thumb_hover": (60, 60, 60),
                    "collapse_idle": (26, 26, 26),
                    "collapse_hover": (110, 110, 110),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                    "scroll_bar_back": (245, 245, 245),
                    "scroll_bar_thumb_idle": (175, 175, 175),
                    "scroll_bar_thumb_hover": (160, 160, 160),
                },
                "turtle": {
                    "back": (255, 255, 255)
                },
            }
        }

        """fonts"""
        self.fonts_paths = {
            "default": "assets/fonts/default.ttf"
        }

        """variables utiles aux fonctions d'obtention"""
        # décalage d'ancre
        self.anchors_offsets = {
            "topleft": (0, 0),
            "midtop": (-0.5, 0),
            "topright": (-1, 0),
            "midright": (-1, -0.5),
            "bottomright": (-1, -1),
            "midbottom": (-0.5, -1),
            "bottomleft": (0, -1),
            "midleft": (0, -0.5),
            "center": (-0.5, -0.5),
        }

        """variables utiles aux éléments pygame"""
        # boutton de repli
        self.collapse_button_settings = {
            "width": 13, # largeur
            "height": 120, # hauteur
        }

        # barre de défilement
        self.scroll_bar_settings = {
            "width": 15, # épaisseur par défaut
            "alpha_duration_in": 0.4, # durée du fade in
            "alpha_duration_out": 1, # durée du fade out
        }

        # menu textuel
        self.text_menu_settings = {
            "general": {
                "surface_width": 260, # largeur
                "surface_height_max": 800, # hauteur max
                "item_height": 26, # hauteur des items
                "item_fontsize": 15, # taille de la police du texte des items
                "item_text_x_offset": 40, # décalage du texte horizontalement
                "item_back_offset": 4, # padding des items au menu
            },
            "normal": {},
            "toggle": {},
            "choices": {},
            "value": {},
        }

            # auto adressage des fonctions utiles
        for item_type in self.text_menu_settings:
            if item_type != "general":
                self.text_menu_settings[item_type]["generate"] = getattr(self, f"generate_text_menu_item_{item_type}") # auto adressage de la fonction générative
                self.text_menu_settings[item_type]["update"] = getattr(self, f"update_text_menu_item_{item_type}") # auto adressage de la fonction de mise à jour

            # stockage des valeurs
        self.text_menus_items_values = {
            "theme": [False, "dark"]
        }

        """variables générales"""
        self.mouse_hover = None # boutton survolé (tuple(category, name))
        self.mouse_grabbing = None # barre attrapée (tuple(category, name))
        
        """handlers (on y stock des fonctions événements)"""
        self.handlers = {"toolbar": {}, "fractals": {}, "settings": {}}

# _________________________- Prédicats -_________________________
    def is_mouse_hover(self, rect: pygame.Rect, surface_rect: pygame.Rect, mutiple: list=[]) -> bool:
        """vérifie si le curseur se trouve sur le rect donné"""
        if self.main.mouse_out: # curseur en dehors de l'écran
            return False
        return rect.collidepoint(self.main.get_relative_pos(surface_rect, mutiple=mutiple))
    
    def is_mouse_hovering(self, category: str, name: str, _id: str="") -> bool:
        """vérifie si le boutton est survolé"""
        if self.mouse_hover is None:
            return False
        elif _id == "":
            return self.mouse_hover[0] == category and self.mouse_hover[1] == name
        return self.mouse_hover == (category, name, _id, name)
    
    def is_mouse_grabbing(self, category: str, name: str, _id: str="") -> bool:
        """vérifie si la barre est attrapée"""
        if self.mouse_grabbing is None:
            return False
        elif _id == "":
            return self.mouse_grabbing[0] == category and self.mouse_grabbing[1] == name
        return self.mouse_grabbing == (category, name, _id)
    
# _________________________- recherches de données -_________________________
    def get_item_value(self, name: str) -> all:
        """renvoie la valeur d'un item"""
        if name in self.text_menus_items_values:
            return self.text_menus_items_values[name][1]
        else:
            print(f"[UIManager] Error: not found {name} item_value")

    def get_color(self, category: str, name: str) -> tuple:
        """renvoie la couleur d'un élément selon le thème choisit"""
        try:
            print(self.text_menus_items_values)
            return self.themes[self.get_item_value("theme")][category][name]
        except Exception as e:
            print(f"[UI_Manager] Get_color error : {e}")
    
    def get_anchor_pos(self, x: int, y: int, width: int, height: int, anchor: str) -> tuple:
        """renvoie la position de l'angle haut gauche d'un élément en fonction de son point d'ancrage"""
        return x + width * self.anchors_offsets.get(anchor, (0, 0))[0], y + height * self.anchors_offsets.get(anchor, (0, 0))[1]
    
    def get_ease_in(self, progression: float, intensity: int=1) -> float:
        """Progression : commence lentement -> finit vite"""
        return min(max(progression**(1 + intensity), 0), 1)

    def get_ease_out(self, progression: float, intensity: int=1) -> float:
        """Progression : commence vite -> finit lentement"""
        return min(max(1 - (1 - progression)**(1 + intensity), 0), 1)

    def get_ease_in_out(self, progression: float, intensity: int=1) -> float:
        """Progression : commence lentement -> progresse vite -> finit lentement"""
        if progression < 0.5: # première moitié
            return 0.5 * (2 * progression) ** (1 + intensity)
        else: # seconde moitié
            return 1 - 0.5 * (2 * (1 - progression)) ** (1 + intensity)
        
    def get_ease_in_out_inverted(self, progression: float, intensity: int=1) -> float:
        """Progression : commence lentement -> progresse vite -> finit lentement"""
        if progression < 0.5: # première moitié
            return 1 - 0.5 * (2 * (1 - progression)) ** (1 + intensity)
        else: # seconde moitié
            return 0.5 * (2 * progression) ** (1 + intensity)

# _________________________- Demandes dynamiques -_________________________
    def ask_for_mouse_hover(self, category: str, name: str, _id: str="") -> bool:
        """assigne is possible le mouse_hover au boutton passé"""
        if self.mouse_grabbing is None:
            self.mouse_hover = (category, name, _id)
            return True
        return False
    
    def ask_for_mouse_grabbing(self, category: str, name: str, _id: str="") -> bool:
        """assigne is possible le mouse_grabbing à la barre passée"""
        self.mouse_grabbing = (category, name, _id)
        self.mouse_hover = None # annulation du mouse_hover
        return True

    def add_handler(self, category: str, name: str, handler: callable):
        """ajoute un événement à un boutton"""
        self.handlers[category][name] = handler
    
    def do_handler(self, category: str, name: str, **kwargs):
        """éxécute un événement"""
        return self.handlers.get(category, {}).get(name, lambda: None)(**kwargs)

# _________________________- Création d'éléments -_________________________
    def generate_text(self, content: str, fontsize: int, wlimit: int=0, font="default", color: tuple=(0, 0, 0), end="" , recursive=False):
        """génère un texte pygame"""
        if recursive: # si appel récursif
            content += "."
        content += end # fin définie            

        font = pygame.font.Font(self.fonts_paths.get(font, self.fonts_paths["default"]), fontsize)
        text = font.render(content, 1, color)
        text_rect = text.get_rect()

        # vérification de la taille limite
        if wlimit > 0 and text_rect.width > wlimit and len(content) > 3 + len(end):
            text, text_rect = self.generate_text(content[:len(content)-len(end)-(2 if recursive else 1)], fontsize, wlimit=wlimit, font=font, color=color, end=end, recursive=True)
        
        return text, text_rect
    
    def generate_image(self, path: str, width: int=0, height: int=0, smoothscale=True):
        """génère une image pygame"""
        # chargement de l'image
        try:
            image = pygame.image.load(self.main.get_path(f"assets/{path}.xcf"))
        except Exception as _:
            print(f"[UIManager] Error : unable to load image assets/{path}.xcf")
            image = pygame.image.load(self.main.get_path(f"assets/default_image.xcf"))
        image_rect = image.get_rect()

        # modification potentielle de l'image
        if width != 0 or height != 0:
            if smoothscale:
                image = pygame.transform.smoothscale(image, (width if width != 0 else image_rect.width, height if height != 0 else image_rect.height))
            else:
                image = pygame.transform.scale(image, (width if width != 0 else image_rect.width, height if height != 0 else image_rect.height))
            image_rect = image.get_rect()

        return image, image_rect

    def generate_collapse_button(self, side: str, x: int, y: int, anchor: bool="topleft") -> dict:
        """génère un boutton de repli pour les overlays"""
        settings = self.collapse_button_settings # raccourci

        # si les coordonnées données ne sont pas le coin haut
        if anchor != "topleft": 
            topleft_pos = self.get_anchor_pos(x, y, settings["width"], settings["height"], anchor)
            return self.generate_collapse_button(side, topleft_pos[0], topleft_pos[1])
        
        # arrière
        back = pygame.Rect(0, 0, settings["width"], settings["height"])
        back.topleft = (x, y)

        # logo
        opposite_side = "left" if side == "right" else "right"
        points = {
            "left": [(back.right - 4, back.centery - 6), (back.left + 3, back.centery), (back.right - 4, back.centery + 6)], # triangle vers la gauche
            "right": [(back.left + 4, back.centery - 6), (back.right - 3, back.centery), (back.left + 4, back.centery + 6)], # triangle vers la droite
        }

        return {"back": back, "opened_points": points[side], "closed_points": points[opposite_side]}
    
    def generate_scroll_bar(self, rect: pygame.Rect, ratio: float, y_offset_start: int=0, y_offset_end: int=0, width: int=0, side: str="right", back=True, hidden=False) -> dict:
        """génère une barre de défilement"""
        scroll_bar = {} # dictionnaire final
        height = rect.height - y_offset_start - y_offset_end
        if width == 0:
            width = self.scroll_bar_settings["width"]

        # création de la barre
        scroll_bar["bar"] = pygame.Surface((width, height)) # slider
        scroll_bar["bar_rect"] = scroll_bar["bar"].get_rect() # rect du slider

        # création du slider
        scroll_bar["thumb"] = pygame.Surface((width, height * min(ratio, 1))) # slider
        scroll_bar["thumb_rect"] = scroll_bar["thumb"].get_rect() # rect du slider

        # positionnement
        if side == "right": # coté droit
            scroll_bar["bar_rect"].topright = (rect.width, y_offset_start)
        else: # coté gauche
            scroll_bar["bar_rect"].topleft = (0, y_offset_start)
        scroll_bar["thumb_rect"].midtop = scroll_bar["bar_rect"].midtop

        # variables utiles
        scroll_bar["back"] = back # affichage de la barre complète
        scroll_bar["hidden"] = hidden # slider avec opacité variable
        scroll_bar["alpha"] = 0 if hidden else 255 # opacité
        scroll_bar["alpha_progression"] = 0 if hidden else 1 # progression des variations d'opacité
        scroll_bar["delta"] = 0 # décalage entre la souris et le slider au moment du grab
        scroll_bar["y_dif"] = 0 # offset réel du contenu
        scroll_bar["ratio"] = min(ratio, 1) # ratio entre les hauteurs absolues et relatives

        return scroll_bar
    
    def generate_section_title(self, description: str, x: int, y: int, width: int, height: int, menu: str="settings") -> dict:
        """génère un titre de section"""
        package = {} # dictionnaire final
        
        # fond
        package["back"] = pygame.Rect(x, y, width, height)
        package["back_y_init"] = package["back"].y

        # texte
        package["text"], package["text_rect"] = self.generate_text(description, int(height*0.68), color=self.get_color(menu, "section"), wlimit=width*0.8)
        package["text_rect"].midleft = (package["back"].left + width * 0.03, package["back"].centery)
        package["text_y_init"] = package["text_rect"].y

        return package
    
    def generate_text_menu(self, content: dict, x: int, y: int) -> dict:
        """génère un menu textuel"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["general"] # raccourci

        # surface
        package["surface"] = pygame.Surface((parameters["surface_width"], parameters["surface_height_max"]), pygame.SRCALPHA)
        package["surface_rect"] = package["surface"].get_rect(topleft=(x, y))

        # génération des éléments
        i_save = 0
        for i, (item_name, item_value) in enumerate(content.items()):
            package[item_name] = self.generate_text_menu_item(item_value, package["surface_rect"], parameters["item_back_offset"] + i * parameters["item_height"])
            i_save = i
        
        # clipping
        package["surface"] = pygame.transform.scale(package["surface"], (parameters["surface_width"], 1 + min(parameters["surface_height_max"], parameters["item_back_offset"] * 2 + (i_save + 1) * parameters["item_height"])))
        package["surface_rect"] = package["surface"].get_rect(topleft=(x, y))

        return package
    
    def generate_text_menu_item(self, content: dict, surface_rect: int, y: int) -> dict:
        """génère un item de menu textuel"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["general"] # raccourci

        # fond
        package["back"] = pygame.Rect(parameters["item_back_offset"], y, parameters["surface_width"] - parameters["item_back_offset"] * 2, parameters["item_height"])

        # contenu général des items
        package["text"], package["text_rect"] = self.generate_text(content["description"], parameters["item_fontsize"], color=self.get_color("text_menu", "text"), wlimit=parameters["surface_width"] * 0.6)
        package["text_rect"].midleft = (parameters["item_text_x_offset"], package["back"].centery)

        # contenu propre à chaque type d'item
        dynamic_content = self.text_menu_settings.get(content["type"], {}).get("generate", lambda **kwargs: {})(content=content, y=y, surface_rect=surface_rect)
        for key, value in dynamic_content.items():
            package[key] = value

        # variables utiles
        package["name"] = content["name"]
        package["type"] = content["type"]

        return package
    
    def generate_text_menu_item_normal(self, **kwargs) -> dict:
        """génère un item de menu textuel de type instantanné (clique = action)"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["normal"] # raccourci

        # récupération des arguments
        content = kwargs["content"]

        # stockage du handler dans un dictionnaire général
        self.text_menus_items_values[content["name"]] = content["handler"]

        return package

    def generate_text_menu_item_toggle(self, **kwargs) -> dict:
        """génère un item de menu textuel de type alternatif (clique = changement d'état True/False)"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["toggle"] # raccourci

        # récupération des arguments
        content = kwargs["content"]

        # stockage de la valeur dans un dictionnaire général
        self.text_menus_items_values[content["name"]] = content["value"]

        return package

    def generate_text_menu_item_choices(self, **kwargs) -> dict:
        """génère un item de menu textuel de type choix (clique = Nouveau menu de choix)"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["choices"] # raccourci

        # récupération des arguments
        content = kwargs["content"]
        y = kwargs["y"]
        surface_rect = kwargs["surface_rect"]

        # création du menu de choix
        package["choices_menu"] = {}
        for choice, description in content["choices"]:
            package["choices_menu"][choice] = {"name": f"{content['name']}.{choice}", "type": "value", "description": description}
        package["choices_menu"]["package"] = self.generate_text_menu(package["choices_menu"], surface_rect.right, surface_rect.top + y - self.text_menu_settings["general"]["item_back_offset"])

        # stockage de l'état (menu de choix : ouvert/fermé) et de la valeur par défaut dans un dictionnaire général
        self.text_menus_items_values[content["name"]] = [False, content["value"]]

        return package
    
    def generate_text_menu_item_value(self, **kwargs) -> dict:
        """génère un item de menu textuel de type choix (clique = Nouveau menu de choix)"""
        package = {} # dictionnaire final
        parameters = self.text_menu_settings["value"] # raccourci

        # récupération des arguments
        content = kwargs["content"]

        return package

# _________________________- Mise à jour d'éléments -_________________________
    def update_collapse_button(self, category: str, surface: pygame.Surface, surface_rect: pygame.Rect, button: dict, opened: bool=True):
        """mise à jour des bouttons de repli"""
        # boutton survolé
        if button["back"].collidepoint(self.main.get_relative_pos(surface_rect)):
            hovered = self.ask_for_mouse_hover(category, "collapse_button")
        else:
            hovered = False
        # fond
        pygame.draw.rect(surface, self.get_color(category, ("collapse_hover" if hovered else "collapse_idle")), button["back"])
        # logo
        pygame.draw.polygon(surface, self.get_color(category, "collapse_logo_hover" if hovered else "collapse_logo_idle"), button[f"{'opened' if opened else 'closed'}_points"])
    
    def update_scroll_bar(self, scroll_bar: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="settings", ratio: float=0):
        """mise à jour des barres de défilement"""
        is_grabbed = self.is_mouse_grabbing(menu, "scroll_bar") # vérification que la barre est attrapée

        # barre complète
        if scroll_bar["back"]:
            scroll_bar["bar"].fill(self.get_color(menu, "scroll_bar_back"))
            surface.blit(scroll_bar["bar"], scroll_bar["bar_rect"])

        # slider (taille)
        if ratio != 0 and ratio != scroll_bar["ratio"]:
            scroll_bar["ratio"] = min(ratio, 1)
            scroll_bar["thumb"] = pygame.transform.scale(scroll_bar["thumb"], (scroll_bar["thumb_rect"].width, scroll_bar["ratio"] * scroll_bar["bar_rect"].height))
            scroll_bar["thumb_rect"] = scroll_bar["thumb"].get_rect(midtop=scroll_bar["thumb_rect"].midtop)

        # slider (hoover)
        if self.is_mouse_hover(scroll_bar["thumb_rect"], surface_rect):
            is_hovered = self.ask_for_mouse_hover(menu, "scroll_bar")
        else:
            is_hovered = False
        
        # slider (grab)
        if is_grabbed:
            top_limit = scroll_bar["bar_rect"].top + scroll_bar["thumb_rect"].height / 2 # limite supérieure du slider
            bottom_limit = scroll_bar["bar_rect"].bottom - scroll_bar["thumb_rect"].height / 2 # limite inférieure du slider

            # suivi du curseur - delta (ancre de saisi)
            scroll_bar["thumb_rect"].centery = min(max(self.main.get_relative_pos(surface_rect)[1] - scroll_bar.get("delta", 0), top_limit), bottom_limit)

            # progression dans la barre
            progression = min(max((scroll_bar["thumb_rect"].centery - top_limit) / max(bottom_limit - top_limit, 10**-9), 0), 1)

            # offset vertical réel
            scroll_bar["y_dif"] = int(progression * (scroll_bar["bar_rect"].height / scroll_bar["ratio"] - scroll_bar["bar_rect"].height))
        
        # slider (visuel)
        scroll_bar["thumb"].fill(self.get_color(menu, f"scroll_bar_thumb_{'hover' if is_hovered or is_grabbed else 'idle'}"))
        if scroll_bar["hidden"]:
            # progression alpha entre 0 et 1
            if is_grabbed or surface_rect.collidepoint((self.main.mouse_x, self.main.mouse_y)): # fade in
                scroll_bar["alpha_progression"] = min(scroll_bar["alpha_progression"] + self.main.dt / self.scroll_bar_settings["alpha_duration_in"], 1)
            else: # fade out
                scroll_bar["alpha_progression"] = max(scroll_bar["alpha_progression"] - self.main.dt / self.scroll_bar_settings["alpha_duration_out"], 0)

            # easing
            eased = self.get_ease_in_out(scroll_bar["alpha_progression"], intensity=2)
            scroll_bar["alpha"] = int(255 * eased)

            scroll_bar["thumb"].set_alpha(scroll_bar["alpha"])

        # slider (affichage)
        surface.blit(scroll_bar["thumb"], scroll_bar["thumb_rect"])

    def update_section_title(self, content: dict, surface: pygame.Surface, y_offset: int=0, menu="settings"):
        """mise à jour des titres de section"""
        package = content["package"] # raccourci

        # défilement
        package["back"].y = package["back_y_init"] - y_offset
        package["text_rect"].y = package["text_y_init"] - y_offset

        # affichage
        pygame.draw.rect(surface, self.get_color(menu, "section_highlight"), package["back"])
        surface.blit(package["text"], package["text_rect"])

    def update_text_menu(self, content: dict, surface: pygame.Surface, menu: str="toolbar"):
        """met à jour un menu textuel"""
        package = content["package"] # raccourci

        # reset du fond avec border radius
        pygame.draw.rect(package["surface"], self.get_color("text_menu", "back"), package["surface"].get_rect(), border_radius=7)

        # mise à jour des items
        for item in package.values():
            if type(item) == dict: # skip de surface et surface_rect
                self.update_text_menu_item(item, package["surface"], package["surface_rect"], menu=menu)

        # affichage
        surface.blit(package["surface"], package["surface_rect"])
    
    def update_text_menu_item(self, content: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="toolbar"):
        "met à jour un item de menu textuel"
        parameters = self.text_menu_settings["general"] # raccourci

        # item survolé
        if self.is_mouse_hover(content["back"], surface_rect):
            hovered = self.ask_for_mouse_hover(menu, "text_menu_item", _id=f"{content['type']}.{content['name']}")
        else:
            hovered = False

        # contenu propre au type
        self.text_menu_settings.get(content["type"], {}).get("update", lambda a, b, c, d, e: None)(content, surface, surface_rect, menu=menu, hovered=hovered)

        # texte
        surface.blit(content["text"], content["text_rect"])
    
    def update_text_menu_item_normal(self, content: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="toolbar", hovered: bool=False):
        "met à jour un item de menu textuel de type normal"
        # affichage du fond
        if hovered:
            pygame.draw.rect(surface, self.get_color("text_menu", "item_hover"), content["back"], border_radius=7)
    
    def update_text_menu_item_toggle(self, content: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="toolbar", hovered: bool=False):
        "met à jour un item de menu textuel de type alternatif"
        # affichage du fond
        if hovered:
            pygame.draw.rect(surface, self.get_color("text_menu", "item_hover"), content["back"], border_radius=7)
    
    def update_text_menu_item_choices(self, content: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="toolbar", hovered: bool=False):
        "met à jour un item de menu textuel de type choix"
        # affichage du fond
        if hovered:
            pygame.draw.rect(surface, self.get_color("text_menu", "item_hover"), content["back"], border_radius=7)
        
        # affichage du menu de choix si menu ouvert
        if self.text_menus_items_values[content["name"]][0]:
            self.update_text_menu(content["choices_menu"], self.main.screen, menu=menu)
    
    def update_text_menu_item_value(self, content: dict, surface: pygame.Surface, surface_rect: pygame.Rect, menu: str="toolbar", hovered: bool=False):
        "met à jour un item de menu textuel de type valeur"
        # affichage du fond
        if hovered:
            pygame.draw.rect(surface, self.get_color("text_menu", "item_hover"), content["back"], border_radius=7)

# _________________________- Handlers -_________________________
    def handle_down_scroll_bar(self):
        """événement: attrape une barre de défilement"""
        menu = self.mouse_hover[0]
        _id = self.mouse_hover[2] # récupération de l'id
        is_grabbed = self.ask_for_mouse_grabbing(menu, "scroll_bar", _id=_id)
        if is_grabbed:
            self.main.menus[menu].scroll_bar["delta"] = self.main.get_relative_pos(self.main.menus[menu].surface_rect)[1] - self.main.menus[menu].scroll_bar["thumb_rect"].centery
    
    def handle_mousewheel_scroll_bar(self, scroll_bar: dict, y_offset):
        """événement: utilise la barre de défilement par molette"""
        top_limit = scroll_bar["bar_rect"].top + scroll_bar["thumb_rect"].height / 2 # limite supérieure du slider
        bottom_limit = scroll_bar["bar_rect"].bottom - scroll_bar["thumb_rect"].height / 2 # limite inférieure du slider

        # suivi du curseur - delta (ancre de saisi)
        scroll_bar["thumb_rect"].centery = min(max(scroll_bar["thumb_rect"].centery + y_offset * scroll_bar["bar_rect"].height * 0.03, top_limit), bottom_limit)

        # progression dans la barre
        progression = min(max((scroll_bar["thumb_rect"].centery - top_limit) / max(bottom_limit - top_limit, 10**-9), 0), 1)

        # offset vertical réel
        scroll_bar["y_dif"] = int(progression * (scroll_bar["bar_rect"].height / scroll_bar["ratio"] - scroll_bar["bar_rect"].height))
    
    def handle_down_text_menu_item(self):
        """événement: clic sur un item de menu textuel"""
        funct_name = f"handle_down_text_menu_item_{self.mouse_hover[2].split('.')[0]}" # récupération de l'adresse de fonction
        func = getattr(self, funct_name, None) # auto redirection vers la fonction associée
        if func: # si la fonction existe
            func(self.mouse_hover[2].split(".")[1]) # récupération du nom de l'item et éxécution du handler associé
        else: # fonction introuvable
            print(f"[UIManager] Error : not found {funct_name}")
    
    def handle_down_text_menu_item_normal(self, item_name: str):
        """événement: clique sur un item de menu textuel de type normal"""
        self.text_menus_items_values[item_name]() # éxécution du handler associé

    def handle_down_text_menu_item_toggle(self, item_name: str):
        """événement: clique sur un item de menu textuel de type alternatif"""
        self.text_menus_items_values[item_name] = not self.text_menus_items_values[item_name] # alternance True/False

    def handle_down_text_menu_item_choices(self, item_name: str):
        """événement: clique sur un item de menu textuel de type choix"""
        self.text_menus_items_values[item_name][0] = not self.text_menus_items_values[item_name][0] # ouverture/fermeture des choix
    
    def handle_down_text_menu_item_value(self, item_name: str):
        """événement: clique sur un item de menu textuel de type choix"""
        self.text_menus_items_values[item_name][1] = self.mouse_hover[2].split(".")[2] # changement de choix
        print(self.text_menus_items_values[item_name][1])