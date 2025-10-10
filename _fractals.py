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
            ("corners_circles", "Corners (cercles)", "preset_patterns"), 
            ("cross_fractal", "Croix Récursive", "preset_patterns"), 
            ("ternary_tree", "Arbre Ternaire", "preset_patterns"),
            ("pentagon_fractal", "Pentagone Récursif", "preset_patterns"), 
            ("circle_limit", "Circle Limit", "preset_patterns"),
            ("circle_universe", "Circle Universe", "preset_patterns"),
            ("mandala_fractal", "Mandala Fractal", "preset_patterns"),
            ("hexaflake", "Hexa Flake", "preset_patterns"),
            ("pythagoras_tree", "Pythagoras Tree", "preset_patterns"),
            ("fibonacci_cross", "Croix de Fibonacci", "preset_patterns"),
            ("sierpinski_carpet", "Sierpinsky Carpet", "preset_patterns"),
            ("vicsek_snowflake", "Flocon de Vicsek", "preset_patterns"),
            ("chaos_eye", "Oeil du Chaos", "special_patterns"),
            ("organic_cathedral", "Cathédrale Organique", "special_patterns"),
            ("explosive_life_flower", "Fleur de Vie", "special_patterns"),
            ("dimension_tree", "Arbre Dimensionnelle", "special_patterns"),
            ]
        
        # auto adressage des fonctions
        self.available_fractals = {}
        for fractal in self.available_fractals_list:
            self.available_fractals[fractal[0]] = getattr(self, f"init_{fractal[0]}", None)

    # _________________- Création -_________________
    def init_creation(self, size: int):
        """création de motifs récursifs"""
        creation_type = self.turtle.get("creation_type") # type de motif

        # appel de la fonction d'initialisation correspondante
        func_name = f"init_{creation_type}"
        func = getattr(self, func_name, None)
        if func:
            yield from func(size)
        else:
            print(f"[Turtle] Unknown creation_type: {creation_type}")

    # _________________- Fonctions d'initialiation -_________________
    def init_radial(self, size: int):
        """initialise un motif radial"""
        # position initiale
        x, y = self.turtle.get("x"), self.turtle.get("y")

        # calcul du nombre de traits théorique
        self.turtle.lines_count_max = self.turtle.get("directions") * (self.turtle.get("divisions")**(self.turtle.get("depth") + 1) - 1) / self.turtle.get("divisions") - 1

        # dessin des racines
        for i in range(self.turtle.get("directions")):
            yield from self.draw_radial_recursive(size, self.turtle.get("depth")) # appel récursif
            self.turtle.do_goto(x, y) # retour à la position initiale
            self.turtle.do_setheading(self.turtle.get("angle") + (i + 1) * self.turtle.get("directions_angle") / self.turtle.get("directions")) # passage à la racine suivante

    def init_tree(self, size: int):
        """initialise un motif arborescent"""       
        # position initiale
        x, y = self.turtle.get("x"), self.turtle.get("y")
        self.turtle.do_left(90) # vers le haut par défaut 
        angle = self.turtle.get("angle")

        # calcul du nombre de traits théorique
        self.turtle.lines_count_max = self.turtle.get("directions") * (self.turtle.get("divisions")**(self.turtle.get("depth") + 1) - 1) / self.turtle.get("divisions") - 1

        # dessin des racines
        for i in range(self.turtle.get("directions")):
            yield from self.draw_tree_recursive(size, self.turtle.get("depth")) # appel récursif
            self.turtle.do_goto(x, y) # retour à la position intiale
            self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("directions_angle") // self.turtle.get("directions")) # passage à la racine suivante

    def init_incurved_tree(self, size: float):
        """Initialise un motif spirale de l'intérieur vers l'extérieur"""
        # position initiale
        self.turtle.do_left(90)
        x, y = self.turtle.get("x"), self.turtle.get("y")
        angle = self.turtle.get("angle")

        # calcul du nombre de traits théorique
        self.turtle.lines_count_max = self.turtle.get("directions") * (self.turtle.get("divisions")**(self.turtle.get("depth") + 1) - 1) / self.turtle.get("divisions") - 1

        # dessin des racines
        for i in range(self.turtle.get("directions")):
            yield from self.draw_incurved_tree_recursive(size, self.turtle.get("depth"), self.turtle.get("x"), self.turtle.get("y"), self.turtle.get("angle"))
            self.turtle.do_goto(x, y) # retour à la position initiale
            self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("directions_angle") // self.turtle.get("directions")) # passage à la racine suivante

    def init_spiral(self, size: float):
        """Initialise une spirale"""
        # position initiale
        x, y = self.turtle.get("x"), self.turtle.get("y")
        start_angle = self.turtle.get("angle")
        directions = self.turtle.get("directions")
        directions_angle = self.turtle.get("directions_angle")

        # calcul du nombre de traits théorique
        self.turtle.lines_count_max = self.turtle.get("directions") * self.turtle.get("divisions") * self.turtle.get("depth")

        # dessin des racines
        for i in range(directions):
            angle = (start_angle - directions_angle / 2) + i * (directions_angle / directions) # passage à la racine suivante
            yield from self.draw_single_spiral(x, y, angle, size, self.turtle.get("depth")) # appel récursif

    # _________________- Fonctions de génération récursive -_________________
    def draw_radial_recursive(self, size: int, depth: int):
        """génération récursive radiale"""
        if depth == 0: # cas de base
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        # dessine le motif principal
        yield from self.draw_motif(size, self.turtle.get("motif_shape"))

        # récupération des paramètres des sous-motifs
        divisions = self.turtle.get("divisions")
        angle_offset = self.turtle.get("divisions_angle")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100

        # position initiale
        x, y = self.turtle.get("x"), self.turtle.get("y")
        base_angle = self.turtle.get("angle")

        # centrage du faisceau de sous-motifs
        self.turtle.do_left(angle_offset * (divisions - 1) / 2)

        # chaque sous-branche
        for i in range(divisions):
            self.turtle.do_forward(size * 0.5, penup=True) # décalage avant
            yield from self.draw_radial_recursive(size * scale_factor, depth - 1) # appel récursif

            # repositionnement
            self.turtle.do_goto(x, y) 
            self.turtle.do_setheading(base_angle)
            self.turtle.do_right(angle_offset * (i + 1))

    def draw_tree_recursive(self, size: int, depth: int):
        """génération récursive en arborescence"""
        if depth == 0: # cas de base
            yield from self.draw_motif(size, self.turtle.get("motif_shape"),) # motif
            return

        # dessin du motif principal
        yield from self.draw_motif(size, self.turtle.get("motif_shape")) # motif  
        
        # préparation des sous-branches
        self.turtle.do_left(self.turtle.get("divisions_angle") / 2)
        x, y = self.turtle.get("x"), self.turtle.get("y")
        angle = self.turtle.get("angle")

        # chaque sous-branche
        for i in range(self.turtle.get("divisions")):
            yield from self.draw_tree_recursive(size * self.turtle.get("divisions_scale_factor") / 100, depth - 1) # appel récursif
            if self.turtle.get("divisions") > 1: # si plus de 1 sous-branche
                self.turtle.do_goto(x, y) # retour à la position initiale
                self.turtle.do_setheading(angle + (i + 1) * self.turtle.get("divisions_angle") // (self.turtle.get("divisions") - 1)) # préparation de la prochaine sous-branche

    def draw_incurved_tree_recursive(self, size: float, depth: int, x: float, y: float, angle: float):
        """génération récursive en spirale"""
        if depth == 0: # cas de base
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(angle)
            yield from self.draw_motif(size, self.turtle.get("motif_shape"))
            return

        # paramètres des sous-branches
        divisions = self.turtle.get("divisions")
        divisions_angle = self.turtle.get("divisions_angle")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100
        step_distance = size * 0.5

        # calcul de l'angle de départ pour centrer les sous-branches
        start_angle = angle - divisions_angle * (divisions - 1) / 2

        # chaque sous-branche
        for i in range(divisions):
            # placement du sous-motif au centre du motif
            self.turtle.do_goto(x, y)
            self.turtle.do_setheading(start_angle + i * divisions_angle)
            # décalage pour positionner le sous-motif
            self.turtle.do_forward(step_distance, penup=True)
            new_x, new_y = self.turtle.get("x"), self.turtle.get("y")
            new_angle = self.turtle.get("angle")
            # appel récursif
            yield from self.draw_incurved_tree_recursive(size * scale_factor, depth - 1, new_x, new_y, new_angle)

        # dessine le motif actuel après ses sous-branches
        self.turtle.do_goto(x, y)
        self.turtle.do_setheading(angle)
        yield from self.draw_motif(size, self.turtle.get("motif_shape"))

    def draw_single_spiral(self, x: float, y: float, angle: float, final_size: float, depth: int):
        """Dessine une seule spirale avec précision grâce aux divisions"""
        if depth <= 0: # cas de base
            return

        # récupération des paramètres des sous-branches
        segments = self.turtle.get("divisions")
        scale_factor = self.turtle.get("divisions_scale_factor") / 100
        step_size = final_size * (scale_factor ** (depth - 1)) / segments
        current_size = step_size
        current_x, current_y = x, y
        current_angle = angle

        # chaque sous-branche
        for _ in range(segments):
            # retour à la position initiale
            self.turtle.do_goto(current_x, current_y)
            self.turtle.do_setheading(current_angle)

            # dessin du motif
            yield from self.draw_motif(current_size, self.turtle.get("motif_shape"))

            # décalage avant pour le prochain segment
            self.turtle.do_forward(current_size, penup=True)
            current_x, current_y = self.turtle.get("x"), self.turtle.get("y")

            # rotation
            current_angle += self.turtle.get("divisions_angle")
            # augmentation de la taille
            current_size *= scale_factor

        # appel récursif
        yield from self.draw_single_spiral(current_x, current_y, current_angle, final_size, depth - 1)

    # _________________- Formes -_________________
    def draw_motif(self, size, motif_shape):
        """dessine une forme géométrique"""
        if motif_shape == "triangle":
            local_points = [self.turtle.get_pos(self.turtle.get("x"), self.turtle.get("y"))] # points du triangle
            for i in range(3): # pattern
                self.turtle.do_forward(size, penup=True, add_line=i==0)
                local_points.append(self.turtle.get_pos(self.turtle.get("x"), self.turtle.get("y"))) # ajout d'un sommet
                yield
                self.turtle.do_right(120)
            
            if self.turtle.get("filling"):
                pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("filling"), local_points) # remplissage
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("color"), local_points, self.turtle.get("width")) # dessin du motif
            
        elif motif_shape == "square":
            local_points = [self.turtle.get_pos(self.turtle.get("x"), self.turtle.get("y"))] # points du carré
            for i in range(4): # pattern du carré
                self.turtle.do_forward(size, penup=True, add_line=i==0)
                local_points.append(self.turtle.get_pos(self.turtle.get("x"), self.turtle.get("y"))) # ajout d'un coin
                yield
                self.turtle.do_right(90)

            if self.turtle.get("filling"):
                pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("filling"), local_points) # remplissage
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("color"), local_points, self.turtle.get("width")) # dessin du motif

        elif motif_shape == "circle":
            self.turtle.draw_circle(self.turtle.get("x"), self.turtle.get("y"), size / 2, centered=False, fill=self.turtle.get("filling")) # dessin du cercle
            yield

        elif motif_shape == "line":
            self.turtle.do_forward(size) # dessin de la ligne
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

        # calcul du nombre de lignes théorique
        self.turtle.lines_count_max = 3 * 4**(self.turtle.get("depth"))
        
        # dessin
        for _ in range(3):
            yield from self.draw_koch_triangles_recursive(size, depth=self.turtle.get("depth"))
            self.turtle.do_right(120)
        
        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("filling"), self.turtle.all_points)

    def draw_koch_triangles_recursive(self, size, depth=0):
        """Récursion pour dessiner un flocon de Koch (carrés)"""
        if depth == 0: # cas de base
            self.turtle.do_forward(size)
            yield
            return
        
        # facteur de rétrecissement
        new_size = size / 3
        
        # appels récursifs
        yield from self.draw_koch_triangles_recursive(new_size, depth - 1)
        self.turtle.do_left(60)
        yield from self.draw_koch_triangles_recursive(new_size, depth - 1)
        self.turtle.do_right(120)
        yield from self.draw_koch_triangles_recursive(new_size, depth - 1)
        self.turtle.do_left(60)
        yield from self.draw_koch_triangles_recursive(new_size, depth - 1)

    # _________________- Flocon de Koch (carrés)-_________________
    def init_koch_squares(self, size, **kwargs):
        """dessine un flocon de Koch (carrés)"""
        # centrage
        if self.turtle.get("centered"):
            start_angle = self.turtle.get("start_angle")
            offset_x, offset_y = -size/2, -size/2
            rx, ry = self.turtle.get_rotated_offset(offset_x, offset_y, start_angle)
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"))
        
        # dessin
        for _ in range(4):
            yield from self.draw_koch_squares_recursive(size, self.turtle.get("depth"))
            self.turtle.do_right(90)

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("filling"), self.turtle.all_points)

    def draw_koch_squares_recursive(self, size, depth=0):
        """Récursion pour dessiner un flocon de Kosh (carrés)"""
        if depth == 0:
            self.turtle.do_forward(size)
            yield
            return
        
        new_size = size / 3
        
        yield from self.draw_koch_squares_recursive(new_size, depth - 1)
        self.turtle.do_left(180)
        for _ in range(3):
            self.turtle.do_right(90)
            yield from self.draw_koch_squares_recursive(new_size, depth - 1)
        self.turtle.do_left(90)
        yield from self.draw_koch_squares_recursive(new_size, depth - 1)

    # _________________- Dragon Curve -_________________
    def init_dragon_curve(self, size, **kwargs):
        """Dessine un Dragon Curve (dual) progressivement"""
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
            offset = DRAGON_CENTER_OFFSET.get(self.turtle.get("depth"), (0,0))
            start_angle = self.turtle.get("start_angle")
            rx, ry = self.turtle.get_rotated_offset(offset[0], offset[1], start_angle)
            self.turtle.do_goto(rx + self.turtle.get("x_offset"), ry + self.turtle.get("y_offset"))

        yield from self.draw_dragon_recursive(size, self.turtle.get("depth"), 1)
        self.turtle.do_right(90)
        yield from self.draw_dragon_recursive(size, self.turtle.get("depth"), -1)

        # remplissage
        if self.turtle.get("filling") and len(self.turtle.all_points) >= 3:
            pygame.draw.polygon(self.turtle.turtle_surface, self.turtle.get_color("filling"), self.turtle.all_points)

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

