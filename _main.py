import pygame
from _ui_manager import UIManager
from _turtle import Turtle
from _tools_bar import ToolsBar
from _fractals_menu import FractalsMenu
from _settings_menu import SettingsMenu
import sys
import os


# _________________________- Main -_________________________
class Main:

    def __init__(self):
        """variables utiles"""
        self.running = True  # état du logiciel

        # curseur
        self.mouse_x = 0
        self.mouse_y = 0

        """pygame"""
        pygame.init()

        # écran virtuel
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.screen.fill((255, 255, 255))

        # écran réel
        self.screen_resized_width = 1280
        self.screen_resized_height = 720
        self.screen_resized = pygame.display.set_mode((self.screen_resized_width, self.screen_resized_height), pygame.RESIZABLE)

        # design de la fenêtre
        pygame.display.set_caption("Fractals Generator - by Imagine having to do this project solo because none of your classmates can even understand what you wrote, lol ! xd")  # titre de la fenêtre
        pygame.display.set_icon(pygame.image.load(self.get_path("assets/start_button.xcf")))  # icone de la fenêtre
        
        """sous classes"""
        self.ui_manager = UIManager(self)
        self.tools_bar = ToolsBar(self)
        self.fractals_menu = FractalsMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.turtle = Turtle(self)

    def loop(self):
        """loop principal du logiciel"""
        while self.running:
            # souris
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.mouse_x = mouse_x / (self.screen_resized_width / self.screen_width) # conversion de la coordonée x
            self.mouse_y = mouse_y / (self.screen_resized_height / self.screen_height) # conversion de la coordonée y

            # vérification des entrées utilisateur
            self.handle_inputs()

            # update de turtle
            self.turtle.update()

            # update des menus dans l'ordre de priorité 
            self.tools_bar.update()
            self.fractals_menu.update()
            self.settings_menu.update()
                  
            # mise à jour de l'écran
            self.blit_screen_resized()
            pygame.display.update()

    def handle_inputs(self):
        """vérification des entrées utilisateur"""
        self.ui_manager.mouse_hover = None # reset du mouse_hover
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.turtle.draw("koch", 800, centered=True, max_depth=10, color=(15, 15, 220))

    def blit_screen_resized(self):
        """redimensionne l'écran virtuel sur l'écran réel"""
        self.screen_resized_width = self.screen_resized.get_width()
        self.screen_resized_height = self.screen_resized.get_height()

        # on prend le ratio min
        scale = min(
            self.screen_resized_width / self.screen_width,
            self.screen_resized_height / self.screen_height
        )

        # nouvelle taille de l’écran virtuel
        new_width = int(self.screen_width * scale)
        new_height = int(self.screen_height * scale)

        # centrage dans la fenêtre
        x_offset = (self.screen_resized_width - new_width) // 2
        y_offset = (self.screen_resized_height - new_height) // 2

        # Retourne la zone à dessiner
        new_screen = pygame.transform.smoothscale(self.screen, (new_width, new_height))
        self.screen_resized.blit(new_screen, (x_offset, y_offset))

    def get_relative_pos(self, rect: pygame.Rect, x: int =None, y: int=None) -> tuple:
        """renvoie la position relative de la souris sur un rect"""
        relative_x = (x if x is not None else self.mouse_x) - rect.left
        relative_y = (y if y is not None else self.mouse_y) - rect.top
        return relative_x, relative_y
    
    @staticmethod
    def get_path(relative_path):
        """Obtention du chemin absolu des assets"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def close_window(self):
        """fonction de fermeture du logiciel"""
        pygame.display.quit()
        self.running = False
        exit()
                

# _________________________- Démarrage -_________________________
main = Main()
main.loop()