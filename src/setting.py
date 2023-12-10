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
HEIGHT_IN = 60

ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

def get_alphacol(col):
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return ALPHACOLS[col]

def get_number(val):
    NUMBERS = {'a': 0,'b': 1 ,'c': 2 ,'d': 3 ,'e': 4 ,'f': 5 ,'g': 6 ,'h': 7}
    return NUMBERS[val]

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
        self.voices = ['female_voice', 'male_voice']
        self._add_themes()
        self.idx = 0
        self.idx2 = 0
        self.show_reverse = 0

        self.theme = self.themes[self.idx]
        self.voice_sex = self.voices[self.idx2]

        self.lvfont = pygame.font.Font(
            os.path.join('assets', 'fonts', 'Blinker-Bold.ttf')
            , 48)
        self.font = pygame.font.Font(
            os.path.join('assets', 'fonts', 'Impact.ttf')
            , 18)
        self.interfont = pygame.font.Font(
            os.path.join('assets', 'fonts', 'Blinker-Bold.ttf')
            , 24)
        
        # images
        self.game_title = os.path.join(
            'assets', 'images', 'chess_title.png')
        self.people1_btn = os.path.join(
            'assets', 'images', 'people1_btn.png')
        self.people2_btn = os.path.join(
            'assets', 'images', 'people2_btn.png')
        self.people1_btn_gray = os.path.join(
            'assets', 'images', 'people1_btn_gray.png')
        self.people2_btn_gray = os.path.join(
            'assets', 'images', 'people2_btn_gray.png')
        
        self.right_btn = os.path.join(
            'assets', 'images', 'right_arrow.png')
        self.left_btn = os.path.join(
            'assets', 'images', 'left_arrow.png')
        self.right_btn_gray = os.path.join(
            'assets', 'images', 'right_arrow_gray.png')
        self.left_btn_gray = os.path.join(
            'assets', 'images', 'left_arrow_gray.png')
        
        self.white_com = os.path.join(
            'assets', 'images', 'white_computer.png')
        self.black_com = os.path.join(
            'assets', 'images', 'black_computer.png')
        self.white_com_selected = os.path.join(
            'assets', 'images', 'white_computer_selected.png')
        self.black_com_selected = os.path.join(
            'assets', 'images', 'black_computer_selected.png')

        self.white_icon = os.path.join(
            'assets', 'images', 'white_icon.png')
        self.black_icon = os.path.join(
            'assets', 'images', 'black_icon.png')

        self.move_point = os.path.join(
            'assets', 'images', 'move_point.png')
        self.attack_point = os.path.join(
            'assets', 'images', 'attack_point.png')
        
        self.game_end = os.path.join(
            'assets', 'images', 'game_end.png')
        
        # sounds
        self.click_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'click.wav'))
        self.start_sound = Sound(
            os.path.join('assets', 'sounds', 'effects', 'board_start.mp3'))
        
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
        
        self.sound_init()
        
    def sound_init(self):
        # voices
        self.change_voice = Sound(
            os.path.join('assets', 'sounds', self.voice_sex, 'change_voice.mp3'))
        
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

    def change_sound(self):
        self.idx2 += 1
        self.idx2 %= len(self.voices)
        self.voice_sex = self.voices[self.idx2]
        self.sound_init()

    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        self.themes = [brown, green]