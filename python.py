import sys, time
from centralPython import stockfish

def run(fen):
    stockfish.set_fen_position(fen)

    start_time = time.time()

    best_move = stockfish.get_best_move()

    end_time = time.time()
    print("Engine time:", end_time - start_time)

    print(best_move)

run(sys.argv[1])