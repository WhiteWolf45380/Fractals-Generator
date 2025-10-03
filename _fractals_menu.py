import pygame

# _________________________- Menu de choix de fractal -_________________________
class FractalsMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "fractals"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width // 5 # largeur du menu
        self.surface_height = self.main.screen_height - self.main.menus["toolbar"].surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topleft=(0, self.main.menus["toolbar"].surface_height))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        # titre
        self.title_back = pygame.Rect(0, 0, self.surface_width, 40)
        self.title_text, self.title_text_rect = self.ui_manager.generate_text("Sélection du motif", 25, color=self.ui_manager.get_color(self.name, "title"))
        self.title_text_rect.midleft = (self.surface_width * 0.05, 20)
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "highlight"), self.title_back)
        self.surface.blit(self.title_text, self.title_text_rect)

        """boutton de repli"""
        self.collapse_button_dict = self.ui_manager.generate_collapse_button("left", self.surface_width, self.surface_height / 2, anchor="midright")
        self.ui_manager.add_handler(self.name, "down_collapse_button", self.handle_down_collapse_button)

        """surface finale post chargement servant de base au contenu dynamique"""
        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (self.surface_width - 2, 0), (self.surface_width - 2, self.surface_height), width=2)
        self.surface_init = self.surface.copy()

        """variables utiles"""
        # ouverture/fermeture
        self.opened = True
        self.offset_x_init = self.surface_rect.left
        self.offset_x_final = self.surface_rect.left - (self.surface_rect.width - self.collapse_button_dict["back"].width)
        self.offset_duration = 1
        self.offset_progression = 1

        # paramètres pour les patterns
        self.parameters = {
            "y_start": 60, # placement y des patterns le plus haut
            "cols_number": 2, # nombre de colonnes
            "cols_space_factor": 0.3, # espacement horizontal entre les patterns (% de l'image)
            "rows_space_factor": 0.4, # espacement vertical entre les patterns (% de l'image)
            "text_fontsize": 15, # taille de la police du texte
            "text_len_mean": 15, # moyenne prédite de la longueur des descriptions
            "text_font_factor": 0.42, # rapport entre fontsize et la longueur moyenne d'un caractère
            "text_y_offset_factor": 1.2, # rapport entre fontsize et l'écart image/description
            "animation_factor_max": 1.08, # agrandissement max pour le survolement
            "animation_factor_min": 0.92, # resize factor min pour le choix actuel
            "animation_duration": 0.2, # durée de resize
        }

        """motifs disponibles"""
        self.patterns = {
            "creation": {"name": "creation", "section": "created_patterns", "description": "Crée ton motif"},
            "koch_triangles": {"name": "koch_triangles", "section": "preset_patterns", "description": "Koch (triangles)"},
            "koch_squares": {"name": "koch_squares", "section": "preset_patterns", "description": "Koch (carrés)"},
        }

        # génération des motifs
        for i, pattern in enumerate(self.patterns):
            self.patterns[pattern]["package"] = self.generate_pattern_button(self.patterns[pattern], i)
        
        # ajout des handlers
        self.ui_manager.add_handler(self.name, "down_pattern_button", self.handle_down_pattern_button)

    def update(self):
        """Mise à jour du menu de choix de fractal"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # ouverture/fermeture du menu
        if self.offset_progression < 1:
            self.offset_progression = min(1.0, self.offset_progression + self.main.dt / self.offset_duration)

            # easing
            eased = self.ui_manager.get_ease_out(self.offset_progression, intensity=1.5)

            # interpolation
            x = self.offset_x_init + (self.offset_x_final - self.offset_x_init) * eased
            self.surface_rect.left = int(x)

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict, opened=self.opened)

        # update des patterns
        for pattern in self.patterns:
            self.update_pattern_button(self.patterns[pattern])

        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

# _________________________- Handlers controllers -_________________________
    def handle_left_click_down(self, button: str):
        """évènements associés au clique souris gauche"""
        self.ui_manager.do_handler(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """évènements associés au relâchement du clique souris gauche"""

    def handle_mousewheel(self, y_offset: int):
        """événements associés à l'utilisation de la molette"""

