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
        self.x_init = self.surface_rect.left
        self.opened = True
        self.offset_velocity = 13
        self.offset_closed = self.surface_width - self.collapse_button_dict["back"].width
        self.offset_current = 0

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
        }

        """motifs disponibles"""
        self.patterns = {
            "creation": {"name": "creation", "description": "Crée ton motif"},
            "koch_triangles": {"name": "koch_triangles", "description": "Koch (triangles)"},
            "koch_squares": {"name": "koch_squares", "description": "Koch (carrés)"},
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
        if self.opened and self.offset_current > 0:
            progression = self.offset_current / self.offset_closed
            self.offset_current = max(0, self.offset_current - self.offset_velocity * self.get_incrementation(progression))
        elif not self.opened and self.offset_current < self.offset_closed:
            progression = 1 - self.offset_current / self.offset_closed
            self.offset_current = min(self.offset_closed, self.offset_current + self.offset_velocity * self.get_incrementation(progression))
        self.surface_rect.left = self.x_init - self.offset_current

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict, opened=self.opened)

        # update des patterns
        for pattern in self.patterns:
            self.update_pattern_button(self.patterns[pattern])

        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)

    def get_incrementation(self, progression: float) -> float:
        """renvoie un ratio pour une croissance non linéaire"""
        return progression ** 0.5

# _________________________- Handlers controllers -_________________________
    def handle_left_click_down(self, button: str):
        """évènements associés au clique souris gauche"""
        self.ui_manager.do_handler(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """évènements associés au relâchement du clique souris gauche"""
        pass

# _________________________- Handlers -_________________________
    def handle_down_collapse_button(self):
        """évènement(clique gauche): bouton de repli"""
        self.opened = not self.opened

    def handle_down_pattern_button(self):
        """évènement(clique gauche): bouton de motif"""
        pass

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

        # texte
        fontsize = max(8, int(package["image_rect"].width / (self.parameters["text_len_mean"] * self.parameters["text_font_factor"])))
        package["text"], package["text_rect"] = self.ui_manager.generate_text(content["description"], fontsize, color=self.ui_manager.get_color(self.name, "text"), wlimit=package["image_rect"].width*1.1)
        package["text_rect"].center = (package["image_rect"].centerx, package["image_rect"].bottom + fontsize * self.parameters["text_y_offset_factor"])

        return package
    
# _________________________- Mise à jour d'éléments -_________________________
    def update_pattern_button(self, content: dict):
        """met à jour les patterns"""
        package = content["package"] # raccourci

        # affichage
        self.surface.blit(package["image"], package["image_rect"]) # image
        pygame.draw.rect(self.surface, (0, 0, 0), package["image_rect"], 2) # bordure
        self.surface.blit(package["text"], package["text_rect"]) # description