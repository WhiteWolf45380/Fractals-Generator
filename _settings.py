import pygame


class Settings:
    
    def __init__(self, main):
        """passerelles"""
        self.main = main

        """surface"""
        # définition
        self.surface_offset = 10
        self.surface_width = self.main.screen_width // 3 - self.surface_offset
        self.surface_height = self.main.screen_height - 2 * self.surface_offset
        self.surface = pygame.Surface((self.surface_width, self.surface_height))
        self.surface_rect = self.surface.get_rect(topleft=(self.main.screen_width * 2 / 3, self.surface_offset))
        self.surface_form = self.surface.get_rect()
        self.surface_color = (50, 50, 50)
        self.surface.fill((255, 255, 255))

        # fond avec coins arrondis
        pygame.draw.rect(self.surface, self.surface_color, self.surface_form, border_radius=20)
        pygame.draw.rect(self.surface, (0, 0, 0), self.surface_form, 5, border_radius=20)

        """variables utiles"""
        # polices
        self.font_title = pygame.font.Font("assets/fonts/default.ttf", 60)
        self.font_text = pygame.font.Font("assets/fonts/default.ttf", 40)
        self.font_value = pygame.font.Font("assets/fonts/default.ttf", 30)

        # surface des paramètres        
        self.settings_x_offset = 20 # décalage du texte des paramètres
        self.settings_y_offset = 0 # écart entre relative et absolute
        self.settings_surface_absolute = pygame.Surface((self.surface_rect.width - 2 * self.settings_x_offset, self.surface_rect.height * 0.75)) # surface fixe
        self.settings_surface_relative = pygame.Surface((self.surface_rect.width - 2 * self.settings_x_offset, self.surface_rect.height * 2)) # surface mobile
        self.settings_surface_rect = self.settings_surface_absolute.get_rect(topleft=(self.settings_x_offset, self.surface_rect.height * 0.125))

        # ensemble des paramètres
        self.settings = {
            "size": {"name": "Taille :", "type": "bar", "value_min": 100, "value_max": 1000, "value_init": 400}
        }

        # raccourcis vers les fonctions
        self.functions = {
            "generate_setting_bar": self.generate_setting_bar,
        }

        """pygame"""
        # titre
        self.title = self.font_title.render("Paramètres", 1, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.surface_rect.width / 2, 50))
        self.surface.blit(self.title, self.title_rect)

            # ligne de séparation
        line_start = (self.title_rect.left - 40, self.title_rect.bottom + 15)
        line_end = (self.title_rect.right + 40, self.title_rect.bottom + 15)
        pygame.draw.line(self.surface, (255, 255, 255), line_start, line_end, width=2)

        # création des assets liés aux paramètres
        next_offset = 0 # point le plus haut des paramètres
        for setting in self.settings:
            self.settings[setting]["package"], next_offset = self.functions.get(f"generate_setting_{self.settings[setting]['type']}")(self.settings[setting], next_offset)

        """surface intiale"""
        self.surface_init = self.surface.copy()

    def update(self):
        """met à jour les paramètres"""
        self.surface.blit(self.surface_init, (0, 0))
        pygame.draw.rect(self.surface, (200, 200, 200), self.settings_surface_rect)

        # actualisation des paramètres
        self.settings_surface_relative.fill(self.surface_color)
        for setting in self.settings:
            package = self.settings[setting]["package"]
            self.settings_surface_relative.blit(package["text"], package["text_rect"])
        
        # blit des surfaces de paramètres
        self.settings_surface_absolute.blit(self.settings_surface_relative, (0, -self.settings_y_offset))
        self.surface.blit(self.settings_surface_absolute, self.settings_surface_rect)

        self.main.screen.blit(self.surface, self.surface_rect)
    
    def generate_setting_bar(self, setting, offset):
        """génère un paramètre en barre"""
        # paramètres généraux du type barre
        parameters = {
            "width": 200,
            "height": 50
        }

        # package à renvoyer
        package = {}

        # texte
        package["text"] = self.font_text.render(setting["name"], 1, (255, 255, 255))
        package["text_rect"] = package["text"].get_rect(topleft=(0, offset))

        bar_back = pygame.Rect(0, 0, parameters["width"], parameters["height"])
        bar = bar_back.copy()
        bar.width = bar_back.width() * (setting["value_max"] - setting["value_min"]) / setting["value_max"]

        return package, package["text_rect"].bottom + 50