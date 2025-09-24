import pygame
import math
import traceback

# _________________________- Painting -_________________________
class Painting:
    
    def __init__(self, main):
        """passerelles"""
        self.main = main

        """pygame"""
        # tableau
        self.surface_side = self.main.screen_width * 2 // 3
        self.surface = pygame.Surface((self.surface_side, self.surface_side))
        self.surface.fill((255, 255, 255))
        self.surface_rect = (0, (self.main.screen_height - self.surface_side) // 2)

        """turtle remake"""
        # paramètres de la tortue
        self.parameters_init = {
            "x": 0,
            "y": 0,
            "angle": 0,
            "color": (0, 0, 0),
            "width": 2,
        }
        self.parameters = self.parameters_init.copy()

        # dictionnaire des dessins disponibles
        self.available_draws = {
            "koch": self.draw_koch_flake,
            "koch_squares": self.draw_koch_squares_flake,
            "dragon_curve": self.draw_dragon_curve,
        }

        # générateur courant (dessin en cours)
        self.current_generator = None

    def update(self):
        """update du dessin"""
        # poursuite d'un dessin en cours
        if self.current_generator:
            try:
                for _ in range(5000):  # nombre de segments dessinés par frame
                    next(self.current_generator)
            except StopIteration:
                self.current_generator = None
        
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Outils -_________________________

    def get(self, parameter: str):
        """retourne le paramètre correspondant"""
        return self.parameters.get(parameter, None)
    
    def change(self, parameter: str, value, index=None):
        """change la valeur d'un paramètre"""
        self.parameters[parameter] = value

    def get_pos(self, x: float, y: float) -> tuple:
        """obtention de la position absolue à partir de la relative"""
        return x + self.surface_side / 2, y + self.surface_side / 2
    
    def get_relative_pos(self, x: float, y: float) -> tuple:
        """obtention de la position relative à partir de l'absolue"""
        return x - self.surface_side / 2, y - self.surface_side / 2

# _________________________- Turtle -_________________________

    def do_reset(self):
        """reset du tableau"""
        self.surface.fill((255, 255, 255))
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
            pygame.draw.line(self.surface, self.get("color"), (int(x), int(y)), (int(x_final), int(y_final)), width=self.get("width"),)

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

# _________________________- Dessins -_________________________

    def draw(self, name: str, size: int, **kwargs):
        """prépare un dessin progressif"""
        self.do_reset()
        try:
            self.current_generator = self.available_draws[name](size, **kwargs)
        except Exception as e:
            traceback.print_exc()
            self.current_generator = None
            print(f"[Painting] Error during the drawing start")
    
    def draw_square(self, size: int, **kwargs):
        """dessine un carré progressivement"""
        for _ in range(4):
            self.do_forward(size)
            yield
            self.do_left(90)

    # _________________- Flocon de Koch (triangles)-_________________
    def draw_koch_flake(self, size, **kwargs):
        """dessine un flocon de Koch"""
        max_depth = kwargs.get("max_depth", 5)
        centered = kwargs.get("centered", False)

        if centered:
            height = (3**0.5 / 2) * size
            self.do_goto(-size/2, -height/3)
        
        for _ in range(3):
            yield from self.draw_koch_segment(size, max_depth)
            self.do_right(120)

    def draw_koch_segment(self, size, max_depth, depth=0):
        """dessine un segment du flocon de Koch"""
        if depth == max_depth:
            self.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.do_left(60)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.do_right(120)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.do_left(60)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)

    # _________________- Flocon de Koch (carrés)-_________________
    def draw_koch_squares_flake(self, size, **kwargs):
        """dessine un flocon de Koch progressivement"""
        max_depth = kwargs.get("max_depth", 4)
        centered = kwargs.get("centered", False)

        if centered:
            self.do_goto(-size/2, -size/2)
        
        for _ in range(4):
            yield from self.draw_koch_squares_segment(size, max_depth)
            self.do_right(90)

    def draw_koch_squares_segment(self, size, max_depth, depth=0):
        if depth == max_depth:
            self.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)
        self.do_left(180)
        for _ in range(3):
            self.do_right(90)
            yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)
        self.do_left(90)
        yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)

    # _________________- Dragon Curve -_________________
    def draw_dragon_curve(self, size, **kwargs):
        """Dessine un Dragon Curve (île) progressivement"""
        max_depth = kwargs.get("max_depth", 16)  # profondeur par défaut
        centered = kwargs.get("centered", False)

        if centered:
            DRAGON_CENTER_OFFSET = {
                1: (0, 0),
                2: (-25, 25),
                3: (-40, 40),
                4: (-55, 55),
                5: (-70, 70),
                6: (-85, 85),
                7: (-100, 100),
                8: (-115, 115),
                9: (-130, 130),
                10: (-145, 145),
                11: (-160, 160),
                12: (-175, 175),
            }
            offset = DRAGON_CENTER_OFFSET.get(max_depth, (0,0))
            self.do_goto(offset[0], offset[1])

        yield from self.draw_dragon_segment(size, max_depth, 1)
        self.do_right(90)
        yield from self.draw_dragon_segment(size, max_depth, -1)

    def draw_dragon_segment(self, size, depth, sign=1):
        """Dessine un segment du Dragon Curve"""
        if depth == 0:
            self.do_forward(size)
            yield
            return
        
        yield from self.draw_dragon_segment(size / 1.4142, depth - 1, 1)
        if sign == 1:
            self.do_right(90)
        else:
            self.do_left(90)
        yield
        yield from self.draw_dragon_segment(size / 1.4142, depth - 1, -1)