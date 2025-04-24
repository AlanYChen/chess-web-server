from engineWrappers import Stockfish, StockfishException, Maia, MaiaException
import platform
import time
from logger import log

system = platform.system()

# Stockfish
stockfish_executable_name = "stockfish" if system == "Linux" else "stockfish.exe"
stockfish_path = ("../bin/" + stockfish_executable_name)

stockfish = Stockfish(path=stockfish_path)

# Maia(s)
leela_path = "../bin/lc0"
maias = {}

for i in range(11, 20):
    rating = i * 100
    weights_path = "../maia_weights/maia-1100.pb.gz"
    maias[rating] = Maia(leela_path, weights_path)

def run_engine(fen, i):
    if i == 13:
        raise StockfishException("Simulated stockfish exception")
    
    start_time = time.time()
    
    # segments = fen.split(",")
    # if len(segments) == 2:
    #     skill_level = int(segments[1])
    # else:
    #     skill_level = 20
    # stockfish.set_skill_level(skill_level)

    segments = fen.split(",")
    fen = segments[0]

    engine = None

    log(f"segments: {segments}")

    # fen, elo, depth => Stockfish with limited elo & depth
    if len(segments) == 3:
        elo = int(segments[1])
        depth = int(segments[2])

        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "true", "UCI_Elo": elo, "Slow Mover": 0, "Minimum Thinking Time": 0}
        )
        stockfish.set_depth(depth)
        engine = stockfish

    # fen, elo => Maia with specific elo
    elif len(segments) == 2:
        elo = int(segments[1])
        engine = maias[elo]
    else:
        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "false", "MultiPV": 1, "Slow Mover": 100, "Minimum Thinking Time": 20}
        )
        stockfish.set_depth(15)
        engine = stockfish

    engine.set_fen_position(fen)
    engine_output = engine.get_best_move()

    end_time = time.time()
    log(f"#{i} Engine calculation time: {end_time - start_time}")

    ### Maia Testing
    # print(f"fen: {fen}")
    # maia.set_fen_position(fen)
    # maia_best_move = maia.get_best_move()
    # print(f"maia_best_move: {maia_best_move}")
    
    return engine_output

def re_instantiate_engine():
    log(f"Reinstantiated engine")
    global stockfish, maia
    stockfish = Stockfish(path=stockfish_path)

def shutdown_engines():
    global stockfish, maia
    del stockfish
    del maia