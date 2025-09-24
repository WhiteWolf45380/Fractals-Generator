import pygame
from _painting import Painting
from _settings import Settings


class Main:

    def __init__(self):
        """variables utiles"""
        self.running = True  # état du logiciel

        """pygame"""
        pygame.init()

        # écran virtuel
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.Surface((self.screen_width, self.screen_height))

        # écran réel
        self.screen_resized_width = 1280
        self.screen_resized_height = 720
        self.screen_resized = pygame.display.set_mode((self.screen_resized_width, self.screen_resized_height))

        """sous classes"""
        self.painting = Painting(self)
        self.settings = Settings(self)

    def loop(self):
        """loop principal du logiciel"""
        while self.running:
            # vérification des entrées utilisateur
            self.check_inputs()

            # update des sous classes
            self.settings.update()
            self.painting.update()            

            # mise à jour
            self.blit_screen_resized()
            pygame.display.update()

    def check_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.painting.draw("square", 100)

    def blit_screen_resized(self):
        """redimensionne l'écran virtuel sur l'écran réel"""
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
    
    def close_window(self):
        pygame.display.quit()
        self.running = False
        exit()
                

main = Main()
main.loop()