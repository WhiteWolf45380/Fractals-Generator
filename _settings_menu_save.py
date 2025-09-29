import pygame


class SettingsMenu:
    
    def __init__(self, main):
        """formalités"""
        self.main = main
        self.name = "settings_menu"

        """Base du menu"""
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
        self.settings_surface_absolute_rect = self.settings_surface_absolute.get_rect(topleft=(self.settings_x_offset, self.surface_rect.height * 0.125))
        self.settings_surface_relative = pygame.Surface((self.surface_rect.width - 2 * self.settings_x_offset, self.surface_rect.height * 2)) # surface mobile
        self.settings_surface_relative_rect = self.settings_surface_absolute.get_rect()

        # ensemble des paramètres
        self.settings = {
            "size": {"name": "Taille :", "type": "bar", "value_min": 100, "value_max": 1000, "value_init": 400}
        }
        self.settings_following = None # curseur sur le paramètre

        # raccourcis vers les fonctions
        self.functions = {
            "generate_setting_bar": self.generate_setting_bar,
            "update_setting_bar": self.update_setting_bar,
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

        # actualisation des paramètres
        self.settings_surface_relative.fill(self.surface_color)
        self.settings_following = None
        for setting in self.settings:
            if self.functions[f"update_setting_{self.settings[setting]['type']}"](setting):
                self.settings_following = setting
        
        # blit des surfaces de paramètres
        self.settings_surface_relative_rect.top = -self.settings_y_offset
        self.settings_surface_absolute.blit(self.settings_surface_relative, self.settings_surface_relative_rect)
        self.surface.blit(self.settings_surface_absolute, self.settings_surface_absolute_rect)

        self.main.screen.blit(self.surface, self.surface_rect)
    
    def generate_setting_bar(self, setting: str, offset: int):
        """génère un paramètre en barre"""
        # paramètres généraux du type barre
        parameters = {
            "width": 300,
            "height": 35
        }

        # package à renvoyer
        package = {}

        # texte
        package["text"] = self.font_text.render(setting["name"], 1, (255, 255, 255))
        package["text_rect"] = package["text"].get_rect(topleft=(0, offset))

        # barre
        package["bar_back"] = pygame.Rect(0, 0, parameters["width"], parameters["height"])
        package["bar_back"].midleft = (self.settings_surface_relative_rect.width * 0.35, (package["text_rect"].centery))
        package["bar"] = package["bar_back"].copy()
        package["bar"].width = package["bar_back"].width * 0.3
        package["bar"].midleft = package["bar_back"].midleft

        return package, package["text_rect"].bottom + 20
    
    def update_setting_bar(self, setting: str):
        package = self.settings[setting]["package"] # raccourci
        # texte
        self.settings_surface_relative.blit(package["text"], package["text_rect"])
        # barre
        following = package["bar"].collidepoint(self.get_settings_mouse_pos())
        pygame.draw.rect(self.settings_surface_relative, (255, 255, 255), package["bar_back"], border_radius=15)
        pygame.draw.rect(self.settings_surface_relative, (80, 80, 80) if following else (100, 100, 100), package["bar"], border_radius=15)
        # vérifie  le curseur se trouve sur la barre
        return following
    
    def get_settings_mouse_pos(self):
        step = self.main.get_relative_pos(self.surface_rect)
        step = self.main.get_relative_pos(self.settings_surface_absolute_rect, x=step[0], y=step[1])
        step = self.main.get_relative_pos(self.settings_surface_relative_rect, x=step[0], y=step[1])
        return step