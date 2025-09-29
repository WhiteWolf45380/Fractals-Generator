class UIManager:

    def __init__(self, main):
        """formalités"""
        self.main = main
        
        """thèmes"""
        self.current_theme = "light"
        self.themes = {
            "dark": {
                "tools_bar": {"back": (43, 43, 43), "text": (224, 224, 224)},
                "fractals_menu": {"back": (51, 51, 51), "text": (240, 240, 240)},
                "turtle": {"back": (30, 30, 30)},
                "settings_menu": {"back": (42, 42, 42), "text": (221, 221, 221)},
            },

            "light": {
                "tools_bar": {"back": (240, 240, 240), "text": (34, 34, 34)},
                "fractals_menu": {"back": (230, 230, 230), "text": (17, 17, 17)},
                "turtle": {"back": (255, 255, 255)},
                "settings_menu": {"back": (235, 235, 235), "text": (26, 26, 26)},
            }
        }
    
    def get_color(self, category: str, name: str) -> tuple:
        """renvoie la couleur d'un élément selon le thème choisit"""
        try:
            return self.themes[self.current_theme][category][name]
        except Exception as e:
            print(f"[UI_Manager] Get_color error : {e}")