# _________________- Corners Carrés -_________________
    def init_corners_squares(self, size: float):
        """Carrés dans les coins, toujours à l'intérieur du parent"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Position du coin haut-gauche du carré principal
        if self.turtle.get("centered"):
            cx -= size / 2
            cy -= size / 2
        
        yield from self.draw_corners_squares_recursive(cx, cy, size, self.turtle.get("depth"))

    def draw_corners_squares_recursive(self, x: float, y: float, size: float, depth: int):
        """Dessine un carré puis place des carrés plus petits dans ses coins"""
        # Se positionner au départ du carré
        self.turtle.do_goto(x, y)
        
        # Dessiner le carré (4 côtés)
        for _ in range(4):
            self.turtle.do_setheading(self.turtle.get("angle"))
            self.turtle.do_forward(size)
            yield
            self.turtle.do_right(90)
        
        if depth == 0:
            return
        
        # Taille des carrés enfants
        child_size = size / 3
        
        # Positions des 4 coins INTÉRIEURS
        corners = [
            (x, y),  # coin bas-gauche
            (x + size - child_size, y),  # coin bas-droit
            (x, y + size - child_size),  # coin haut-gauche
            (x + size - child_size, y + size - child_size)  # coin haut-droit
        ]
        
        for corner_x, corner_y in corners:
            yield from self.draw_corners_squares_recursive(corner_x, corner_y, child_size, depth - 1)

    # _________________- Corners Triangles -_________________
    def init_corners_triangles(self, size: float):
        """Triangles dans les sommets, toujours à l'intérieur du parent""" 
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        height = size * math.sqrt(3) / 2
        
        # triangle équilatéral centré
        points = [
            (cx, cy - height * 2/3), # sommet haut
            (cx - size/2, cy + height/3), # bas gauche
            (cx + size/2, cy + height/3) # bas droit
        ]
        
        yield from self.draw_corners_triangles_recursive(points, self.turtle.get("depth"))

    def draw_corners_triangles_recursive(self, points: list, depth: int):
        """Dessine un triangle puis place des triangles plus petits à ses sommets"""
        # Dessiner le triangle
        self.turtle.do_goto(points[0][0], points[0][1])
        
        for i in range(3):
            next_point = points[(i + 1) % 3]
            
            # Calculer angle et distance
            dx = next_point[0] - points[i][0]
            dy = next_point[1] - points[i][1]
            distance = math.sqrt(dx * dx + dy * dy)
            angle = math.degrees(math.atan2(dy, dx))
            
            # Orienter et tracer
            self.turtle.do_setheading(angle)
            self.turtle.do_forward(distance)
            yield
        
        if depth == 0:
            return
        
        # Taille réduite pour les triangles enfants
        scale = 1/3
        
        # Centre du triangle parent
        center_x = sum(p[0] for p in points) / 3
        center_y = sum(p[1] for p in points) / 3
        
        # Pour chaque sommet, créer un triangle plus petit orienté vers l'intérieur
        for i, vertex in enumerate(points):
            # Direction vers le centre
            dx = center_x - vertex[0]
            dy = center_y - vertex[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Offset vers l'intérieur
            offset_factor = 0.2
            child_center_x = vertex[0] + dx * offset_factor
            child_center_y = vertex[1] + dy * offset_factor
            
            # Taille du triangle enfant
            child_size = dist * scale * 2
            child_height = child_size * math.sqrt(3) / 2
            
            # Angle de rotation pour orienter le triangle
            base_angle = math.degrees(math.atan2(dy, dx))
            
            # Créer les 3 sommets du triangle enfant
            child_points = []
            for j in range(3):
                angle = math.radians(base_angle + 90 + j * 120)
                px = child_center_x + math.cos(angle) * child_size / math.sqrt(3)
                py = child_center_y + math.sin(angle) * child_size / math.sqrt(3)
                child_points.append((px, py))
            
            yield from self.draw_corners_triangles_recursive(child_points, depth - 1)


    # _________________- Corners Cercles -_________________
    def init_corners_circles(self, size: float):
        """Cercles dans les coins, toujours à l'intérieur du carré parent"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        yield from self.draw_corners_circles_recursive(cx, cy, size, self.turtle.get("depth"))

    def draw_corners_circles_recursive(self, cx: float, cy: float, size: float, depth: int):
        """Dessine un carré avec un cercle inscrit, puis des cercles plus petits aux coins"""
        # Dessiner le carré englobant
        half = size / 2
        self.turtle.do_goto(cx - half, cy - half)
        self.turtle.do_setheading(0)
        
        for _ in range(4):
            self.turtle.do_forward(size)
            yield
            self.turtle.do_right(90)
        
        # Cercle inscrit dans le carré
        radius = size / 2
        self.turtle.draw_circle(cx, cy, radius, centered=True)
        yield
        
        if depth == 0:
            return
        
        # Cercles enfants aux coins
        child_size = size / 3.5
        offset = size / 2 - child_size / 2
        
        corners = [
            (cx - offset, cy - offset),  # bas-gauche
            (cx + offset, cy - offset),  # bas-droit
            (cx - offset, cy + offset),  # haut-gauche
            (cx + offset, cy + offset)   # haut-droit
        ]
        
        for corner_x, corner_y in corners:
            yield from self.draw_corners_circles_recursive(corner_x, corner_y, child_size, depth - 1)


    # _________________- Croix Récursive -_________________
    def init_cross_fractal(self, size: float):
        """Croix qui génère des croix plus petites à ses extrémités"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        yield from self.draw_recursive_cross(cx, cy, size, 0, self.turtle.get("depth"))

    def draw_recursive_cross(self, cx: float, cy: float, size: float, rotation: float, depth: int):
        """Dessine une croix puis génère des croix plus petites aux 4 extrémités"""
        import math
        
        # Dessiner la croix (4 branches)
        arm_length = size / 2
        
        for i in range(4):
            angle = rotation + i * 90
            
            # Se positionner au centre
            self.turtle.do_goto(cx, cy)
            
            # Orienter et tracer la branche
            self.turtle.do_setheading(angle)
            self.turtle.do_forward(arm_length)
            yield
        
        if depth == 0:
            return
        
        # Croix enfants aux extrémités
        child_size = size * 0.4
        distance = arm_length * 0.7
        
        for i in range(4):
            angle = rotation + i * 90
            rad = math.radians(angle)
            
            child_x = cx + math.cos(rad) * distance
            child_y = cy + math.sin(rad) * distance
            
            yield from self.draw_recursive_cross(child_x, child_y, child_size, rotation + 45, depth - 1)


    # _________________- Pentagone Fractal -_________________
    def init_pentagon_fractal(self, size: float):
        """Pentagones dans les sommets, toujours à l'intérieur"""
        import math
        
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Créer les 5 sommets du pentagone
        points = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)  # -90 pour commencer en haut
            x = cx + math.cos(angle) * size
            y = cy + math.sin(angle) * size
            points.append((x, y))
        
        yield from self.draw_pentagon_recursive(points, self.turtle.get("depth"))

    def draw_pentagon_recursive(self, points: list, depth: int):
        """Dessine un pentagone puis place des pentagones aux sommets"""
        import math
        
        # Dessiner le pentagone
        self.turtle.do_goto(points[0][0], points[0][1])
        
        for i in range(5):
            next_point = points[(i + 1) % 5]
            
            # Calculer angle et distance
            dx = next_point[0] - points[i][0]
            dy = next_point[1] - points[i][1]
            distance = math.sqrt(dx * dx + dy * dy)
            angle = math.degrees(math.atan2(dy, dx))
            
            # Orienter et tracer
            self.turtle.do_setheading(angle)
            self.turtle.do_forward(distance)
            yield
        
        if depth == 0:
            return
        
        # Centre du pentagone
        cx = sum(p[0] for p in points) / 5
        cy = sum(p[1] for p in points) / 5
        
        # Taille réduite pour les enfants
        scale = 0.35
        
        # Créer un petit pentagone à chaque sommet
        for vertex in points:
            # Direction vers l'intérieur
            dx = cx - vertex[0]
            dy = cy - vertex[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Décalage vers l'intérieur
            offset = 0.25
            child_cx = vertex[0] + dx * offset
            child_cy = vertex[1] + dy * offset
            
            # Taille du pentagone enfant
            child_size = dist * scale
            
            # Créer les sommets du pentagone enfant
            child_points = []
            base_angle = math.atan2(dy, dx)
            for i in range(5):
                angle = base_angle + math.radians(i * 72)
                x = child_cx + math.cos(angle) * child_size
                y = child_cy + math.sin(angle) * child_size
                child_points.append((x, y))
            
            yield from self.draw_pentagon_recursive(child_points, depth - 1)

    # _________________- Circle limit -_________________
    def init_circle_limit(self, size: float):
        """dessine un motif circle limit à la Escher"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Cercle central
        self.turtle.draw_circle(cx, cy, size / 2, centered=True, fill=self.turtle.get("filling"))
        yield
        
        # Lancement de la récursion avec plusieurs branches radiales
        num_branches = 6  # nombre de branches principales
        yield from self.draw_circle_limit_recursive(cx, cy, size / 2, self.turtle.get("depth"), num_branches)

    def draw_circle_limit_recursive(self, cx: float, cy: float, initial_radius: float, depth: int, num_branches: int):
        """récursion circle limit : cercles qui s'insèrent entre les précédents"""
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
                self.turtle.draw_circle(x, y, child_radius, centered=True, fill=self.turtle.get("filling"))
                yield

    # _________________- Circle universe -_________________
    def init_circle_universe(self, size: float):
        """dessine un motif circle limit à la Escher"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Cercle central
        self.turtle.draw_circle(cx, cy, size / 2, centered=True, fill=self.turtle.get("filling"))
        yield
        
        # Lancement de la récursion avec plusieurs branches radiales
        num_branches = 8  # nombre de branches principales
        yield from self.draw_circle_limit_universe(cx, cy, size / 2, self.turtle.get("depth"), num_branches)

    def draw_circle_limit_universe(self, cx: float, cy: float, initial_radius: float, depth: int, num_branches: int):
        """récursion circle limit : tous les cercles référencés au centre initial"""
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
                self.turtle.draw_circle(x, y, child_radius, centered=True, fill=self.turtle.get("filling"))
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
        if depth == 0 or size < 2:
            return
        
        # Sauvegarder état
        old_x, old_y = self.turtle.get("x"), self.turtle.get("y")
        old_angle = self.turtle.get("angle")
        
        # Dessiner le carré
        self.turtle.do_goto(x, y)
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
        
        self.turtle.do_goto(top_left[0], top_left[1])
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
        self.turtle.do_goto(old_x, old_y)
        self.turtle.do_setheading(old_angle)

    # _________________- Mandala Fractal -_________________
    def init_mandala_fractal(self, size: float):
        """mandala avec pétales fractals"""        
        x, y = self.turtle.get("x"), self.turtle.get("y")
        yield from self.draw_mandala_recursive(x, y, size, 0, self.turtle.get("depth"), 12)

    def draw_mandala_recursive(self, cx: float, cy: float, radius: float, rotation: float, depth: int, petals: int):
        """mandala avec rotation et récursion"""        
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
            self.turtle.do_goto(cx, cy)
            self.turtle.do_goto(petal_x, petal_y)
            yield
        
        # Récursion
        next_radius = radius * 0.6
        next_rotation = rotation + 360 / (petals * 2)
        
        yield from self.draw_mandala_recursive(cx, cy, next_radius, next_rotation, depth - 1, petals)

    # _________________- Hexaflake -_________________
    def init_hexaflake(self, size: float):
        """flocon hexagonal fractal"""       
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
        if depth == 0:
            self.turtle.do_goto(x1, y1)
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

# _________________- L'Œil du Chaos -_________________
    def init_chaos_eye(self, size: float):
        """L'Œil du Chaos - fractal organique original"""
        import math
        
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # L'iris central - un polygone qui se déforme
        num_petals = 7  # nombre premier pour asymétrie
        
        # Dessiner l'iris principal
        iris_points = []
        for i in range(num_petals):
            angle = math.radians(i * 360 / num_petals)
            # Déformation ondulante de l'iris
            wave = 1 + 0.15 * math.sin(i * 3)
            radius = size * 0.3 * wave
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            iris_points.append((x, y))
        
        # Tracer l'iris
        self.turtle.do_goto(iris_points[0][0], iris_points[0][1])
        for point in iris_points:
            self.turtle.do_goto(point[0], point[1], penup=False)
            yield
        self.turtle.do_goto(iris_points[0][0], iris_points[0][1], penup=False)
        yield
        
        # La pupille - un trou noir tourbillonnant
        spiral_points = 20
        for i in range(spiral_points):
            progress = i / spiral_points
            angle = progress * math.pi * 6  # 3 tours
            radius = size * 0.15 * (1 - progress)
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            
            if i == 0:
                self.turtle.do_goto(x, y)
            else:
                self.turtle.do_goto(x, y, penup=False)
                yield
        
        # Lancer la récursion fractale
        yield from self.draw_chaos_eye_recursive(cx, cy, size, iris_points, 0, self.turtle.get("depth"))

    def draw_chaos_eye_recursive(self, cx: float, cy: float, size: float, parent_points: list, rotation: float, depth: int):
        """Récursion de L'Œil du Chaos"""
        import math
        
        if depth == 0 or size < 5:
            return
        
        num_petals = len(parent_points)
        
        # Pour chaque pétale de l'iris parent, créer une excroissance fractale
        for i, point in enumerate(parent_points):
            # Direction vers l'extérieur (du centre vers le point)
            dx = point[0] - cx
            dy = point[1] - cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 0.1:
                continue
            
            # Angle de croissance
            base_angle = math.atan2(dy, dx)
            
            # Métamorphose : alterne entre formes organiques
            metamorphosis = (depth % 3)
            
            if metamorphosis == 0:
                # MODE CRISTAL : structures géométriques rigides
                yield from self.draw_crystal_branch(point[0], point[1], size * 0.35, base_angle, depth - 1)
            
            elif metamorphosis == 1:
                # MODE TENTACULE : courbes organiques qui s'enroulent
                yield from self.draw_tentacle(point[0], point[1], size * 0.4, base_angle + rotation, depth - 1)
            
            else:
                # MODE ÉCLOSION : mini-yeux qui bourgeonnent
                yield from self.draw_eye_bud(point[0], point[1], size * 0.3, base_angle, depth - 1)

    def draw_crystal_branch(self, x: float, y: float, size: float, angle: float, depth: int):
        """Branche cristalline - structure géométrique"""
        import math
        
        if depth == 0 or size < 3:
            return
        
        # Créer un diamant cristallin
        crystal_points = []
        for i in range(4):
            a = angle + math.radians(i * 90)
            radius = size * (0.7 if i % 2 == 0 else 0.4)
            px = x + math.cos(a) * radius
            py = y + math.sin(a) * radius
            crystal_points.append((px, py))
        
        # Tracer le cristal
        self.turtle.do_goto(crystal_points[0][0], crystal_points[0][1])
        for point in crystal_points:
            self.turtle.do_goto(point[0], point[1], penup=False)
            yield
        self.turtle.do_goto(crystal_points[0][0], crystal_points[0][1], penup=False)
        yield
        
        # Bifurcation : deux cristaux plus petits aux pointes
        for i in [0, 2]:  # pointes opposées
            point = crystal_points[i]
            branch_angle = angle + math.radians(i * 90)
            yield from self.draw_crystal_branch(point[0], point[1], size * 0.5, branch_angle + math.radians(30), depth - 1)

    def draw_tentacle(self, x: float, y: float, size: float, angle: float, depth: int):
        """Tentacule organique - courbe sinueuse"""
        import math
        
        if depth == 0 or size < 3:
            return
        
        segments = 8
        curve_amplitude = size * 0.3
        
        self.turtle.do_goto(x, y)
        
        points = []
        for i in range(segments + 1):
            progress = i / segments
            
            # Courbe sinusoïdale pour effet ondulant
            wave = math.sin(progress * math.pi * 3) * curve_amplitude * (1 - progress * 0.5)
            
            # Position le long du tentacule
            distance = size * progress
            perpendicular = angle + math.pi / 2
            
            px = x + math.cos(angle) * distance + math.cos(perpendicular) * wave
            py = y + math.sin(angle) * distance + math.sin(perpendicular) * wave
            
            points.append((px, py))
            
            if i > 0:
                self.turtle.do_goto(px, py, penup=False)
                yield
        
        # Ventouses le long du tentacule
        for i in range(2, segments - 1, 2):
            sucker_x, sucker_y = points[i]
            sucker_radius = size * 0.15 * (1 - i / segments)
            self.turtle.draw_circle(sucker_x, sucker_y, sucker_radius, centered=True)
            yield
        
        # Récursion à l'extrémité avec division
        end_x, end_y = points[-1]
        for branch_offset in [-35, 35]:
            branch_angle = angle + math.radians(branch_offset)
            yield from self.draw_tentacle(end_x, end_y, size * 0.4, branch_angle, depth - 1)

    def draw_eye_bud(self, x: float, y: float, size: float, angle: float, depth: int):
        """Bourgeon d'œil - mini-iris qui éclot"""
        import math
        
        if depth == 0 or size < 3:
            return
        
        # Offset vers l'extérieur
        offset = size * 0.5
        bud_x = x + math.cos(angle) * offset
        bud_y = y + math.sin(angle) * offset
        
        # Tige de connexion
        self.turtle.do_goto(x, y)
        self.turtle.do_goto(bud_x, bud_y, penup=False)
        yield
        
        # Mini-iris (pentagone pour différencier du parent)
        num_sides = 5
        iris_points = []
        for i in range(num_sides):
            a = angle + math.radians(i * 360 / num_sides + depth * 20)  # rotation basée sur la profondeur
            radius = size * 0.4
            px = bud_x + math.cos(a) * radius
            py = bud_y + math.sin(a) * radius
            iris_points.append((px, py))
        
        # Tracer le mini-iris
        self.turtle.do_goto(iris_points[0][0], iris_points[0][1])
        for point in iris_points:
            self.turtle.do_goto(point[0], point[1], penup=False)
            yield
        self.turtle.do_goto(iris_points[0][0], iris_points[0][1], penup=False)
        yield
        
        # Pupille centrale
        self.turtle.draw_circle(bud_x, bud_y, size * 0.15, centered=True)
        yield
        
        # Cils radiaux
        for i in range(num_sides):
            point = iris_points[i]
            # Cil qui s'étend vers l'extérieur
            dx = point[0] - bud_x
            dy = point[1] - bud_y
            lash_length = size * 0.3
            lash_x = point[0] + dx * 0.5
            lash_y = point[1] + dy * 0.5
            
            self.turtle.do_goto(point[0], point[1])
            self.turtle.do_goto(lash_x, lash_y, penup=False)
            yield
        
        # Récursion : nouveaux bourgeons plus petits
        if depth > 1:
            for point in iris_points[::2]:  # Un bourgeon sur deux
                dx = point[0] - bud_x
                dy = point[1] - bud_y
                new_angle = math.atan2(dy, dx)
                yield from self.draw_eye_bud(point[0], point[1], size * 0.35, new_angle, depth - 1)

# _________________- La Cathédrale Organique -_________________
    def init_organic_cathedral(self, size: float):
        """La Cathédrale Organique - fractal harmonieux et visuellement sublime"""
        import math
        
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        # Rosace centrale (comme les vitraux de cathédrale)
        num_petals = 12
        
        # Cercle extérieur de la rosace
        outer_radius = size * 0.4
        self.turtle.draw_circle(cx, cy, outer_radius, centered=True)
        yield
        
        # Cercle central
        inner_radius = size * 0.15
        self.turtle.draw_circle(cx, cy, inner_radius, centered=True)
        yield
        
        # Pétales de la rosace centrale
        petal_points = []
        for i in range(num_petals):
            angle = math.radians(i * 360 / num_petals)
            x = cx + math.cos(angle) * outer_radius
            y = cy + math.sin(angle) * outer_radius
            petal_points.append((x, y, angle))
            
            # Lignes radiales vers le centre
            self.turtle.do_goto(cx, cy)
            self.turtle.do_goto(x, y, penup=False)
            yield
        
        # Arcs entre les pétales (effet dentelle)
        for i in range(num_petals):
            next_i = (i + 1) % num_petals
            p1 = petal_points[i]
            p2 = petal_points[next_i]
            
            # Arc courbe entre deux pétales
            mid_angle = (p1[2] + p2[2]) / 2
            if next_i == 0:
                mid_angle = (p1[2] + p2[2] + 2 * math.pi) / 2
            
            # Point de contrôle pour la courbe (vers l'extérieur)
            arc_radius = outer_radius * 1.15
            arc_x = cx + math.cos(mid_angle) * arc_radius
            arc_y = cy + math.sin(mid_angle) * arc_radius
            
            # Dessiner l'arc en segments
            segments = 5
            self.turtle.do_goto(p1[0], p1[1])
            for s in range(1, segments + 1):
                t = s / segments
                # Courbe de Bézier quadratique
                bx = (1-t)**2 * p1[0] + 2*(1-t)*t * arc_x + t**2 * p2[0]
                by = (1-t)**2 * p1[1] + 2*(1-t)*t * arc_y + t**2 * p2[1]
                self.turtle.do_goto(bx, by, penup=False)
                yield
        
        # Lancer la récursion pour les voûtes et colonnes
        yield from self.draw_cathedral_recursive(cx, cy, size, petal_points, self.turtle.get("depth"))

    def draw_cathedral_recursive(self, cx: float, cy: float, size: float, parent_points: list, depth: int):
        """Récursion harmonieuse - voûtes gothiques et colonnes"""
        import math
        
        if depth == 0 or size < 8:
            return
        
        num_points = len(parent_points)
        child_size = size * 0.45
        
        # Pour chaque pétale, créer une structure architecturale
        for i, (px, py, angle) in enumerate(parent_points):
            # Distance du centre au pétale
            dx = px - cx
            dy = py - cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Position de la structure fille (vers l'extérieur)
            offset = dist * 0.6
            struct_x = px + math.cos(angle) * offset
            struct_y = py + math.sin(angle) * offset
            
            # === VOÛTE GOTHIQUE ===
            vault_height = child_size * 0.8
            vault_width = child_size * 0.6
            
            # Base de la voûte
            left_base_x = struct_x - math.cos(angle + math.pi/2) * vault_width / 2
            left_base_y = struct_y - math.sin(angle + math.pi/2) * vault_width / 2
            right_base_x = struct_x + math.cos(angle + math.pi/2) * vault_width / 2
            right_base_y = struct_y + math.sin(angle + math.pi/2) * vault_width / 2
            
            # Sommet de la voûte (arc brisé gothique)
            apex_x = struct_x + math.cos(angle) * vault_height
            apex_y = struct_y + math.sin(angle) * vault_height
            
            # Point de contrôle gauche (arc)
            ctrl_left_x = left_base_x + math.cos(angle) * vault_height * 0.7
            ctrl_left_y = left_base_y + math.sin(angle) * vault_height * 0.7
            
            # Point de contrôle droit (arc)
            ctrl_right_x = right_base_x + math.cos(angle) * vault_height * 0.7
            ctrl_right_y = right_base_y + math.sin(angle) * vault_height * 0.7
            
            # Dessiner l'arc gauche de la voûte (courbe de Bézier)
            self.turtle.do_goto(left_base_x, left_base_y)
            segments = 8
            for s in range(1, segments + 1):
                t = s / segments
                bx = (1-t)**2 * left_base_x + 2*(1-t)*t * ctrl_left_x + t**2 * apex_x
                by = (1-t)**2 * left_base_y + 2*(1-t)*t * ctrl_left_y + t**2 * apex_y
                self.turtle.do_goto(bx, by, penup=False)
                yield
            
            # Dessiner l'arc droit de la voûte
            for s in range(1, segments + 1):
                t = s / segments
                bx = (1-t)**2 * apex_x + 2*(1-t)*t * ctrl_right_x + t**2 * right_base_x
                by = (1-t)**2 * apex_y + 2*(1-t)*t * ctrl_right_y + t**2 * right_base_y
                self.turtle.do_goto(bx, by, penup=False)
                yield
            
            # Fermer la base
            self.turtle.do_goto(left_base_x, left_base_y, penup=False)
            yield
            
            # === COLONNE DE CONNEXION ===
            # Ligne élégante du pétale parent à la voûte
            self.turtle.do_goto(px, py)
            self.turtle.do_goto(struct_x, struct_y, penup=False)
            yield
            
            # === ROSACE INTÉRIEURE ===
            # Mini-rosace dans la voûte
            rosace_radius = vault_width * 0.25
            rosace_x = struct_x + math.cos(angle) * vault_height * 0.4
            rosace_y = struct_y + math.sin(angle) * vault_height * 0.4
            
            self.turtle.draw_circle(rosace_x, rosace_y, rosace_radius, centered=True)
            yield
            
            # Petits rayons dans la rosace
            mini_petals = 6
            for j in range(mini_petals):
                mini_angle = angle + math.radians(j * 360 / mini_petals + depth * 15)
                mini_x = rosace_x + math.cos(mini_angle) * rosace_radius
                mini_y = rosace_y + math.sin(mini_angle) * rosace_radius
                
                self.turtle.do_goto(rosace_x, rosace_y)
                self.turtle.do_goto(mini_x, mini_y, penup=False)
                yield
            
            # === ORNEMENTS LATÉRAUX ===
            # Petites volutes sur les côtés
            for side in [-1, 1]:
                volute_x = struct_x + math.cos(angle + math.pi/2 * side) * vault_width * 0.4
                volute_y = struct_y + math.sin(angle + math.pi/2 * side) * vault_width * 0.4
                volute_radius = child_size * 0.12
                
                self.turtle.draw_circle(volute_x, volute_y, volute_radius, centered=True)
                yield
                
                # Connexion élégante à la voûte
                connect_x = struct_x + math.cos(angle + math.pi/2 * side) * vault_width * 0.25
                connect_y = struct_y + math.sin(angle + math.pi/2 * side) * vault_width * 0.25
                self.turtle.do_goto(connect_x, connect_y)
                self.turtle.do_goto(volute_x, volute_y, penup=False)
                yield
        
        # === RÉCURSION ===
        # Créer les points pour le niveau suivant (au sommet des voûtes)
        child_points = []
        for i, (px, py, angle) in enumerate(parent_points):
            dx = px - cx
            dy = py - cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            offset = dist * 0.6
            struct_x = px + math.cos(angle) * offset
            struct_y = py + math.sin(angle) * offset
            
            vault_height = child_size * 0.8
            apex_x = struct_x + math.cos(angle) * vault_height
            apex_y = struct_y + math.sin(angle) * vault_height
            
            child_points.append((apex_x, apex_y, angle))
        
        # Récursion uniquement sur quelques points pour éviter la surcharge
        selected_points = [child_points[i] for i in range(0, len(child_points), 2)]
        
        if len(selected_points) > 0:
            yield from self.draw_cathedral_recursive(cx, cy, child_size, selected_points, depth - 1)

# _________________- La Fleur de Vie Explosive -_________________
    def init_explosive_life_flower(self, size: float):
        """La Fleur de Vie Explosive - métamorphose visuelle à chaque niveau"""
        import math
        
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        yield from self.draw_explosive_flower_recursive(cx, cy, size, 0, self.turtle.get("depth"), "seed")

    def draw_explosive_flower_recursive(self, cx: float, cy: float, size: float, rotation: float, depth: int, stage: str):
        """Récursion avec métamorphose visuelle radicale"""
        import math
        
        if depth == 0 or size < 5:
            return
        
        # === CYCLE DE MÉTAMORPHOSE À 4 STADES ===
        current_depth_mod = (self.turtle.get("depth") - depth) % 4
        
        if current_depth_mod == 0:
            # STADE 1 : LA GRAINE - cercles concentriques pulsants
            yield from self.draw_seed_stage(cx, cy, size, rotation, depth)
            
        elif current_depth_mod == 1:
            # STADE 2 : L'ÉCLOSION - pétales qui s'ouvrent
            yield from self.draw_blooming_stage(cx, cy, size, rotation, depth)
            
        elif current_depth_mod == 2:
            # STADE 3 : L'EXPLOSION - rayons énergétiques
            yield from self.draw_explosion_stage(cx, cy, size, rotation, depth)
            
        else:
            # STADE 4 : LA CRISTALLISATION - géométrie sacrée
            yield from self.draw_crystal_stage(cx, cy, size, rotation, depth)

    def draw_seed_stage(self, cx: float, cy: float, size: float, rotation: float, depth: int):
        """Stade 1 : Graines - cercles concentriques organiques"""
        import math
        
        # Cercles concentriques avec épaisseur variable
        num_rings = 5
        for i in range(num_rings):
            progress = (i + 1) / num_rings
            radius = size * 0.5 * progress
            
            # Déformation organique (pas des cercles parfaits)
            num_points = 36
            self.turtle.do_goto(cx + radius, cy)
            
            for j in range(num_points + 1):
                angle = rotation + j * 2 * math.pi / num_points
                # Ondulation pour effet organique
                wave = 1 + 0.08 * math.sin(j * 5 + i * 2)
                r = radius * wave
                x = cx + math.cos(angle) * r
                y = cy + math.sin(angle) * r
                self.turtle.do_goto(x, y, penup=False)
                yield
        
        # Noyau central lumineux
        core_radius = size * 0.12
        self.turtle.draw_circle(cx, cy, core_radius, centered=True)
        yield
        
        # Points de germination (8 positions)
        num_sprouts = 8
        child_positions = []
        for i in range(num_sprouts):
            angle = rotation + i * 2 * math.pi / num_sprouts
            distance = size * 0.45
            sx = cx + math.cos(angle) * distance
            sy = cy + math.sin(angle) * distance
            child_positions.append((sx, sy, angle))
            
            # Petit cercle de germination
            sprout_radius = size * 0.08
            self.turtle.draw_circle(sx, sy, sprout_radius, centered=True)
            yield
            
            # Lien au centre
            self.turtle.do_goto(cx, cy)
            self.turtle.do_goto(sx, sy, penup=False)
            yield
        
        # RÉCURSION vers stade 2
        for sx, sy, angle in child_positions:
            yield from self.draw_explosive_flower_recursive(sx, sy, size * 0.4, angle, depth - 1, "bloom")

    def draw_blooming_stage(self, cx: float, cy: float, size: float, rotation: float, depth: int):
        """Stade 2 : Éclosion - pétales qui s'ouvrent en fleur"""
        import math
        
        num_petals = 6
        petal_positions = []
        
        for i in range(num_petals):
            angle = rotation + i * 2 * math.pi / num_petals
            
            # Base du pétale (près du centre)
            base_dist = size * 0.15
            base_x = cx + math.cos(angle) * base_dist
            base_y = cy + math.sin(angle) * base_dist
            
            # Extrémité du pétale (vers l'extérieur)
            tip_dist = size * 0.5
            tip_x = cx + math.cos(angle) * tip_dist
            tip_y = cy + math.sin(angle) * tip_dist
            
            # Points latéraux pour donner la forme de pétale
            petal_width = size * 0.25
            left_angle = angle - math.pi / 8
            right_angle = angle + math.pi / 8
            
            left_mid_x = cx + math.cos(left_angle) * tip_dist * 0.7
            left_mid_y = cy + math.sin(left_angle) * tip_dist * 0.7
            
            right_mid_x = cx + math.cos(right_angle) * tip_dist * 0.7
            right_mid_y = cy + math.sin(right_angle) * tip_dist * 0.7
            
            # Dessiner le pétale avec courbes
            self.turtle.do_goto(base_x, base_y)
            
            # Courbe gauche du pétale
            segments = 6
            for s in range(segments + 1):
                t = s / segments
                bx = (1-t)**2 * base_x + 2*(1-t)*t * left_mid_x + t**2 * tip_x
                by = (1-t)**2 * base_y + 2*(1-t)*t * left_mid_y + t**2 * tip_y
                self.turtle.do_goto(bx, by, penup=False)
                yield
            
            # Courbe droite du pétale
            for s in range(segments + 1):
                t = s / segments
                bx = (1-t)**2 * tip_x + 2*(1-t)*t * right_mid_x + t**2 * base_x
                by = (1-t)**2 * tip_y + 2*(1-t)*t * right_mid_y + t**2 * base_y
                self.turtle.do_goto(bx, by, penup=False)
                yield
            
            petal_positions.append((tip_x, tip_y, angle))
            
            # Nervure centrale du pétale
            self.turtle.do_goto(base_x, base_y)
            self.turtle.do_goto(tip_x, tip_y, penup=False)
            yield
        
        # Cœur de la fleur (pistil)
        pistil_radius = size * 0.12
        self.turtle.draw_circle(cx, cy, pistil_radius, centered=True)
        yield
        
        # Étamines autour du pistil
        for i in range(num_petals):
            angle = rotation + i * 2 * math.pi / num_petals + math.pi / num_petals
            stamen_dist = size * 0.18
            stamen_x = cx + math.cos(angle) * stamen_dist
            stamen_y = cy + math.sin(angle) * stamen_dist
            
            self.turtle.do_goto(cx, cy)
            self.turtle.do_goto(stamen_x, stamen_y, penup=False)
            yield
            
            # Anthère (bout de l'étamine)
            anther_radius = size * 0.04
            self.turtle.draw_circle(stamen_x, stamen_y, anther_radius, centered=True)
            yield
        
        # RÉCURSION vers stade 3
        for tip_x, tip_y, angle in petal_positions:
            yield from self.draw_explosive_flower_recursive(tip_x, tip_y, size * 0.45, angle + math.pi/6, depth - 1, "explosion")

    def draw_explosion_stage(self, cx: float, cy: float, size: float, rotation: float, depth: int):
        """Stade 3 : Explosion - rayons énergétiques radiants"""
        import math
        
        num_rays = 12
        ray_positions = []
        
        # Noyau explosif central
        core_radius = size * 0.1
        
        # Anneaux de choc
        for ring in range(3):
            ring_radius = core_radius * (1 + ring * 0.8)
            self.turtle.draw_circle(cx, cy, ring_radius, centered=True)
            yield
        
        # Rayons énergétiques
        for i in range(num_rays):
            angle = rotation + i * 2 * math.pi / num_rays
            
            # Rayon principal
            ray_length = size * 0.5
            end_x = cx + math.cos(angle) * ray_length
            end_y = cy + math.sin(angle) * ray_length
            
            # Épaisseur du rayon (effet de foudre)
            self.turtle.do_goto(cx, cy)
            
            # Rayon avec zig-zag pour effet énergétique
            segments = 8
            for s in range(segments + 1):
                t = s / segments
                base_x = cx + math.cos(angle) * ray_length * t
                base_y = cy + math.sin(angle) * ray_length * t
                
                # Perturbation pour effet électrique
                perturb = math.sin(s * 2) * size * 0.05 * (1 - t)
                perp_angle = angle + math.pi / 2
                
                zap_x = base_x + math.cos(perp_angle) * perturb
                zap_y = base_y + math.sin(perp_angle) * perturb
                
                self.turtle.do_goto(zap_x, zap_y, penup=False)
                yield
            
            ray_positions.append((end_x, end_y, angle))
            
            # Éclat à l'extrémité
            spark_radius = size * 0.08
            self.turtle.draw_circle(end_x, end_y, spark_radius, centered=True)
            yield
            
            # Mini-rayons secondaires
            for mini in [-1, 1]:
                mini_angle = angle + mini * math.pi / 8
                mini_length = size * 0.2
                mini_x = end_x + math.cos(mini_angle) * mini_length
                mini_y = end_y + math.sin(mini_angle) * mini_length
                
                self.turtle.do_goto(end_x, end_y)
                self.turtle.do_goto(mini_x, mini_y, penup=False)
                yield
        
        # RÉCURSION vers stade 4
        for end_x, end_y, angle in ray_positions[::2]:  # Un rayon sur deux
            yield from self.draw_explosive_flower_recursive(end_x, end_y, size * 0.35, angle + math.pi/4, depth - 1, "crystal")

    def draw_crystal_stage(self, cx: float, cy: float, size: float, rotation: float, depth: int):
        """Stade 4 : Cristallisation - géométrie sacrée complexe"""
        import math
        
        # Hexagone extérieur (géométrie sacrée)
        hex_points = []
        for i in range(6):
            angle = rotation + i * math.pi / 3
            x = cx + math.cos(angle) * size * 0.5
            y = cy + math.sin(angle) * size * 0.5
            hex_points.append((x, y))
        
        # Tracer l'hexagone
        self.turtle.do_goto(hex_points[0][0], hex_points[0][1])
        for point in hex_points:
            self.turtle.do_goto(point[0], point[1], penup=False)
            yield
        self.turtle.do_goto(hex_points[0][0], hex_points[0][1], penup=False)
        yield
        
        # Étoile intérieure (connexions diagonales)
        for i in range(6):
            for j in range(i + 2, min(i + 4, 6)):
                self.turtle.do_goto(hex_points[i][0], hex_points[i][1])
                self.turtle.do_goto(hex_points[j][0], hex_points[j][1], penup=False)
                yield
        
        # Fleur de vie au centre
        flower_radius = size * 0.15
        self.turtle.draw_circle(cx, cy, flower_radius, centered=True)
        yield
        
        # 6 cercles autour formant la fleur de vie
        flower_circles = []
        for i in range(6):
            angle = rotation + i * math.pi / 3
            fx = cx + math.cos(angle) * flower_radius
            fy = cy + math.sin(angle) * flower_radius
            flower_circles.append((fx, fy, angle))
            
            self.turtle.draw_circle(fx, fy, flower_radius, centered=True)
            yield
        
        # Runes/symboles aux som

# _________________- L'Arbre des Dimensions -_________________
    def init_dimension_tree(self, size: float):
        """L'Arbre des Dimensions"""
        cx, cy = self.turtle.get("x"), self.turtle.get("y")
        if self.turtle.get("centered"):
            cy += size
        
        # Tronc initial - portail dimensionnel
        trunk_height = size * 0.6
        trunk_width = size * 0.15
        
        # Dessiner le tronc comme un portail
        self.turtle.do_goto(cx - trunk_width/2, cy - size/2)
        self.turtle.do_goto(cx - trunk_width/2, cy - size/2 + trunk_height, penup=False)
        yield
        self.turtle.do_goto(cx + trunk_width/2, cy - size/2 + trunk_height, penup=False)
        yield
        self.turtle.do_goto(cx + trunk_width/2, cy - size/2, penup=False)
        yield
        self.turtle.do_goto(cx - trunk_width/2, cy - size/2, penup=False)
        yield
        
        # Racines énergétiques
        num_roots = 5
        for i in range(num_roots):
            root_angle = math.radians(180 + 60 + i * 60 / (num_roots - 1))
            root_length = size * 0.3
            root_x = cx + math.cos(root_angle) * root_length
            root_y = cy - size/2 + math.sin(root_angle) * root_length
            
            self.turtle.do_goto(cx, cy - size/2)
            self.turtle.do_goto(root_x, root_y, penup=False)
            yield
        
        # Point de départ de la récursion (sommet du tronc)
        start_x = cx
        start_y = cy - size/2 + trunk_height
        
        yield from self.draw_dimension_branch(start_x, start_y, size * 0.5, -90, self.turtle.get("depth"), 0)

    def draw_dimension_branch(self, x: float, y: float, size: float, angle: float, depth: int, generation: int):
        """Branche récursive avec évolution visuelle continue"""
        import math
        
        if depth == 0 or size < 2:
            # Même au dernier niveau, dessiner quelque chose de beau
            leaf_radius = max(2, size * 0.3)
            self.turtle.draw_circle(x, y, leaf_radius, centered=True)
            yield
            return
        
        # La branche change de forme selon la génération (modulo 3 pour variation)
        style = generation % 3
        
        # === DESSINER LA BRANCHE ACTUELLE ===
        branch_length = size * 0.7
        end_x = x + math.cos(math.radians(angle)) * branch_length
        end_y = y + math.sin(math.radians(angle)) * branch_length
        
        if style == 0:
            # STYLE ORGANIQUE : branche courbe ondulante
            segments = 8
            for i in range(segments + 1):
                t = i / segments
                # Courbe avec ondulation
                wave = math.sin(t * math.pi * 2) * size * 0.1
                perp_angle = math.radians(angle + 90)
                
                curr_x = x + (end_x - x) * t + math.cos(perp_angle) * wave
                curr_y = y + (end_y - y) * t + math.sin(perp_angle) * wave
                
                if i == 0:
                    self.turtle.do_goto(curr_x, curr_y)
                else:
                    self.turtle.do_goto(curr_x, curr_y, penup=False)
                    yield
            
        elif style == 1:
            # STYLE CRISTALLIN : branche droite avec arêtes
            self.turtle.do_goto(x, y)
            self.turtle.do_goto(end_x, end_y, penup=False)
            yield
            
            # Arêtes cristallines
            for side in [-1, 1]:
                edge_angle = angle + side * 25
                edge_length = branch_length * 0.3
                edge_x = x + branch_length * 0.5 * math.cos(math.radians(angle))
                edge_y = y + branch_length * 0.5 * math.sin(math.radians(angle))
                edge_end_x = edge_x + math.cos(math.radians(edge_angle)) * edge_length
                edge_end_y = edge_y + math.sin(math.radians(edge_angle)) * edge_length
                
                self.turtle.do_goto(edge_x, edge_y)
                self.turtle.do_goto(edge_end_x, edge_end_y, penup=False)
                yield
        
        else:
            # STYLE SPIRALE : branche qui tourne
            segments = 10
            for i in range(segments + 1):
                t = i / segments
                rotation = t * 180  # demi-tour pendant la croissance
                radius = size * 0.15 * math.sin(t * math.pi)
                
                curr_x = x + (end_x - x) * t + math.cos(math.radians(angle + rotation)) * radius
                curr_y = y + (end_y - y) * t + math.sin(math.radians(angle + rotation)) * radius
                
                if i == 0:
                    self.turtle.do_goto(curr_x, curr_y)
                else:
                    self.turtle.do_goto(curr_x, curr_y, penup=False)
                    yield
        
        # === NŒUD DIMENSIONNEL AU BOUT DE LA BRANCHE ===
        node_radius = size * 0.12
        self.turtle.draw_circle(end_x, end_y, node_radius, centered=True)
        yield
        
        # Cercle intérieur du nœud
        inner_radius = node_radius * 0.5
        self.turtle.draw_circle(end_x, end_y, inner_radius, centered=True)
        yield
        
        # === MOTIF UNIQUE AU NŒUD (change avec la génération) ===
        pattern = (generation + depth) % 4
        
        if pattern == 0:
            # Croix énergétique
            for cross_angle in [0, 90, 180, 270]:
                cross_x = end_x + math.cos(math.radians(cross_angle)) * node_radius * 1.5
                cross_y = end_y + math.sin(math.radians(cross_angle)) * node_radius * 1.5
                self.turtle.do_goto(end_x, end_y)
                self.turtle.do_goto(cross_x, cross_y, penup=False)
                yield
        
        elif pattern == 1:
            # Spirale autour du nœud
            spiral_segments = 12
            for i in range(spiral_segments):
                t = i / spiral_segments
                spiral_angle = t * 360 * 2  # 2 tours
                spiral_radius = node_radius * (1 + t)
                spiral_x = end_x + math.cos(math.radians(spiral_angle)) * spiral_radius
                spiral_y = end_y + math.sin(math.radians(spiral_angle)) * spiral_radius
                
                if i == 0:
                    self.turtle.do_goto(spiral_x, spiral_y)
                else:
                    self.turtle.do_goto(spiral_x, spiral_y, penup=False)
                    yield
        
        elif pattern == 2:
            # Étoile à 5 branches
            for star_i in range(5):
                star_angle = star_i * 144  # 144° pour étoile à 5 branches
                star_x = end_x + math.cos(math.radians(star_angle)) * node_radius * 1.8
                star_y = end_y + math.sin(math.radians(star_angle)) * node_radius * 1.8
                self.turtle.do_goto(end_x, end_y)
                self.turtle.do_goto(star_x, star_y, penup=False)
                yield
        
        else:
            # Triangle runique
            for tri_i in range(3):
                tri_angle = angle + tri_i * 120
                tri_x = end_x + math.cos(math.radians(tri_angle)) * node_radius * 1.5
                tri_y = end_y + math.sin(math.radians(tri_angle)) * node_radius * 1.5
                
                if tri_i == 0:
                    self.turtle.do_goto(tri_x, tri_y)
                else:
                    self.turtle.do_goto(tri_x, tri_y, penup=False)
                    yield
            # Fermer le triangle
            tri_x = end_x + math.cos(math.radians(angle)) * node_radius * 1.5
            tri_y = end_y + math.sin(math.radians(angle)) * node_radius * 1.5
            self.turtle.do_goto(tri_x, tri_y, penup=False)
            yield
        
        # === RÉCURSION : CRÉER LES BRANCHES ENFANTS ===
        # Nombre de branches enfants varie selon le niveau
        if depth > 3:
            num_children = 3  # Beaucoup de branches au début
        elif depth > 1:
            num_children = 2  # Puis bifurcation classique
        else:
            num_children = 2  # Continue jusqu'au bout
        
        # Angle d'écartement des branches
        if num_children == 3:
            branch_angles = [angle - 35, angle, angle + 35]
        else:
            branch_angles = [angle - 30, angle + 30]
        
        # Taille réduite pour les enfants (ratio d'or pour beauté)
        child_size = size * 0.65
        
        # RÉCURSION sur chaque branche enfant
        for branch_angle in branch_angles:
            yield from self.draw_dimension_branch(
                end_x, end_y, 
                child_size, 
                branch_angle, 
                depth - 1, 
                generation + 1
            )
        
        # === BONUS : BRANCHES LATÉRALES OCCASIONNELLES ===
        # Ajoute de la complexité visuelle
        if depth % 2 == 0 and depth > 1:
            # Petite branche latérale
            side = 1 if (generation % 2 == 0) else -1
            lateral_angle = angle + side * 75
            lateral_size = size * 0.35
            lateral_length = size * 0.3
            lateral_x = x + branch_length * 0.4 * math.cos(math.radians(angle))
            lateral_y = y + branch_length * 0.4 * math.sin(math.radians(angle))
            
            yield from self.draw_dimension_branch(
                lateral_x, lateral_y,
                lateral_size,
                lateral_angle,
                depth - 2,  # Moins de récursion pour les latérales
                generation + 1
            )

# _________________- Flocon de Vicsek -_________________
    def init_vicsek_snowflake(self, size: float):
        """Flocon de Vicsek - croix fractale élégante"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        yield from self.draw_vicsek_recursive(cx, cy, size, self.turtle.get("depth"))

    def draw_vicsek_recursive(self, cx: float, cy: float, size: float, depth: int):
        """Règle unique : carré central + 4 carrés aux coins"""
        if depth == 0 or size < 3:
            return
        
        # Dessiner le carré central
        half = size / 6  # Taille du carré central (1/3 de la taille totale)
        self.turtle.do_goto(cx - half, cy - half)
        self.turtle.do_goto(cx + half, cy - half, penup=False)
        yield
        self.turtle.do_goto(cx + half, cy + half, penup=False)
        yield
        self.turtle.do_goto(cx - half, cy + half, penup=False)
        yield
        self.turtle.do_goto(cx - half, cy - half, penup=False)
        yield
        
        # Taille des carrés enfants
        child_size = size / 3
        offset = size / 3  # Distance du centre aux enfants
        
        # 4 positions aux coins
        positions = [
            (cx - offset, cy - offset),
            (cx + offset, cy - offset),
            (cx - offset, cy + offset),
            (cx + offset, cy + offset)
        ]
        
        # Récursion sur chaque position
        for px, py in positions:
            yield from self.draw_vicsek_recursive(px, py, child_size, depth - 1)


    # _________________- Tapis de Sierpinski -_________________
    def init_sierpinski_carpet(self, size: float):
        """Tapis de Sierpinski - carré fractal avec trous"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        start_x = cx - size / 2
        start_y = cy - size / 2
        
        yield from self.draw_carpet_recursive(start_x, start_y, size, self.turtle.get("depth"))

    def draw_carpet_recursive(self, x: float, y: float, size: float, depth: int):
        """Règle unique : diviser en 9, enlever le centre"""
        if depth == 0 or size < 3:
            # Dessiner le carré plein
            self.turtle.do_goto(x, y)
            self.turtle.do_goto(x + size, y, penup=False)
            yield
            self.turtle.do_goto(x + size, y + size, penup=False)
            yield
            self.turtle.do_goto(x, y + size, penup=False)
            yield
            self.turtle.do_goto(x, y, penup=False)
            yield
            return
        
        # Diviser en 9 carrés
        child_size = size / 3
        
        # 8 positions (on saute le centre)
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:  # Sauter le centre
                    continue
                
                child_x = x + i * child_size
                child_y = y + j * child_size
                
                yield from self.draw_carpet_recursive(child_x, child_y, child_size, depth - 1)

    # _________________- Croix de Fibonacci -_________________
    def init_fibonacci_cross(self, size: float):
        """Croix de Fibonacci - motif en spirale dorée"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        yield from self.draw_fibonacci_cross_recursive(cx, cy, size, 0, self.turtle.get("depth"))

    def draw_fibonacci_cross_recursive(self, cx: float, cy: float, size: float, rotation: int, depth: int):
        """Règle unique : 4 branches qui tournent selon le ratio d'or"""
        import math
        
        if depth == 0 or size < 2:
            return
        
        # Dessiner une croix
        arm_length = size / 2
        
        for i in range(4):
            angle = rotation + i * 90
            rad = math.radians(angle)
            
            end_x = cx + math.cos(rad) * arm_length
            end_y = cy + math.sin(rad) * arm_length
            
            self.turtle.do_goto(cx, cy)
            self.turtle.do_goto(end_x, end_y, penup=False)
            yield
        
        # Ratio d'or
        phi = 1.618033988749895
        child_size = size / phi
        child_distance = arm_length * 0.7
        
        # 4 croix enfants aux extrémités, tournées selon Fibonacci
        for i in range(4):
            angle = rotation + i * 90
            rad = math.radians(angle)
            
            child_x = cx + math.cos(rad) * child_distance
            child_y = cy + math.sin(rad) * child_distance
            
            # Rotation de 90° pour créer l'effet spirale
            child_rotation = (rotation + 90) % 360
            
            yield from self.draw_fibonacci_cross_recursive(child_x, child_y, child_size, child_rotation, depth - 1)


    # _________________- Arbre Ternaire -_________________
    def init_ternary_tree(self, size: float):
        """Arbre ternaire - 3 branches à chaque nœud"""
        if self.turtle.get("centered"):
            cx, cy = 0, 0
        else:
            cx, cy = self.turtle.get("x"), self.turtle.get("y")
        
        start_y = cy + size / 2
        
        self.turtle.do_goto(cx, start_y)
        yield from self.draw_ternary_recursive(cx, start_y, size * 0.4, -90, self.turtle.get("depth"))

    def draw_ternary_recursive(self, x: float, y: float, length: float, angle: float, depth: int):
        """Règle unique : branche qui se divise en 3"""
        import math
        
        if depth == 0 or length < 2:
            return
        
        # Dessiner la branche
        rad = math.radians(angle)
        end_x = x + math.cos(rad) * length
        end_y = y + math.sin(rad) * length
        
        self.turtle.do_goto(x, y)
        self.turtle.do_goto(end_x, end_y, penup=False)
        yield
        
        # 3 branches enfants
        child_length = length * 0.7
        angles = [angle - 30, angle, angle + 30]
        
        for branch_angle in angles:
            yield from self.draw_ternary_recursive(end_x, end_y, child_length, branch_angle, depth - 1)