import pygame


# _________________________- Stockage des fractals -_________________________
class Fractals:

    def __init__(self, turtle):
        """formalités"""
        self.turtle = turtle

        self.available_fractals = {
            "creation": self.draw_creation,
            "koch_triangles": self.draw_koch_triangles_flake,
            "koch_squares": self.draw_koch_squares_flake,
            "dragon_curve": self.draw_dragon_curve,
        }

    # _________________- Création -_________________
    def draw_creation(self, size: int):
        """création de motifs récursifs"""
        # récupération des paramètres
        creation_type = self.turtle.get("creation_type")

        # appel de la fonction d'initialisation
        func_name = f"init_{creation_type}"
        func = getattr(self, func_name, None)
        if func:
            yield from func(size)
        else:
            print(f"[Turtle] Unknown creation_type: {creation_type}")

    # _________________- Fonctions d'initialiation -_________________
    def init_radial(self, size: int):
        """initialise un motif radial"""
        directions = self.turtle.get("directions")
        step_angle = 360 / directions

        x, y = self.turtle.get("x"), self.turtle.get("y")
        start_angle = self.turtle.get("angle")

        for i in range(directions):
            yield from self.draw_radial_recursive(size, self.turtle.get("depth"))
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(start_angle + (i + 1) * step_angle)

    def init_tree(self, size: int):
        """initialise un motif arborescent"""        
        self.turtle.do_left(90 + self.turtle.get("directions_angle") // self.turtle.get("directions"))
        x, y = self.turtle.get("x"), self.turtle.get("y")
        angle = self.turtle.get("angle")
        for i in range(self.turtle.get("directions")):
            yield from self.draw_tree_recursive(size, self.turtle.get("depth"))
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("directions_angle") // self.turtle.get("directions"))

    def init_spiral(self, size: int):
        """initialise un motif en spriale"""
        yield from self.draw_spiral_recursive(size, self.turtle.get("depth"))

    def init_grid(self, size: int):
        """initialise un motif en grille"""
        divisions = self.turtle.get("divisions")
        for dx in range(divisions):
            for dy in range(divisions):
                x_offset = dx * size
                y_offset = dy * size
                self.turtle.do_goto(x_offset, y_offset, add_point=False)
                yield from self.draw_grid_recursive(size * self.turtle.get("divisions_scale_factor") / 100, self.turtle.get("depth") - 1)

    # _________________- Fonctions de génération récursive -_________________
    def draw_radial_recursive(self, size: int, depth: int):
        """génération récursive radiale"""
        if depth == 0:
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        # Dessine le motif principal
        yield from self.draw_motif(size, self.turtle.get("motif_shape"))

        # Prépare les sous-motifs
        divisions = self.turtle.get("divisions")
        angle_offset = self.turtle.get("divisions_angle")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100

        # Position de départ
        x, y = self.turtle.get("x"), self.turtle.get("y")
        base_angle = self.turtle.get("angle")

        # Centre le faisceau de sous-motifs
        total_angle = angle_offset * (divisions - 1)
        self.turtle.do_left(total_angle / 2)

        for _ in range(divisions):
            # Avance avant de créer la récursion
            self.turtle.do_forward(size * 0.5, penup=True)
            yield from self.draw_radial_recursive(size * scale_factor, depth - 1)
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(base_angle)
            self.turtle.do_right(angle_offset * (_ + 1))

        # Restaure l'orientation initiale
        self.turtle.do_setheading(base_angle)
        self.turtle.do_goto(x, y)

    def draw_tree_recursive(self, size: int, depth: int):
        """génération récursive en arborescence"""
        yield from self.draw_motif(size, self.turtle.get("motif_shape")) # trait
        if depth == 0:
            return
        
        self.turtle.do_left(self.turtle.get("divisions_angle") / 2)
        x, y = self.turtle.get("x"), self.turtle.get("y")
        angle = self.turtle.get("angle")
        for i in range(self.turtle.get("divisions")):
            yield from self.draw_tree_recursive(size * self.turtle.get("divisions_scale_factor") / 100, depth - 1)
            if self.turtle.get("divisions") > 1:
                self.turtle.do_goto(x, y)
                self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("divisions_angle") // (self.turtle.get("divisions") - 1))

    def draw_spiral_recursive(self, size, depth: int):
        """génération récursive en spirale"""
        if depth == 0:
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        yield from self.draw_motif(size, self.turtle.get("motif_shape"))
        self.turtle.do_right(self.turtle.get("divisions_angle"))
        yield from self.draw_spiral_recursive(size * self.turtle.get("divisions_scale_factor") / 100, depth - 1)

    def draw_grid_recursive(self, size, depth: int):
        """génération récursive en grille"""
        if depth == 0:
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        divisions = self.turtle.get("divisions")
        for dx in range(divisions):
            for dy in range(divisions):
                x_offset = dx * size
                y_offset = dy * size
                self.turtle.do_goto(x_offset, y_offset, add_point=False)
                yield from self.draw_grid_recursive(size * self.turtle.get("divisions_scale_factor") / 100, depth - 1)


    # _________________- Formes -_________________
    def draw_motif(self, size, motif_shape):
        """dessine une forme géométrique"""
        if motif_shape == "triangle":
            for _ in range(3):
                self.turtle.do_forward(size)
                yield
                self.turtle.do_right(120)
        elif motif_shape == "square":
            for _ in range(4):
                self.turtle.do_forward(size)
                yield
                self.turtle.do_right(90)
        elif motif_shape == "circle":
            self.turtle.draw_circle(self.turtle.get("x"), self.turtle.get("y"), self.turtle.get("size"), centered=False)
            yield
        elif motif_shape == "line":
            self.turtle.do_forward(size)
            yield

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

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)

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