import pygame
import math


# _________________________- Stockage des fractals -_________________________
class Fractals:

    def __init__(self, turtle):
        """formalités"""
        self.turtle = turtle

        # ensemble des fractals disponibles
        self.available_fractals_list = [
            ("creation", "Crée ton motif", "created_patterns"), 
            ("koch_triangles", "Koch (triangles)", "preset_patterns"), 
            ("koch_squares", "Koch (carrés)", "preset_patterns"), 
            ("dragon_curve", "Dragon Curve", "preset_patterns"),
            ("corners_triangles", "Corners (triangles)", "preset_patterns"),
            ("corners_squares", "Corners (carrés)", "preset_patterns"), 
            ("corners_diagonals", "Corners (diagonals)", "preset_patterns"), 
            ("circle_limit", "Circle Limit", "preset_patterns"),
            ("circle_universe", "Circle Universe", "preset_patterns"),
            ("mandala_fractal", "Mandala Fractal", "preset_patterns"),
            ("hexaflake", "Hexa Flake", "preset_patterns"),
            ("pythagoras_tree", "Pythagoras Tree", "preset_patterns")
            ]
        
        # auto adressage des fonctions
        self.available_fractals = {}
        for fractal in self.available_fractals_list:
            self.available_fractals[fractal[0]] = getattr(self, f"init_{fractal[0]}", None)

    # _________________- Création -_________________
    def init_creation(self, size: int):
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

    def init_incurved_tree(self, size: float):
        """Initialise un motif spirale de l'intérieur vers l'extérieur"""
        self.turtle.do_left(90 + self.turtle.get("directions_angle") // self.turtle.get("directions"))
        x, y = self.turtle.get("x"), self.turtle.get("y")
        angle = self.turtle.get("angle")
        for i in range(self.turtle.get("directions")):
            yield from self.draw_incurved_tree_recursive(size, self.turtle.get("depth"), self.turtle.get("x"), self.turtle.get("y"), self.turtle.get("angle"))
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("directions_angle") // self.turtle.get("directions"))

    def init_spiral(self, size: float):
        """Initialise une spirale"""
        x, y = self.turtle.get("x"), self.turtle.get("y")
        start_angle = self.turtle.get("angle")
        directions = self.turtle.get("directions")
        directions_angle = self.turtle.get("directions_angle")

        # Angle de départ pour centrer les racines
        base_angle = start_angle - directions_angle / 2
        for i in range(directions):
            angle = base_angle + i * (directions_angle / max(1, directions - 1))
            yield from self.draw_single_spiral(x, y, angle, size, self.turtle.get("depth"))

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

    def draw_incurved_tree_recursive(self, size: float, depth: int, x: float, y: float, angle: float):
        """génération récursive en spirale"""
        if depth == 0:
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(angle)
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        # Paramètres fractals
        divisions = self.turtle.get("divisions")
        divisions_angle = self.turtle.get("divisions_angle")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100
        step_distance = size * 0.5

        # Calcul de l'angle de départ pour centrer les sous-motifs
        start_angle = angle - divisions_angle * (divisions - 1) / 2

        # Dessine d'abord les sous-motifs plus petits (intérieur)
        child_size = size * scale_factor
        for i in range(divisions):
            # Place le turtle au centre du parent
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(start_angle + i * divisions_angle)
            # Avance pour positionner le sous-motif
            self.turtle.do_forward(step_distance, penup=True)
            new_x, new_y = self.turtle.get("x"), self.turtle.get("y")
            new_angle = self.turtle.get("angle")
            # Appel récursif pour l'intérieur
            yield from self.draw_incurved_tree_recursive(child_size, depth - 1, new_x, new_y, new_angle)

        # Dessine le motif actuel après ses enfants
        self.turtle.do_goto(x, y)
        self.turtle.do_setheading(angle)
        yield from self.draw_motif(size, self.turtle.get("motif_shape"))

    def draw_single_spiral(self, x: float, y: float, angle: float, final_size: float, depth: int):
        """Dessine une seule spirale avec précision grâce aux divisions"""
        if depth <= 0:
            return

        # Nombre de sous-branches pour lisser la spirale
        segments = self.turtle.get("divisions")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100
        step_size = final_size * (scale_factor ** (depth - 1)) / segments

        current_size = step_size
        current_x, current_y = x, y
        current_angle = angle

        for _ in range(segments):
            # Place le turtle et dessine le motif
            self.turtle.do_goto(current_x, current_y)
            self.turtle.do_setheading(current_angle)
            yield from self.draw_motif(current_size, self.turtle.get("motif_shape"))

            # Avance légèrement pour le prochain segment
            self.turtle.do_forward(current_size, penup=True)
            current_x, current_y = self.turtle.get("x"), self.turtle.get("y")

            # Tourne pour créer la courbure
            current_angle += self.turtle.get("divisions_angle")
            # Augmente la taille progressivement pour l'effet extérieur
            current_size *= scale_factor

        # Appel récursif pour le prochain niveau de profondeur
        yield from self.draw_single_spiral(current_x, current_y, current_angle, final_size, depth - 1)

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
            self.turtle.draw_circle(self.turtle.get("x"), self.turtle.get("y"), size / 2, centered=False)
            yield
        elif motif_shape == "line":
            self.turtle.do_forward(size)
            yield

    # _________________- Flocon de Koch (triangles)-_________________
    def init_koch_triangles(self, size):
        """dessine un flocon de Koch"""
        # centrage
        if self.turtle.get("centered"):
            height = (3**0.5 / 2) * size
            offset_x = -size/2
            offset_y = -height/(3 if self.turtle.get("depth") > 0 else 2)
            rx, ry = self.turtle.get_rotated_offset(offset_x, offset_y, self.turtle.get("start_angle"))
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"))
        
        # dessin
        for _ in range(3):
            yield from self.draw_koch_triangles_recursive(size, self.turtle.get("depth"))
            self.turtle.do_right(120)
        
        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)

    def draw_koch_triangles_recursive(self, size, max_depth, depth=0):
        """Récursion pour dessiner un flocon de Koch (carrés)"""
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
    def init_koch_squares(self, size, **kwargs):
        """dessine un flocon de Koch (carrés)"""
        max_depth = self.turtle.get("depth")
        centered = self.turtle.get("centered")

        # centrage
        if centered:
            start_angle = self.turtle.get("start_angle")
            offset_x, offset_y = -size/2, -size/2
            rx, ry = self.turtle.get_rotated_offset(offset_x, offset_y, start_angle)
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"))
        
        # dessin
        for _ in range(4):
            yield from self.draw_koch_squares_recursive(size, max_depth)
            self.turtle.do_right(90)

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get("filling", multiple=("r", "g", "b", "a")), self.turtle.all_points)

    def draw_koch_squares_recursive(self, size, max_depth, depth=0):
        """Récursion pour dessiner un flocon de Kosh (carrés)"""
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
    def init_dragon_curve(self, size, **kwargs):
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
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"))

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

    # _________________- Corners (carrés) -_________________
    def init_corners_square(self, size: int):
        """dessine un motif corners avec des formes carrés"""
        x, y = self.turtle.get("x"), self.turtle.get("y") # position initiale (pre centrage)

        if self.turtle.get("centered"): # centrage
            x_offset, y_offset = -size / 2 + x, -size / 2 + y # offset
            self.turtle.do_goto(x_offset, y_offset) # déplacement initial

        offsets = [ # positions des coins
            (0, 0),
            (size, 0),
            (0, size),
            (size, size)
        ]

        for dx, dy in offsets: # chaque coin
            self.turtle.do_goto(x + dx, y + dy)
            yield from self.draw_corners_square_recursive(size, self.turtle.get("depth")) # appel récursif

    def draw_corners_squares_recursive(self, size: int, depth: int):
        """Récursion pour dessiner un motif de type corners avec des formes carrés"""
        if depth == 0: # cas de base
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        x, y = self.turtle.get("x"), self.turtle.get("y") # stockage des coordonnées
        offsets = [ # positions des coins
            (0, 0),
            (size, 0),
            (0, size),
            (size, size)
        ]

        for dx, dy in offsets: # chaque coin
            self.turtle.do_goto(x + dx, y + dy)
            yield from self.draw_corners_squares_recursive(size / 2, depth - 1)

    # _________________- Corners (triangles) -_________________
    def init_corners_triangle(self, size: int):
        """dessine un motif corners avec des formes triangles"""
        x, y = self.turtle.get("x"), self.turtle.get("y") # position initiale
        height = (3**0.5 / 2) * size # hauteur du triangle

        if self.turtle.get("centered"):  # centrage
            offset_x, offset_y = -size / 2 + x, -height / 3 + y # offsets
            self.turtle.do_goto(offset_x, offset_y, add_point=False) # déplacement initial

        offsets = [ # positions des sommets
            (0, 0),
            (size, 0),
            (size / 2, height)
        ]

        for dx, dy in offsets:
            self.turtle.do_goto(x + dx, y + dy) # chaque sommet
            yield from self.draw_corners_triangle_recursive(size, self.turtle.get("depth")) # appel récursif

    def draw_corners_triangles_recursive(self, size: int, depth: int):
        """Récursion pour dessiner un motif de type corners avec des formes triangles"""
        if depth == 0: # cas de base
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        x, y = self.turtle.get("x"), self.turtle.get("y")
        height = (3**0.5 / 2) * size
        offsets = [
            (0, 0),
            (size, 0),
            (size/2, height)
        ]

        for dx, dy in offsets: # chaque sommet
            self.turtle.do_goto(x + dx, y + dy)
            yield from self.draw_corners_triangles_recursive(size / 2, depth - 1)

    # _________________- Corners (diagonals) -_________________
    def init_corners_cross(self, size: int):
        """dessine un motif corners avec des formes particulières"""
        x, y = self.turtle.get("x"), self.turtle.get("y") # position initiale

        if self.turtle.get("centered"): # centrage
            offset_x, offset_y = -size / 2, -size / 2  # offset
            self.turtle.do_goto(x + offset_x, y + offset_y) # déplacement initial

        offsets = [  # centre + diagonales
            (0, 0),
            (size, size),
            (-size, size),
            (size, -size),
            (-size, -size)
        ]

        for dx, dy in offsets:
            self.turtle.do_goto(x + dx, y + dy) # chaque position
            yield from self.draw_corners_cross_recursive(size, self.turtle.get("depth")) # appel récursif

    def draw_corners_diagonals_recursive(self, size: int, depth: int):
        """Récursion pour dessiner un motif de type corners avec des formes particulières"""
        if depth == 0: # cas de base
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        x, y = self.turtle.get("x"), self.turtle.get("y")
        offsets = [ # centre + diagonales
            (0, 0),
            (size, size),
            (-size, size),
            (size, -size),
            (-size, -size)
        ]

        for dx, dy in offsets: # chaque position
            self.turtle.do_goto(x + dx, y + dy)
            yield from self.draw_corners_diagonals_recursive(size / 2, depth - 1)

    # _________________- Circle limit -_________________
    def init_circle_limit(self, size: float):
        """dessine un motif circle limit à la Escher"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Cercle central
        self.turtle.draw_circle(cx, cy, size, centered=True)
        yield
        
        # Lancement de la récursion avec plusieurs branches radiales
        num_branches = 6  # nombre de branches principales
        yield from self.draw_circle_limit_recursive(cx, cy, size, self.turtle.get("depth"), num_branches)

    def draw_circle_limit_recursive(self, cx: float, cy: float, initial_radius: float, depth: int, num_branches: int):
        """récursion circle limit : cercles qui s'insèrent entre les précédents"""
        import math

        if depth == 0:
            return

        # Calcul des anneaux concentriques depuis le centre initial
        for ring in range(1, depth + 1):
            # Rayon des cercles diminue avec la distance
            child_radius = initial_radius / (1.8 ** ring)
            
            if child_radius < 1:  # trop petit, on arrête
                return
            
            # Distance depuis le centre : les cercles se touchent tangentiellement
            ring_distance = initial_radius + child_radius
            for i in range(1, ring):
                ring_distance += 2 * (initial_radius / (1.8 ** i))
            
            # Nombre de cercles dans cet anneau
            circles_in_ring = num_branches * (2 ** ring)
            
            # Décalage angulaire pour intercaler entre les cercles précédents
            angle_offset = (math.pi / (num_branches * (2 ** (ring - 1)))) if ring > 1 else 0
            
            # Dessiner tous les cercles de cet anneau
            for i in range(circles_in_ring):
                angle = (2 * math.pi * i) / circles_in_ring + angle_offset
                
                # Position calculée depuis le centre initial
                x = cx + math.cos(angle) * ring_distance
                y = cy + math.sin(angle) * ring_distance
                
                # Dessiner le cercle
                self.turtle.draw_circle(x, y, child_radius, centered=True)
                yield

    # _________________- Circle universe -_________________
    def init_circle_universe(self, size: float):
        """dessine un motif circle limit à la Escher"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Cercle central
        self.turtle.draw_circle(cx, cy, size / 4, centered=True)
        yield
        
        # Lancement de la récursion avec plusieurs branches radiales
        num_branches = 8  # nombre de branches principales
        yield from self.draw_circle_limit_universe(cx, cy, size / 4, self.turtle.get("depth"), num_branches)

    def draw_circle_limit_universe(self, cx: float, cy: float, initial_radius: float, depth: int, num_branches: int):
        """récursion circle limit : tous les cercles référencés au centre initial"""
        import math

        if depth == 0:
            return

        # Calcul des anneaux concentriques depuis le centre initial
        for ring in range(1, depth + 1):
            # Rayon des cercles diminue hyperboliquement avec la distance
            # Formule inspirée du disque de Poincaré
            distance_factor = 1 + ring * 0.4  # facteur de distance du centre
            child_radius = initial_radius / (distance_factor ** 2)
            
            if child_radius < 1:  # trop petit, on arrête
                return
            
            # Distance depuis le centre initial
            ring_distance = initial_radius + sum(initial_radius / ((1 + i * 0.4) ** 1.5) for i in range(1, ring + 1))
            
            # Nombre de cercles dans cet anneau (augmente avec la distance)
            circles_in_ring = num_branches * (ring + 1)
            
            # Dessiner tous les cercles de cet anneau
            for i in range(circles_in_ring):
                angle = (2 * math.pi * i) / circles_in_ring
                
                # Position calculée depuis le centre initial
                x = cx + math.cos(angle) * ring_distance
                y = cy + math.sin(angle) * ring_distance
                
                # Dessiner le cercle
                self.turtle.draw_circle(x, y, child_radius, centered=True)
                yield

    # _________________- Arbre de Pythagore -_________________
    def init_pythagoras_tree(self, size: float):
        """arbre fractal basé sur le théorème de Pythagore"""
        x, y = self.turtle.get("x"), self.turtle.get("y") # position intiale

        if self.turtle.get("centered"):
            x -= size / 2
            y += size
            self.turtle.do_goto(x, y)
        
        yield from self.draw_pythagoras_recursive(x, y, size, -135, self.turtle.get("depth"))

    def draw_pythagoras_recursive(self, x: float, y: float, size: float, angle: float, depth: int):
        """arbre de Pythagore avec carrés"""
        import math
        
        if depth == 0 or size < 2:
            return
        
        # Sauvegarder état
        old_x, old_y = self.turtle.get("x"), self.turtle.get("y")
        old_angle = self.turtle.get("angle")
        
        # Dessiner le carré
        self.turtle.do_goto(x, y, add_point=False)
        self.turtle.do_setheading(angle)
        
        corners = [(x, y)]
        for i in range(4):
            self.turtle.do_forward(size)
            corners.append((self.turtle.get("x"), self.turtle.get("y")))
            yield
            self.turtle.do_right(90)
        
        # Sommets du carré
        top_left = corners[2]
        top_right = corners[3]
        
        # Triangle au sommet
        apex_x = (top_left[0] + top_right[0]) / 2 + math.cos(math.radians(angle)) * size / 2
        apex_y = (top_left[1] + top_right[1]) / 2 + math.sin(math.radians(angle)) * size / 2
        
        self.turtle.do_goto(top_left[0], top_left[1], add_point=False)
        self.turtle.do_goto(apex_x, apex_y)
        yield
        self.turtle.do_goto(top_right[0], top_right[1])
        yield
        
        # Deux carrés enfants
        new_size = size / math.sqrt(2)
        
        # Carré gauche
        yield from self.draw_pythagoras_recursive(top_left[0], top_left[1], new_size, angle + 45, depth - 1)
        
        # Carré droit
        yield from self.draw_pythagoras_recursive(top_right[0], top_right[1], new_size, angle - 45, depth - 1)
        
        # Restaurer
        self.turtle.do_goto(old_x, old_y, add_point=False)
        self.turtle.do_setheading(old_angle)

    # _________________- Mandala Fractal -_________________
    def init_mandala_fractal(self, size: float):
        """mandala avec pétales fractals"""        
        x, y = self.turtle.get("x"), self.turtle.get("y")
        yield from self.draw_mandala_recursive(x, y, size, 0, self.turtle.get("depth"), 12)

    def draw_mandala_recursive(self, cx: float, cy: float, radius: float, rotation: float, depth: int, petals: int):
        """mandala avec rotation et récursion"""
        import math
        
        if depth == 0 or radius < 2:
            return
        
        # Cercle central
        self.turtle.draw_circle(cx, cy, radius * 0.76, centered=True)
        yield
        
        # Pétales
        for i in range(petals):
            angle = rotation + (360 * i) / petals
            petal_x = cx + math.cos(math.radians(angle)) * radius
            petal_y = cy + math.sin(math.radians(angle)) * radius
            petal_radius = radius * 0.3
            
            self.turtle.draw_circle(petal_x, petal_y, petal_radius * 0.8, centered=True, fill=self.turtle.get("filling"))
            yield
            
            # Lignes au centre
            self.turtle.do_goto(cx, cy, add_point=False)
            self.turtle.do_goto(petal_x, petal_y)
            yield
        
        # Récursion
        next_radius = radius * 0.6
        next_rotation = rotation + 360 / (petals * 2)
        
        yield from self.draw_mandala_recursive(cx, cy, next_radius, next_rotation, depth - 1, petals)

    # _________________- Hexaflake -_________________
    def init_hexaflake(self, size: float):
        """flocon hexagonal fractal"""
        import math
        
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Hexagone initial
        for i in range(6):
            angle = i * 60
            x = cx + math.cos(math.radians(angle)) * size
            y = cy + math.sin(math.radians(angle)) * size
            next_angle = (i + 1) * 60
            nx = cx + math.cos(math.radians(next_angle)) * size
            ny = cy + math.sin(math.radians(next_angle)) * size
            
            yield from self.draw_hexaflake_recursive(x, y, nx, ny, self.turtle.get("depth"))

    def draw_hexaflake_recursive(self, x1: float, y1: float, x2: float, y2: float, depth: int, penup=False):
        """récursion hexaflake"""
        import math
        
        if depth == 0:
            self.turtle.do_goto(x1, y1, add_point=False)
            self.turtle.do_goto(x2, y2, penup=penup)
            yield
            return
        
        # Division en 3
        dx = (x2 - x1) / 3
        dy = (y2 - y1) / 3
        
        p1 = (x1 + dx, y1 + dy)
        p2 = (x1 + 2*dx, y1 + 2*dy)
        
        # Hexagone central
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        # 7 segments (hexagone protrusion)
        hex_points = []
        for i in range(7):
            hex_angle = angle + math.radians(i * 60)
            px = p1[0] + math.cos(hex_angle) * length
            py = p1[1] + math.sin(hex_angle) * length
            hex_points.append((px, py))
        
        # Récursion
        yield from self.draw_hexaflake_recursive(x1, y1, p1[0], p1[1], depth - 1, penup=True)
        for i in range(6):
            yield from self.draw_hexaflake_recursive(hex_points[i][0], hex_points[i][1], hex_points[i+1][0], hex_points[i+1][1], depth - 1)
        yield from self.draw_hexaflake_recursive(p2[0], p2[1], x2, y2, depth - 1)