import pygame

# _________________________- Menu des paramètres -_________________________
class SettingsMenu:

    def __init__(self, main):
        """formalités"""
        self.main = main
        self.ui_manager = self.main.ui_manager
        self.name = "settings"
        
        """Base du menu"""
        self.surface_width = self.main.screen_width // 4 # largeur du menu
        self.surface_height = self.main.screen_height - self.main.menus["toolbar"].surface_height # hauteur du menu
        self.surface = pygame.Surface((self.surface_width, self.surface_height)) # fond du menu
        self.surface_rect = self.surface.get_rect(topright=(self.main.screen_width, self.main.menus["toolbar"].surface_height))# placement en haut de l'écran
        self.surface_color = self.ui_manager.get_color(self.name, "back") # couleur de fond
        self.surface.fill(self.surface_color)

        # trait pour accentuer la démarquation
        pygame.draw.line(self.surface, self.ui_manager.get_color(self.name, "line"), (0, 0), (0, self.surface_height), width=2)

        """boutton de repli"""
        self.collapse_button_dict = self.ui_manager.generate_collapse_button("right", 0, self.surface_height / 2, anchor="midleft")
        self.ui_manager.add_handle(self.name, "down_collapse_button", self.handle_down_collapse_button)

        """surface finale post chargement servant de base au contenu dynamique"""
        self.surface_init = self.surface.copy()

        """variables utiles"""
        self.x_init = self.surface_rect.left
        self.opened = True
        self.offset_velocity = 13
        self.offset_closed = self.surface_width - self.collapse_button_dict["back"].width
        self.offset_current = 0

    def update(self):
        """Mise à jour de la barre d'outils"""
        # refresh
        self.surface.blit(self.surface_init, (0, 0))

        # ouverture/fermeture du menu
        if self.opened and self.offset_current > 0:
            progression = self.offset_current / self.offset_closed
            self.offset_current = max(0, self.offset_current - self.offset_velocity * self.get_incrementation(progression))
        elif not self.opened and self.offset_current < self.offset_closed:
            progression = 1 - self.offset_current / self.offset_closed
            self.offset_current = min(self.offset_closed, self.offset_current + self.offset_velocity * self.get_incrementation(progression))
        self.surface_rect.left = self.x_init + self.offset_current

        # update du boutton de repli
        self.ui_manager.update_collapse_button(self.name, self.surface, self.surface_rect, self.collapse_button_dict, opened=self.opened)
        
        # affichage
        self.main.screen.blit(self.surface, self.surface_rect)
    
    def get_incrementation(self, progression: float) -> float:
        """renvoie un ratio pour une croissance non linéaire"""
        return progression ** 0.5

# _________________________- Handles controllers -_________________________
    def handle_left_click_down(self, button: str):
        """évènements associés au clique souris gauche"""
        self.ui_manager.do_handle(self.name, f"down_{button}")

    def handle_left_click_up(self):
        """évènements associés au relâchement du clique souris gauche"""
        pass

# _________________________- Handles -_________________________
    def handle_down_collapse_button(self):
        self.opened = not self.opened