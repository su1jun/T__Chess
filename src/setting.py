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

ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

def get_alphacol(col):
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return ALPHACOLS[col]

ATTACK_DARK = "#C84646"
ATTACK_LIGHT = "#C86464"

REVERSED = 0

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
        self.voice_sex = 'female_voice'
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.show_reverse = 0

        # images
        self.move_point = os.path.join(
            'assets', 'images', 'move_point.png')
        self.attack_point = os.path.join(
            'assets', 'images', 'attack_point.png')
        
        # sounds
        self.move_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'move_self.mp3'))
        self.capture_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'capture.mp3'))
        self.check_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'move_check.mp3'))
        self.castling_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'castling.mp3'))
        self.promotion_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'promotion.mp3'))
        
        # voices
        self.check_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'check_voice.mp3'))
        self.checkmate_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'checkmate_voice.mp3'))
        self.stalemate_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'stalemate_voice.mp3'))
        self.draw_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'draw_voice.mp3'))
        
        self.queen_castling_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'queen_castling_voice.mp3'))
        self.king_castling_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'king_castling_voice.mp3'))
        
        self.en_passant_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'en_passant_voice.mp3'))
        self.promotion_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'promotion_voice.mp3'))

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