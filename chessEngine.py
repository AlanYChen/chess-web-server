from engineWrappers import Stockfish, StockfishException, Maia, MaiaException
import platform
import time
from logger import log

system = platform.system()

# Stockfish
stockfish_executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
stockfish_path = ("../bin/" + stockfish_executable_name)

stockfish = Stockfish(path=stockfish_path)

# Maia
leela_path = "../bin/lc0"
weights_path = "../bin/maia_weights/maia-1100.pb.gz"

maia = Maia(leela_path=leela_path, weights_path=weights_path)

def run_engine(fen, i):
    if i == 13:
        raise StockfishException("Simulated stockfish exception")
    
    ### Maia Testing
    maia.set_fen_position(fen)
    maia_best_move = maia.get_best_move()
    print(f"maia_best_move: {maia_best_move}")
    ###
    
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
    stockfish = Stockfish(path=stockfish_path)

def shutdown_engines():
    global stockfish, maia
    del stockfish
    del maia