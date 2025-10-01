import pygame


# _________________________- Manager de l'UI -_________________________
class UIManager:

    def __init__(self, main):
        """formalités"""
        self.main = main
        
        """thèmes"""
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "toolbar": {
                    "back": (43, 43, 43), 
                    "text": (200, 200, 200),
                    "line": (220, 220, 220),
                    "button_idle": (55, 55, 55),
                    "button_hover": (70, 70, 70),
                },
                "fractals": {
                    "back": (51, 51, 51), 
                    "title": (255, 255, 255),
                    "text": (240, 240, 240),
                    "highlight": (81, 81, 81),
                    "line": (180, 180, 180), 
                    "button_idle": (60, 60, 60),
                    "button_hover": (90, 90, 90),
                    "collapse_idle": (240, 240, 240),
                    "collapse_hover": (170, 170, 170),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                },
                "settings": {
                    "back": (42, 42, 42),
                    "title": (236, 236, 236),
                    "text": (221, 221, 221),
                    "highlight": (72, 72, 72),
                    "line": (180, 180, 180),
                    "button_idle": (55, 55, 55),
                    "button_hover": (85, 85, 85),
                    "collapse_idle": (221, 221, 221),
                    "collapse_hover": (160, 160, 160),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                },
                "turtle": {
                    "back": (30, 30, 30)
                },
            },

            "light": {
                "toolbar": {
                    "back": (240, 240, 240), 
                    "text": (30, 30, 30),
                    "line": (35, 35, 35),
                    "button_idle": (225, 225, 225),
                    "button_hover": (200, 200, 200),
                },
                "fractals": {
                    "back": (230, 230, 230), 
                    "title": (7, 7, 7),
                    "text": (17, 17, 17), 
                    "highlight": (200, 200, 200),
                    "line": (75, 75, 75),
                    "button_idle": (215, 215, 215),
                    "button_hover": (190, 190, 190),
                    "collapse_idle": (17, 17, 17),
                    "collapse_hover": (100, 100, 100),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                },
                "settings": {
                    "back": (235, 235, 235), 
                    "title": (16, 16, 16),
                    "text": (26, 26, 26),
                    "highlight": (205, 205, 205),
                    "line": (75, 75, 75),
                    "button_idle": (220, 220, 220),
                    "button_hover": (195, 195, 195),
                    "collapse_idle": (26, 26, 26),
                    "collapse_hover": (110, 110, 110),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
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
        
        """handles (on y stock des fonctions évènements)"""
        self.handles = {"toolbar": {}, "fractals": {}, "settings": {}}
    
# _________________________- Obtention d'informations -_________________________
    def get_color(self, category: str, name: str) -> tuple:
        """renvoie la couleur d'un élément selon le thème choisit"""
        try:
            return self.themes[self.current_theme][category][name]
        except Exception as e:
            print(f"[UI_Manager] Get_color error : {e}")
    
    def get_anchor_pos(self, x: int, y: int, width: int, height: int, anchor: str) -> tuple:
        """renvoie la position de l'angle haut gauche d'un élément en fonction de son point d'ancrage"""
        return x + width * self.anchors_offsets.get(anchor, (0, 0))[0], y + height * self.anchors_offsets.get(anchor, (0, 0))[1]
    
    def is_mouse_hover(self, rect: pygame.Rect, surface_rect: pygame.Rect) -> bool:
        """vérifie si le curseur se trouve sur le rect donné"""
        return rect.collidepoint(self.main.get_relative_pos(surface_rect))
    
# _________________________- Demandes dynamiques -_________________________
    def ask_for_mouse_hover(self, category: str, name: str) -> bool:
        """assigne is possible le mouse_hover au boutton passé"""
        if self.mouse_hover is None:
            self.mouse_hover = (category, name)
            return True
        return False

    def add_handle(self, category: str, name: str, handle: callable):
        """ajoute un évènement à un boutton"""
        self.handles[category][name] = handle
    
    def do_handle(self, category: str, name: str, **kwargs):
        """éxécute un évènement"""
        return self.handles.get(category, {}).get(name, lambda: None)(**kwargs)

# _________________________- Création d'éléments -_________________________
    def generate_text(self, content: str, fontsize: int, wlimit: int=0, font="default", color: tuple=(0, 0, 0), recursive=False):
        """génère un texte pygame"""
        if recursive: # si appel récursif
            content += "."

        font = pygame.font.Font(self.fonts_paths.get(font, self.fonts_paths["default"]), fontsize)
        text = font.render(content, 1, color)
        text_rect = text.get_rect()

        # vérification de la taille limite
        if wlimit > 0 and text_rect.width > wlimit and len(content > 3):
            text, text_rect = self.generate_text(content[:len(content)-(1 if not recursive else 2)], fontsize, wlimit=wlimit, font=font, color=color)
        
        return text, text_rect

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

# _________________________- Mise à jour d'éléments -_________________________
    def update_collapse_button(self, category: str, surface: pygame.Surface, surface_rect: pygame.Rect, button: dict, opened: bool=True):
        """mise à jour des bouttons de repli"""
        # -- boutton survolé
        if button["back"].collidepoint(self.main.get_relative_pos(surface_rect)):
            hovered = self.ask_for_mouse_hover(category, "collapse_button")
        else:
            hovered = False
        # -- fond
        pygame.draw.rect(surface, self.get_color(category, ("collapse_hover" if hovered else "collapse_idle")), button["back"])
        # -- logo
        pygame.draw.polygon(surface, self.get_color(category, "collapse_logo_hover" if hovered else "collapse_logo_idle"), button[f"{'opened' if opened else 'closed'}_points"])