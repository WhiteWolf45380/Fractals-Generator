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
        self.surface_height = self.main.screen_height - self.main.tools_bar.surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(midbottom=(self.main.screen_width / 2, self.main.screen_height))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        """zone de dessin"""
        self.turtle_surface_side = self.main.screen_width * 2
        self.turtle_surface = pygame.Surface((self.turtle_surface_side, self.turtle_surface_side), pygame.SRCALPHA)
        self.turtle_surface_rect = self.turtle_surface.get_rect(center=self.surface_rect.center)
        self.turtle_surface_x_offset = 0 # décalage de l'axe x
        self.turtle_surface_y_offset = 0 # décalage de l'axe y

        """paramètres turtle"""
        self.parameters_init = {
            "x": 0,
            "y": 0,
            "angle": 0,
            "color": (0, 0, 0),
            "width": 1,
            "speed": 9,
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
        }

        """stockage des fractals"""
        self.fractals = Fractals(self)

        """générateur courant (dessin en cours)"""
        self.current_generator = None

    def update(self):
        """mise à jour du dessin"""
        self.surface.fill(self.surface_color)
        if self.current_generator:
            try:
                for _ in range(self.get_speed()):  # nombre de segments dessinés par frame
                    next(self.current_generator)
            except StopIteration:
                self.current_generator = None
        
        self.surface.blit(self.turtle_surface, self.turtle_surface_rect)
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Dessin -_________________________
    def draw(self, name: str, size: int, **kwargs):
        """prépare un dessin progressif"""
        self.do_reset()

        self.change("color", kwargs.get("color", self.get("color")))
                
        try:
            self.current_generator = self.fractals.available_fractals[name](size, **kwargs)
        except Exception as e:
            traceback.print_exc()
            self.current_generator = None
            print(f"[Painting] Error during the drawing start")

# _________________________- Outils -_________________________

    def get(self, parameter: str):
        """retourne le paramètre correspondant"""
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

# _________________________- Turtle -_________________________

    def do_reset(self):
        """reset du tableau"""
        self.surface.fill(self.surface_color)
        self.turtle_surface.fill((0, 0, 0, 0))
        self.do_goto(0, 0)
        self.do_setheading(0)
    
    def do_goto(self, x: float, y: float):
        """se rend à une position"""
        self.change("x", x)
        self.change("y", y)
    
    def do_forward(self, distance: float, penup=False):
        """avance en dessinant"""
        # calcul des positions absolues initiales et finales
        x, y = self.get_pos(self.get("x"), self.get("y"))
        x_final = x + distance * math.cos(math.radians(self.get("angle")))
        y_final = y + distance * math.sin(math.radians(self.get("angle")))

        # traçage du trait
        if not penup:
            pygame.draw.line(self.turtle_surface, self.get("color"), (int(x), int(y)), (int(x_final), int(y_final)), width=self.get("width"),)

        # mise à jour de la position
        x, y = self.get_relative_pos(x_final, y_final)
        self.change("x", x)
        self.change("y", y)
    
    def do_setheading(self, angle: int):
        """fixe l'angle"""
        self.parameters["angle"] = angle % 360
    
    def do_left(self, angle: int):
        """tourne à gauche"""
        self.parameters["angle"] = (self.parameters["angle"] - angle) % 360

    def do_right(self, angle: int):
        """tourne à droite"""
        self.parameters["angle"] = (self.parameters["angle"] + angle) % 360