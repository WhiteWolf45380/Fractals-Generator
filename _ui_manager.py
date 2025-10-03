import pygame


# _________________________- Manager de l'UI -_________________________
class UIManager:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.name = "ui_manager"
        
        """thèmes"""
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "toolbar": {
                    "back": (43, 43, 43), 
                    "text": (200, 200, 200),
                    "line": (220, 220, 220),
                    "button_hover": (70, 70, 70),
                },
                "fractals": {
                    "back": (51, 51, 51), 
                    "title": (0, 0, 0),
                    "text": (240, 240, 240),
                    "highlight": (190, 190, 190),
                    "line": (180, 180, 180), 
                    "selection": (20, 180, 255),
                    "button_hover": (90, 90, 90),
                    "collapse_idle": (240, 240, 240),
                    "collapse_hover": (170, 170, 170),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                    "scroll_bar_back": (31, 31, 31),
                    "scroll_bar_thumb_idle": (75, 75, 75),
                    "scroll_bar_thumb_hover": (85, 85, 85),
                },
                "settings": {
                    "back": (42, 42, 42),
                    "title": (0, 0, 0),
                    "text": (201, 201, 201),
                    "highlight": (200, 200, 200),
                    "line": (180, 180, 180),
                    "button_hover": (85, 85, 85),
                    "bar": (70, 70, 70),
                    "thumb_idle": (150, 150, 150),
                    "thumb_hover": (240, 240, 240),
                    "collapse_idle": (221, 221, 221),
                    "collapse_hover": (160, 160, 160),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                    "scroll_bar_back": (22, 22, 22),
                    "scroll_bar_thumb_idle": (65, 65, 65),
                    "scroll_bar_thumb_hover": (75, 75, 75),
                },
                "turtle": {
                    "back": (30, 30, 30)
                },
            },

            "light": {
                "toolbar": {
                    "back": (200, 200, 200), 
                    "text": (30, 30, 30),
                    "line": (35, 35, 35),
                    "button_idle": (225, 225, 225),
                    "button_hover": (180, 180, 180),
                },
                "fractals": {
                    "back": (230, 230, 230), 
                    "title": (255, 255, 255),
                    "text": (17, 17, 17), 
                    "highlight": (45, 45, 45),
                    "line": (75, 75, 75),
                    "selection": (40, 60, 255),
                    "button_hover": (190, 190, 190),
                    "collapse_idle": (17, 17, 17),
                    "collapse_hover": (100, 100, 100),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                    "scroll_bar_back": (250, 250, 250),
                    "scroll_bar_thumb_idle": (170, 170, 170),
                    "scroll_bar_thumb_hover": (155, 155, 155),
                },
                "settings": {
                    "back": (235, 235, 235), 
                    "title": (255, 255, 255),
                    "text": (26, 26, 26),
                    "highlight": (45, 45, 45),
                    "line": (75, 75, 75),
                    "button_hover": (195, 195, 195),
                    "bar": (150, 150, 150),
                    "thumb_idle": (105, 105, 105),
                    "thumb_hover": (60, 60, 60),
                    "collapse_idle": (26, 26, 26),
                    "collapse_hover": (110, 110, 110),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                    "scroll_bar_back": (255, 255, 255),
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
            "width": 13,
            "height": 120,
        }

        """variables générales"""
        self.mouse_hover = None # boutton survolé (tuple(category, name))
        self.mouse_grabbing = None # barre attrapée (tuple(category, name))
        
        """handlers (on y stock des fonctions événements)"""
        self.handlers = {"toolbar": {}, "fractals": {}, "settings": {}}

# _________________________- Prédicats -_________________________
    def is_mouse_hover(self, rect: pygame.Rect, surface_rect: pygame.Rect, mutiple: list=[]) -> bool:
        """vérifie si le curseur se trouve sur le rect donné"""
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
    def get_color(self, category: str, name: str) -> tuple:
        """renvoie la couleur d'un élément selon le thème choisit"""
        try:
            return self.themes[self.current_theme][category][name]
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
        if self.mouse_hover is None and self.mouse_grabbing is None:
            self.mouse_hover = (category, name, _id)
            return True
        return False
    
    def ask_for_mouse_grabbing(self, category: str, name: str, _id: str="") -> bool:
        """assigne is possible le mouse_grabbing à la barre passée"""
        if self.mouse_grabbing is None:
            self.mouse_grabbing = (category, name, _id)
            self.mouse_hover = None # annulation du mouse_hover
            return True
        return False

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
    
    def generate_scroll_bar(self, rect: pygame.Rect, ratio: float, y_offset_start: int=0, y_offset_end: int=0, width: int=15, side: str="right", back=False, hidden=True) -> dict:
        """génère une barre de défilement"""
        scroll_bar = {} # dictionnaire final
        height = rect.height - y_offset_start - y_offset_end

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
        scroll_bar["delta"] = 0 # décalage entre la souris et le slider au moment du grab
        scroll_bar["y_dif"] = 0 # offset réel du contenu
        scroll_bar["ratio"] = min(ratio, 1) # ratio entre les hauteurs absolues et relatives

        return scroll_bar

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
        # barre complète
        if scroll_bar["back"]:
            scroll_bar["bar"].fill(self.get_color(menu, "scroll_bar_back"))
            surface.blit(scroll_bar["bar"], scroll_bar["bar_rect"])

        # slider (taille)
        if ratio != 0:
            scroll_bar["thumb"] = pygame.transform.scale(scroll_bar["thumb"], (scroll_bar["thumb_rect"].width, ratio * scroll_bar["bar_rect"].height))
            scroll_bar["thumb_rect"] = scroll_bar["thumb"].get_rect(midtop=scroll_bar["thumb_rect"].midtop)

        # slider (hoover)
        if self.is_mouse_hover(scroll_bar["thumb_rect"], surface_rect):
            hovered = self.ask_for_mouse_hover(menu, "scroll_bar")
        else:
            hovered = False
        
        # slider (visuel)
        if scroll_bar["hidden"]:
            if surface_rect.collidepoint((self.main.mouse_x, self.main.mouse_y)):
                scroll_bar["alpha"] = 255
            else:
                scroll_bar["alpha"] = 0
            scroll_bar["thumb"].set_alpha(scroll_bar["alpha"])
        scroll_bar["thumb"].fill(self.get_color(menu, f"scroll_bar_thumb_{'hover' if hovered else 'idle'}"))

        # slider (affichage)
        surface.blit(scroll_bar["thumb"], scroll_bar["thumb_rect"])

# _________________________- Handlers -_________________________
    def handle_down_scroll_bar(self):
        """événement: attrape une barre de défilement"""
        menu = self.mouse_hover[0]
        _id = self.mouse_hover[2] # récupération de l'id
        grabbed = self.ask_for_mouse_grabbing(menu, "scroll_bar", _id=_id)
        if grabbed:
            self.main.menus[menu].scroll_bar["delta"] = self.main.get_relative_pos(self.main.menus[menu].surface_rect)[1] - self.main.menus[menu].scroll_bar["package"]["thumb_rect"].centery