# _________________________- Handlers -_________________________
    def handle_down_collapse_button(self):
        """évènement(clique gauche): bouton de repli"""
        self.opened = not self.opened
        self.offset_progression = 0
        # position actuelle comme nouveau départ
        self.offset_x_init = self.surface_rect.left
        if self.opened:
            self.offset_x_final = 0
        else:
            self.offset_x_final = -(self.surface_width - self.collapse_button_dict["back"].width)

    def handle_down_pattern_button(self):
        """évènement(clique gauche): bouton de motif"""
        self.main.turtle.change("pattern", self.ui_manager.mouse_hover[2])

# _________________________- Création d'éléments -_________________________
    def generate_pattern_button(self, content: dict, number: int) -> dict:
        """génère un choix de motif"""
        package = {} # dictionnaire final

        # calcul automatique des dimensions
        image_width = self.surface_width / (self.parameters["cols_number"] + self.parameters["cols_space_factor"] * (self.parameters["cols_number"] + 1))
        image_height = image_width
        spacing_x = image_width * self.parameters["cols_space_factor"]

        # génération de l'image
        package["image"], package["image_rect"] = self.ui_manager.generate_image(f"patterns/{content['name']}", width=int(image_width), height=int(image_height))
        
        # positionnement
        col = number % self.parameters["cols_number"]
        row = number // self.parameters["cols_number"]
        spacing_x = (self.surface_width - self.parameters["cols_number"] * package["image_rect"].width) / (self.parameters["cols_number"] + 1)
        package["image_rect"].x = spacing_x + col * (package["image_rect"].width + spacing_x)
        package["image_rect"].y = self.parameters["y_start"] + row * package["image_rect"].height * (1 + self.parameters["rows_space_factor"])
        package["animation_progression"] = 0.5 # état normal

        # texte
        fontsize = max(8, int(package["image_rect"].width / (self.parameters["text_len_mean"] * self.parameters["text_font_factor"])))
        package["text"], package["text_rect"] = self.ui_manager.generate_text(content["description"], fontsize, color=self.ui_manager.get_color(self.name, "text"), wlimit=package["image_rect"].width*1.1)
        package["text_rect"].center = (package["image_rect"].centerx, package["image_rect"].bottom + fontsize * self.parameters["text_y_offset_factor"])

        return package
    
# _________________________- Mise à jour d'éléments -_________________________
    def update_pattern_button(self, content: dict):
        """met à jour les patterns"""
        package = content["package"] # raccourci

        # pattern survolé
        is_current = content["name"] == self.main.turtle.get("pattern")
        if not is_current and self.ui_manager.is_mouse_hover(package["image_rect"], self.surface_rect):
            is_hovered = self.ui_manager.ask_for_mouse_hover(self.name, "pattern_button", _id=content["name"])
        else:
            is_hovered = False

        # animation (calculs)
        step = self.main.dt / self.parameters["animation_duration"]
        if is_hovered: # état survolé
            package["animation_progression"] = min(package["animation_progression"] + step, 1)

        elif is_current: # état séléctionner
            package["animation_progression"] = max(package["animation_progression"] - step, 0)

        elif package["animation_progression"] > 0.5: # état normal (supérieur)
            package["animation_progression"] = max(package["animation_progression"] - step, 0.5)

        elif package["animation_progression"] < 0.5: # état normal (inférieur)
                package["animation_progression"] = min(package["animation_progression"] + step, 0.5)
        
        # animation (resize)
        size_factor = self.parameters["animation_factor_min"] + (self.parameters["animation_factor_max"] - self.parameters["animation_factor_min"]) * package["animation_progression"]
        image, image_rect = package["image"].copy(), package["image_rect"].copy() # copie de l'image
        if package["animation_progression"] != 0.5:
            image = pygame.transform.smoothscale(image, (image_rect.width * size_factor, image_rect.height * size_factor))
            image_rect = image.get_rect(center=image_rect.center)

        # affichage
        self.surface.blit(image, image_rect) # image
        pygame.draw.rect(self.surface, self.ui_manager.get_color(self.name, "selection") if is_current else (80, 80, 80), image_rect, 3) # bordure
        self.surface.blit(package["text"], package["text_rect"]) # description