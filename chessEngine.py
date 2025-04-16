from stockfishPython import Stockfish
import platform
import time

LOGGING = True

def log(msg):
    if LOGGING:
        print(msg)

system = platform.system()

executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
executable_path = ("../bin/" + executable_name)

stockfish = Stockfish(path=executable_path)

def run_engine(fen):
    stockfish.set_fen_position(fen)

    start_time = time.time()

    best_move = stockfish.get_best_move()

    end_time = time.time()
    log("Engine calculation time:", end_time - start_time)

    return best_move