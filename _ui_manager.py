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
                "tools_bar": {
                    "back": (43, 43, 43), 
                    "text": (224, 224, 224),
                    "line": (220, 220, 220),
                    "button_idle": (55, 55, 55),
                    "button_hover": (70, 70, 70),
                },
                "fractals_menu": {
                    "back": (51, 51, 51), 
                    "text": (240, 240, 240),
                    "line": (180, 180, 180), 
                    "button_idle": (60, 60, 60),
                    "button_hover": (90, 90, 90),
                    "collapse_idle": (240, 240, 240),
                    "collapse_hover": (170, 170, 170),
                    "collapse_logo_idle": (10, 10, 10),
                    "collapse_logo_hover": (240, 240, 240),
                },
                "settings_menu": {
                    "back": (42, 42, 42), 
                    "text": (221, 221, 221),
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
                "tools_bar": {
                    "back": (240, 240, 240), 
                    "text": (34, 34, 34),
                    "line": (35, 35, 35),
                    "button_idle": (225, 225, 225),
                    "button_hover": (200, 200, 200),
                },
                "fractals_menu": {
                    "back": (230, 230, 230), 
                    "text": (17, 17, 17), 
                    "line": (75, 75, 75),
                    "button_idle": (215, 215, 215),
                    "button_hover": (190, 190, 190),
                    "collapse_idle": (17, 17, 17),
                    "collapse_hover": (100, 100, 100),
                    "collapse_logo_idle": (240, 240, 240),
                    "collapse_logo_hover": (10, 10, 10),
                },
                "settings_menu": {
                    "back": (235, 235, 235), 
                    "text": (26, 26, 26),
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
    
# _________________________- Obtention d'informations -_________________________
    def get_color(self, category: str, name: str) -> tuple:
        """renvoie la couleur d'un élément selon le thème choisit"""
        try:
            return self.themes[self.current_theme][category][name]
        except Exception as e:
            print(f"[UI_Manager] Get_color error : {e}")
    
    def get_anchor_pos(self, x: int, y: int, width: int, height: int, anchor: str) -> tuple:
        """renvoie la position de l'angle haut gauche d'un élément"""
        return x + width * self.anchors_offsets.get(anchor, (0, 0))[0], y + height * self.anchors_offsets.get(anchor, (0, 0))[1]
    
# _________________________- Demandes dynamiques -_________________________
    def ask_for_following(self, category: str, name: str) -> bool:
        """assigne is possible le mouse_hover au boutton passé"""
        if self.mouse_hover is None:
            self.mouse_hover = (category, name)
            return True
        return False

# _________________________- Création d'éléments -_________________________
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

        return {"state": "opened", "back": back, "opened_points": points[side], "closed_points": points[opposite_side]}

# _________________________- Mise à jour d'éléments -_________________________
    def update_collapse_button(self, category: str, surface: pygame.Surface, surface_rect: pygame.Rect, button: dict):
        """mise à jour des bouttons de repli"""
        # -- boutton survolé
        if button["back"].collidepoint(self.main.get_relative_pos(surface_rect)):
            self.ask_for_following(category, "collapse_button")
            hovered =  self.mouse_hover == (category, "collapse_button")
        else:
            hovered = False
        # -- fond
        pygame.draw.rect(surface, self.get_color(category, ("collapse_hover" if hovered else "collapse_idle")), button["back"])
        # -- logo
        pygame.draw.polygon(surface, self.get_color(category, "collapse_logo_hover" if hovered else "collapse_logo_idle"), button[f"{button['state']}_points"])