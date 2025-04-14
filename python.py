import sys
from centralPython import stockfish

def run(fen):
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    print(best_move)

run(sys.argv[1])