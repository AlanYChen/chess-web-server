from stockfishPython import Stockfish, StockfishException
import platform
import time
from logger import log

system = platform.system()

executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
executable_path = ("../bin/" + executable_name)

stockfish = Stockfish(path=executable_path)

def run_engine(fen, i):
    if i == 13:
        raise StockfishException("Simulated stockfish exception")
    
    # segments = fen.split(",")
    # if len(segments) == 2:
    #     skill_level = int(segments[1])
    # else:
    #     skill_level = 20
    # stockfish.set_skill_level(skill_level)

    segments = fen.split(",")
    if len(segments) == 3:
        elo = int(segments[1])
        depth = int(segments[2])
        multiPV = int(segments[3])

        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "true", "UCI_Elo": elo, "MultiPV": multiPV, "Slow Mover": 0, "Minimum Thinking Time": 0}
        )
        stockfish.set_depth(depth)
    else:
        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "false", "MultiPV": 1, "Slow Mover": 100, "Minimum Thinking Time": 20}
        )
        stockfish.set_depth(15)

    stockfish.set_fen_position(fen)

    start_time = time.time()

    engine_output = stockfish.get_best_move()

    end_time = time.time()
    log(f"#{i} Engine calculation time: {end_time - start_time}")
    return engine_output

def re_instantiate_engine():
    log(f"Reinstantiated engine")
    global stockfish
    stockfish = Stockfish(path=executable_path)