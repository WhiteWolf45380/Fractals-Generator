import pygame
import math
import traceback
from _fractals import Fractals

# _________________________- Remake de turtle -_________________________
class Turtle:
    
    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "turtle"

        """Zone d'affichage du dessin"""
        self.surface_width = self.main.screen_width # largeur du menu
        self.surface_height = self.main.screen_height - self.main.menus["toolbar"].surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(midbottom=(self.main.screen_width / 2, self.main.screen_height)) # placement en bas au centre de l'écran

        """zone de dessin"""
        self.turtle_surface_side = 5000
        self.turtle_surface = pygame.Surface((self.turtle_surface_side, self.turtle_surface_side), pygame.SRCALPHA)
        self.turtle_surface_rect = self.turtle_surface.get_rect(center=self.surface.get_rect().center)
        self.turtle_surface_x_offset = 0 # décalage de l'axe x
        self.turtle_surface_y_offset = 0 # décalage de l'axe y

        """paramètres turtle"""
        self.parameters_init = {
            "pattern": "koch_triangles", # motif
            "depth": 10, # profondeur de récursion
            "size": 100, # taille du motif
            "x_offset": 0, # décalage x
            "y_offset": 0, # décalage y
            "start_angle": 0, # angle de la figure
            "width": 1, # épaisseur
            "color_r": 255, # canal rouge
            "color_g": 255, # canal vert
            "color_b": 255, # canal bleu
            "color_a": 255, # opacité
            "filling": False, # remplissage
            "filling_r": 255, # remplissage rouge
            "filling_g": 0, # remplissage vert
            "filling_b": 0, # remplissage bleu
            "filling_a": 255, # remplissage opacité
            "centered": True, # ancre
            "speed": 5, # vitesse d'éxécution
            "x": 0, # position x (not to define)
            "y": 0, # position y (not to define)
            "angle": 0, # angle (not to define)
        }
        self.parameters = self.parameters_init.copy()

        self.speed_conversions = {
            1: 1,
            2: 5,
            3: 20,
            4: 100,
            5: 300,
            6: 1000,
            7: 1500,
            8: 2500,
            9: 5000,
            10: 10000,
        }

        """stockage des fractals"""
        self.fractals = Fractals(self)

        """générateur courant (dessin en cours)"""
        self.current_generator = None # stockage du générateur
        self.pause = False # paramètre de pause
        self.all_points = [] # stockage de tous les points du dessin pour le remplissage

    def update(self):
        """mise à jour du dessin"""
        self.surface.fill(self.ui_manager.get_color(self.name, "back"))
        if self.current_generator and not self.pause:
            try:
                for _ in range(self.get_speed()):  # nombre de segments dessinés par frame
                    next(self.current_generator)
            except StopIteration:
                self.current_generator = None
        self.surface.blit(self.turtle_surface, self.turtle_surface_rect)
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Dessin -_________________________
    def draw(self):
        """prépare un dessin progressif"""
        self.push(self.main.menus["settings"].settings)
        self.do_reset() # remise du dessin à blanc
        self.all_points = [] # reset des points de dessin
                
        try:
            self.current_generator = self.fractals.available_fractals[self.get("pattern")](self.get("size"))
        except Exception as e:
            traceback.print_exc()
            self.current_generator = None
            print(f"[Painting] Error during the drawing start")

    def get(self, parameter: str) -> int | str | tuple:
        """renvoie la valeur du paramètre demandé"""
        if parameter not in self.parameters:
            print(f"[Turtle] Error : undefined parameter : {parameter}")
            return
        return self.parameters[parameter]

    def push(self, settings_dict: dict):
        """récupère les valeurs des propriétés avant le lancement du dessin"""
        for setting in settings_dict:
            if setting in self.parameters:
                self.parameters[setting] = settings_dict[setting]["value"]

# _________________________- Outils -_________________________

    def get(self, parameter: str, multiple: tuple=None) -> str | int | tuple:
        """retourne le paramètre correspondant"""
        if multiple is not None:
            return tuple(self.parameters.get(f"{parameter}_{single}", 0) for single in multiple)
        return self.parameters.get(parameter, None)
    
    def change(self, parameter: str, value, index=None):
        """change la valeur d'un paramètre"""
        self.parameters[parameter] = value

    def get_pos(self, x: float, y: float) -> tuple:
        """obtention de la position absolue à partir de la relative"""
        return x + self.turtle_surface_side / 2, y + self.turtle_surface_side / 2
    
    def get_relative_pos(self, x: float, y: float) -> tuple:
        """obtention de la position relative à partir de l'absolue"""
        return x - self.turtle_surface_side / 2, y - self.turtle_surface_side / 2
    
    def get_speed(self) -> int:
        """obtention de la vitesse de dessin"""
        return self.speed_conversions[self.parameters["speed"]]
    
    def get_rotated_offset(self, x, y, angle_deg):
        """obtention du centrage avec angle non nul"""
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x * cos_a - y * sin_a, x * sin_a + y * cos_a

# _________________________- Turtle -_________________________

    def do_reset(self):
        """reset du tableau"""
        self.surface.fill(self.ui_manager.get_color(self.name, "back"))
        self.turtle_surface.fill((0, 0, 0, 0))
        self.do_goto(self.get("x_offset"), self.get("y_offset"))
        self.do_setheading(self.get("start_angle"))
    
    def do_goto(self, x: float, y: float, add_point=True):
        """se rend à une position"""
        self.change("x", x)
        self.change("y", y)
        if add_point:
            self.all_points.append(self.get_pos(x, y))
    
    def do_forward(self, distance: float, penup=False):
        """avance en dessinant"""
        # calcul des positions absolues initiales et finales
        x, y = self.get_pos(self.get("x"), self.get("y"))
        x_final = x + distance * math.cos(math.radians(self.get("angle")))
        y_final = y + distance * math.sin(math.radians(self.get("angle")))

        # traçage du trait
        if not penup:
            color = self.get("color", multiple=("r", "g", "b", "a"))
            width = self.get("width")
            
            if width == 1:# ligne fine
                pygame.draw.aaline(self.turtle_surface, color, (int(x), int(y)), (int(x_final), int(y_final)))
            else:# ligne épaisse
                radius = max(1, (width + 1) // 2)
                pygame.draw.line(self.turtle_surface, color, (int(x), int(y)), (int(x_final), int(y_final)), width)
                pygame.draw.circle(self.turtle_surface, color, (int(x), int(y)), radius)
                pygame.draw.circle(self.turtle_surface, color, (int(x_final), int(y_final)), radius)
            
            # ajout du point final
            self.all_points.append((x_final, y_final))

        # mise à jour de la position
        x_rel, y_rel = self.get_relative_pos(x_final, y_final)
        self.change("x", x_rel)
        self.change("y", y_rel)
    
    def do_setheading(self, angle: int):
        """fixe l'angle"""
        self.parameters["angle"] = angle % 360
    
    def do_left(self, angle: int):
        """tourne à gauche"""
        self.parameters["angle"] = (self.parameters["angle"] - angle) % 360

    def do_right(self, angle: int):
        """tourne à droite"""
        self.parameters["angle"] = (self.parameters["angle"] + angle) % 360
    
    def do_pause(self):
        """met pause si un dessin est en cours"""
        if self.current_generator is not None:
            self.pause = True
    
    def do_unpause(self):
        """reprends le dessin"""
        self.pause = False