import pygame
import math
import traceback


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
            "square": self.draw_square,
            "koch": self.draw_koch_flake,
        }

        # générateur courant (dessin en cours)
        self.current_generator = None

    def update(self):
        """update du dessin"""
        # poursuite d'un dessin en cours
        if self.current_generator:
            try:
                for _ in range(100):  # nombre de segments dessinés par frame
                    next(self.current_generator)
            except StopIteration:
                self.current_generator = None
        
        self.main.screen.blit(self.surface, self.surface_rect)

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

    def draw_koch_flake(self, size, **kwargs):
        """dessine un flocon de Koch progressivement"""
        sides = kwargs.get("sides", 3)
        max_depth = kwargs.get("max_depth", 2)

        if sides == 3:
            height = (3**0.5 / 2) * size
            self.do_goto(-size/2, -height/3)
        elif sides == 4:
            self.do_goto(-size/2, -size/2)
        
        for _ in range(sides):
            if sides == 3:
                yield from self.draw_koch_segment(size, max_depth)
                self.do_right(120)
            elif sides == 4:
                yield from self.draw_koch_squares_segment(size, max_depth)
                self.do_right(90)

    def draw_koch_segment(self, size, max_depth, depth=0):
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