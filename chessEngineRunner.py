from stockfishPython import StockfishException
from chessEngine import run_engine
from logger import log

def get_total_engine_output(request):
    fens = get_fens(request)

    engine_outputs = []
    for i, fen in enumerate(fens):
        try:
            engine_outputs.append(run_engine(fen, i))
        except StockfishException as e:
            log(f"StockfishException: {e}")
            for j in range(i, len(fens)):
                log(f"Append err: {j}")
                engine_outputs.append("err")
            break
    
    total_engine_output = ','.join(engine_outputs)
    return total_engine_output

def get_fens(request):
    lines = request.splitlines()

    for i, line in enumerate(lines):
        if line == '':
            return lines[i + 1:]
    raise ValueError("get_fens received a request with no empty line")