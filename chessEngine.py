from engineWrappers import Stockfish, Maia
from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
import time, platform
from logger import log

system = platform.system()

# Stockfish
stockfish_path = "bin/stockfish"
stockfish = Stockfish(path=stockfish_path)

# Maia(s)
leela_path = "bin/lc0-dir/lc0"
# maias = None

# def instantiate_maias():
#     global maias
#     maias = {}
#     for i in range(11, 20):
#         rating = i * 100
#         weights_path = "maia_weights/maia-" + str(rating) + ".pb.gz"
#         maias[rating] = Maia(leela_path, weights_path)

# instantiate_maias()

def run_engine(fen, i):
    # if i == 13:
    #     raise ChessEngineException("Simulated chess engine exception")
    
    start_time = time.time()
    
    segments = fen.split(",")
    fen = segments[0]
    log(f"segments: {segments}")

    engine = None

    # fen, elo, depth => Stockfish with limited elo & depth
    if len(segments) == 3:
        elo, depth = int(segments[1]), int(segments[2])

        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "true", "UCI_Elo": elo, "Slow Mover": 0, "Minimum Thinking Time": 0}
        )
        stockfish.set_depth(depth)
        engine = stockfish

    # fen, elo => Maia with specific elo
    elif len(segments) == 2:
        elo = int(segments[1])
        # if not elo in maias:
        #     raise ChessEngineImproperInputException(str(elo) + ": not valid elo for Maia")
        # engine = maias[elo]

        maia_creation_start_time = time.time()

        weights_path = "maia_weights/maia-" + str(elo) + ".pb.gz"
        engine = Maia(leela_path, weights_path)

        maia_creation_end_time = time.time()
        log(f"Maia creation time: {maia_creation_end_time - maia_creation_start_time}")
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
    
    return engine_output

def re_instantiate_engines():
    log("Reinstantiate engines")
    global stockfish #, maias

    del stockfish #, maias
    stockfish = Stockfish(path=stockfish_path)
    # instantiate_maias()

    log("Engine reinstantiation complete")

def shutdown_engines():
    global stockfish
    # for elo in list(maias.keys()):
    #     del maias[elo]
    # del stockfish, maias
    del stockfish