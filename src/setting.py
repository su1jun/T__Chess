import pygame, os

# const
# Screen dimensions
WIDTH = 720
HEIGHT = 720

# Board dimensions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS

# Inter face
WIDTH_IN = 720
HEIGHT_IN = 0

class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

class Color:
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark

class Theme:
    def __init__(self, light_bg, dark_bg, 
                       light_trace, dark_trace,
                       light_moves, dark_moves):
        
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)

class Config:
    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)

        # images
        self.move_point = os.path.join(
            'assets', 'images', 'move_point.png')
        self.attack_point = os.path.join(
            'assets', 'images', 'attack_point.png')
        
        # sounds
        self.move_sound = Sound(
            os.path.join('assets', 'sounds', 'move_self.mp3'))
        self.capture_sound = Sound(
            os.path.join('assets', 'sounds', 'capture.mp3'))
        self.check_sound = Sound(
            os.path.join('assets', 'sounds', 'move_check.mp3'))
        self.castling_sound = Sound(
            os.path.join('assets', 'sounds', 'castling.mp3'))
        self.promote_sound = Sound(
            os.path.join('assets', 'sounds', 'promote.mp3'))
        
        # voices
        self.check_voice = Sound(
            os.path.join('assets', 'sounds', 'check_voice.mp3'))
        self.checkmate_voice = Sound(
            os.path.join('assets', 'sounds', 'checkmate_voice.mp3'))
        self.stalemate_voice = Sound(
            os.path.join('assets', 'sounds', 'stalemate_voice.mp3'))
        self.castling_voice = Sound(
            os.path.join('assets', 'sounds', 'castling_voice.mp3'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')

        self.themes = [brown, blue, gray, green]