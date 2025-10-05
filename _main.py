import pygame
from _ui_manager import UIManager
from _turtle import Turtle
from _toolbar_menu import ToolbarMenu
from _fractals_menu import FractalsMenu
from _settings_menu import SettingsMenu
import sys
import os
import math


# _________________________- Main -_________________________
class Main:

    def __init__(self):
        """variables utiles"""
        self.running = True  # état du logiciel
        self.clock = pygame.time.Clock() # clock pygame
        self.fps_max = 60 # limite de fps
        self.dt = 0 # delta time utilisé pour les animations

        # curseur
        self.mouse_out = False # curseur en dehors de l'écran
        self.mouse_x = 0
        self.mouse_y = 0

        """pygame"""
        pygame.init()

        # écran virtuel
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.screen.fill((255, 255, 255))

        # écran intermédiaire (taille réelle mais sans bandes noires)
        self.screen_final_width = self.screen_width
        self.screen_final_height = self.screen_height
        self.screen_x_offset = 0 # bandes verticales
        self.screen_y_offset = 0 # bandes horizontales

        # écran réel
        self.screen_resized_width = 1280
        self.screen_resized_height = 720
        self.screen_resized = pygame.display.set_mode((self.screen_resized_width, self.screen_resized_height), pygame.RESIZABLE)

        # design de la fenêtre
        pygame.display.set_caption("Fractals Generator - by Imagine having to do this project solo because none of your classmates can even understand what you wrote, lol ! xd")  # titre de la fenêtre
        pygame.display.set_icon(pygame.image.load(self.get_path("assets/start_button.xcf")))  # icone de la fenêtre
        
        """sous classes"""
        self.ui_manager = UIManager(self)
        self.menus = {} # ensemble des menus
        self.menus["toolbar"] = ToolbarMenu(self)
        self.menus["fractals"] = FractalsMenu(self)
        self.menus["settings"] = SettingsMenu(self)
        self.turtle = Turtle(self)

    def loop(self):
        """loop principal du logiciel"""
        while self.running:
            self.dt = self.clock.tick(self.fps_max) / 1000.0 # limite de fps
            self.calc_screen_offsets() # adadptation des dimensions de l'écran

            # souris
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not self.screen_x_offset <= mouse_x <= self.screen_resized_width - self.screen_x_offset or not self.screen_y_offset <= mouse_y <= self.screen_resized_height - self.screen_y_offset: # limite à l'écran
                self.mouse_out = True
            else:
                self.mouse_out = False
            self.mouse_x = (mouse_x - self.screen_x_offset) / (self.screen_final_width / self.screen_width) # conversion de la coordonée x
            self.mouse_y = (mouse_y - self.screen_y_offset) / (self.screen_final_height / self.screen_height) # conversion de la coordonée y
            self.ui_manager.mouse_hover = None # reset du mouse_hover

            # update de turtle
            self.turtle.update()

            # update des menus dans l'ordre de priorité 
            self.menus["fractals"].update()
            self.menus["settings"].update()
            self.menus["toolbar"].update()

            # vérification des entrées utilisateur
            self.handle_inputs()
                  
            # mise à jour de l'écran
            self.blit_screen_resized()
            pygame.display.update()

    def handle_inputs(self):
        """vérification des entrées utilisateur"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # fermeture de la fenêtre
                self.close_window()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # clique gauche (appuyé)
                # événements indépendants
                self.menus["toolbar"].handle_down_text_menu()
                
                if self.ui_manager.mouse_hover is not None: # si un boutton est survolé
                    self.menus[self.ui_manager.mouse_hover[0]].handle_left_click_down(self.ui_manager.mouse_hover[1])
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # clique gauche (relaché)
                self.ui_manager.mouse_grabbing = None
                for menu in self.menus.values(): # tous les menus
                    menu.handle_left_click_up()
            
            elif event.type == pygame.MOUSEWHEEL: # molette
                for menu in self.menus.values(): # tous les menus
                    menu.handle_mousewheel(-event.y)
    
    def calc_screen_offsets(self):
        """calcul les décalages dû aux dimensions de fenêtre incompatibles"""
        self.screen_resized_width = self.screen_resized.get_width()
        self.screen_resized_height = self.screen_resized.get_height()

        # on prend le ratio min
        scale = min(
            self.screen_resized_width / self.screen_width,
            self.screen_resized_height / self.screen_height
        )

        # nouvelle taille de l’écran virtuel
        self.screen_final_width = int(self.screen_width * scale)
        self.screen_final_height = int(self.screen_height * scale)

        # centrage dans la fenêtre
        self.screen_x_offset = (self.screen_resized_width - self.screen_final_width) // 2
        self.screen_y_offset = (self.screen_resized_height - self.screen_final_height) // 2

    def blit_screen_resized(self):
        """redimensionne l'écran virtuel sur l'écran réel"""
        new_screen = pygame.transform.smoothscale(self.screen, (self.screen_final_width, self.screen_final_height))
        self.screen_resized.fill((0, 0, 0)) # pour les bandes noires
        self.screen_resized.blit(new_screen, (self.screen_x_offset, self.screen_y_offset))

    def get_relative_pos(self, rect: pygame.Rect, x: int =None, y: int=None, mutiple: list=[]) -> tuple:
        """renvoie la position relative sur un rect (par défaut pos du curseur)"""
        relative_x = (x if x is not None else self.mouse_x) - rect.left
        relative_y = (y if y is not None else self.mouse_y) - rect.top
        if len(mutiple) > 0: # rects embriqués
            return self.get_relative_pos(mutiple[0], x=relative_x, y=relative_y, mutiple=mutiple.pop(0))
        return relative_x, relative_y
    
    @staticmethod
    def snap_value(n: int | float, value_min: int, value_max: int) -> int:
        """snap une valeur (arrondi complexe)"""
        range_ = value_max - value_min
        if range_ == 0:
            return int(n)

        # ordre de grandeur de la plage
        magnitude = 10 ** math.floor(math.log10(range_))
        # pas = magnitude / 50
        step = max(magnitude // 50, 1)

        # arrondi
        return min(max(int(round(n / step) * step), value_min), value_max)
    
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