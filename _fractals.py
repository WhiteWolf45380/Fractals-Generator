import pygame


# _________________________- Stockage des fractals -_________________________
class Fractals:

    def __init__(self, turtle):
        """formalités"""
        self.turtle = turtle

        self.available_fractals = {
            "koch": self.draw_koch_flake,
            "koch_squares": self.draw_koch_squares_flake,
            "dragon_curve": self.draw_dragon_curve,
            "circle_limit": self.draw_circle_limit,
        }

    # _________________- Flocon de Koch (triangles)-_________________
    def draw_koch_flake(self, size):
        """dessine un flocon de Koch"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

        if centered:
            height = (3**0.5 / 2) * size
            self.turtle.do_goto(-size/2, -height/(2.5 if max_depth > 0 else 2))
        
        for _ in range(3):
            yield from self.draw_koch_segment(size, max_depth)
            self.turtle.do_right(120)

    def draw_koch_segment(self, size, max_depth, depth=0):
        """dessine un segment du flocon de Koch"""
        if depth == max_depth:
            self.turtle.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.turtle.do_left(60)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.turtle.do_right(120)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)
        self.turtle.do_left(60)
        yield from self.draw_koch_segment(new_size, max_depth, depth+1)

    # _________________- Flocon de Koch (carrés)-_________________
    def draw_koch_squares_flake(self, size, **kwargs):
        """dessine un flocon de Koch progressivement"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

        if centered:
            self.turtle.do_goto(-size/2, -size/2)
        
        for _ in range(4):
            yield from self.draw_koch_squares_segment(size, max_depth)
            self.turtle.do_right(90)

    def draw_koch_squares_segment(self, size, max_depth, depth=0):
        if depth == max_depth:
            self.turtle.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)
        self.turtle.do_left(180)
        for _ in range(3):
            self.turtle.do_right(90)
            yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)
        self.turtle.do_left(90)
        yield from self.draw_koch_squares_segment(new_size, max_depth, depth+1)

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
            self.turtle.do_goto(offset[0], offset[1])

        yield from self.draw_dragon_segment(size, max_depth, 1)
        self.turtle.do_right(90)
        yield from self.draw_dragon_segment(size, max_depth, -1)

    def draw_dragon_segment(self, size, depth, sign=1):
        """Dessine un segment du Dragon Curve"""
        if depth == 0:
            self.turtle.do_forward(size)
            yield
            return
        
        yield from self.draw_dragon_segment(size / 1.4142, depth - 1, 1)
        if sign == 1:
            self.turtle.do_right(90)
        else:
            self.turtle.do_left(90)
        yield
        yield from self.draw_dragon_segment(size / 1.4142, depth - 1, -1)
    
    # _________________- Circle Limit (type Escher) -_________________
    def draw_circle_limit(self, size, **kwargs):
        """Dessine un Circle Limit progressif"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

        yield from self.draw_circle_limit_recursive(0, 0, size, max_depth)

    def draw_circle_limit_recursive(self, x, y, radius, depth):
        """Récursion pour dessiner le Circle Limit"""
        if depth == 0:
            # Dessine un cercle
            cx, cy = self.turtle.get_pos(x, y)
            pygame.draw.circle(self.turtle.surface, self.turtle.get("color"), (int(cx), int(cy)), int(radius), width=self.turtle.get("width"))
            yield
            return
        
        # Dessine le cercle principal
        cx, cy = self.turtle.get_pos(x, y)
        pygame.draw.circle(self.turtle.surface, self.turtle.get("color"), (int(cx), int(cy)), int(radius), width=self.turtle.get("width"))
        yield

        # Subdivision en 4 cercles autour
        new_radius = radius / 2
        offsets = [(-new_radius, -new_radius), (-new_radius, new_radius), (new_radius, -new_radius), (new_radius, new_radius)]
        for dx, dy in offsets:
            yield from self.draw_circle_limit_recursive(x + dx, y + dy, new_radius, depth - 1)