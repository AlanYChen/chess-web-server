from stockfishPython import Stockfish, StockfishException
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
    global stockfish
    try:
        stockfish.set_fen_position(fen)

        start_time = time.time()

        engine_output = stockfish.get_best_move()

        end_time = time.time()
        log(f"Engine calculation time: {end_time - start_time}")
        return engine_output
    except StockfishException as e:
        print(f"StockfishException: {e}")
        stockfish = Stockfish(path=executable_path)
        return "err"
    