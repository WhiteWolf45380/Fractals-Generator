import pygame


# _________________________- Stockage des fractals -_________________________
class Fractals:

    def __init__(self, turtle):
        """formalités"""
        self.turtle = turtle

        self.available_fractals = {
            "koch_triangles": self.draw_koch_triangles_flake,
            "koch_squares": self.draw_koch_squares_flake,
            "dragon_curve": self.draw_dragon_curve,
        }

    # _________________- Flocon de Koch (triangles)-_________________
    def draw_koch_triangles_flake(self, size):
        """dessine un flocon de Koch"""
        # centrage
        if self.turtle.get("centered"):
            height = (3**0.5 / 2) * size
            offset_x = -size/2
            offset_y = -height/(3 if self.turtle.get("depth") > 0 else 2)
            rx, ry = self.turtle.get_rotated_offset(offset_x, offset_y, self.turtle.get("start_angle"))
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"), add_point=False)
        
        # dessin
        for _ in range(3):
            yield from self.draw_koch_triangles_recursive(size, self.turtle.get("depth"))
            self.turtle.do_right(120)
        
        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)

    def draw_koch_triangles_recursive(self, size, max_depth, depth=0):
        """Récursion pour dessiner Dragon Curve"""
        if depth == max_depth:
            self.turtle.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_triangles_recursive(new_size, max_depth, depth+1)
        self.turtle.do_left(60)
        yield from self.draw_koch_triangles_recursive(new_size, max_depth, depth+1)
        self.turtle.do_right(120)
        yield from self.draw_koch_triangles_recursive(new_size, max_depth, depth+1)
        self.turtle.do_left(60)
        yield from self.draw_koch_triangles_recursive(new_size, max_depth, depth+1)

    # _________________- Flocon de Koch (carrés)-_________________
    def draw_koch_squares_flake(self, size, **kwargs):
        """dessine un flocon de Koch progressivement"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

        # centrage
        if centered:
            start_angle = self.turtle.get("start_angle")
            offset_x, offset_y = -size/2, -size/2
            rx, ry = self.turtle.get_rotated_offset(offset_x, offset_y, start_angle)
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"), add_point=False)
        
        # dessin
        for _ in range(4):
            yield from self.draw_koch_squares_recursive(size, max_depth)
            self.turtle.do_right(90)

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)

    def draw_koch_squares_recursive(self, size, max_depth, depth=0):
        if depth == max_depth:
            self.turtle.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_squares_recursive(new_size, max_depth, depth+1)
        self.turtle.do_left(180)
        for _ in range(3):
            self.turtle.do_right(90)
            yield from self.draw_koch_squares_recursive(new_size, max_depth, depth+1)
        self.turtle.do_left(90)
        yield from self.draw_koch_squares_recursive(new_size, max_depth, depth+1)

    # _________________- Dragon Curve -_________________
    def draw_dragon_curve(self, size, **kwargs):
        """Dessine un Dragon Curve (île) progressivement"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

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
            start_angle = self.turtle.get("start_angle")
            rx, ry = self.turtle.get_rotated_offset(offset[0], offset[1], start_angle)
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"), add_point=False)

        yield from self.draw_dragon_recursive(size, max_depth, 1)
        self.turtle.do_right(90)
        yield from self.draw_dragon_recursive(size, max_depth, -1)

    def draw_dragon_recursive(self, size, depth, sign=1):
        """Récursion pour dessiner Dragon Curve"""
        if depth == 0:
            self.turtle.do_forward(size)
            yield
            return
        
        yield from self.draw_dragon_recursive(size / 1.4142, depth - 1, 1)
        if sign == 1:
            self.turtle.do_right(90)
        else:
            self.turtle.do_left(90)
        yield
        yield from self.draw_dragon_recursive(size / 1.4142, depth - 1, -1)

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)