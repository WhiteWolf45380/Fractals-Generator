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
            # motif
            "pattern": "koch_triangles", # choix du motif

            # géométrie
            "depth": 10, # profondeur de récursion
            "size": 100, # taille du motif
            "start_angle": 0, # angle de la figure

            # lignes
            "width": 1, # épaisseur
            "color_r": 255, # canal rouge
            "color_g": 255, # canal vert
            "color_b": 255, # canal bleu
            "color_a": 255, # opacité

            "color_gradient": False, # dégradé
            "color_gradient_type": "linear", # type de progression
            "color_gradient_intensity": 1, # itensité du dégradé
            "color_gradient_r": 255, # dégradé rouge
            "color_gradient_g": 255, # dégradé vert
            "color_gradient_b": 255, # dégradé bleu
            "color_gradient_a": 255, # dégradé opacité

            # remplissage
            "filling": False, # remplissage
            "filling_r": 255, # remplissage rouge
            "filling_g": 0, # remplissage vert
            "filling_b": 0, # remplissage bleu
            "filling_a": 255, # remplissage opacité

            "filling_gradient": False, # dégradé
            "filling_gradient_type": "linear", # type de progression
            "filling_gradient_intensity": 1, # itensité du dégradé
            "filling_gradient_r": 255, # dégradé rouge
            "filling_gradient_g": 0, # dégradé vert
            "filling_gradient_b": 0, # dégradé bleu
            "filling_gradient_a": 255, # dégradé opacité

            # position
            "centered": True, # ancre
            "x_offset": 0, # décalage x
            "y_offset": 0, # décalage y

            # création
            "creation_type": self.ui_manager.get_item_value("creation_type"), # type de motif (radial, tree, incurved_tree, spiral)
            "motif_shape": self.ui_manager.get_item_value("motif_shape"), # forme répétée : (triangle, square, circle, line)
            "directions": 6, # nombre de branches à la racine
            "directions_angle": 180, # cone des racines
            "divisions": 2, # nombre de sous-éléments à chaque niveau
            "divisions_angle": 30, # décalage angulaire appliqué à chaque niveau
            "divisions_scale_factor": 70, # réduction de taille à chaque niveau

            "speed": 10, # vitesse d'éxécution
            "clear": True, # remise à blanc du dessin

            "x": 0, # position x (not to define)
            "y": 0, # position y (not to define)
            "angle": 0, # angle (not to define)
            "color_start": (255, 255, 255, 255), # couleur des lignes initial
            "filling_start": (255, 0, 0, 255), # remplissage initial
        }
        self.parameters = self.parameters_init.copy()

        self.speed_conversions = { # traits par boucle selon speed
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

        # types de progression de dégradé disponibles
        self.available_gradient_types = [("linear", "Linéaire"), ("exponential", "Exponentielle"), ("ease_in_out", "Quadratique"), ("symetrical", "Symétrique")]

        # types de génération disponibles
        self.available_types = [("radial", "Radiale"), ("tree", "Arbre"), ("incurved_tree", "Arbre incurvé"), ("spiral", "Spirale")]
        
        # formes de motif disponibles
        self.available_shapes = [("line", "Ligne"), ("square", "Carré"), ("triangle", "Triangle"), ("circle", "Cercle")]

        """stockage des fractals"""
        self.fractals = Fractals(self)

        """générateur courant (dessin en cours)"""
        self.current_generator = None # stockage du générateur
        self.pause = False # paramètre de pause
        self.all_points = [] # stockage de tous les points du dessin pour le remplissage
        self.lines_count_max = 1 # nombre de ligne théorique
        self.lines_count = 0 # compte le nombre de lignes pour calculer le ratio du dégradé

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
    
    def draw_circle(self, x: int, y: int, radius: int, centered=True, fill=False):
        """dessine un cercle"""
        # incrémentation du compteur
        self.lines_count += 1


        if not centered: # si non centré -> dessine devant
            angle = math.radians(self.get("angle")) # récupération de l'angle
            x = x + math.cos(angle) * radius # décalage horizontal
            y = y + math.sin(angle) * radius # décalage vertical
        abs_x, abs_y = self.get_pos(x, y) # récupération des coordonnées absolues

        color = self.get_color("color") # couleur du contour
        if fill: # si remplissage
            filling = self.get_color("filling") # couleur de remplissage
            pygame.draw.circle(self.turtle_surface, filling, (int(abs_x), int(abs_y)), int(radius)) # remplissage
        pygame.draw.circle(self.turtle_surface, color, (int(abs_x), int(abs_y)), int(radius), self.get("width")) # contour


# _________________________- Outils -_________________________
    def push(self, settings_dict: dict):
        """récupère les valeurs des propriétés avant le lancement du dessin"""
        for setting in settings_dict:
            if setting in self.parameters:
                if "value" in settings_dict[setting]:
                    self.parameters[setting] = settings_dict[setting]["value"]
                else:
                    self.parameters[setting] = self.ui_manager.get_item_value(setting)
        
        # préchargement des couleurs
        self.parameters["color_start"] = self.get("color", multiple=["r", "g", "b", "a"])
        self.parameters["color_final"] = self.get("color_gradient", multiple=["r", "g", "b", "a"])
        self.parameters["filling_start"] = self.get("filling", multiple=["r", "g", "b", "a"])
        self.parameters["filling_final"] = self.get("filling_gradient", multiple=["r", "g", "b", "a"])

    def get(self, parameter: str, multiple: tuple=None) -> str | int | tuple:
        """retourne le paramètre correspondant"""
        if multiple is not None:
            return tuple(self.parameters.get(f"{parameter}_{single}", 0) for single in multiple)
        return self.parameters.get(parameter)
    
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

    def get_interpolated_color(self, color_start: tuple[int], color_final: tuple[int], intensity: int, progression_type: str) -> tuple[int]:
        """Renvoie la couleur interpolée selon la profondeur"""
        progress = min(1.0, max(0.0, self.lines_count / max(self.lines_count_max, 1)))
        intensity_factor = intensity / 100
        print(self.lines_count, self.lines_count_max)

        if progression_type == "exponential":
            factor = progress ** (0.3 + 2.7 * (1 - intensity_factor))

        elif progression_type == "ease_in_out":
            if progress < 0.5:
                factor = 0.5 * (2 * progress) ** (2 + 8 * intensity_factor)
            else:
                factor = 1 - 0.5 * (2 * (1 - progress)) ** (2 + 8 * intensity_factor)

        elif progression_type == "symetrical":
            if progress < 0.5:
                factor = (2 * progress) ** (0.5 + 2 * (1 - intensity_factor))
            else:
                factor = (2 * (1 - progress)) ** (0.5 + 2 * (1 - intensity_factor))
    
        else:
            factor = progress

        # interpolation rgba
        r = color_start[0] + (color_final[0] - color_start[0]) * factor
        g = color_start[1] + (color_final[1] - color_start[1]) * factor
        b = color_start[2] + (color_final[2] - color_start[2]) * factor
        a = color_start[3] + (color_final[3] - color_start[3]) * factor

        return (int(r), int(g), int(b), int(a))

    def get_color(self, category: str) -> tuple[int]:
        """renvoie la couleur correspondant à la catégorie"""
        if self.get(f"{category}_gradient"): # si dégradé -> interpolation
            return self.get_interpolated_color(self.get(f"{category}_start"), self.get(f"{category}_final"), self.get(f"{category}_gradient_intensity"), self.get(f"{category}_gradient_type"))
        else: # sinon -> couleur intiale
            return self.get(f"{category}_start")

# _________________________- Turtle -_________________________

    def do_reset(self):
        """reset de turtle"""
        # remise à blanc de la zone de dessin
        if self.get("clear"):
            self.surface.fill(self.ui_manager.get_color(self.name, "back"))
            self.turtle_surface.fill((0, 0, 0, 0))
        
        # repositionnement
        self.do_goto(self.get("x_offset"), self.get("y_offset"))
        self.do_setheading(self.get("start_angle"))

        # mise par défaut du nombre de lignes théorique à 1
        self.lines_count = 0
        self.lines_count_max = 1
    
    def do_goto(self, x: float, y: float, penup: bool=True, add_line: bool=True):
        """se rend à une position"""
        if not penup: # traçage du trait
            # récupération des paramètres
            old_x, old_y = self.get_pos(self.get("x"), self.get("y"))
            new_x, new_y = self.get_pos(x, y)
            color = self.get_color("color")
            width = self.get("width")
            
            if width == 1:# ligne fine
                pygame.draw.aaline(self.turtle_surface, color, (int(old_x), int(old_y)), (int(new_x), int(new_y)))
            else:# ligne épaisse
                radius = max(1, (width + 1) // 2)
                pygame.draw.line(self.turtle_surface, color, (int(old_x), int(old_y)), (int(new_x), int(new_y)), width)
                pygame.draw.circle(self.turtle_surface, color, (int(old_x), int(old_y)), radius)
                pygame.draw.circle(self.turtle_surface, color, (int(new_x), int(new_y)), radius)
            
            # ajout du point final
            self.all_points.append(self.get_pos(x, y)) 

            if add_line: # incrémentation du nombre de traits
                self.lines_count += 1

        # repositionnement
        self.change("x", x)
        self.change("y", y)                       
    
    def do_forward(self, distance: float, penup: bool=False, add_line: bool=True):
        """avance en dessinant"""
        # incrémentation du compteur
        if add_line:
            self.lines_count += 1

        # calcul des positions absolues initiales et finales
        x, y = self.get_pos(self.get("x"), self.get("y"))
        x_final = x + distance * math.cos(math.radians(self.get("angle")))
        y_final = y + distance * math.sin(math.radians(self.get("angle")))

        # traçage du trait
        if not penup:
            # récupéraition des paramètres
            color = self.get_color("color")
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