import pygame
import math
import traceback
import time


class Painting:
    
    def __init__(self, main):
        """passerelles"""
        self.main = main

        """pygame"""
        self.surface_side = self.main.screen_width * 2 // 3
        self.surface = pygame.Surface((self.surface_side, self.surface_side))
        self.surface.fill((255, 255, 255))
        self.surface_rect = (0, (self.main.screen_height - self.surface_side) // 2)

        """turtle remake"""
        self.parameters_init = {
            "x": 0,
            "y": 0,
            "angle": 0,
            "color": (0, 0, 0),
            "width": 2,
        }
        self.parameters = self.parameters_init.copy()

        self.available_draws = {
            "square": self.draw_square,
        }

    def update(self):
        """update du dessin"""
        self.main.screen.blit(self.surface, self.surface_rect)
    
    def get(self, parameter: str):
        """retourne le paramètre correspondant"""
        return self.parameters.get(parameter, None)
    
    def change(self, parameter: str, value, index=None):
        """change la valeur d'un paramètre"""
        if index is not None:
            self.parameters[parameter] = (k if i != index else value for i, k in enumerate(self.parameters))
        else:
            self.parameters[parameter] = value

    def get_pos(self, x: int, y: int) -> tuple:
        """obtention de la position absolue à partir de la relative"""
        return int(x + self.surface_side / 2), int(y + self.surface_side / 2)
    
    def get_relative_pos(self, x: int, y: int) -> tuple:
        """obtention de la position relative à partir de l'absolue"""
        return int(x - self.surface_side / 2), int(y - self.surface_side / 2)

    def do_reset(self):
        """reset du tableau"""
        self.do_go
        self.do_setheading(0)
    
    def do_goto(self, x: int, y: int):
        """se rend à une position"""
        self.change("x", x)
        self.change("y", y)
    
    def do_forward(self, distance: int, penup=False):
        """avance en dessinant"""
        x, y = self.get_pos(self.get("x"), self.get("y"))
        x_final = x + distance * math.cos(math.radians(self.get("angle")))
        y_final = y + distance * math.sin(math.radians(self.get("angle")))

        if not penup:
            pygame.draw.line(self.surface, self.get("color"), (x, y), (x_final, y_final), width=self.get("width"))
        x, y = self.get_relative_pos(x_final, y_final)
        self.change("x")
        self.change("y")
    
    def do_setheading(self, angle: int):
        """fixe l'angle"""
        self.parameters["angle"] = angle % 360
    
    def do_left(self, angle: int):
        """tourne à gauche"""
        self.parameters["angle"] = (self.parameters["angle"] - angle) % 360

    def do_right(self, angle: int):
        """tourne à droite"""
        self.parameters["angle"] = (self.parameters["angle"] + angle) % 360

    def draw(self, name: str, size: int):
        """dessine un fractal"""
        self.do_reset()
        try:
            self.available_draws[name](size)
        except Exception as e:
            traceback.print_exc()
            print(f"[Painting] Error during the drawing start")
    
    def draw_square(self, size: int):
        "dessine un carré"
        for _ in range(4):
            print(self.get("x"), self.get("y"))
            self.do_forward(size)
            self.do_left(90)


    def draw_koch_segment(self, size, max_depth, depth=0):
        if depth == max_depth:
            self.do_forward(size)
            return
        
        new_size = size / 3
        
        self.draw_koch_segment(new_size, max_depth, depth=depth+1)
        self.do_left(60)
        self.draw_koch_segment(new_size, max_depth, depth=depth+1)
        self.do_right(120)
        self.draw_koch_segment(new_size, max_depth, depth=depth+1)
        self.do_left(60)
        self.draw_koch_segment(new_size, max_depth, depth=depth+1)


    def draw_koch_squares_segment(self, size, max_depth, depth=0):
        if depth == max_depth:
            self.do_forward(size)
            return
        
        new_size = size / 3
        
        self.draw_koch_squares_segment(new_size, max_depth, depth=depth+1)
        self.do_left(180)
        for _ in range(3):
            self.do_right(90)
            self.draw_koch_squares_segment(new_size, max_depth, depth=depth+1)
        self.do_left(90)
        self.draw_koch_squares_segment(new_size, max_depth, depth=depth+1)

    def draw_koch_flake(self, size, max_depth=2, sides=3):
        self.do_goto(-size/2, (3**0.5 / 2) * size /3)
        
        for _ in range(sides):
            if sides == 3:
                draw_koch_segment(size, max_depth)
                right(120)
            elif sides == 4:
                draw_koch_squares_segment(size, max_depth)
                right(90)
            