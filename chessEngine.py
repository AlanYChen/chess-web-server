import platform
# import time
from stockfishPython import Stockfish

system = platform.system()

executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
executable_path = ("../bin/" + executable_name)

stockfish = Stockfish(path=executable_path)

def run_engine(fen):
    stockfish.set_fen_position(fen)

    # start_time = time.time()

    best_move = stockfish.get_best_move()

    # end_time = time.time()
    # print("Engine calculation time:", end_time - start_time)

    return best_move