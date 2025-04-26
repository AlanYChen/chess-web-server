from engineWrappers import Stockfish, Maia
from engineWrappers.chessRelatedExceptions import ChessEngineException, ChessEngineImproperInputException
from logger import log
import os

STOCKFISH_PATH = "../bin/stockfish"
LEELA_PATH = "../bin/lc0-dir/lc0"

stockfish = None
maias = None

is_stockfish_server =  os.path.exists("../bin/stockfish")

def instantiate_maias():
    global maias
    maias = {}
    for i in range(11, 20):
        rating = i * 100
        weights_path = "../bin/lc0-dir/maia_weights/maia-" + str(rating) + ".pb.gz"
        maias[rating] = Maia(LEELA_PATH, weights_path)

if is_stockfish_server:
    stockfish = Stockfish(path=STOCKFISH_PATH)
else:
    instantiate_maias()

def run_engine(fen):
    segments = fen.split(",")
    fen = segments[0]

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
        if not elo in maias:
            raise ChessEngineImproperInputException(str(elo) + ": not valid elo for Maia")
        engine = maias[elo]
    else:
        stockfish.update_engine_parameters(
            {"UCI_LimitStrength": "false", "MultiPV": 1, "Slow Mover": 100, "Minimum Thinking Time": 20}
        )
        stockfish.set_depth(15)
        engine = stockfish

    engine.set_fen_position(fen)
    return engine.get_best_move()

def re_instantiate_engines():
    global stockfish, maias
    if stockfish is not None:
        
        del stockfish
        stockfish = Stockfish(path=STOCKFISH_PATH)
    if maias is not None:
        for elo in list(maias.keys()):
            del maias[elo]
        del maias
        instantiate_maias()

    log("Engine reinstantiation complete")

def shutdown_engines():
    global stockfish, maias
    if stockfish is not None:
        del stockfish
    if maias is not None:
        for elo in list(maias.keys()):
            del maias[elo]
        del maias