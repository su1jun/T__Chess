import subprocess

class ChessBot:
    def __init__(self):
        self.engine_path = 'stockfish/stockfish-windows-x86-64-avx2.exe'
        self.engine = subprocess.Popen(
            self.engine_path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        self.level = 1
        self.timeout = 2500

        self.initial_bot()

    # Order transfer function
    def send_command(self, command):
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    # Response reception function
    def read_engine_output(self):
        while True:
            line = self.engine.stdout.readline().strip()
            if line.startswith('bestmove'):
                return line.split(' ')[1]
    
    # initialize
    def initial_bot(self):
        self.send_command('uci')

    def initial_level(self):
        self.send_command(f'setoption name Skill Level value {self.level}')

    def cal_move(self, fen):
        self.send_command('position fen ' + fen)
        self.send_command(f'go movetime {self.timeout}')
        best_move = self.read_engine_output()
        return best_move

    def quit_engine(self):
        self.send_command('quit')
